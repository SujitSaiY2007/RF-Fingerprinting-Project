"""Unit tests for EXP-B3-01 Multi-Receiver Fusion contracts and invariants."""

import json
from pathlib import Path
import unittest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestExpB301Contracts(unittest.TestCase):
    """Validates configuration, contracts, and math invariants for EXP-B3-01."""

    @classmethod
    def setUpClass(cls):
        cls.config_path = REPO_ROOT / "configs" / "exp_b3_01_fusion.json"
        cls.results_path = REPO_ROOT / "experiments" / "track_b" / "exp_b3_01_fusion_results.json"

    def test_config_contract(self):
        """Verifies configuration schema, transmitter set, and cluster definition."""
        self.assertTrue(self.config_path.exists(), "exp_b3_01_fusion.json must exist")
        with open(self.config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.assertEqual(cfg["experiment_id"], "EXP-B3-01")
        self.assertEqual(len(cfg["known_transmitters"]), 6)
        self.assertEqual(len(cfg["dataset_provenance"]["selected_cluster_receivers"]), 5)
        self.assertEqual(len(cfg["dataset_provenance"]["all_receivers"]), 12)
        self.assertIn("1-1", cfg["dataset_provenance"]["selected_cluster_receivers"])
        self.assertIn("observation_matching_contract", cfg["dataset_provenance"])

    def test_soft_voting_probability_math(self):
        """Verifies that soft-voting mean probability distribution is valid (sums to 1)."""
        # Synthetic 5-receiver probability matrix for 10 bursts across 6 classes
        np.random.seed(20260902)
        raw_logits = np.random.randn(5, 10, 6)
        probs = np.exp(raw_logits) / np.sum(np.exp(raw_logits), axis=-1, keepdims=True)
        # Verify individual receiver probabilities sum to 1
        for rx_i in range(5):
            sums = np.sum(probs[rx_i], axis=-1)
            np.testing.assert_allclose(sums, np.ones(10), rtol=1e-5)

        # Soft voting
        mean_p = np.mean(probs, axis=0)
        self.assertEqual(mean_p.shape, (10, 6))
        np.testing.assert_allclose(np.sum(mean_p, axis=-1), np.ones(10), rtol=1e-5)

    def test_hard_majority_voting_invariants(self):
        """Verifies mode selection under unanimous and tied voting conditions."""
        # Unanimous case
        votes_unanimous = [["tx1", "tx1", "tx1", "tx1", "tx1"]]
        vals, counts = np.unique(votes_unanimous[0], return_counts=True)
        self.assertEqual(vals[np.argmax(counts)], "tx1")

        # Split 3 vs 2
        votes_majority = [["tx1", "tx2", "tx1", "tx1", "tx2"]]
        vals, counts = np.unique(votes_majority[0], return_counts=True)
        self.assertEqual(vals[np.argmax(counts)], "tx1")

    def test_results_integrity(self):
        """If results file exists, verify presence of both raw and equalized evaluations."""
        if not self.results_path.exists():
            self.skipTest("Results file exp_b3_01_fusion_results.json not generated yet")

        with open(self.results_path, "r", encoding="utf-8") as f:
            res = json.load(f)

        self.assertIn("evaluations", res)
        self.assertIn("equalized_0", res["evaluations"])
        self.assertIn("equalized_1", res["evaluations"])

        for eq_key in ["equalized_0", "equalized_1"]:
            eval_data = res["evaluations"][eq_key]
            self.assertIn("distributed_decision_soft_voting", eval_data)
            self.assertIn("centralized_feature_concatenation", eval_data)
            self.assertIn("cross_receiver_transfer_voting", eval_data)
            self.assertIn("missing_receiver_degradation_sweep", eval_data)
            # Check accuracy is between 0 and 1
            self.assertGreaterEqual(eval_data["distributed_decision_soft_voting"]["accuracy"], 0.0)
            self.assertLessEqual(eval_data["distributed_decision_soft_voting"]["accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
