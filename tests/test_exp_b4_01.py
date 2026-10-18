"""Unit tests for EXP-B4-01 Integrated Authentication and Continual Adaptation Defense."""

import json
from pathlib import Path
import unittest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]

from src.community_graph import WitnessReport
from src.integrated_auth_engine import (
    DecisionOutcome,
    IntegratedAuthEngine,
    PersistentDeviceProfile,
    RejectionReason,
)


class TestExpB401Contracts(unittest.TestCase):
    """Validates configuration, decision contracts, failure modes, and hash chain integrity."""

    @classmethod
    def setUpClass(cls):
        cls.config_path = REPO_ROOT / "configs" / "exp_b4_01_integrated_defense.json"
        cls.results_path = REPO_ROOT / "experiments" / "track_b" / "exp_b4_01_integrated_defense_results.json"

    def setUp(self):
        self.profile = PersistentDeviceProfile(
            device_id="DEV_TEST_01",
            target_transmitter="14-10",
            feature_prototype=np.zeros(16, dtype=np.float64),
            feature_variance=np.ones(16, dtype=np.float64),
        )
        self.engine = IntegratedAuthEngine(
            learning_rate=0.05,
            max_drift_threshold_std=3.0,
            open_set_confidence_threshold=0.65,
            quarantine_capacity=5,
            min_witnesses_required=2,
        )

    def test_config_contract(self):
        """Verifies simulation parameters and round distribution."""
        self.assertTrue(self.config_path.exists(), "exp_b4_01_integrated_defense.json must exist")
        with open(self.config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.assertEqual(cfg["experiment_id"], "EXP-B4-01")
        self.assertEqual(cfg["simulation_parameters"]["total_rounds"], 1000)
        rounds_sum = sum(cfg["simulation_parameters"]["round_distribution"].values())
        self.assertEqual(rounds_sum, 1000)

    def test_malformed_input_rejection(self):
        """Verifies that malformed or NaN feature vectors are immediately rejected."""
        res_nan = self.engine.evaluate_transaction(
            profile=self.profile,
            candidate_features=np.array([np.nan] * 16),
            witness_reports=[],
            sequence_no=1,
            timestamp=1.0,
        )
        self.assertEqual(res_nan["decision"], DecisionOutcome.REJECT_DISCARD.value)
        self.assertEqual(res_nan["reason_code"], RejectionReason.INVALID_INPUT.value)

    def test_stale_replay_rejection(self):
        """Verifies that duplicate signature or stale sequence numbers are rejected."""
        features = np.ones(16) * 0.5
        witnesses = [
            WitnessReport("GW_0", "DEV_TEST_01", 10.0, "14-10", 0.95, -60.0, 25.0),
            WitnessReport("GW_1", "DEV_TEST_01", 10.0, "14-10", 0.92, -65.0, 22.0),
        ]
        # First transaction passes
        res1 = self.engine.evaluate_transaction(self.profile, features, witnesses, sequence_no=10, timestamp=10.0)
        self.assertEqual(res1["decision"], DecisionOutcome.AUTHORIZED_COMMIT.value)

        # Replay with same features or lower sequence number
        res2 = self.engine.evaluate_transaction(self.profile, features, witnesses, sequence_no=10, timestamp=10.0)
        self.assertEqual(res2["decision"], DecisionOutcome.REJECT_DISCARD.value)
        self.assertEqual(res2["reason_code"], RejectionReason.REPLAY_DETECTED.value)

    def test_unknown_transmitter_rejection(self):
        """Verifies that low-confidence predictions trigger unknown transmitter rejection."""
        features = np.ones(16) * 1.0
        # Witnesses have low confidence < 0.65
        witnesses = [
            WitnessReport("GW_0", "DEV_TEST_01", 20.0, "14-10", 0.45, -70.0, 15.0),
            WitnessReport("GW_1", "DEV_TEST_01", 20.0, "14-10", 0.50, -75.0, 14.0),
        ]
        res = self.engine.evaluate_transaction(self.profile, features, witnesses, sequence_no=20, timestamp=20.0)
        self.assertEqual(res["decision"], DecisionOutcome.REJECT_DISCARD.value)
        self.assertEqual(res["reason_code"], RejectionReason.UNKNOWN_TRANSMITTER.value)

    def test_excessive_drift_quarantine(self):
        """Verifies that candidate features exceeding standard deviation envelope are quarantined."""
        features = np.ones(16) * 5.0  # 5 std drift
        witnesses = [
            WitnessReport("GW_0", "DEV_TEST_01", 30.0, "14-10", 0.95, -60.0, 25.0),
            WitnessReport("GW_1", "DEV_TEST_01", 30.0, "14-10", 0.92, -65.0, 22.0),
        ]
        res = self.engine.evaluate_transaction(self.profile, features, witnesses, sequence_no=30, timestamp=30.0)
        self.assertEqual(res["decision"], DecisionOutcome.QUARANTINE_HOLD.value)
        self.assertEqual(res["reason_code"], RejectionReason.EXCESSIVE_DRIFT.value)

    def test_cryptographic_audit_hash_chain(self):
        """Verifies that the audit log maintains an unbroken SHA-256 hash chain."""
        features = np.ones(16) * 0.2
        witnesses = [
            WitnessReport("GW_0", "DEV_TEST_01", 40.0, "14-10", 0.95, -60.0, 25.0),
            WitnessReport("GW_1", "DEV_TEST_01", 40.0, "14-10", 0.92, -65.0, 22.0),
        ]
        self.engine.evaluate_transaction(self.profile, features, witnesses, sequence_no=40, timestamp=40.0)
        self.assertGreater(len(self.engine.audit_log), 0)
        for i in range(1, len(self.engine.audit_log)):
            self.assertEqual(self.engine.audit_log[i]["prev_hash"], self.engine.audit_log[i-1]["entry_hash"])

    def test_results_integrity(self):
        """If results file exists, verify that contamination rate is 0.0 for proposed method."""
        if not self.results_path.exists():
            self.skipTest("Results file exp_b4_01_integrated_defense_results.json not generated yet")

        with open(self.results_path, "r", encoding="utf-8") as f:
            res = json.load(f)

        self.assertIn("evaluations", res)
        evals = res["evaluations"]
        self.assertIn("no_community_naive", evals)
        self.assertIn("threshold_only", evals)
        self.assertIn("community_gated_integrated", evals)

        proposed = evals["community_gated_integrated"]
        self.assertEqual(proposed["continual_adaptation_metrics"]["contamination_rate"], 0.0)
        self.assertTrue(proposed["security_audit_logging"]["cryptographic_hash_chain_verified"])


if __name__ == "__main__":
    unittest.main()
