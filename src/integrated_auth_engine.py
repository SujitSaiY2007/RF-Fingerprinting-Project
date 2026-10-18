"""Integrated Community-Aware Authentication and Continual Adaptation Engine.

Implements the decoupled 8-stage decision contract for Phase 4:
1. RF observation ingestion & validation
2. Identity classification
3. Open-set known/unknown determination
4. Multi-receiver evidence fusion & disagreement assessment
5. Community witness consensus
6. Adaptation authorization gating
7. Profile update / quarantine / rejection state machine
8. Cryptographic hash-chained audit logging
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import math
import time
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from src.community_graph import ConsensusDecision, WitnessReport


class DecisionOutcome(str, Enum):
    AUTHORIZED_COMMIT = "AUTHORIZED_COMMIT"
    QUARANTINE_HOLD = "QUARANTINE_HOLD"
    REJECT_DISCARD = "REJECT_DISCARD"


class RejectionReason(str, Enum):
    UNKNOWN_TRANSMITTER = "UNKNOWN_TRANSMITTER"
    REPLAY_DETECTED = "REPLAY_DETECTED"
    EXCESSIVE_DRIFT = "EXCESSIVE_DRIFT"
    INSUFFICIENT_WITNESSES = "INSUFFICIENT_WITNESSES"
    WITNESS_DISAGREEMENT = "WITNESS_DISAGREEMENT"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    INVALID_INPUT = "INVALID_INPUT"


@dataclass
class PersistentDeviceProfile:
    device_id: str
    target_transmitter: str
    feature_prototype: np.ndarray  # Shape (16,)
    feature_variance: np.ndarray   # Shape (16,)
    update_count: int = 0
    drift_history: List[float] = field(default_factory=list)
    quarantine_buffer: List[np.ndarray] = field(default_factory=list)


class ReplayTracker:
    """Stateful nonce/sequence tracking for replay defense.
    
    RF physical features alone cannot detect identical bit-level replays in static
    channels without temporal or sequence protocol metadata. This tracker explicitly
    models that protocol boundary.
    """
    def __init__(self, window_size: int = 100):
        self.seen_signatures: set = set()
        self.last_sequence_numbers: Dict[str, int] = {}
        self.window_size = window_size

    def check_and_update(self, device_id: str, sequence_no: int, feature_hash: str) -> bool:
        """Returns True if observation is FRESH, False if REPLAY/STALE."""
        if feature_hash in self.seen_signatures:
            return False  # Replay of identical observation
        last_seq = self.last_sequence_numbers.get(device_id, -1)
        if sequence_no <= last_seq:
            return False  # Stale sequence number
        self.seen_signatures.add(feature_hash)
        self.last_sequence_numbers[device_id] = sequence_no
        return True


class IntegratedAuthEngine:
    """Decoupled 8-stage community-aware authentication and adaptation engine."""

    def __init__(
        self,
        learning_rate: float = 0.05,
        max_drift_threshold_std: float = 3.0,
        open_set_confidence_threshold: float = 0.65,
        quarantine_capacity: int = 5,
        min_witnesses_required: int = 2,
    ):
        self.learning_rate = learning_rate
        self.max_drift_threshold_std = max_drift_threshold_std
        self.open_set_confidence_threshold = open_set_confidence_threshold
        self.quarantine_capacity = quarantine_capacity
        self.min_witnesses_required = min_witnesses_required
        self.replay_tracker = ReplayTracker()
        self.audit_log: List[Dict[str, Any]] = []
        self.prev_log_hash: str = "GENESIS_BLOCK_0000000000000000"

    def compute_feature_distance(self, profile: PersistentDeviceProfile, features: np.ndarray) -> float:
        """Normalized Mahalanobis-like distance along feature standard deviations."""
        std = np.sqrt(np.maximum(profile.feature_variance, 1e-6))
        norm_diff = (features - profile.feature_prototype) / std
        return float(np.sqrt(np.mean(norm_diff ** 2)))

    def evaluate_transaction(
        self,
        profile: PersistentDeviceProfile,
        candidate_features: np.ndarray,
        witness_reports: List[WitnessReport],
        sequence_no: int,
        timestamp: float,
        gating_mode: str = "community_gated_integrated",
    ) -> Dict[str, Any]:
        """Executes the full decoupled decision pipeline."""
        # Stage 1: Input Validation
        if candidate_features is None or len(candidate_features) != 16 or np.any(np.isnan(candidate_features)):
            return self._record_decision(
                profile, candidate_features, DecisionOutcome.REJECT_DISCARD,
                RejectionReason.INVALID_INPUT.value, "Malformed or NaN feature vector", 0.0
            )

        feature_hash = hashlib.sha256(candidate_features.tobytes()).hexdigest()
        is_fresh = self.replay_tracker.check_and_update(profile.device_id, sequence_no, feature_hash)

        # Stage 2 & 3: Multi-Receiver Fusion & Prediction
        if not witness_reports:
            return self._record_decision(
                profile, candidate_features, DecisionOutcome.QUARANTINE_HOLD,
                RejectionReason.INSUFFICIENT_WITNESSES.value, "Zero witness reports available", 0.0
            )

        witness_ids = [r.gateway_id for r in witness_reports]
        witness_preds = [r.predicted_identity for r in witness_reports]
        witness_confs = [r.rf_confidence for r in witness_reports]

        mean_conf = float(np.mean(witness_confs))
        vals, counts = np.unique(witness_preds, return_counts=True)
        majority_id = vals[np.argmax(counts)]
        agreement_ratio = float(counts[np.argmax(counts)] / len(witness_reports))

        # Open-set check: is mean confidence below open-set calibration threshold?
        is_known = mean_conf >= self.open_set_confidence_threshold
        dist = self.compute_feature_distance(profile, candidate_features)
        drift_pass = dist <= self.max_drift_threshold_std

        # --- Architecture A: No Community Naive Baseline ---
        if gating_mode == "no_community_naive":
            # Relies only on primary single-node prediction, ignores multi-receiver agreement & replay
            primary_pred = witness_preds[0]
            primary_conf = witness_confs[0]
            if primary_pred == profile.target_transmitter and primary_conf >= 0.70:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.AUTHORIZED_COMMIT,
                    "AUTHORIZED", "Naive single-node confidence accepted", dist
                )
            else:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.REJECT_DISCARD,
                    RejectionReason.IDENTITY_MISMATCH.value, "Naive single-node rejected", dist
                )

        # --- Architecture B: Threshold Only Baseline ---
        elif gating_mode == "threshold_only":
            # Checks distance envelope only, ignores witness consensus and replay tracking
            if majority_id == profile.target_transmitter:
                if drift_pass:
                    return self._record_decision(
                        profile, candidate_features, DecisionOutcome.AUTHORIZED_COMMIT,
                        "AUTHORIZED", "Feature distance within threshold", dist
                    )
                else:
                    return self._record_decision(
                        profile, candidate_features, DecisionOutcome.QUARANTINE_HOLD,
                        RejectionReason.EXCESSIVE_DRIFT.value, "Feature distance exceeds threshold", dist
                    )
            else:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.REJECT_DISCARD,
                    RejectionReason.IDENTITY_MISMATCH.value, "Identity mismatch", dist
                )

        # --- Architecture C: Proposed Community-Gated Integrated Defense ---
        elif gating_mode == "community_gated_integrated":
            # Replay defense check (protocol-level evidence)
            if not is_fresh:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.REJECT_DISCARD,
                    RejectionReason.REPLAY_DETECTED.value, "Duplicate signature or stale sequence number", dist
                )

            # Open-set check
            if not is_known:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.REJECT_DISCARD,
                    RejectionReason.UNKNOWN_TRANSMITTER.value, f"Low confidence ({mean_conf:.3f} < {self.open_set_confidence_threshold:.3f}) indicating unknown transmitter", dist
                )

            # Witness quorum check
            if len(witness_reports) < self.min_witnesses_required:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.QUARANTINE_HOLD,
                    RejectionReason.INSUFFICIENT_WITNESSES.value, f"Quorum not reached ({len(witness_reports)} < {self.min_witnesses_required})", dist
                )

            # Witness consensus check
            if agreement_ratio < 0.60 or majority_id != profile.target_transmitter:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.QUARANTINE_HOLD,
                    RejectionReason.WITNESS_DISAGREEMENT.value, f"Disagreement among witnesses ({agreement_ratio*100:.1f}% agreement on {majority_id})", dist
                )

            # Physical drift envelope check
            if not drift_pass:
                return self._record_decision(
                    profile, candidate_features, DecisionOutcome.QUARANTINE_HOLD,
                    RejectionReason.EXCESSIVE_DRIFT.value, f"Witnesses agree, but physical drift exceeds bound ({dist:.2f} > {self.max_drift_threshold_std:.2f})", dist
                )

            # All 8 gates passed -> Authorized Adaptation
            return self._record_decision(
                profile, candidate_features, DecisionOutcome.AUTHORIZED_COMMIT,
                "AUTHORIZED", "All 8 verification gates cleared: Fresh, Known, Consensus, and Within-Envelope", dist
            )
        else:
            raise ValueError(f"Unknown gating mode: {gating_mode}")

    def _record_decision(
        self,
        profile: PersistentDeviceProfile,
        candidate_features: np.ndarray,
        decision: DecisionOutcome,
        reason_code: str,
        reason_detail: str,
        drift_distance: float,
    ) -> Dict[str, Any]:
        # Execute persistent update if authorized
        if decision == DecisionOutcome.AUTHORIZED_COMMIT:
            profile.feature_prototype = (1.0 - self.learning_rate) * profile.feature_prototype + self.learning_rate * candidate_features
            profile.update_count += 1
            profile.drift_history.append(drift_distance)
        elif decision == DecisionOutcome.QUARANTINE_HOLD:
            if len(profile.quarantine_buffer) < self.quarantine_capacity:
                profile.quarantine_buffer.append(candidate_features)

        # Cryptographic audit logging
        log_entry = {
            "entry_index": len(self.audit_log),
            "device_id": profile.device_id,
            "decision": decision.value,
            "reason_code": reason_code,
            "reason_detail": reason_detail,
            "drift_distance": drift_distance,
            "update_count": profile.update_count,
            "prev_hash": self.prev_log_hash,
        }
        entry_hash = hashlib.sha256(json.dumps(log_entry, sort_keys=True).encode("utf-8")).hexdigest()
        log_entry["entry_hash"] = entry_hash
        self.prev_log_hash = entry_hash
        self.audit_log.append(log_entry)

        return log_entry
