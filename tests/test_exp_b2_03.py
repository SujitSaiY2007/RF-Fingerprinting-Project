"""Unit and contract tests for EXP-B2-03 Temporal Generalization."""

import json
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.manysig_features import FEATURE_NAMES


class TestExpB203(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = REPO_ROOT / "configs" / "exp_b2_03_temporal.json"
        with cls.config_path.open("r", encoding="utf-8") as f:
            cls.config = json.load(f)

    def test_config_contract(self):
        self.assertEqual(self.config["experiment_id"], "EXP-B2-03")
        self.assertEqual(self.config["dataset_provenance"]["selected_receiver"], "1-1")
        self.assertEqual(len(self.config["dataset_provenance"]["capture_dates"]), 4)
        self.assertEqual(len(self.config["feature_contract"]["feature_names"]), 16)
        self.assertIn("temporal_decay_single_date", self.config["protocols"])
        self.assertIn("training_coverage_scaling", self.config["protocols"])
        self.assertIn("leave_one_date_out_cv", self.config["protocols"])

    def test_fold_orthogonality(self):
        folds = self.config["protocols"]["leave_one_date_out_cv"]["folds"]
        self.assertEqual(len(folds), 4)
        for fold in folds:
            test_d = fold["test"]
            train_ds = set(fold["train"])
            self.assertNotIn(test_d, train_ds)
            self.assertEqual(len(train_ds), 3)


if __name__ == "__main__":
    unittest.main()
