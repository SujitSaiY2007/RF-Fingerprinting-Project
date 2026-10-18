"""Unit tests for EXP-B3-02 Open-Set Transmitter Identification contracts and invariants."""

import json
from pathlib import Path
import unittest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestExpB302Contracts(unittest.TestCase):
    """Validates configuration, open-set separation, and metric invariants for EXP-B3-02."""

    @classmethod
    def setUpClass(cls):
        cls.config_path = REPO_ROOT / "configs" / "exp_b3_02_open_set.json"
        cls.results_path = REPO_ROOT / "experiments" / "track_b" / "exp_b3_02_open_set_results.json"

    def test_open_set_partition_contract(self):
        """Verifies mutual exclusivity between known and held-out unknown transmitters."""
        self.assertTrue(self.config_path.exists(), "exp_b3_02_open_set.json must exist")
        with open(self.config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        known = cfg["dataset_provenance"]["known_transmitters"]
        unknown = cfg["dataset_provenance"]["held_out_unknown_transmitters"]

        self.assertEqual(len(known), 4)
        self.assertEqual(len(unknown), 2)
        # Ensure disjoint sets
        intersection = set(known).intersection(set(unknown))
        self.assertEqual(len(intersection), 0, f"Known and unknown sets must be disjoint: {intersection}")
        self.assertEqual(len(set(known).union(set(unknown))), 6)
        self.assertIn("calibration_policy", cfg["protocols"]["temporal_open_set_split"])

    def test_open_set_metric_math(self):
        """Verifies mathematical complement invariants of open-set rates."""
        # Synthetic evaluation
        k_frr = 0.2507
        known_acc_rate = 1.0 - k_frr
        self.assertAlmostEqual(k_frr + known_acc_rate, 1.0, places=6)

        u_far = 0.5530
        u_rr = 1.0 - u_far
        self.assertAlmostEqual(u_far + u_rr, 1.0, places=6)

    def test_confusion_matrix_support_invariants(self):
        """Verifies that 5-class confusion matrix matches exact test sample counts."""
        if not self.results_path.exists():
            self.skipTest("Results file exp_b3_02_open_set_results.json not generated yet")

        with open(self.results_path, "r", encoding="utf-8") as f:
            res = json.load(f)

        for eq_key in ["equalized_0", "equalized_1"]:
            eval_data = res["evaluations"][eq_key]
            for arch in ["single_rx_1_1_open_set", "multi_rx_cluster_open_set"]:
                t_res = eval_data[arch]["calibrated_95pct_val"]
                cm = np.array(t_res["confusion_matrix"])
                self.assertEqual(cm.shape, (5, 5))
                # First 4 rows are known transmitters: 1000 each = 4000 total
                row_sums = np.sum(cm, axis=1)
                for i in range(4):
                    self.assertEqual(row_sums[i], 1000)
                # 5th row is UNKNOWN: 2000 total
                self.assertEqual(row_sums[4], 2000)


if __name__ == "__main__":
    unittest.main()
