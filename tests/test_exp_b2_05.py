"""Unit tests for EXP-B2-05 Community Gated Adaptation and Threat Model."""

import json
from pathlib import Path
import unittest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.community_graph import ConsensusDecision
from src.community_gating import (
    CommunityGatedAdapter,
    DeviceProfile,
    UpdateDecision,
)


class TestExpB205(unittest.TestCase):
    def setUp(self):
        self.adapter = CommunityGatedAdapter(
            learning_rate=0.05,
            max_drift_threshold_std=3.0,
        )
        self.profile = DeviceProfile(
            device_id="DEV-001",
            target_transmitter="TX-1",
            feature_prototype=np.zeros(16, dtype=np.float64),
            feature_variance=np.ones(16, dtype=np.float64),
        )

    def test_legitimate_update_commit(self):
        candidate = np.full(16, 0.5)
        cons = {
            "decision": ConsensusDecision.UNANIMOUS_ACCEPT.value,
            "consensus_identity": "TX-1",
            "mean_confidence": 0.95,
        }
        res = self.adapter.evaluate_update_contract(
            self.profile, candidate, cons, gating_mode="community_gated"
        )
        self.assertEqual(res["update_decision"], UpdateDecision.AUTHORIZED_COMMIT.value)
        self.assertEqual(self.profile.update_count, 1)

    def test_excessive_drift_quarantine(self):
        # 4.0 sigma displacement
        candidate = np.full(16, 4.0)
        cons = {
            "decision": ConsensusDecision.UNANIMOUS_ACCEPT.value,
            "consensus_identity": "TX-1",
            "mean_confidence": 0.95,
        }
        res = self.adapter.evaluate_update_contract(
            self.profile, candidate, cons, gating_mode="community_gated"
        )
        self.assertEqual(res["update_decision"], UpdateDecision.QUARANTINE_HOLD.value)
        self.assertEqual(self.profile.update_count, 0)
        self.assertEqual(len(self.profile.quarantine_buffer), 1)

    def test_rejection_on_consensus_rejection(self):
        candidate = np.full(16, 0.2)
        cons = {
            "decision": ConsensusDecision.CONSENSUS_REJECT.value,
            "consensus_identity": None,
            "mean_confidence": 0.40,
        }
        res = self.adapter.evaluate_update_contract(
            self.profile, candidate, cons, gating_mode="community_gated"
        )
        self.assertEqual(res["update_decision"], UpdateDecision.REJECT_DISCARD.value)
        self.assertEqual(self.profile.update_count, 0)

    def test_naive_vulnerability_to_spoofing(self):
        # Attacker matches target with high single-node confidence but large drift
        candidate = np.full(16, 3.5)
        cons = {
            "decision": ConsensusDecision.UNANIMOUS_ACCEPT.value,
            "consensus_identity": "TX-1",
            "mean_confidence": 0.90,
        }
        # Naive accepts
        res_naive = self.adapter.evaluate_update_contract(
            self.profile, candidate, cons, gating_mode="no_community_naive"
        )
        self.assertEqual(res_naive["update_decision"], UpdateDecision.AUTHORIZED_COMMIT.value)


if __name__ == "__main__":
    unittest.main()
