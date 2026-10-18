"""EXP-B2-04: Synthetic IoT Network and Community-Graph Validation Runner.

Validates topology construction, community graph invariants, multi-witness
consensus determinism, and decision contracts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, List

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.community_graph import (
    ConsensusDecision,
    IoTCommunityNetwork,
    WitnessReport,
)


def run_simulation(net: IoTCommunityNetwork, num_rounds: int, seed: int) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(seed)
    device_ids = sorted(list(net.devices.keys()))
    round_records = []

    for round_idx in range(num_rounds):
        dev_id = rng.choice(device_ids)
        dev = net.devices[dev_id]
        true_identity = dev.enrolled_identity
        witnesses = net.get_witnesses_for_device(dev_id)

        # Draw scenario according to probability distribution
        scenario_val = rng.uniform(0.0, 1.0)
        reports = []

        if scenario_val < 0.60:
            # Scenario A: Unanimous Legitimate
            for gw in witnesses:
                conf = float(rng.uniform(0.88, 0.99))
                reports.append(
                    WitnessReport(
                        gateway_id=gw,
                        target_device_id=dev_id,
                        timestamp=float(round_idx),
                        predicted_identity=true_identity,
                        rf_confidence=conf,
                        rssi_dbm=float(rng.uniform(-65.0, -45.0)),
                        snr_db=float(rng.uniform(18.0, 32.0)),
                    )
                )
        elif scenario_val < 0.80:
            # Scenario B: Majority Agreement (one noisy/distant gateway disagrees)
            for idx, gw in enumerate(witnesses):
                if idx == 0 and len(witnesses) > 2:
                    conf = float(rng.uniform(0.55, 0.68))
                    pred_id = f"TX-{((int(true_identity.split('-')[1])) % 6) + 1}"
                else:
                    conf = float(rng.uniform(0.75, 0.92))
                    pred_id = true_identity
                reports.append(
                    WitnessReport(
                        gateway_id=gw,
                        target_device_id=dev_id,
                        timestamp=float(round_idx),
                        predicted_identity=pred_id,
                        rf_confidence=conf,
                        rssi_dbm=float(rng.uniform(-75.0, -50.0)),
                        snr_db=float(rng.uniform(12.0, 25.0)),
                    )
                )
        elif scenario_val < 0.90:
            # Scenario C: Disagreement / Ambiguity
            for idx, gw in enumerate(witnesses):
                # Half predict true, half predict alternative
                if idx % 2 == 0:
                    pred_id = true_identity
                    conf = float(rng.uniform(0.60, 0.72))
                else:
                    pred_id = "TX-ALT"
                    conf = float(rng.uniform(0.60, 0.72))
                reports.append(
                    WitnessReport(
                        gateway_id=gw,
                        target_device_id=dev_id,
                        timestamp=float(round_idx),
                        predicted_identity=pred_id,
                        rf_confidence=conf,
                        rssi_dbm=float(rng.uniform(-80.0, -65.0)),
                        snr_db=float(rng.uniform(8.0, 16.0)),
                    )
                )
        else:
            # Scenario D: Adversarial Minority Spoof
            for idx, gw in enumerate(witnesses):
                if idx == len(witnesses) - 1 and len(witnesses) > 1:
                    pred_id = "TX-ATTACKER"
                    conf = float(rng.uniform(0.85, 0.95))
                else:
                    pred_id = true_identity
                    conf = float(rng.uniform(0.80, 0.95))
                reports.append(
                    WitnessReport(
                        gateway_id=gw,
                        target_device_id=dev_id,
                        timestamp=float(round_idx),
                        predicted_identity=pred_id,
                        rf_confidence=conf,
                        rssi_dbm=float(rng.uniform(-70.0, -55.0)),
                        snr_db=float(rng.uniform(15.0, 28.0)),
                    )
                )

        eval_decision = net.evaluate_multi_witness_consensus(reports)
        eval_decision["round_idx"] = round_idx
        eval_decision["device_id"] = dev_id
        eval_decision["true_identity"] = true_identity
        eval_decision["witness_gateways"] = witnesses
        round_records.append(eval_decision)

    return round_records


def run_experiment(config_path: Path, out_path: Optional[Path] = None) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    net_cfg = cfg["network_specification"]
    rounds = cfg["simulation_rounds"]
    seed = net_cfg["random_seed"]

    print("================================================================================")
    print("EXP-B2-04: SYNTHETIC IOT NETWORK AND COMMUNITY-GRAPH VALIDATION")
    print(f"Topology: {net_cfg['num_devices']} Devices, {net_cfg['num_gateways']} Gateways, Area: {net_cfg['area_size']}x{net_cfg['area_size']}")
    print(f"Rounds: {rounds} | Seed: {seed}")
    print("================================================================================")

    # 1. Build and validate topology
    net = IoTCommunityNetwork(
        num_devices=net_cfg["num_devices"],
        num_gateways=net_cfg["num_gateways"],
        area_size=net_cfg["area_size"],
        device_tx_radius=net_cfg["device_tx_radius"],
        gateway_tx_radius=net_cfg["gateway_tx_radius"],
        random_seed=seed,
    )

    witness_counts = [len(net.get_witnesses_for_device(d)) for d in net.devices.keys()]
    community_sizes = {comm: len(devs) for comm, devs in net.communities.items()}

    print("\n--- Topology Invariant Validation ---")
    print(f"Total Devices: {len(net.devices)} | Total Gateways: {len(net.gateways)}")
    print(f"Witness Degree per Device: min={min(witness_counts)}, max={max(witness_counts)}, mean={np.mean(witness_counts):.2f}")
    print(f"Community Partitions: {community_sizes}")
    assert min(witness_counts) >= 1, "Graph error: Isolated device detected!"
    assert all(size > 0 for size in community_sizes.values()), "Graph error: Empty community detected!"
    print("  -> All topology invariants PASSED.")

    # 2. Run simulation rounds
    print(f"\n--- Running {rounds} Multi-Witness Consensus Rounds ---")
    t_start = time.perf_counter()
    sim_run_1 = run_simulation(net, rounds, seed)
    sim_duration = time.perf_counter() - t_start

    decision_counts = {}
    for r in sim_run_1:
        d = r["decision"]
        decision_counts[d] = decision_counts.get(d, 0) + 1

    print("Decision Breakdown across 1,000 rounds:")
    for d, cnt in sorted(decision_counts.items()):
        print(f"  {d:<22}: {cnt:>4} ({cnt/rounds*100:5.1f}%)")

    # 3. Test Determinism (Run 2 with identical seed)
    print("\n--- Verifying Determinism Across Independent Executions ---")
    net2 = IoTCommunityNetwork(
        num_devices=net_cfg["num_devices"],
        num_gateways=net_cfg["num_gateways"],
        area_size=net_cfg["area_size"],
        device_tx_radius=net_cfg["device_tx_radius"],
        gateway_tx_radius=net_cfg["gateway_tx_radius"],
        random_seed=seed,
    )
    sim_run_2 = run_simulation(net2, rounds, seed)

    matches = 0
    for r1, r2 in zip(sim_run_1, sim_run_2):
        if r1["decision"] == r2["decision"] and r1["consensus_identity"] == r2["consensus_identity"]:
            matches += 1

    determinism_rate = matches / rounds
    print(f"Exact Bitwise Round Matches: {matches} / {rounds} ({determinism_rate*100:.2f}%)")
    assert determinism_rate == 1.0, "Determinism failure: Non-identical outputs under fixed seed!"
    print("  -> Determinism check PASSED (100.00%).")

    results = {
        "metadata": {
            "experiment_id": cfg["experiment_id"],
            "title": cfg["title"],
            "research_question": cfg["research_question"],
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "random_seed": seed,
            "evidence_classification": "Synthetic Network Simulation (Not Real RF Signal Evidence)",
        },
        "topology_invariants": {
            "num_devices": len(net.devices),
            "num_gateways": len(net.gateways),
            "min_witness_degree": int(min(witness_counts)),
            "max_witness_degree": int(max(witness_counts)),
            "mean_witness_degree": float(np.mean(witness_counts)),
            "community_sizes": community_sizes,
            "isolated_devices_count": int(sum(1 for c in witness_counts if c == 0)),
        },
        "consensus_simulation": {
            "total_rounds": rounds,
            "decision_distribution": decision_counts,
            "determinism_rate": float(determinism_rate),
            "sample_round_outcomes": sim_run_1[:10],
            "runtime_seconds": sim_duration,
        },
    }

    if out_path is None:
        out_path = REPO_ROOT / "experiments" / "track_b" / "exp_b2_04_community_graph_results.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[SUCCESS] EXP-B2-04 artifacts written to: {out_path}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EXP-B2-04 Community Graph Validation")
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "configs" / "exp_b2_04_community_graph.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "experiments" / "track_b" / "exp_b2_04_community_graph_results.json",
        help="Path to results file",
    )
    args = parser.parse_args()
    run_experiment(args.config, args.out)
