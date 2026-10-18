"""EXP-B4-01: Integrated Community-Aware Authorization and Continual Adaptation Defense Runner.

Simulates 1,000 adaptation rounds across legitimate drift, stealthy poisoning, target spoofing,
stale replay, and unknown transmitters under matched threat models and denominators.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import psutil

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.community_graph import WitnessReport
from src.integrated_auth_engine import DecisionOutcome, IntegratedAuthEngine, PersistentDeviceProfile
from src.manysig_features import FEATURE_NAMES

PRIMARY_DEVICE_ID = "DEV_AUTH_01"
TARGET_TRANSMITTER = "14-10"


def get_environment_info() -> Dict[str, str]:
    import sklearn
    import pyarrow
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "scikit_learn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "pyarrow_version": pyarrow.__version__,
    }


def load_ground_truth_profile(features_dir: Path) -> Tuple[np.ndarray, np.ndarray]:
    parquet_path = features_dir / "rx_id=1-1" / "is_equalized=1" / "data.parquet"
    df = pd.read_parquet(parquet_path)
    tx_df = df[df["tx_id"] == TARGET_TRANSMITTER]
    mean_vec = tx_df[list(FEATURE_NAMES)].mean().values.astype(np.float64)
    var_vec = tx_df[list(FEATURE_NAMES)].var().values.astype(np.float64)
    return mean_vec, var_vec


def generate_scenarios(
    base_prototype: np.ndarray,
    base_variance: np.ndarray,
    sim_params: Dict[str, Any],
) -> List[Dict[str, Any]]:
    np.random.seed(sim_params["random_seed"])
    rounds_spec = sim_params["round_distribution"]
    std_vec = np.sqrt(np.maximum(base_variance, 1e-6))

    # Interleave rounds deterministically
    scenario_types = (
        ["legitimate_drift"] * rounds_spec["legitimate_drift"]
        + ["stealthy_poisoning"] * rounds_spec["stealthy_poisoning"]
        + ["target_spoofing"] * rounds_spec["target_spoofing"]
        + ["stale_replay"] * rounds_spec["stale_replay"]
        + ["unknown_transmitter"] * rounds_spec["unknown_transmitter"]
    )
    np.random.shuffle(scenario_types)

    scenarios: List[Dict[str, Any]] = []
    poison_direction = np.ones(16) * 3.0 * std_vec
    past_legitimate_features: List[np.ndarray] = [base_prototype.copy()]

    for t, stype in enumerate(scenario_types, start=1):
        if stype == "legitimate_drift":
            drift = np.random.normal(0.0, 1.0, size=16) * std_vec
            feat = base_prototype + drift
            past_legitimate_features.append(feat.copy())
            num_witnesses = np.random.randint(3, 6)
            witnesses = [
                WitnessReport(
                    gateway_id=f"GW_{w}",
                    target_device_id=PRIMARY_DEVICE_ID,
                    timestamp=float(t),
                    predicted_identity=TARGET_TRANSMITTER,
                    rf_confidence=float(np.random.uniform(0.85, 0.99)),
                    rssi_dbm=float(np.random.uniform(-65, -50)),
                    snr_db=float(np.random.uniform(20, 35)),
                )
                for w in range(num_witnesses)
            ]
            scenarios.append({
                "round_id": t - 1,
                "category": "legitimate_drift",
                "is_attack": False,
                "candidate_features": feat,
                "witnesses": witnesses,
                "sequence_no": t,
                "timestamp": float(t),
            })

        elif stype == "stealthy_poisoning":
            noise = np.random.normal(0.0, 0.3, size=16) * std_vec
            feat = base_prototype + poison_direction + noise
            witnesses = [
                WitnessReport("GW_0", PRIMARY_DEVICE_ID, float(t), TARGET_TRANSMITTER, 0.75, -60.0, 25.0),
                WitnessReport("GW_1", PRIMARY_DEVICE_ID, float(t), "14-7", 0.55, -75.0, 15.0),
                WitnessReport("GW_2", PRIMARY_DEVICE_ID, float(t), TARGET_TRANSMITTER, 0.60, -72.0, 18.0),
            ]
            scenarios.append({
                "round_id": t - 1,
                "category": "stealthy_poisoning",
                "is_attack": True,
                "candidate_features": feat,
                "witnesses": witnesses,
                "sequence_no": t,
                "timestamp": float(t),
            })

        elif stype == "target_spoofing":
            displacement = np.random.normal(4.5, 0.5, size=16) * std_vec
            feat = base_prototype + displacement
            witnesses = [
                WitnessReport("GW_0", PRIMARY_DEVICE_ID, float(t), TARGET_TRANSMITTER, 0.72, -55.0, 28.0),
                WitnessReport("GW_1", PRIMARY_DEVICE_ID, float(t), "20-15", 0.70, -80.0, 12.0),
            ]
            scenarios.append({
                "round_id": t - 1,
                "category": "target_spoofing",
                "is_attack": True,
                "candidate_features": feat,
                "witnesses": witnesses,
                "sequence_no": t,
                "timestamp": float(t),
            })

        elif stype == "stale_replay":
            # Replay a previously transmitted feature with a stale sequence number
            past_idx = np.random.randint(0, len(past_legitimate_features))
            feat = past_legitimate_features[past_idx].copy()
            stale_seq = np.random.randint(1, max(2, t))  # Stale sequence number
            witnesses = [
                WitnessReport("GW_0", PRIMARY_DEVICE_ID, float(stale_seq), TARGET_TRANSMITTER, 0.98, -55.0, 30.0),
                WitnessReport("GW_1", PRIMARY_DEVICE_ID, float(stale_seq), TARGET_TRANSMITTER, 0.96, -58.0, 28.0),
            ]
            scenarios.append({
                "round_id": t - 1,
                "category": "stale_replay",
                "is_attack": True,
                "candidate_features": feat,
                "witnesses": witnesses,
                "sequence_no": stale_seq,
                "timestamp": float(stale_seq),
            })

        elif stype == "unknown_transmitter":
            displacement = np.random.normal(2.0, 1.0, size=16) * std_vec
            feat = base_prototype + displacement
            witnesses = [
                WitnessReport(
                    f"GW_{w}",
                    PRIMARY_DEVICE_ID,
                    float(t),
                    np.random.choice(["6-15", "8-20", TARGET_TRANSMITTER]),
                    float(np.random.uniform(0.35, 0.58)),
                    -70.0,
                    16.0,
                )
                for w in range(3)
            ]
            scenarios.append({
                "round_id": t - 1,
                "category": "unknown_transmitter",
                "is_attack": True,
                "candidate_features": feat,
                "witnesses": witnesses,
                "sequence_no": t,
                "timestamp": float(t),
            })

    return scenarios


def evaluate_architecture(
    gating_mode: str,
    scenarios: List[Dict[str, Any]],
    base_prototype: np.ndarray,
    base_variance: np.ndarray,
    sim_params: Dict[str, Any],
    disrupt_gateways_50pct: bool = False,
) -> Dict[str, Any]:
    profile = PersistentDeviceProfile(
        device_id=PRIMARY_DEVICE_ID,
        target_transmitter=TARGET_TRANSMITTER,
        feature_prototype=base_prototype.copy(),
        feature_variance=base_variance.copy(),
    )
    engine = IntegratedAuthEngine(
        learning_rate=sim_params["learning_rate"],
        max_drift_threshold_std=sim_params["max_drift_threshold_std"],
        open_set_confidence_threshold=sim_params["open_set_confidence_threshold"],
        quarantine_capacity=sim_params["quarantine_capacity"],
        min_witnesses_required=sim_params["min_witnesses_required"],
    )

    legitimate_total = 0
    legitimate_accepted = 0
    legitimate_held = 0
    legitimate_rejected = 0

    attack_total = 0
    attack_accepted = 0
    attack_breakdown: Dict[str, Dict[str, int]] = {
        "stealthy_poisoning": {"total": 0, "accepted": 0, "held": 0, "rejected": 0},
        "target_spoofing": {"total": 0, "accepted": 0, "held": 0, "rejected": 0},
        "stale_replay": {"total": 0, "accepted": 0, "held": 0, "rejected": 0},
        "unknown_transmitter": {"total": 0, "accepted": 0, "held": 0, "rejected": 0},
    }

    for sc in scenarios:
        witnesses = sc["witnesses"]
        if disrupt_gateways_50pct:
            keep_count = max(0, len(witnesses) // 2)
            witnesses = witnesses[:keep_count]

        res = engine.evaluate_transaction(
            profile=profile,
            candidate_features=sc["candidate_features"],
            witness_reports=witnesses,
            sequence_no=sc["sequence_no"],
            timestamp=sc["timestamp"],
            gating_mode=gating_mode,
        )

        dec = res["decision"]
        is_att = sc["is_attack"]
        cat = sc["category"]

        if not is_att:
            legitimate_total += 1
            if dec == DecisionOutcome.AUTHORIZED_COMMIT.value:
                legitimate_accepted += 1
            elif dec == DecisionOutcome.QUARANTINE_HOLD.value:
                legitimate_held += 1
            else:
                legitimate_rejected += 1
        else:
            attack_total += 1
            attack_breakdown[cat]["total"] += 1
            if dec == DecisionOutcome.AUTHORIZED_COMMIT.value:
                attack_accepted += 1
                attack_breakdown[cat]["accepted"] += 1
            elif dec == DecisionOutcome.QUARANTINE_HOLD.value:
                attack_breakdown[cat]["held"] += 1
            else:
                attack_breakdown[cat]["rejected"] += 1

    total_updates = profile.update_count
    unauthorized_updates = attack_accepted
    contamination_rate = float(unauthorized_updates / total_updates) if total_updates > 0 else 0.0

    final_prototype = profile.feature_prototype
    prototype_displacement_norm = float(np.linalg.norm(final_prototype - base_prototype))

    audit_chain_valid = True
    for idx, entry in enumerate(engine.audit_log):
        computed_hash = hashlib.sha256(json.dumps({k: v for k, v in entry.items() if k != "entry_hash"}, sort_keys=True).encode("utf-8")).hexdigest()
        if computed_hash != entry["entry_hash"]:
            audit_chain_valid = False
            break

    return {
        "gating_mode": gating_mode,
        "disrupt_gateways_50pct": disrupt_gateways_50pct,
        "total_rounds_evaluated": len(scenarios),
        "legitimate_metrics": {
            "total_legitimate_rounds": legitimate_total,
            "accepted_count": legitimate_accepted,
            "held_count": legitimate_held,
            "rejected_count": legitimate_rejected,
            "acceptance_rate": float(legitimate_accepted / legitimate_total),
            "false_rejection_or_hold_rate": float((legitimate_held + legitimate_rejected) / legitimate_total),
        },
        "attack_metrics": {
            "total_attack_rounds": attack_total,
            "unauthorized_accepted_count": attack_accepted,
            "overall_attack_acceptance_rate": float(attack_accepted / attack_total),
            "overall_attack_block_rate": float(1.0 - (attack_accepted / attack_total)),
            "category_breakdown": attack_breakdown,
        },
        "continual_adaptation_metrics": {
            "total_profile_updates": total_updates,
            "legitimate_updates": legitimate_accepted,
            "unauthorized_updates": unauthorized_updates,
            "contamination_rate": contamination_rate,
            "prototype_distortion_euclidean": prototype_displacement_norm,
        },
        "security_audit_logging": {
            "total_log_entries": len(engine.audit_log),
            "cryptographic_hash_chain_verified": audit_chain_valid,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EXP-B4-01 Integrated Defense")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "exp_b4_01_integrated_defense.json")
    parser.add_argument("--features-dir", type=Path, default=REPO_ROOT / "datasets" / "features" / "manysig")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "experiments" / "track_b" / "exp_b4_01_integrated_defense_results.json")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    start_time = time.time()
    base_proto, base_var = load_ground_truth_profile(args.features_dir)
    scenarios = generate_scenarios(base_proto, base_var, config["simulation_parameters"])

    results: Dict[str, Any] = {
        "metadata": {
            "experiment_id": config["experiment_id"],
            "title": config["title"],
            "target_transmitter": TARGET_TRANSMITTER,
            "total_rounds": len(scenarios),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "environment": get_environment_info(),
        },
        "evaluations": {},
    }

    for mode in config["evaluated_architectures"]:
        print(f"\nEvaluating architecture: {mode}...")
        res = evaluate_architecture(mode, scenarios, base_proto, base_var, config["simulation_parameters"], disrupt_gateways_50pct=False)
        results["evaluations"][mode] = res
        print(f"  Legitimate Acceptance: {res['legitimate_metrics']['acceptance_rate']*100:.2f}%")
        print(f"  Attack Acceptance: {res['attack_metrics']['overall_attack_acceptance_rate']*100:.2f}% (Block Rate: {res['attack_metrics']['overall_attack_block_rate']*100:.2f}%)")
        print(f"  Contamination Rate: {res['continual_adaptation_metrics']['contamination_rate']*100:.2f}%")
        print(f"  Profile Distortion: {res['continual_adaptation_metrics']['prototype_distortion_euclidean']:.4f}")

    # Ablation: 50% gateway disruption
    print("\nEvaluating ablation: community_gated_integrated with 50% gateway disruption...")
    ablation_res = evaluate_architecture("community_gated_integrated", scenarios, base_proto, base_var, config["simulation_parameters"], disrupt_gateways_50pct=True)
    results["evaluations"]["ablation_disrupted_gateways_50pct"] = ablation_res
    print(f"  Legitimate Acceptance: {ablation_res['legitimate_metrics']['acceptance_rate']*100:.2f}%")
    print(f"  Attack Acceptance: {ablation_res['attack_metrics']['overall_attack_acceptance_rate']*100:.2f}%")

    elapsed = time.time() - start_time
    results["metadata"]["execution_time_seconds"] = round(elapsed, 2)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nEXP-B4-01 completed successfully in {elapsed:.2f}s.")
    print(f"Authoritative results written to: {args.output}")


if __name__ == "__main__":
    main()
