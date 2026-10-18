"""EXP-B2-03: Temporal Generalization and Drift Decay Benchmark.

Characterizes classifier sensitivity to elapsed capture time, evaluates
training-date coverage scaling, and computes Leave-One-Date-Out cross-validation.
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
TARGET_RECEIVER = "1-1"


def evaluate_model(
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
    cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()
    return {
        "accuracy": acc,
        "balanced_accuracy": bal_acc,
        "macro_precision": float(macro_p),
        "macro_recall": float(macro_r),
        "macro_f1": float(macro_f1),
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
    rx_id = cfg["dataset_provenance"]["selected_receiver"]
    labels = cfg["known_transmitters"]
    feat_names = cfg["feature_contract"]["feature_names"]
    rf_cfg = cfg["model_configuration"]
    dates = cfg["dataset_provenance"]["capture_dates"]

    print("================================================================================")
    print("EXP-B2-03: TEMPORAL GENERALIZATION AND DRIFT BENCHMARK")
    print(f"Receiver: {rx_id} | Dates: {dates} | Transmitters: {len(labels)}")
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
            "nominal_sample_rate_hz": DEFAULT_SAMPLE_RATE_HZ,
        },
        "receiver_id": rx_id,
        "known_transmitters": labels,
        "features": feat_names,
        "evaluations": {},
    }

    process = psutil.Process()

    for eq_state, eq_label in [(0, "raw_equalized_0"), (1, "equalized_1")]:
        print(f"\n--- Condition: {eq_label} ---")
        t_start = time.perf_counter()
        mem_before = process.memory_info().rss

        parquet_path = features_base / f"rx_id={rx_id}" / f"is_equalized={eq_state}" / "data.parquet"
        df = pq.ParquetFile(parquet_path).read().to_pandas()

        eq_eval = {}

        # ----------------------------------------------------------------------
        # 1. Temporal Decay from Single-Day Training (Day 1 -> Days 2, 3, 4)
        # ----------------------------------------------------------------------
        print("1. Evaluating Temporal Decay from Single-Day Training (Day 1 -> Days 2, 3, 4)...")
        mask_d1 = df["capture_date"] == "2021_03_01"
        X_d1 = df.loc[mask_d1, feat_names].values.astype(np.float64)
        y_d1 = df.loc[mask_d1, "tx_id"].values.astype(str)

        clf_d1 = RandomForestClassifier(
            n_estimators=rf_cfg["n_estimators"],
            max_features=rf_cfg["max_features"],
            class_weight=None,
            random_state=seed,
            n_jobs=-1,
        )
        clf_d1.fit(X_d1, y_d1)

        decay_results = {}
        for eval_d, elapsed_days in [("2021_03_08", 7), ("2021_03_15", 14), ("2021_03_23", 22)]:
            mask_eval = df["capture_date"] == eval_d
            X_eval = df.loc[mask_eval, feat_names].values.astype(np.float64)
            y_eval = df.loc[mask_eval, "tx_id"].values.astype(str)
            res_d = evaluate_model(clf_d1, X_eval, y_eval, labels=labels)
            res_d["elapsed_days"] = elapsed_days
            decay_results[eval_d] = res_d
            print(f"   Day 1 -> {eval_d} (+{elapsed_days:>2}d): Acc = {res_d['accuracy']*100:6.2f}% | F1 = {res_d['macro_f1']:.4f}")

        eq_eval["temporal_decay_single_day"] = decay_results

        # ----------------------------------------------------------------------
        # 2. Historical Training Coverage Scaling (Test on Day 4)
        # ----------------------------------------------------------------------
        print("\n2. Evaluating Training Coverage Scaling on Fixed Day 4...")
        mask_d4 = df["capture_date"] == "2021_03_23"
        X_d4 = df.loc[mask_d4, feat_names].values.astype(np.float64)
        y_d4 = df.loc[mask_d4, "tx_id"].values.astype(str)

        coverage_results = {}
        for cov_label, cov_dates in [
            ("1_day (Day 1)", ["2021_03_01"]),
            ("2_days (Days 1-2)", ["2021_03_01", "2021_03_08"]),
            ("3_days (Days 1-3)", ["2021_03_01", "2021_03_08", "2021_03_15"]),
        ]:
            mask_cov = df["capture_date"].isin(cov_dates)
            X_cov = df.loc[mask_cov, feat_names].values.astype(np.float64)
            y_cov = df.loc[mask_cov, "tx_id"].values.astype(str)

            clf_cov = RandomForestClassifier(
                n_estimators=rf_cfg["n_estimators"],
                max_features=rf_cfg["max_features"],
                class_weight=None,
                random_state=seed,
                n_jobs=-1,
            )
            clf_cov.fit(X_cov, y_cov)
            res_cov = evaluate_model(clf_cov, X_d4, y_d4, labels=labels)
            res_cov["train_dates"] = cov_dates
            res_cov["train_bursts"] = int(len(y_cov))
            coverage_results[cov_label] = res_cov
            print(f"   Coverage {cov_label:<18}: Day 4 Acc = {res_cov['accuracy']*100:6.2f}% | F1 = {res_cov['macro_f1']:.4f}")

        eq_eval["training_coverage_scaling"] = coverage_results

        # ----------------------------------------------------------------------
        # 3. Leave-One-Date-Out Cross-Validation (4 Folds)
        # ----------------------------------------------------------------------
        print("\n3. Evaluating Leave-One-Date-Out Cross-Validation (4 Folds)...")
        cv_folds = cfg["protocols"]["leave_one_date_out_cv"]["folds"]
        fold_results = []
        fold_accs = []
        fold_f1s = []

        for f_idx, fold in enumerate(cv_folds):
            test_d = fold["test"]
            train_ds = fold["train"]

            mask_tr = df["capture_date"].isin(train_ds)
            mask_te = df["capture_date"] == test_d

            X_tr = df.loc[mask_tr, feat_names].values.astype(np.float64)
            y_tr = df.loc[mask_tr, "tx_id"].values.astype(str)
            X_te = df.loc[mask_te, feat_names].values.astype(np.float64)
            y_te = df.loc[mask_te, "tx_id"].values.astype(str)

            clf_fold = RandomForestClassifier(
                n_estimators=rf_cfg["n_estimators"],
                max_features=rf_cfg["max_features"],
                class_weight=None,
                random_state=seed,
                n_jobs=-1,
            )
            clf_fold.fit(X_tr, y_tr)
            res_f = evaluate_model(clf_fold, X_te, y_te, labels=labels)
            res_f["test_date"] = test_d
            res_f["train_dates"] = train_ds
            fold_results.append(res_f)
            fold_accs.append(res_f["accuracy"])
            fold_f1s.append(res_f["macro_f1"])
            print(f"   Fold {f_idx+1} (Test: {test_d}): Acc = {res_f['accuracy']*100:6.2f}% | F1 = {res_f['macro_f1']:.4f}")

        cv_summary = {
            "mean_accuracy": float(np.mean(fold_accs)),
            "std_accuracy": float(np.std(fold_accs)),
            "mean_macro_f1": float(np.mean(fold_f1s)),
            "std_macro_f1": float(np.std(fold_f1s)),
            "min_accuracy": float(np.min(fold_accs)),
            "max_accuracy": float(np.max(fold_accs)),
            "folds": fold_results,
        }
        print(f"   CV Mean Accuracy: {cv_summary['mean_accuracy']*100:6.2f}% (+/- {cv_summary['std_accuracy']*100:.2f}%)")
        eq_eval["leave_one_date_out_cv"] = cv_summary

        mem_after = process.memory_info().rss
        eq_eval["performance"] = {
            "total_seconds": time.perf_counter() - t_start,
            "memory_delta_mb": (mem_after - mem_before) / (1024 * 1024),
        }
        results["evaluations"][eq_label] = eq_eval

    if out_path is None:
        out_path = REPO_ROOT / "experiments" / "track_b" / "exp_b2_03_temporal_results.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[SUCCESS] EXP-B2-03 artifacts written to: {out_path}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EXP-B2-03 Temporal Generalization Benchmark")
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "configs" / "exp_b2_03_temporal.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "experiments" / "track_b" / "exp_b2_03_temporal_results.json",
        help="Path to results file",
    )
    args = parser.parse_args()
    run_experiment(args.config, args.out)
