"""D8 persistent RF profile evolution primitives.

The module deliberately separates identity recognition from permission to mutate
persistent identity state. It accepts externally produced recognition evidence
(predicted identity + confidence) and never trains/retrains a classifier.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import hashlib, json
import numpy as np

class Decision(str, Enum):
    ACCEPT_UPDATE = "ACCEPT_UPDATE"
    HOLD = "HOLD_QUARANTINE"
    REJECT = "REJECT"

class Policy(str, Enum):
    FROZEN = "frozen_no_update"
    ALWAYS = "always_update"
    CONFIDENCE = "confidence_only"
    MULTI = "multi_evidence"

@dataclass
class AuditEvent:
    source_id: str
    identity: int | None
    decision: str
    reason: str
    policy: str
    confidence: float
    consistency_distance: float | None
    synthetic: bool
    profile_version_before: int | None
    profile_version_after: int | None

@dataclass
class Profile:
    identity: int
    mean: np.ndarray
    m2: np.ndarray
    count: int
    version: int = 1
    last_source_index: int | None = None
    audit: list[AuditEvent] = field(default_factory=list)

    @property
    def variance(self) -> np.ndarray:
        return self.m2 / max(self.count - 1, 1)

    def distance(self, x: np.ndarray) -> float:
        x = np.asarray(x, dtype=float)
        return float(np.sqrt(np.mean((x - self.mean) ** 2)))

    def update(self, x: np.ndarray, source_index: int | None = None) -> float:
        x = np.asarray(x, dtype=float)
        before = self.mean.copy()
        n1 = self.count + 1
        delta = x - self.mean
        self.mean = self.mean + delta / n1
        self.m2 = self.m2 + delta * (x - self.mean)
        self.count = n1
        self.version += 1
        self.last_source_index = source_index
        return float(np.linalg.norm(self.mean - before))

class ProfileManager:
    def __init__(self, profiles: dict[int, Profile], confidence_threshold: float = 0.30,
                 consistency_threshold: float = 1.0, replay_guard: bool = False):
        self.profiles = profiles
        self.confidence_threshold = float(confidence_threshold)
        self.consistency_threshold = float(consistency_threshold)
        self.replay_guard = bool(replay_guard)
        self._seen_fingerprints: dict[str, int] = {}

    @classmethod
    def enroll(cls, x_by_identity: dict[int, np.ndarray], **kwargs) -> "ProfileManager":
        profiles = {}
        for identity, X in sorted(x_by_identity.items()):
            X = np.asarray(X, dtype=float)
            if X.ndim != 2 or len(X) == 0:
                raise ValueError("enrollment data must be non-empty 2-D arrays")
            mean = X.mean(axis=0)
            centered = X - mean
            profiles[int(identity)] = Profile(
                identity=int(identity), mean=mean,
                m2=np.sum(centered ** 2, axis=0), count=len(X)
            )
        return cls(profiles, **kwargs)

    def recognize_profile(self, x: np.ndarray) -> tuple[int, float]:
        labels = list(self.profiles)
        d = np.asarray([self.profiles[k].distance(x) for k in labels])
        j = int(np.argmin(d))
        return labels[j], float(d[j])

    def authorize(self, predicted_identity: int | None, confidence: float,
                  x: np.ndarray, policy: Policy, source_id: str,
                  synthetic: bool = False, source_index: int | None = None) -> AuditEvent:
        before = after = None
        distance = None
        identity = int(predicted_identity) if predicted_identity is not None else None
        if identity not in self.profiles:
            decision, reason = Decision.REJECT, "identity_not_in_profile_store"
        else:
            profile = self.profiles[identity]
            before = profile.version
            distance = profile.distance(x)
            if policy == Policy.FROZEN:
                decision, reason = Decision.HOLD, "profile_updates_disabled"
            elif policy == Policy.ALWAYS:
                decision, reason = Decision.ACCEPT_UPDATE, "recognized_identity"
            elif policy == Policy.CONFIDENCE:
                if confidence >= self.confidence_threshold:
                    decision, reason = Decision.ACCEPT_UPDATE, "confidence_pass"
                else:
                    decision, reason = Decision.HOLD, "confidence_below_threshold"
            elif policy == Policy.MULTI:
                fp = hashlib.sha256(np.asarray(x, dtype=np.float64).round(12).tobytes()).hexdigest()
                repeated = self._seen_fingerprints.get(fp, 0) > 0
                if confidence < self.confidence_threshold:
                    decision, reason = Decision.HOLD, "confidence_below_threshold"
                elif distance > self.consistency_threshold:
                    decision, reason = Decision.HOLD, "profile_inconsistency"
                elif self.replay_guard and repeated:
                    decision, reason = Decision.HOLD, "replay_detected"
                else:
                    decision, reason = Decision.ACCEPT_UPDATE, "confidence_and_consistency_pass"
            else:
                raise ValueError(f"unsupported policy: {policy}")
            if decision == Decision.ACCEPT_UPDATE:
                profile.update(x, source_index)
                after = profile.version
        fp = hashlib.sha256(np.asarray(x, dtype=np.float64).round(12).tobytes()).hexdigest()
        self._seen_fingerprints[fp] = self._seen_fingerprints.get(fp, 0) + 1
        event = AuditEvent(
            source_id=str(source_id), identity=identity, decision=decision.value,
            reason=reason, policy=policy.value, confidence=float(confidence),
            consistency_distance=distance, synthetic=bool(synthetic),
            profile_version_before=before, profile_version_after=after,
        )
        if identity in self.profiles:
            self.profiles[identity].audit.append(event)
        return event

    def state_digest(self) -> str:
        payload = {}
        for k, p in sorted(self.profiles.items()):
            payload[str(k)] = {
                "count": p.count, "version": p.version,
                "last_source_index": p.last_source_index,
                "mean": np.round(p.mean, 12).tolist(),
                "audit_count": len(p.audit),
            }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
