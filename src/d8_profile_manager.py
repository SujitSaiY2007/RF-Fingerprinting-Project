"""Version-B D8 persistent profiles and protected update authorization."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List
import math

@dataclass
class ObservationEvidence:
    device_id: int
    observation_id: str
    source_kind: str
    recognition_confidence: float
    novelty_score: float
    consistency_score: float
    chronological_index: int
    feature_vector: List[float]

@dataclass
class Profile:
    device_id: int
    mean: List[float]
    m2: List[float]
    count: int = 0
    profile_version: int = 0
    last_observation_index: int = -1
    audit_history: List[dict] = field(default_factory=list)
    def variance(self):
        return [x / (self.count - 1) for x in self.m2] if self.count > 1 else [0.0] * len(self.mean)
    def std(self):
        return [math.sqrt(max(v, 0.0)) for v in self.variance()]

class ProfileManager:
    def __init__(self, *, confidence_threshold=0.90, novelty_threshold=0.30, consistency_threshold=0.70, max_update_step=0.20):
        self.profiles: Dict[int, Profile] = {}
        self.audit: List[dict] = []
        self.confidence_threshold = confidence_threshold
        self.novelty_threshold = novelty_threshold
        self.consistency_threshold = consistency_threshold
        self.max_update_step = max_update_step

    def enroll(self, device_id, vector, observation_id, source_kind, chronological_index):
        if device_id in self.profiles:
            raise ValueError(f"Device {device_id} is already enrolled")
        p = Profile(device_id, list(vector), [0.0] * len(vector), 1, 1, chronological_index)
        e = self._event(observation_id, device_id, "ENROLL", "ACCEPT_UPDATE", source_kind, chronological_index, 1)
        p.audit_history.append(e); self.profiles[device_id] = p; self.audit.append(e)
        return p

    def authorize(self, evidence: ObservationEvidence, policy: str) -> str:
        if evidence.device_id not in self.profiles: return "REJECT"
        if policy == "frozen": return "HOLD"
        if policy == "always_update": return "ACCEPT_UPDATE"
        if policy == "confidence_only":
            return "ACCEPT_UPDATE" if evidence.recognition_confidence >= self.confidence_threshold else "HOLD"
        if policy != "multi_evidence": raise ValueError(f"Unknown D8 policy: {policy}")
        if evidence.recognition_confidence < self.confidence_threshold: return "HOLD"
        if evidence.novelty_score > self.novelty_threshold: return "REJECT"
        if evidence.consistency_score < self.consistency_threshold: return "HOLD"
        return "ACCEPT_UPDATE"

    def process(self, evidence, policy, allow_update=True):
        decision = self.authorize(evidence, policy)
        if decision == "ACCEPT_UPDATE" and allow_update: self._bounded_update(evidence)
        version = self.profiles[evidence.device_id].profile_version if evidence.device_id in self.profiles else 0
        event = self._event(evidence.observation_id, evidence.device_id, "OBSERVATION", decision, evidence.source_kind, evidence.chronological_index, version)
        self.audit.append(event)
        if evidence.device_id in self.profiles: self.profiles[evidence.device_id].audit_history.append(event)
        return decision

    def _bounded_update(self, evidence):
        p = self.profiles[evidence.device_id]
        if evidence.chronological_index <= p.last_observation_index:
            raise ValueError("Chronological leakage: observation is not later than profile state")
        alpha = min(self.max_update_step, 1.0 / max(p.count + 1, 1))
        delta = [x - m for x, m in zip(evidence.feature_vector, p.mean)]
        p.mean = [m + alpha*d for m, d in zip(p.mean, delta)]
        delta2 = [x - m for x, m in zip(evidence.feature_vector, p.mean)]
        p.m2 = [a + d1*d2 for a, d1, d2 in zip(p.m2, delta, delta2)]
        p.count += 1; p.profile_version += 1; p.last_observation_index = evidence.chronological_index

    @staticmethod
    def _event(observation_id, device_id, event_type, decision, source_kind, chronological_index, profile_version):
        return {"observation_id": observation_id, "device_id": device_id, "event_type": event_type, "decision": decision, "source_kind": source_kind, "chronological_index": chronological_index, "profile_version": profile_version}

    def export_state(self):
        return {"profiles": {str(k): asdict(v) for k, v in self.profiles.items()}, "audit": list(self.audit), "policy_config": {"confidence_threshold": self.confidence_threshold, "novelty_threshold": self.novelty_threshold, "consistency_threshold": self.consistency_threshold, "max_update_step": self.max_update_step}}

POLICIES = ("frozen", "always_update", "confidence_only", "multi_evidence")
