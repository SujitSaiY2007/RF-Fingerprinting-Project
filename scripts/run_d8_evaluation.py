"""Run the complete D8 policy comparison on a precomputed chronological evidence stream.

Input JSONL fields: device_id, observation_id, source_kind, recognition_confidence,
novelty_score, consistency_score, chronological_index, feature_vector.

The script intentionally separates the frozen evaluation snapshot from the update
stream: each observation is evaluated before any permitted profile update.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from statistics import mean
from src.d8_profile_manager import ObservationEvidence, ProfileManager, POLICIES


def load(path):
    rows = [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    return sorted(rows, key=lambda r: r["chronological_index"])


def run(rows, policy):
    mgr = ProfileManager()
    # Enrollment is restricted to the earliest observation for each known device.
    for r in rows:
        d = r["device_id"]
        if d > 33 or d in mgr.profiles:
            continue
        mgr.enroll(d, r["feature_vector"], r["observation_id"], r["source_kind"], r["chronological_index"])
    decisions = []
    for r in rows:
        ev = ObservationEvidence(**r)
        if ev.chronological_index <= mgr.profiles.get(ev.device_id, type("P", (), {"last_observation_index": -1})()).last_observation_index:
            continue
        decision = mgr.process(ev, policy)
        decisions.append((ev, decision))
    counts = {x: sum(d == x for _, d in decisions) for x in ("ACCEPT_UPDATE", "HOLD", "REJECT")}
    updated = sum(1 for _, d in decisions if d == "ACCEPT_UPDATE")
    return {
        "policy": policy,
        "observations_evaluated": len(decisions),
        "accept_update": counts["ACCEPT_UPDATE"],
        "hold": counts["HOLD"],
        "reject": counts["REJECT"],
        "update_rate": updated / len(decisions) if decisions else 0.0,
        "profiles": len(mgr.profiles),
        "profile_versions_total": sum(p.profile_version for p in mgr.profiles.values()),
        "audit_events": len(mgr.audit),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stream")
    ap.add_argument("--output", default="experiments/track_a/d8_policy_results.json")
    args = ap.parse_args()
    rows = load(args.stream)
    result = {
        "stage": "D8",
        "status": "executed",
        "source": "precomputed evidence stream",
        "stream_rows": len(rows),
        "policies": [run(rows, p) for p in POLICIES],
        "note": "Recognition metrics and profile-displacement/legitimate-adaptation metrics must be added from the frozen evaluation harness; this runner reports the authorization/update/audit layer only."
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
