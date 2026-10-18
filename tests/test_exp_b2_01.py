"""Lightweight unit and contract tests for EXP-B2-01 Matched-Receiver RF Baseline."""

import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO_ROOT = Path(__file__).resolve().parents[1]
import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.manysig_features import FEATURE_NAMES
from scripts.run_manysig_exp_b2_01 import evaluate_split, load_partition


class TestExpB201(unittest.TestCase):
    """Test suite certifying EXP-B2-01 configuration, data partitions, and split protocol."""

    @classmethod
    def setUpClass(cls):
        cls.config_path = REPO_ROOT / "configs" / "exp_b2_01_matched_rx.json"
        cls.features_dir = REPO_ROOT / "datasets" / "features" / "manysig"
        with cls.config_path.open("r", encoding="utf-8") as f:
            cls.config = json.load(f)

    def test_config_contract(self):
        """Verify configuration schema, 16 features, 6 transmitters, and leakage controls."""
        self.assertEqual(self.config["experiment_id"], "EXP-B2-01")
        self.assertEqual(self.config["dataset_provenance"]["selected_receiver"], "1-1")
        self.assertEqual(len(self.config["known_transmitters"]), 6)
        self.assertEqual(len(self.config["feature_contract"]["feature_names"]), 16)
        self.assertEqual(tuple(self.config["feature_contract"]["feature_names"]), FEATURE_NAMES)
        self.assertIn("primary_temporal_holdout", self.config["protocols"])
        self.assertIn("leakage_controls", self.config)

    def test_partition_integrity_rx_1_1(self):
        """Verify receiver 1-1 partition row counts, class balance, and lack of nulls."""
        df_raw = load_partition(self.features_dir, rx_id="1-1", is_equalized=0)
        self.assertEqual(len(df_raw), 24000)
        self.assertEqual(df_raw[list(FEATURE_NAMES)].isnull().sum().sum(), 0)
        
        # Verify 6 transmitters with exactly 4000 bursts each
        tx_counts = df_raw["tx_id"].value_counts()
        self.assertEqual(len(tx_counts), 6)
        for tx, count in tx_counts.items():
            self.assertEqual(count, 4000)

        # Verify 4 capture dates with exactly 6000 bursts each
        date_counts = df_raw["capture_date"].value_counts()
        self.assertEqual(len(date_counts), 4)
        for date, count in date_counts.items():
            self.assertEqual(count, 6000)

    def test_split_orthogonality(self):
        """Verify that train and test dates have zero intersection and preserve class balance."""
        proto = self.config["protocols"]["primary_temporal_holdout"]
        train_dates = set(proto["train_dates"])
        test_dates = set(proto["test_dates"])
        self.assertEqual(train_dates.intersection(test_dates), set())

        df_raw = load_partition(self.features_dir, rx_id="1-1", is_equalized=0)
        mask_train = df_raw["capture_date"].isin(train_dates)
        mask_test = df_raw["capture_date"].isin(test_dates)

        self.assertEqual(int(mask_train.sum()), 18000)
        self.assertEqual(int(mask_test.sum()), 6000)
        self.assertEqual(int(mask_train.sum() + mask_test.sum()), 24000)

    def test_evaluate_split_contract(self):
        """Verify evaluate_split produces all required metrics on a small slice."""
        df_raw = load_partition(self.features_dir, rx_id="1-1", is_equalized=0)
        slice_df = df_raw.iloc[:600]
        X = slice_df[list(FEATURE_NAMES)].values
        y = slice_df["tx_id"].values
        labels = sorted(list(set(y)))

        res = evaluate_split(
            X_train=X[:400],
            y_train=y[:400],
            X_test=X[400:],
            y_test=y[400:],
            feature_names=FEATURE_NAMES,
            labels=labels,
            seed=20260902,
            n_estimators=5,
        )

        self.assertIn("overall_accuracy", res)
        self.assertIn("balanced_accuracy", res)
        self.assertIn("macro_precision", res)
        self.assertIn("macro_recall", res)
        self.assertIn("macro_f1", res)
        self.assertIn("per_class", res)
        self.assertIn("confusion_matrix", res)
        self.assertIn("feature_importances", res)
        self.assertIn("sample_counts", res)
        self.assertIn("performance", res)
        self.assertEqual(len(res["confusion_matrix"]["matrix"]), len(labels))


if __name__ == "__main__":
    unittest.main()
