"""Unit tests for EXP-B2-04 Synthetic IoT Network and Community Graph."""

import json
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.community_graph import (
    ConsensusDecision,
    IoTCommunityNetwork,
    WitnessReport,
)


class TestExpB204(unittest.TestCase):
    def setUp(self):
        self.net = IoTCommunityNetwork(
            num_devices=50,
            num_gateways=5,
            area_size=100.0,
            device_tx_radius=40.0,
            gateway_tx_radius=60.0,
            random_seed=20260902,
        )

    def test_topology_counts_and_invariants(self):
        self.assertEqual(len(self.net.devices), 50)
        self.assertEqual(len(self.net.gateways), 5)
        # Every device must have at least 1 gateway witness
        for dev_id in self.net.devices.keys():
            witnesses = self.net.get_witnesses_for_device(dev_id)
            self.assertGreaterEqual(len(witnesses), 1)

    def test_community_partitioning(self):
        # 5 gateways -> 5 communities
        self.assertEqual(len(self.net.communities), 5)
        total_assigned = sum(len(devs) for devs in self.net.communities.values())
        self.assertEqual(total_assigned, 50)

    def test_unanimous_consensus(self):
        reports = [
            WitnessReport("GW-1", "DEV-001", 0.0, "TX-1", 0.95, -50.0, 25.0),
            WitnessReport("GW-2", "DEV-001", 0.0, "TX-1", 0.92, -55.0, 22.0),
            WitnessReport("GW-3", "DEV-001", 0.0, "TX-1", 0.89, -60.0, 20.0),
        ]
        res = self.net.evaluate_multi_witness_consensus(reports)
        self.assertEqual(res["decision"], ConsensusDecision.UNANIMOUS_ACCEPT.value)
        self.assertEqual(res["consensus_identity"], "TX-1")
        self.assertEqual(res["agreement_ratio"], 1.0)

    def test_majority_consensus(self):
        reports = [
            WitnessReport("GW-1", "DEV-001", 0.0, "TX-1", 0.85, -50.0, 25.0),
            WitnessReport("GW-2", "DEV-001", 0.0, "TX-1", 0.80, -55.0, 22.0),
            WitnessReport("GW-3", "DEV-001", 0.0, "TX-2", 0.60, -75.0, 10.0),
        ]
        res = self.net.evaluate_multi_witness_consensus(reports)
        self.assertEqual(res["decision"], ConsensusDecision.MAJORITY_ACCEPT.value)
        self.assertEqual(res["consensus_identity"], "TX-1")

    def test_quarantine_single_witness(self):
        reports = [
            WitnessReport("GW-1", "DEV-001", 0.0, "TX-1", 0.99, -50.0, 25.0)
        ]
        res = self.net.evaluate_multi_witness_consensus(reports)
        self.assertEqual(res["decision"], ConsensusDecision.QUARANTINE_HOLD.value)

    def test_rejection_on_split_vote(self):
        reports = [
            WitnessReport("GW-1", "DEV-001", 0.0, "TX-1", 0.50, -60.0, 15.0),
            WitnessReport("GW-2", "DEV-001", 0.0, "TX-2", 0.50, -60.0, 15.0),
            WitnessReport("GW-3", "DEV-001", 0.0, "TX-3", 0.50, -60.0, 15.0),
        ]
        res = self.net.evaluate_multi_witness_consensus(reports)
        self.assertEqual(res["decision"], ConsensusDecision.CONSENSUS_REJECT.value)
        self.assertIsNone(res["consensus_identity"])


if __name__ == "__main__":
    unittest.main()
