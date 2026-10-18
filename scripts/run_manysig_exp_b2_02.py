"""EXP-B2-02: Cross-Receiver Spatial Generalization and Confounding Benchmark.

Quantifies the performance drop when a 16-feature Random Forest trained on a
source receiver (rx_id=1-1) is evaluated on 11 unseen target receivers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import sys
import time
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import psutil
import pyarrow.parquet as pq
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
SOURCE_RECEIVER = "1-1"
ALL_RECEIVERS = [
    "1-1",
    "1-19",
    "14-7",
    "18-2",
    "19-2",
    "2-1",
    "2-19",
    "20-1",
    "3-19",
    "7-14",
    "7-7",
    "8-8",
]


def load_rx_partition(features_dir: Path, rx_id: str, is_equalized: int) -> pd.DataFrame:
    parquet_path = features_dir / f"rx_id={rx_id}" / f"is_equalized={is_equalized}" / "data.parquet"
    if not parquet_path.exists():
        raise FileNotFoundError(f"Partition missing: {parquet_path}")
    return pq.ParquetFile(parquet_path).read().to_pandas()


def evaluate_receiver_prediction(
    clf: RandomForestClassifier,
    X_test: np.ndarray,
    y_test: np.ndarray,
    labels: List[str],
) -> Dict[str, Any]:
    y_pred = clf.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    bal_acc = float(balanced_accuracy_score(y_test, y_pred))
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="macro", zero_division=0
    )
    per_p, per_r, per_f1, per_supp = precision_recall_fscore_support(
        y_test, y_pred, labels=labels, zero_division=0
    )
    cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()

    per_class = {}
    for idx, lbl in enumerate(labels):
        per_class[lbl] = {
            "precision": float(per_p[idx]),
            "recall": float(per_r[idx]),
            "f1_score": float(per_f1[idx]),
            "support": int(per_supp[idx]),
        }

    return {
        "accuracy": acc,
        "balanced_accuracy": bal_acc,
        "macro_precision": float(macro_p),
        "macro_recall": float(macro_r),
        "macro_f1": float(macro_f1),
        "per_class": per_class,
        "confusion_matrix": {
            "labels": labels,
            "matrix": cm,
        },
        "test_bursts": int(len(y_test)),
    }


def run_experiment(config_path: Path, out_path: Optional[Path] = None) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    seed = cfg.get("random_seed", 20260902)
    features_base = REPO_ROOT / "datasets" / "features" / "manysig"
    src_rx = cfg["dataset_provenance"]["source_receiver"]
    labels = cfg["known_transmitters"]
    feat_names = cfg["feature_contract"]["feature_names"]
    rf_cfg = cfg["model_configuration"]
    train_dates = cfg["protocols"]["cross_receiver_evaluation"]["training_dates"]
    test_dates = cfg["protocols"]["cross_receiver_evaluation"]["testing_dates"]

    print("================================================================================")
    print("EXP-B2-02: CROSS-RECEIVER SPATIAL GENERALIZATION BENCHMARK")
    print(f"Source Receiver: {src_rx} | Target Receivers: {len(ALL_RECEIVERS)-1} unseen")
    print(f"Training Dates: {train_dates} | Testing Date: {test_dates}")
    print("================================================================================")

    results: Dict[str, Any] = {
        "metadata": {
            "experiment_id": cfg["experiment_id"],
            "title": cfg["title"],
            "research_question": cfg["research_question"],
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "environment": {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
            },
            "config_file": str(config_path),
            "nominal_sample_rate_hz": DEFAULT_SAMPLE_RATE_HZ,
        },
        "source_receiver": src_rx,
        "known_transmitters": labels,
        "features": feat_names,
        "evaluations": {},
    }

    process = psutil.Process()

    for eq_state, eq_label in [(0, "raw_equalized_0"), (1, "equalized_1")]:
        print(f"\n--- Condition: {eq_label} ---")
        t_start = time.perf_counter()
        mem_before = process.memory_info().rss

        # 1. Train on source receiver 1-1 Days 1-3
        df_src = load_rx_partition(features_base, rx_id=src_rx, is_equalized=eq_state)
        mask_train = df_src["capture_date"].isin(train_dates).values
        X_train = df_src.loc[mask_train, feat_names].values.astype(np.float64)
        y_train = df_src.loc[mask_train, "tx_id"].values.astype(str)

        clf = RandomForestClassifier(
            n_estimators=rf_cfg["n_estimators"],
            max_features=rf_cfg["max_features"],
            class_weight=None,
            random_state=seed,
            n_jobs=-1,
        )
        clf.fit(X_train, y_train)
        train_duration = time.perf_counter() - t_start

        # 2. Evaluate across all 12 receivers on test date (Day 4)
        rx_results = {}
        unseen_accuracies = []
        matched_acc = 0.0

        for rx in ALL_RECEIVERS:
            df_tgt = load_rx_partition(features_base, rx_id=rx, is_equalized=eq_state)
            mask_test = df_tgt["capture_date"].isin(test_dates).values
            X_test = df_tgt.loc[mask_test, feat_names].values.astype(np.float64)
            y_test = df_tgt.loc[mask_test, "tx_id"].values.astype(str)

            eval_res = evaluate_receiver_prediction(clf, X_test, y_test, labels=labels)
            is_matched = (rx == src_rx)
            eval_res["is_matched_source"] = is_matched
            rx_results[rx] = eval_res

            if is_matched:
                matched_acc = eval_res["accuracy"]
                print(f"  [MATCHED CONTROL] RX {rx:>5}: Acc = {eval_res['accuracy']*100:6.2f}% | F1 = {eval_res['macro_f1']:.4f}")
            else:
                unseen_accuracies.append(eval_res["accuracy"])
                print(f"  [UNSEEN TARGET  ] RX {rx:>5}: Acc = {eval_res['accuracy']*100:6.2f}% | F1 = {eval_res['macro_f1']:.4f}")

        mem_after = process.memory_info().rss
        mean_unseen = float(np.mean(unseen_accuracies))
        std_unseen = float(np.std(unseen_accuracies))
        min_unseen = float(np.min(unseen_accuracies))
        max_unseen = float(np.max(unseen_accuracies))
        degradation_drop = float(matched_acc - mean_unseen)

        print(f"\nSummary for {eq_label}:")
        print(f"  Matched Control Accuracy : {matched_acc*100:6.2f}%")
        print(f"  Unseen Mean Accuracy     : {mean_unseen*100:6.2f}% (+/- {std_unseen*100:.2f}%)")
        print(f"  Unseen Min / Max Accuracy: {min_unseen*100:6.2f}% / {max_unseen*100:6.2f}%")
        print(f"  Average Spatial Drop     : {degradation_drop*100:6.2f}%")

        results["evaluations"][eq_label] = {
            "matched_receiver_accuracy": matched_acc,
            "mean_unseen_accuracy": mean_unseen,
            "std_unseen_accuracy": std_unseen,
            "min_unseen_accuracy": min_unseen,
            "max_unseen_accuracy": max_unseen,
            "spatial_degradation_drop": degradation_drop,
            "per_receiver_results": rx_results,
            "performance": {
                "train_seconds": train_duration,
                "total_seconds": time.perf_counter() - t_start,
                "memory_delta_mb": (mem_after - mem_before) / (1024 * 1024),
            },
        }

    if out_path is None:
        out_path = REPO_ROOT / "experiments" / "track_b" / "exp_b2_02_cross_rx_results.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[SUCCESS] EXP-B2-02 artifacts written to: {out_path}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EXP-B2-02 Cross-Receiver Benchmark")
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "configs" / "exp_b2_02_cross_rx.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "experiments" / "track_b" / "exp_b2_02_cross_rx_results.json",
        help="Path to results file",
    )
    args = parser.parse_args()
    run_experiment(args.config, args.out)
