"""Community-Gated Continual Adaptation and Poisoning Defense Engine.

EXP-B2-05: Implements the decision contract separating identity classification,
authentication confidence, update authorization, quarantine holds, and rejection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from src.community_graph import ConsensusDecision, WitnessReport


class UpdateDecision(str, Enum):
    AUTHORIZED_COMMIT = "AUTHORIZED_COMMIT"
    QUARANTINE_HOLD = "QUARANTINE_HOLD"
    REJECT_DISCARD = "REJECT_DISCARD"


@dataclass
class DeviceProfile:
    device_id: str
    target_transmitter: str
    feature_prototype: np.ndarray  # (16,) physical feature mean vector
    feature_variance: np.ndarray   # (16,) feature variance vector
    update_count: int = 0
    drift_history: List[float] = field(default_factory=list)
    quarantine_buffer: List[np.ndarray] = field(default_factory=list)


class CommunityGatedAdapter:
    """Manages profile updates under community consensus and threat model gates."""

    def __init__(
        self,
        learning_rate: float = 0.05,
        max_drift_threshold_std: float = 3.0,
        quarantine_capacity: int = 5,
        unanimous_conf_threshold: float = 0.85,
        majority_conf_threshold: float = 0.70,
    ):
        self.learning_rate = learning_rate
        self.max_drift_threshold_std = max_drift_threshold_std
        self.quarantine_capacity = quarantine_capacity
        self.unanimous_conf_threshold = unanimous_conf_threshold
        self.majority_conf_threshold = majority_conf_threshold

    def compute_feature_distance(self, profile: DeviceProfile, candidate_features: np.ndarray) -> float:
        """Normalized Mahalanobis-like distance along feature standard deviations."""
        std = np.sqrt(np.maximum(profile.feature_variance, 1e-6))
        norm_diff = (candidate_features - profile.feature_prototype) / std
        return float(np.sqrt(np.mean(norm_diff ** 2)))

    def evaluate_update_contract(
        self,
        profile: DeviceProfile,
        candidate_features: np.ndarray,
        consensus_outcome: Dict[str, Any],
        gating_mode: str = "community_gated",
    ) -> Dict[str, Any]:
        """Evaluates authorization contract for updating persistent device profile.

        gating_mode options:
          - "no_community_naive": Updates if local classifier confidence >= 0.70 (ignores community consensus).
          - "threshold_only": Updates if feature distance <= threshold (ignores community consensus).
          - "community_gated": Requires BOTH community consensus acceptance AND feature distance <= threshold.
        """
        dist = self.compute_feature_distance(profile, candidate_features)
        distance_pass = dist <= self.max_drift_threshold_std
        consensus_dec = consensus_outcome.get("decision", ConsensusDecision.INSUFFICIENT_WITNESS.value)
        predicted_id = consensus_outcome.get("consensus_identity")

        # Check identity match
        identity_match = (predicted_id == profile.target_transmitter)

        if gating_mode == "no_community_naive":
            # Naive baseline: trusts single receiver classification if confidence >= 0.7
            mean_conf = consensus_outcome.get("mean_confidence", 0.0)
            if identity_match and mean_conf >= 0.70:
                decision = UpdateDecision.AUTHORIZED_COMMIT
                reason = "Naive local acceptance (single-node confidence passed)"
            else:
                decision = UpdateDecision.REJECT_DISCARD
                reason = "Naive local rejection"

        elif gating_mode == "threshold_only":
            # Distance envelope only
            if identity_match and distance_pass:
                decision = UpdateDecision.AUTHORIZED_COMMIT
                reason = "Feature distance within standard deviation envelope"
            elif identity_match and not distance_pass:
                decision = UpdateDecision.QUARANTINE_HOLD
                reason = "Excessive drift outside envelope; held in quarantine"
            else:
                decision = UpdateDecision.REJECT_DISCARD
                reason = "Identity mismatch"

        elif gating_mode == "community_gated":
            # Proposed architecture: Multi-witness consensus + Distance envelope
            if consensus_dec in (ConsensusDecision.UNANIMOUS_ACCEPT.value, ConsensusDecision.MAJORITY_ACCEPT.value):
                if identity_match and distance_pass:
                    decision = UpdateDecision.AUTHORIZED_COMMIT
                    reason = f"Authorized: Verified by community consensus ({consensus_dec}) and within drift bounds"
                elif identity_match and not distance_pass:
                    decision = UpdateDecision.QUARANTINE_HOLD
                    reason = "Consensus accepted identity, but physical drift exceeds threshold; quarantined"
                else:
                    decision = UpdateDecision.REJECT_DISCARD
                    reason = "Identity mismatch under consensus"
            elif consensus_dec == ConsensusDecision.QUARANTINE_HOLD.value:
                decision = UpdateDecision.QUARANTINE_HOLD
                reason = "Witness consensus ambiguous or insufficient; held in quarantine"
            else:
                decision = UpdateDecision.REJECT_DISCARD
                reason = f"Consensus rejected candidate ({consensus_dec})"
        else:
            raise ValueError(f"Unknown gating mode: {gating_mode}")

        # Execute persistent update if authorized
        if decision == UpdateDecision.AUTHORIZED_COMMIT:
            # Exponential moving average update
            profile.feature_prototype = (1.0 - self.learning_rate) * profile.feature_prototype + self.learning_rate * candidate_features
            profile.update_count += 1
            profile.drift_history.append(dist)
        elif decision == UpdateDecision.QUARANTINE_HOLD:
            if len(profile.quarantine_buffer) < self.quarantine_capacity:
                profile.quarantine_buffer.append(candidate_features)

        return {
            "update_decision": decision.value,
            "feature_distance": dist,
            "distance_pass": distance_pass,
            "consensus_decision": consensus_dec,
            "identity_match": identity_match,
            "reason": reason,
            "profile_update_count": profile.update_count,
        }
