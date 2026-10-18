"""EXP-B3-01: Multi-Receiver Observation Fusion and Spatial Rescue Runner.

Evaluates single-receiver baselines, distributed decision-level soft/hard voting,
centralized feature concatenation, cross-receiver transfer voting, and missing-receiver
degradation sweeps on WiSig ManySig under leak-free temporal protocols.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import sys
import time
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import psutil
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.manysig_features import DEFAULT_SAMPLE_RATE_HZ, FEATURE_NAMES

KNOWN_TRANSMITTERS = ["14-10", "14-7", "20-15", "20-19", "6-15", "8-20"]
CORE_CLUSTER_RECEIVERS = ["1-1", "1-19", "2-1", "2-19", "14-7"]
ALL_RECEIVERS = ["1-1", "1-19", "14-7", "18-2", "19-2", "2-1", "2-19", "20-1", "3-19", "7-14", "7-7", "8-8"]


def get_environment_info() -> Dict[str, str]:
    import sklearn
    import pyarrow
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "scikit_learn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "pyarrow_version": pyarrow.__version__,
    }


def load_partition(features_dir: Path, rx_id: str, is_equalized: int) -> pd.DataFrame:
    parquet_path = features_dir / f"rx_id={rx_id}" / f"is_equalized={is_equalized}" / "data.parquet"
    if not parquet_path.exists():
        raise FileNotFoundError(f"Partition not found: {parquet_path}")
    return pd.read_parquet(parquet_path)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, labels: List[str]) -> Dict[str, Any]:
    acc = float(accuracy_score(y_true, y_pred))
    bal_acc = float(balanced_accuracy_score(y_true, y_pred))
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    p, r, f1, s = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=labels).tolist()
    return {
        "accuracy": acc,
        "balanced_accuracy": bal_acc,
        "macro_f1": macro_f1,
        "per_class": {
            lbl: {
                "precision": float(p[i]),
                "recall": float(r[i]),
                "f1": float(f1[i]),
                "support": int(s[i]),
            }
            for i, lbl in enumerate(labels)
        },
        "confusion_matrix": cm,
    }


def run_experiment(features_dir: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    train_dates = config["protocols"]["primary_temporal_split"]["train_dates"]
    test_dates = config["protocols"]["primary_temporal_split"]["test_dates"]
    random_seed = config["random_seed"]

    results: Dict[str, Any] = {
        "metadata": {
            "experiment_id": config["experiment_id"],
            "title": config["title"],
            "dataset": config["dataset"],
            "observation_matching_contract": config["dataset_provenance"]["observation_matching_contract"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "environment": get_environment_info(),
        },
        "evaluations": {},
    }

    for is_eq in config["equalization_states"]:
        eq_key = f"equalized_{is_eq}"
        print(f"\n=================== Processing {eq_key} (is_equalized={is_eq}) ===================")
        eq_results: Dict[str, Any] = {}

        # 1. Load data for core cluster
        cluster_data: Dict[str, Dict[str, np.ndarray]] = {}
        for rx in CORE_CLUSTER_RECEIVERS:
            df = load_partition(features_dir, rx, is_eq)
            train_m = df["capture_date"].isin(train_dates)
            test_m = df["capture_date"].isin(test_dates)
            cluster_data[rx] = {
                "train_X": df.loc[train_m, FEATURE_NAMES].values,
                "train_y": df.loc[train_m, "tx_id"].values,
                "test_X": df.loc[test_m, FEATURE_NAMES].values,
                "test_y": df.loc[test_m, "tx_id"].values,
            }

        y_test_common = cluster_data[CORE_CLUSTER_RECEIVERS[0]]["test_y"]
        y_train_common = cluster_data[CORE_CLUSTER_RECEIVERS[0]]["train_y"]

        # Train local RF for each cluster receiver
        local_models: Dict[str, RandomForestClassifier] = {}
        local_test_probs: Dict[str, np.ndarray] = {}
        local_test_preds: Dict[str, np.ndarray] = {}
        single_rx_metrics: Dict[str, Any] = {}

        print("Training local models for core cluster...")
        for rx in CORE_CLUSTER_RECEIVERS:
            rf = RandomForestClassifier(
                n_estimators=config["model_configuration"]["n_estimators"],
                max_features=config["model_configuration"]["max_features"],
                random_state=random_seed,
                n_jobs=-1,
            )
            rf.fit(cluster_data[rx]["train_X"], cluster_data[rx]["train_y"])
            local_models[rx] = rf
            probs = rf.predict_proba(cluster_data[rx]["test_X"])
            preds = rf.classes_[np.argmax(probs, axis=1)]
            local_test_probs[rx] = probs
            local_test_preds[rx] = preds
            m = compute_metrics(y_test_common, preds, KNOWN_TRANSMITTERS)
            single_rx_metrics[rx] = m
            print(f"  Local RX {rx} Accuracy: {m['accuracy'] * 100:.2f}%, Macro F1: {m['macro_f1']:.4f}")

        eq_results["single_rx_local_baselines"] = single_rx_metrics
        mean_single_acc = float(np.mean([m["accuracy"] for m in single_rx_metrics.values()]))
        eq_results["mean_single_rx_local_accuracy"] = mean_single_acc

        # 2. Distributed Decision-Level Soft Voting (Core Cluster)
        classes = local_models[CORE_CLUSTER_RECEIVERS[0]].classes_
        cluster_probs = np.array([local_test_probs[rx] for rx in CORE_CLUSTER_RECEIVERS])  # shape (5, 6000, 6)
        soft_vote_probs = np.mean(cluster_probs, axis=0)
        soft_vote_preds = classes[np.argmax(soft_vote_probs, axis=1)]
        soft_m = compute_metrics(y_test_common, soft_vote_preds, KNOWN_TRANSMITTERS)
        eq_results["distributed_decision_soft_voting"] = soft_m
        print(f"  Cluster Soft Voting (5-RX) Accuracy: {soft_m['accuracy'] * 100:.2f}%, Macro F1: {soft_m['macro_f1']:.4f}")

        # 3. Distributed Decision-Level Hard Majority Voting
        # Convert predictions to class indices
        cluster_preds_idx = np.array([[np.where(classes == p)[0][0] for p in local_test_preds[rx]] for rx in CORE_CLUSTER_RECEIVERS])
        from scipy.stats import mode
        # Simple manual mode across rows
        hard_preds_list = []
        disagreement_count = 0
        for b_idx in range(len(y_test_common)):
            rx_votes = [local_test_preds[rx][b_idx] for rx in CORE_CLUSTER_RECEIVERS]
            if len(set(rx_votes)) > 1:
                disagreement_count += 1
            vals, counts = np.unique(rx_votes, return_counts=True)
            hard_preds_list.append(vals[np.argmax(counts)])
        hard_vote_preds = np.array(hard_preds_list)
        hard_m = compute_metrics(y_test_common, hard_vote_preds, KNOWN_TRANSMITTERS)
        hard_m["disagreement_rate"] = float(disagreement_count / len(y_test_common))
        eq_results["distributed_decision_hard_majority_voting"] = hard_m
        print(f"  Cluster Hard Voting (5-RX) Accuracy: {hard_m['accuracy'] * 100:.2f}%, Disagreement Rate: {hard_m['disagreement_rate'] * 100:.2f}%")

        # 4. Centralized Feature Concatenation
        train_concat_X = np.hstack([cluster_data[rx]["train_X"] for rx in CORE_CLUSTER_RECEIVERS])
        test_concat_X = np.hstack([cluster_data[rx]["test_X"] for rx in CORE_CLUSTER_RECEIVERS])
        print(f"  Training centralized feature concatenation model ({train_concat_X.shape[1]} features)...")
        rf_fused = RandomForestClassifier(
            n_estimators=config["model_configuration"]["n_estimators"],
            max_features=config["model_configuration"]["max_features"],
            random_state=random_seed,
            n_jobs=-1,
        )
        rf_fused.fit(train_concat_X, y_train_common)
        concat_preds = rf_fused.predict(test_concat_X)
        concat_m = compute_metrics(y_test_common, concat_preds, KNOWN_TRANSMITTERS)
        eq_results["centralized_feature_concatenation"] = concat_m
        print(f"  Feature Concatenation Accuracy: {concat_m['accuracy'] * 100:.2f}%, Macro F1: {concat_m['macro_f1']:.4f}")

        # 5. Missing Receiver Degradation Sweep (1 to 4 receivers dropped from 5-node cluster)
        degradation_results: Dict[str, Any] = {}
        for num_active in range(1, len(CORE_CLUSTER_RECEIVERS)):
            active_rx = CORE_CLUSTER_RECEIVERS[:num_active]
            sub_probs = np.mean([local_test_probs[rx] for rx in active_rx], axis=0)
            sub_preds = classes[np.argmax(sub_probs, axis=1)]
            sub_acc = float(accuracy_score(y_test_common, sub_preds))
            degradation_results[f"{num_active}_active_receivers"] = {
                "active_receivers": active_rx,
                "accuracy": sub_acc,
            }
            print(f"  Degradation ({num_active} RX: {active_rx}) Accuracy: {sub_acc * 100:.2f}%")
        eq_results["missing_receiver_degradation_sweep"] = degradation_results

        # 6. Cross-Receiver Transfer Voting (Can voting rescue a model trained only on RX 1-1?)
        unseen_rx_list = [rx for rx in ALL_RECEIVERS if rx != "1-1"]
        rf_src = local_models["1-1"]
        unseen_probs_list = []
        unseen_single_accs: Dict[str, float] = {}

        print("  Evaluating transfer voting of RX 1-1 model across 11 unseen receivers...")
        for rx in unseen_rx_list:
            df_u = load_partition(features_dir, rx, is_eq)
            test_m_u = df_u["capture_date"].isin(test_dates)
            X_u = df_u.loc[test_m_u, FEATURE_NAMES].values
            y_u = df_u.loc[test_m_u, "tx_id"].values
            u_probs = rf_src.predict_proba(X_u)
            u_preds = classes[np.argmax(u_probs, axis=1)]
            u_acc = float(accuracy_score(y_u, u_preds))
            unseen_single_accs[rx] = u_acc
            unseen_probs_list.append(u_probs)

        mean_unseen_single = float(np.mean(list(unseen_single_accs.values())))
        transfer_vote_prob = np.mean(unseen_probs_list, axis=0)
        transfer_vote_preds = classes[np.argmax(transfer_vote_prob, axis=1)]
        transfer_m = compute_metrics(y_test_common, transfer_vote_preds, KNOWN_TRANSMITTERS)

        eq_results["cross_receiver_transfer_voting"] = {
            "source_model_receiver": "1-1",
            "evaluated_unseen_receivers": unseen_rx_list,
            "individual_unseen_accuracies": unseen_single_accs,
            "mean_individual_unseen_accuracy": mean_unseen_single,
            "transfer_ensemble_voting_metrics": transfer_m,
            "spatial_rescue_gain_percentage_points": float((transfer_m["accuracy"] - mean_unseen_single) * 100.0),
        }
        print(f"  Transfer Voting Mean Single Unseen: {mean_unseen_single * 100:.2f}% -> Ensemble: {transfer_m['accuracy'] * 100:.2f}% (Gain: +{eq_results['cross_receiver_transfer_voting']['spatial_rescue_gain_percentage_points']:.2f} pp)")

        results["evaluations"][eq_key] = eq_results

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EXP-B3-01 Multi-Receiver Fusion")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "exp_b3_01_fusion.json")
    parser.add_argument("--features-dir", type=Path, default=REPO_ROOT / "datasets" / "features" / "manysig")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "experiments" / "track_b" / "exp_b3_01_fusion_results.json")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    start_time = time.time()
    results = run_experiment(args.features_dir, config)
    elapsed = time.time() - start_time
    results["metadata"]["execution_time_seconds"] = round(elapsed, 2)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nEXP-B3-01 completed successfully in {elapsed:.2f}s.")
    print(f"Authoritative results written to: {args.output}")


if __name__ == "__main__":
    main()
