"""EXP-B2-05: Community-Gated Continual Adaptation and Poisoning Evaluation Runner.

Evaluates legitimate adaptation acceptance, poisoning contamination resistance,
and comparative defense performance against naive baselines and network disruptions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Tuple

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.community_graph import (
    ConsensusDecision,
    IoTCommunityNetwork,
    WitnessReport,
)
from src.community_gating import (
    CommunityGatedAdapter,
    DeviceProfile,
    UpdateDecision,
)


def run_architecture_evaluation(
    net: IoTCommunityNetwork,
    adapter: CommunityGatedAdapter,
    mode: str,
    num_rounds: Dict[str, int],
    seed: int,
    disruption_prob: float = 0.0,
) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    dim = 16
    initial_proto = rng.normal(0.0, 1.0, size=(dim,))
    initial_var = np.ones(dim, dtype=np.float64)

    profile = DeviceProfile(
        device_id="DEV-001",
        target_transmitter="TX-1",
        feature_prototype=initial_proto.copy(),
        feature_variance=initial_var.copy(),
    )

    legit_rounds = num_rounds.get("legitimate_adaptation", 500)
    poison_rounds = num_rounds.get("gradual_poisoning", 200)
    spoof_rounds = num_rounds.get("target_like_spoofing", 150)
    replay_rounds = num_rounds.get("replay_attack", 150)

    stats = {
        "legitimate": {"accepted": 0, "quarantined": 0, "rejected": 0, "total": legit_rounds},
        "poisoning": {"accepted": 0, "quarantined": 0, "rejected": 0, "total": poison_rounds},
        "spoofing": {"accepted": 0, "quarantined": 0, "rejected": 0, "total": spoof_rounds},
        "replay": {"accepted": 0, "quarantined": 0, "rejected": 0, "total": replay_rounds},
    }

    # --------------------------------------------------------------------------
    # 1. Legitimate Adaptation Phase (Slow physical drift, multi-witness agreement)
    # --------------------------------------------------------------------------
    current_true_features = initial_proto.copy()
    for _ in range(legit_rounds):
        drift_step = rng.normal(0.0, 0.15, size=(dim,))
        current_true_features += drift_step

        witnesses = net.get_witnesses_for_device("DEV-001")
        if disruption_prob > 0.0:
            witnesses = [gw for gw in witnesses if rng.uniform(0.0, 1.0) > disruption_prob]

        reports = []
        for gw in witnesses:
            reports.append(
                WitnessReport(
                    gateway_id=gw,
                    target_device_id="DEV-001",
                    timestamp=1.0,
                    predicted_identity="TX-1",
                    rf_confidence=float(rng.uniform(0.85, 0.98)),
                    rssi_dbm=float(rng.uniform(-65.0, -50.0)),
                    snr_db=float(rng.uniform(20.0, 30.0)),
                )
            )

        cons = net.evaluate_multi_witness_consensus(reports)
        res = adapter.evaluate_update_contract(
            profile, current_true_features, cons, gating_mode="community_gated" if mode.startswith("community") else mode
        )

        dec = res["update_decision"]
        if dec == UpdateDecision.AUTHORIZED_COMMIT.value:
            stats["legitimate"]["accepted"] += 1
        elif dec == UpdateDecision.QUARANTINE_HOLD.value:
            stats["legitimate"]["quarantined"] += 1
        else:
            stats["legitimate"]["rejected"] += 1

    # --------------------------------------------------------------------------
    # 2. Gradual Poisoning Attack Phase (Malicious drift displaced 3.5 sigma)
    # --------------------------------------------------------------------------
    for _ in range(poison_rounds):
        malicious_features = profile.feature_prototype + rng.normal(3.5, 0.2, size=(dim,))
        witnesses = net.get_witnesses_for_device("DEV-001")
        reports = []
        # Attacker injects observation; minority gateway deceived, majority observes anomaly
        for idx, gw in enumerate(witnesses):
            if idx == 0:
                reports.append(WitnessReport(gw, "DEV-001", 2.0, "TX-1", 0.95, -55.0, 25.0))
            else:
                reports.append(WitnessReport(gw, "DEV-001", 2.0, "TX-ANOMALOUS", 0.50, -75.0, 10.0))

        cons = net.evaluate_multi_witness_consensus(reports)
        res = adapter.evaluate_update_contract(
            profile, malicious_features, cons, gating_mode="community_gated" if mode.startswith("community") else mode
        )

        dec = res["update_decision"]
        if dec == UpdateDecision.AUTHORIZED_COMMIT.value:
            stats["poisoning"]["accepted"] += 1
        elif dec == UpdateDecision.QUARANTINE_HOLD.value:
            stats["poisoning"]["quarantined"] += 1
        else:
            stats["poisoning"]["rejected"] += 1

    # --------------------------------------------------------------------------
    # 3. Target-Like Spoofing Phase (Attacker deceives 1 gateway; honest gateways see anomaly)
    # --------------------------------------------------------------------------
    for _ in range(spoof_rounds):
        # Spoofer crafts features within reasonable distance (1.2 sigma) to target TX-1
        spoofed_features = profile.feature_prototype + rng.normal(1.2, 0.3, size=(dim,))
        witnesses = net.get_witnesses_for_device("DEV-001")
        reports = []
        for idx, gw in enumerate(witnesses):
            if idx == 0:
                # Deceived local gateway predicts TX-1 with high confidence
                reports.append(WitnessReport(gw, "DEV-001", 3.0, "TX-1", 0.92, -58.0, 22.0))
            else:
                # Other distributed gateways see multi-path anomaly / conflicting identity
                reports.append(WitnessReport(gw, "DEV-001", 3.0, "TX-ANOMALOUS", 0.75, -72.0, 12.0))

        cons = net.evaluate_multi_witness_consensus(reports)
        res = adapter.evaluate_update_contract(
            profile, spoofed_features, cons, gating_mode="community_gated" if mode.startswith("community") else mode
        )

        dec = res["update_decision"]
        if dec == UpdateDecision.AUTHORIZED_COMMIT.value:
            stats["spoofing"]["accepted"] += 1
        elif dec == UpdateDecision.QUARANTINE_HOLD.value:
            stats["spoofing"]["quarantined"] += 1
        else:
            stats["spoofing"]["rejected"] += 1

    # --------------------------------------------------------------------------
    # 4. Replay Attack Phase (Single-gateway uncorroborated replay)
    # --------------------------------------------------------------------------
    for _ in range(replay_rounds):
        stale_features = initial_proto.copy()
        # Single witness report without multi-angle corroboration
        reports = [WitnessReport("GW-1", "DEV-001", 4.0, "TX-1", 0.99, -50.0, 30.0)]
        cons = net.evaluate_multi_witness_consensus(reports)
        res = adapter.evaluate_update_contract(
            profile, stale_features, cons, gating_mode="community_gated" if mode.startswith("community") else mode
        )

        dec = res["update_decision"]
        if dec == UpdateDecision.AUTHORIZED_COMMIT.value:
            stats["replay"]["accepted"] += 1
        elif dec == UpdateDecision.QUARANTINE_HOLD.value:
            stats["replay"]["quarantined"] += 1
        else:
            stats["replay"]["rejected"] += 1

    final_distortion = float(np.linalg.norm(profile.feature_prototype - current_true_features))

    return {
        "mode": mode,
        "disruption_prob": disruption_prob,
        "stats": stats,
        "legitimate_acceptance_rate": stats["legitimate"]["accepted"] / legit_rounds,
        "poisoning_contamination_rate": stats["poisoning"]["accepted"] / poison_rounds,
        "spoofing_acceptance_rate": stats["spoofing"]["accepted"] / spoof_rounds,
        "replay_acceptance_rate": stats["replay"]["accepted"] / replay_rounds,
        "false_hold_rate": stats["legitimate"]["quarantined"] / legit_rounds,
        "false_rejection_rate": stats["legitimate"]["rejected"] / legit_rounds,
        "final_profile_distortion": final_distortion,
        "total_updates_committed": profile.update_count,
        "quarantine_buffer_size": len(profile.quarantine_buffer),
    }


def run_experiment(config_path: Path, out_path: Optional[Path] = None) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    seed = cfg["simulation_profile"]["random_seed"]
    rounds = cfg["simulation_profile"]["rounds_per_scenario"]

    print("================================================================================")
    print("EXP-B2-05: COMMUNITY-GATED ADAPTATION AND POISONING EVALUATION")
    print(f"Scenarios: Legitimate={rounds['legitimate_adaptation']}, Poisoning={rounds['gradual_poisoning']}, Spoofing={rounds['target_like_spoofing']}, Replay={rounds['replay_attack']}")
    print(f"Seed: {seed}")
    print("================================================================================")

    net = IoTCommunityNetwork(num_devices=50, num_gateways=5, random_seed=seed)
    adapter = CommunityGatedAdapter(
        learning_rate=cfg["simulation_profile"]["learning_rate"],
        max_drift_threshold_std=cfg["simulation_profile"]["max_drift_threshold_std"],
    )

    evaluations = {}

    for mode in ["no_community_naive", "threshold_only", "community_gated", "community_disrupted_ablation"]:
        disruption = 0.50 if mode == "community_disrupted_ablation" else 0.0
        print(f"\n--- Evaluating Architecture: {mode} (Disruption: {disruption*100:.0f}%) ---")
        res = run_architecture_evaluation(net, adapter, mode, rounds, seed, disruption_prob=disruption)
        evaluations[mode] = res

        print(f"  Legitimate Acceptance Rate : {res['legitimate_acceptance_rate']*100:6.2f}%")
        print(f"  Poisoning Contamination Rate: {res['poisoning_contamination_rate']*100:6.2f}%")
        print(f"  Spoofing Acceptance Rate    : {res['spoofing_acceptance_rate']*100:6.2f}%")
        print(f"  Replay Acceptance Rate      : {res['replay_acceptance_rate']*100:6.2f}%")
        print(f"  False Hold / Reject Rate    : {res['false_hold_rate']*100:5.2f}% / {res['false_rejection_rate']*100:5.2f}%")
        print(f"  Final Profile Distortion    : {res['final_profile_distortion']:.4f}")

    results = {
        "metadata": {
            "experiment_id": cfg["experiment_id"],
            "title": cfg["title"],
            "research_question": cfg["research_question"],
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "threat_model": cfg["threat_model"],
            "evidence_classification": "Synthetic Controlled Attack Simulation (Not Real Physical RF Attack)",
        },
        "evaluations": evaluations,
    }

    if out_path is None:
        out_path = REPO_ROOT / "experiments" / "track_b" / "exp_b2_05_community_gating_results.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[SUCCESS] EXP-B2-05 artifacts written to: {out_path}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EXP-B2-05 Community Gating Evaluation")
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "configs" / "exp_b2_05_community_gating.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "experiments" / "track_b" / "exp_b2_05_community_gating_results.json",
        help="Path to results file",
    )
    args = parser.parse_args()
    run_experiment(args.config, args.out)
