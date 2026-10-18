"""Unit and contract tests for EXP-B2-02 Cross-Receiver Spatial Generalization."""

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
from scripts.run_manysig_exp_b2_02 import ALL_RECEIVERS, load_rx_partition


class TestExpB202(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = REPO_ROOT / "configs" / "exp_b2_02_cross_rx.json"
        cls.features_dir = REPO_ROOT / "datasets" / "features" / "manysig"
        with cls.config_path.open("r", encoding="utf-8") as f:
            cls.config = json.load(f)

    def test_config_contract(self):
        self.assertEqual(self.config["experiment_id"], "EXP-B2-02")
        self.assertEqual(self.config["dataset_provenance"]["source_receiver"], "1-1")
        self.assertEqual(len(self.config["dataset_provenance"]["target_receivers"]), 11)
        self.assertNotIn("1-1", self.config["dataset_provenance"]["target_receivers"])
        self.assertEqual(len(self.config["known_transmitters"]), 6)
        self.assertEqual(len(self.config["feature_contract"]["feature_names"]), 16)

    def test_all_12_receivers_exist_and_complete(self):
        for rx in ALL_RECEIVERS:
            p0 = self.features_dir / f"rx_id={rx}" / "is_equalized=0" / "data.parquet"
            p1 = self.features_dir / f"rx_id={rx}" / "is_equalized=1" / "data.parquet"
            self.assertTrue(p0.exists(), f"Missing partition: {p0}")
            self.assertTrue(p1.exists(), f"Missing partition: {p1}")

    def test_source_receiver_isolation(self):
        """Verify target receivers do not contain source receiver in target list."""
        targets = set(self.config["dataset_provenance"]["target_receivers"])
        src = self.config["dataset_provenance"]["source_receiver"]
        self.assertNotIn(src, targets)
        self.assertEqual(len(targets) + 1, len(ALL_RECEIVERS))


if __name__ == "__main__":
    unittest.main()
