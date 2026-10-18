"""Unit tests for Phase 5 Master Comprehensive Evaluation contracts and evidence synthesis."""

import json
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestPhase5Evaluation(unittest.TestCase):
    """Validates collation, cross-phase invariants, and benchmark evidence in Phase 5."""

    @classmethod
    def setUpClass(cls):
        cls.phase5_results_path = REPO_ROOT / "experiments" / "track_b" / "phase5_comprehensive_evaluation_results.json"

    def test_results_artifact_exists_and_valid(self):
        """Verifies presence and schema of master Phase 5 evaluation results."""
        if not self.phase5_results_path.exists():
            self.skipTest("Phase 5 results not generated yet")

        with open(self.phase5_results_path, "r", encoding="utf-8") as f:
            res = json.load(f)

        self.assertIn("collated_experiments", res)
        self.assertIn("performance_and_resource_benchmarks", res)
        self.assertEqual(res["overall_synthesis_verdict"], "PHASE_2_3_4_COMPLETE_AND_VERIFIED")

        collated = res["collated_experiments"]
        expected_experiments = [
            "EXP-B2-01", "EXP-B2-02", "EXP-B2-03", "EXP-B2-04", "EXP-B2-05",
            "EXP-B3-01", "EXP-B3-02", "EXP-B4-01"
        ]
        for exp_id in expected_experiments:
            self.assertIn(exp_id, collated)
            self.assertEqual(collated[exp_id]["status"], "VALIDATED_AND_VERIFIED")

    def test_resource_benchmarks(self):
        """Verifies that performance and memory benchmarks are positive and reasonable."""
        if not self.phase5_results_path.exists():
            self.skipTest("Phase 5 results not generated yet")

        with open(self.phase5_results_path, "r", encoding="utf-8") as f:
            res = json.load(f)

        benchmarks = res["performance_and_resource_benchmarks"]
        self.assertGreater(benchmarks["consensus_throughput_rounds_per_sec"], 0.0)
        self.assertGreater(benchmarks["auth_throughput_tx_per_sec"], 0.0)
        self.assertGreater(benchmarks["peak_process_rss_mb"], 0.0)


if __name__ == "__main__":
    unittest.main()
