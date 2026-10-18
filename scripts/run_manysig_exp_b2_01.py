"""EXP-B2-01: Matched-Receiver ManySig Random Forest Baseline.

Evaluates the frozen 16-feature Random Forest baseline on ManySig receiver 1-1
under controlled, leak-free split protocols adhering to DEC-035.
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
import pyarrow.parquet as pq
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

# Insert repository root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.manysig_features import DEFAULT_SAMPLE_RATE_HZ, FEATURE_NAMES

KNOWN_TRANSMITTERS = ["14-10", "14-7", "20-15", "20-19", "6-15", "8-20"]
MATCHED_RECEIVER = "1-1"


def get_environment_info() -> Dict[str, str]:
    """Capture runtime environment versions for experimental reproducibility."""
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
    """Read a specific ManySig Parquet partition using direct file access."""
    parquet_path = features_dir / f"rx_id={rx_id}" / f"is_equalized={is_equalized}" / "data.parquet"
    if not parquet_path.exists():
        raise FileNotFoundError(f"Partition not found: {parquet_path}")
    table = pq.ParquetFile(parquet_path).read()
    return table.to_pandas()


def evaluate_split(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    feature_names: Sequence[str],
    labels: List[str],
    seed: int,
    n_estimators: int = 100,
    max_features: str = "sqrt",
) -> Dict[str, Any]:
    """Train Random Forest and compute all required classification and provenance metrics."""
    process = psutil.Process()
    mem_before = process.memory_info().rss
    t_start = time.perf_counter()

    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_features=max_features,
        class_weight=None,
        random_state=seed,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    train_time = time.perf_counter() - t_start
    t_infer_start = time.perf_counter()
    y_pred = clf.predict(X_test)
    inference_time = time.perf_counter() - t_infer_start

    mem_after = process.memory_info().rss
    mem_delta_mb = (mem_after - mem_before) / (1024 * 1024)

    # Core summary metrics
    acc = float(accuracy_score(y_test, y_pred))
    bal_acc = float(balanced_accuracy_score(y_test, y_pred))
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="macro", zero_division=0
    )

    # Per-class metrics
    per_p, per_r, per_f1, per_supp = precision_recall_fscore_support(
        y_test, y_pred, labels=labels, zero_division=0
    )

    per_class_results = {}
    train_class_counts = {lbl: int(np.sum(y_train == lbl)) for lbl in labels}
    test_class_counts = {lbl: int(np.sum(y_test == lbl)) for lbl in labels}

    for idx, lbl in enumerate(labels):
        per_class_results[lbl] = {
            "precision": float(per_p[idx]),
            "recall": float(per_r[idx]),
            "f1_score": float(per_f1[idx]),
            "test_support": int(per_supp[idx]),
            "train_count": train_class_counts[lbl],
            "test_count": test_class_counts[lbl],
        }

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()

    # Feature importances
    importances = {
        name: float(imp)
        for name, imp in sorted(
            zip(feature_names, clf.feature_importances_),
            key=lambda item: -item[1],
        )
    }

    return {
        "overall_accuracy": acc,
        "balanced_accuracy": bal_acc,
        "macro_precision": float(macro_p),
        "macro_recall": float(macro_r),
        "macro_f1": float(macro_f1),
        "per_class": per_class_results,
        "confusion_matrix": {
            "labels": labels,
            "matrix": cm,
        },
        "feature_importances": importances,
        "sample_counts": {
            "total_train_samples": int(len(y_train)),
            "total_test_samples": int(len(y_test)),
            "per_class_train": train_class_counts,
            "per_class_test": test_class_counts,
        },
        "performance": {
            "train_seconds": train_time,
            "inference_seconds": inference_time,
            "memory_delta_mb": mem_delta_mb,
        },
    }


def run_experiment(config_path: Path, out_path: Optional[Path] = None) -> Dict[str, Any]:
    """Execute EXP-B2-01 according to the specified configuration."""
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    seed = cfg.get("random_seed", 20260902)
    features_base = REPO_ROOT / "datasets" / "features" / "manysig"
    rx_id = cfg["dataset_provenance"]["selected_receiver"]
    labels = cfg["known_transmitters"]
    feat_names = cfg["feature_contract"]["feature_names"]
    rf_cfg = cfg["model_configuration"]

    print("================================================================================")
    print("EXP-B2-01: MATCHED-RECEIVER MANYSIG RANDOM FOREST BASELINE")
    print(f"Receiver: {rx_id} | Known Transmitters: {len(labels)} | Seed: {seed}")
    print("================================================================================")

    results: Dict[str, Any] = {
        "metadata": {
            "experiment_id": cfg["experiment_id"],
            "title": cfg["title"],
            "research_question": cfg["research_question"],
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "environment": get_environment_info(),
            "config_file": str(config_path),
            "nominal_sample_rate_hz": DEFAULT_SAMPLE_RATE_HZ,
            "sample_rate_status": "REQUIRES VALIDATION (Engineering default inherited from Track-A)",
        },
        "dataset_provenance": cfg["dataset_provenance"],
        "model_configuration": rf_cfg,
        "features": feat_names,
        "known_transmitters": labels,
        "evaluations": {},
    }

    # Evaluate both equalization states: raw (0) and equalized (1)
    for eq_state, eq_label in [(0, "raw_equalized_0"), (1, "equalized_1")]:
        print(f"\n--- Loading Data: rx_id={rx_id}, is_equalized={eq_state} ({eq_label}) ---")
        df = load_partition(features_base, rx_id=rx_id, is_equalized=eq_state)
        X = df[feat_names].values.astype(np.float64)
        y = df["tx_id"].values.astype(str)

        eq_eval: Dict[str, Any] = {}

        # ----------------------------------------------------------------------
        # 1. PRIMARY BENCHMARK: Date Holdout (Train Days 1-3 -> Test Day 4)
        # ----------------------------------------------------------------------
        train_dates = cfg["protocols"]["primary_temporal_holdout"]["train_dates"]
        test_dates = cfg["protocols"]["primary_temporal_holdout"]["test_dates"]

        mask_train = df["capture_date"].isin(train_dates).values
        mask_test = df["capture_date"].isin(test_dates).values

        print(f"Executing Primary Protocol: Date-Holdout (Train: {train_dates} -> Test: {test_dates})...")
        primary_res = evaluate_split(
            X_train=X[mask_train],
            y_train=y[mask_train],
            X_test=X[mask_test],
            y_test=y[mask_test],
            feature_names=feat_names,
            labels=labels,
            seed=seed,
            n_estimators=rf_cfg["n_estimators"],
            max_features=rf_cfg["max_features"],
        )
        eq_eval["primary_date_holdout_days123_to_day4"] = primary_res

        print(f"  -> Primary Accuracy: {primary_res['overall_accuracy'] * 100:.2f}% | Macro F1: {primary_res['macro_f1']:.4f}")

        # ----------------------------------------------------------------------
        # 2. SECONDARY PROTOCOL: Matched-Date Burst-Block Holdout
        # ----------------------------------------------------------------------
        b_train_range = cfg["protocols"]["secondary_matched_date_chunk_holdout"]["train_burst_range"]
        b_test_range = cfg["protocols"]["secondary_matched_date_chunk_holdout"]["test_burst_range"]

        mask_b_train = (df["burst_index"] >= b_train_range[0]) & (df["burst_index"] <= b_train_range[1]).values
        mask_b_test = (df["burst_index"] >= b_test_range[0]) & (df["burst_index"] <= b_test_range[1]).values

        print("Executing Secondary Protocol: Matched-Date Chunk-Holdout (70% Train -> 15% Test)...")
        secondary_res = evaluate_split(
            X_train=X[mask_b_train],
            y_train=y[mask_b_train],
            X_test=X[mask_b_test],
            y_test=y[mask_b_test],
            feature_names=feat_names,
            labels=labels,
            seed=seed,
            n_estimators=rf_cfg["n_estimators"],
            max_features=rf_cfg["max_features"],
        )
        eq_eval["secondary_matched_date_chunk_holdout"] = secondary_res
        print(f"  -> Secondary Accuracy: {secondary_res['overall_accuracy'] * 100:.2f}% | Macro F1: {secondary_res['macro_f1']:.4f}")

        # ----------------------------------------------------------------------
        # 3. TERTIARY PROTOCOL: Restricted Temporal Observation (Days 1-2 Train -> Day 3 Val -> Day 4 Test)
        # ----------------------------------------------------------------------
        d12_dates = cfg["protocols"]["tertiary_two_date_temporal_holdout"]["train_dates"]
        d3_dates = cfg["protocols"]["tertiary_two_date_temporal_holdout"]["val_dates"]
        d4_dates = cfg["protocols"]["tertiary_two_date_temporal_holdout"]["test_dates"]

        mask_d12 = df["capture_date"].isin(d12_dates).values
        mask_d3 = df["capture_date"].isin(d3_dates).values
        mask_d4 = df["capture_date"].isin(d4_dates).values

        print("Executing Tertiary Protocol: Two-Date Train (Days 1-2 Train -> Day 3 Val & Day 4 Test)...")
        val_d3_res = evaluate_split(
            X_train=X[mask_d12],
            y_train=y[mask_d12],
            X_test=X[mask_d3],
            y_test=y[mask_d3],
            feature_names=feat_names,
            labels=labels,
            seed=seed,
            n_estimators=rf_cfg["n_estimators"],
            max_features=rf_cfg["max_features"],
        )
        test_d4_res = evaluate_split(
            X_train=X[mask_d12],
            y_train=y[mask_d12],
            X_test=X[mask_d4],
            y_test=y[mask_d4],
            feature_names=feat_names,
            labels=labels,
            seed=seed,
            n_estimators=rf_cfg["n_estimators"],
            max_features=rf_cfg["max_features"],
        )
        eq_eval["tertiary_two_date_val_day3"] = val_d3_res
        eq_eval["tertiary_two_date_test_day4"] = test_d4_res
        print(f"  -> Two-Date Train -> Day 3 Val Acc: {val_d3_res['overall_accuracy'] * 100:.2f}% | Day 4 Test Acc: {test_d4_res['overall_accuracy'] * 100:.2f}%")

        results["evaluations"][eq_label] = eq_eval

    # Write output JSON
    if out_path is None:
        out_path = REPO_ROOT / "experiments" / "track_b" / "exp_b2_01_matched_rx_results.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[SUCCESS] EXP-B2-01 artifacts successfully written to: {out_path}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EXP-B2-01 Matched-Receiver RF Baseline")
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "configs" / "exp_b2_01_matched_rx.json",
        help="Path to experiment configuration JSON",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "experiments" / "track_b" / "exp_b2_01_matched_rx_results.json",
        help="Path for destination results JSON",
    )
    args = parser.parse_args()
    run_experiment(args.config, args.out)
