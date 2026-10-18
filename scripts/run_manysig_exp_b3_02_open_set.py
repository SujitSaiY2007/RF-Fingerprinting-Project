"""EXP-B3-02: Open-Set Transmitter Identification and Unknown Rejection Runner.

Evaluates known identification accuracy, known false rejection rate (K-FRR),
unknown false acceptance rate (U-FAR), unknown rejection rate, and open-set macro F1
across single-receiver and multi-receiver soft-voting architectures under leak-free calibration.
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

KNOWN_TRANSMITTERS = ["14-10", "14-7", "20-15", "20-19"]
UNKNOWN_TRANSMITTERS = ["6-15", "8-20"]
ALL_CLASSES_EVAL = ["14-10", "14-7", "20-15", "20-19", "UNKNOWN"]
CORE_CLUSTER_RECEIVERS = ["1-1", "1-19", "2-1", "2-19", "14-7"]


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


def evaluate_threshold(
    y_test_k: np.ndarray,
    test_k_probs: np.ndarray,
    classes: np.ndarray,
    y_test_u: np.ndarray,
    test_u_probs: np.ndarray,
    threshold: float,
    threshold_name: str,
) -> Dict[str, Any]:
    # Known evaluations
    k_pmax = np.max(test_k_probs, axis=1)
    k_preds = classes[np.argmax(test_k_probs, axis=1)]
    k_accepted = k_pmax >= threshold
    k_frr = float(np.mean(~k_accepted))
    k_acc_accepted = float(accuracy_score(y_test_k[k_accepted], k_preds[k_accepted])) if np.sum(k_accepted) > 0 else 0.0
    k_acc_total = float(np.mean((k_preds == y_test_k) & k_accepted))

    # Unknown evaluations
    u_pmax = np.max(test_u_probs, axis=1)
    u_accepted = u_pmax >= threshold  # False acceptance as known
    u_far = float(np.mean(u_accepted))
    u_rr = 1.0 - u_far  # Correct rejection as UNKNOWN

    # Construct 5-class predictions
    y_true_5class = list(y_test_k) + ["UNKNOWN"] * len(y_test_u)
    y_pred_5class = []

    # For known samples: if accepted, predicted class; else UNKNOWN
    for pred, acc in zip(k_preds, k_accepted):
        y_pred_5class.append(pred if acc else "UNKNOWN")

    # For unknown samples: if accepted, false-accepted class; else UNKNOWN
    for idx, acc in enumerate(u_accepted):
        if acc:
            pred_class = classes[np.argmax(test_u_probs[idx])]
            y_pred_5class.append(pred_class)
        else:
            y_pred_5class.append("UNKNOWN")

    # 5-class metrics
    p, r, f1, s = precision_recall_fscore_support(
        y_true_5class, y_pred_5class, labels=ALL_CLASSES_EVAL, zero_division=0
    )
    macro_f1 = float(f1_score(y_true_5class, y_pred_5class, labels=ALL_CLASSES_EVAL, average="macro", zero_division=0))
    bal_acc = float(balanced_accuracy_score(y_true_5class, y_pred_5class))
    cm = confusion_matrix(y_true_5class, y_pred_5class, labels=ALL_CLASSES_EVAL).tolist()

    return {
        "threshold": float(threshold),
        "threshold_name": threshold_name,
        "known_acceptance_rate": float(1.0 - k_frr),
        "known_false_rejection_rate": k_frr,
        "known_accuracy_among_accepted": k_acc_accepted,
        "known_overall_accuracy": k_acc_total,
        "unknown_false_acceptance_rate": u_far,
        "unknown_rejection_rate": u_rr,
        "open_set_balanced_accuracy": bal_acc,
        "open_set_macro_f1": macro_f1,
        "per_class_metrics": {
            lbl: {
                "precision": float(p[i]),
                "recall": float(r[i]),
                "f1": float(f1[i]),
                "support": int(s[i]),
            }
            for i, lbl in enumerate(ALL_CLASSES_EVAL)
        },
        "confusion_matrix": cm,
    }


def run_experiment(features_dir: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    train_dates = config["protocols"]["temporal_open_set_split"]["train_dates"]
    val_dates = config["protocols"]["temporal_open_set_split"]["val_dates"]
    test_dates = config["protocols"]["temporal_open_set_split"]["test_dates"]
    random_seed = config["random_seed"]

    results: Dict[str, Any] = {
        "metadata": {
            "experiment_id": config["experiment_id"],
            "title": config["title"],
            "dataset": config["dataset"],
            "known_transmitters": KNOWN_TRANSMITTERS,
            "held_out_unknown_transmitters": UNKNOWN_TRANSMITTERS,
            "calibration_policy": config["protocols"]["temporal_open_set_split"]["calibration_policy"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "environment": get_environment_info(),
        },
        "evaluations": {},
    }

    for is_eq in config["equalization_states"]:
        eq_key = f"equalized_{is_eq}"
        print(f"\n=================== Processing {eq_key} (is_equalized={is_eq}) ===================")
        eq_results: Dict[str, Any] = {}

        # -------------------------------------------------------------
        # Part A: Primary Single-Receiver Evaluation (RX 1-1)
        # -------------------------------------------------------------
        print("--- Part A: Primary Single-Receiver Evaluation (RX 1-1) ---")
        df_primary = load_partition(features_dir, "1-1", is_eq)
        known_m = df_primary["tx_id"].isin(KNOWN_TRANSMITTERS)
        unknown_m = df_primary["tx_id"].isin(UNKNOWN_TRANSMITTERS)

        train_m = known_m & df_primary["capture_date"].isin(train_dates)
        val_m = known_m & df_primary["capture_date"].isin(val_dates)
        test_k_m = known_m & df_primary["capture_date"].isin(test_dates)
        test_u_m = unknown_m & df_primary["capture_date"].isin(test_dates)

        X_train_1_1 = df_primary.loc[train_m, FEATURE_NAMES].values
        y_train_1_1 = df_primary.loc[train_m, "tx_id"].values
        X_val_1_1 = df_primary.loc[val_m, FEATURE_NAMES].values
        y_val_1_1 = df_primary.loc[val_m, "tx_id"].values
        X_test_k_1_1 = df_primary.loc[test_k_m, FEATURE_NAMES].values
        y_test_k = df_primary.loc[test_k_m, "tx_id"].values
        X_test_u_1_1 = df_primary.loc[test_u_m, FEATURE_NAMES].values
        y_test_u = df_primary.loc[test_u_m, "tx_id"].values

        rf_1_1 = RandomForestClassifier(
            n_estimators=config["model_configuration"]["n_estimators"],
            max_features=config["model_configuration"]["max_features"],
            random_state=random_seed,
            n_jobs=-1,
        )
        rf_1_1.fit(X_train_1_1, y_train_1_1)
        classes = rf_1_1.classes_

        # Calibrate thresholds strictly on known validation set
        val_probs_1_1 = rf_1_1.predict_proba(X_val_1_1)
        val_pmax_1_1 = np.max(val_probs_1_1, axis=1)

        test_k_probs_1_1 = rf_1_1.predict_proba(X_test_k_1_1)
        test_u_probs_1_1 = rf_1_1.predict_proba(X_test_u_1_1)

        thresholds_to_eval = {}
        for pct in config["threshold_calibration_percentiles"]:
            t_val = float(np.percentile(val_pmax_1_1, pct))
            thresholds_to_eval[f"calibrated_{int(100 - pct)}pct_val"] = (t_val, f"Calibrated {int(100-pct)}% Validation Target (percentile {pct})")
        for fix_t in config["fixed_baseline_thresholds"]:
            thresholds_to_eval[f"fixed_{fix_t:.2f}"] = (fix_t, f"Fixed Confidence Baseline ({fix_t:.2f})")

        single_rx_threshold_results: Dict[str, Any] = {}
        for t_key, (t_val, t_desc) in thresholds_to_eval.items():
            t_res = evaluate_threshold(y_test_k, test_k_probs_1_1, classes, y_test_u, test_u_probs_1_1, t_val, t_desc)
            single_rx_threshold_results[t_key] = t_res
            print(f"  RX 1-1 [{t_key}] (T={t_val:.4f}): Known Acc={t_res['known_accuracy_among_accepted']*100:.2f}%, K-FRR={t_res['known_false_rejection_rate']*100:.2f}%, Unknown Rejection={t_res['unknown_rejection_rate']*100:.2f}%, Macro F1={t_res['open_set_macro_f1']:.4f}")

        eq_results["single_rx_1_1_open_set"] = single_rx_threshold_results

        # -------------------------------------------------------------
        # Part B: Multi-Receiver Open-Set Soft Voting Evaluation
        # -------------------------------------------------------------
        print("--- Part B: Multi-Receiver Open-Set Soft Voting (5-RX Cluster) ---")
        cluster_val_probs: List[np.ndarray] = []
        cluster_test_k_probs: List[np.ndarray] = []
        cluster_test_u_probs: List[np.ndarray] = []

        for rx in CORE_CLUSTER_RECEIVERS:
            df_rx = load_partition(features_dir, rx, is_eq)
            k_m = df_rx["tx_id"].isin(KNOWN_TRANSMITTERS)
            u_m = df_rx["tx_id"].isin(UNKNOWN_TRANSMITTERS)

            tr_m = k_m & df_rx["capture_date"].isin(train_dates)
            v_m = k_m & df_rx["capture_date"].isin(val_dates)
            te_k_m = k_m & df_rx["capture_date"].isin(test_dates)
            te_u_m = u_m & df_rx["capture_date"].isin(test_dates)

            rf_rx = RandomForestClassifier(
                n_estimators=config["model_configuration"]["n_estimators"],
                max_features=config["model_configuration"]["max_features"],
                random_state=random_seed,
                n_jobs=-1,
            )
            rf_rx.fit(df_rx.loc[tr_m, FEATURE_NAMES].values, df_rx.loc[tr_m, "tx_id"].values)

            cluster_val_probs.append(rf_rx.predict_proba(df_rx.loc[v_m, FEATURE_NAMES].values))
            cluster_test_k_probs.append(rf_rx.predict_proba(df_rx.loc[te_k_m, FEATURE_NAMES].values))
            cluster_test_u_probs.append(rf_rx.predict_proba(df_rx.loc[te_u_m, FEATURE_NAMES].values))

        # Soft voting across 5 receivers
        cluster_val_soft = np.mean(cluster_val_probs, axis=0)
        cluster_test_k_soft = np.mean(cluster_test_k_probs, axis=0)
        cluster_test_u_soft = np.mean(cluster_test_u_probs, axis=0)

        val_pmax_soft = np.max(cluster_val_soft, axis=1)

        cluster_thresholds_to_eval = {}
        for pct in config["threshold_calibration_percentiles"]:
            t_val = float(np.percentile(val_pmax_soft, pct))
            cluster_thresholds_to_eval[f"calibrated_{int(100 - pct)}pct_val"] = (t_val, f"Calibrated {int(100-pct)}% Validation Target (percentile {pct})")
        for fix_t in config["fixed_baseline_thresholds"]:
            cluster_thresholds_to_eval[f"fixed_{fix_t:.2f}"] = (fix_t, f"Fixed Confidence Baseline ({fix_t:.2f})")

        multi_rx_threshold_results: Dict[str, Any] = {}
        for t_key, (t_val, t_desc) in cluster_thresholds_to_eval.items():
            t_res = evaluate_threshold(y_test_k, cluster_test_k_soft, classes, y_test_u, cluster_test_u_soft, t_val, t_desc)
            multi_rx_threshold_results[t_key] = t_res
            print(f"  Cluster Soft Vote [{t_key}] (T={t_val:.4f}): Known Acc={t_res['known_accuracy_among_accepted']*100:.2f}%, K-FRR={t_res['known_false_rejection_rate']*100:.2f}%, Unknown Rejection={t_res['unknown_rejection_rate']*100:.2f}%, Macro F1={t_res['open_set_macro_f1']:.4f}")

        eq_results["multi_rx_cluster_open_set"] = multi_rx_threshold_results
        results["evaluations"][eq_key] = eq_results

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EXP-B3-02 Open-Set Evaluation")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "exp_b3_02_open_set.json")
    parser.add_argument("--features-dir", type=Path, default=REPO_ROOT / "datasets" / "features" / "manysig")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "experiments" / "track_b" / "exp_b3_02_open_set_results.json")
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

    print(f"\nEXP-B3-02 completed successfully in {elapsed:.2f}s.")
    print(f"Authoritative results written to: {args.output}")


if __name__ == "__main__":
    main()
