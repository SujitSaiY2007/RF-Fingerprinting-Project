"""Community-Aware IoT Network Graph and Multi-Witness Consensus Engine.

EXP-B2-04: Implements the network and community layer for multi-gateway
witness aggregation, independently of real RF signal classification.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import math
from typing import Any, Dict, List, Optional, Set, Tuple
import numpy as np


class ConsensusDecision(str, Enum):
    UNANIMOUS_ACCEPT = "UNANIMOUS_ACCEPT"
    MAJORITY_ACCEPT = "MAJORITY_ACCEPT"
    QUARANTINE_HOLD = "QUARANTINE_HOLD"
    CONSENSUS_REJECT = "CONSENSUS_REJECT"
    INSUFFICIENT_WITNESS = "INSUFFICIENT_WITNESS"


@dataclass(frozen=True)
class WitnessReport:
    gateway_id: str
    target_device_id: str
    timestamp: float
    predicted_identity: str
    rf_confidence: float
    rssi_dbm: float
    snr_db: float


@dataclass
class IoTNode:
    node_id: str
    node_type: str  # "device" or "gateway"
    x: float
    y: float
    transmission_radius: float
    enrolled_identity: Optional[str] = None
    active_community_id: Optional[str] = None
    simulated_trust_score: float = 1.0  # Bounded [0.0, 1.0]; simulated metric, NOT cryptographic auth


class IoTCommunityNetwork:
    """Manages the synthetic IoT topology, spatial connectivity, and community clusters."""

    def __init__(
        self,
        num_devices: int = 50,
        num_gateways: int = 5,
        area_size: float = 100.0,
        device_tx_radius: float = 40.0,
        gateway_tx_radius: float = 60.0,
        random_seed: int = 20260902,
    ):
        self.num_devices = num_devices
        self.num_gateways = num_gateways
        self.area_size = area_size
        self.device_tx_radius = device_tx_radius
        self.gateway_tx_radius = gateway_tx_radius
        self.random_seed = random_seed

        self.devices: Dict[str, IoTNode] = {}
        self.gateways: Dict[str, IoTNode] = {}
        self.device_gateway_edges: Dict[str, Set[str]] = {}  # device_id -> set of gateway_ids
        self.communities: Dict[str, Set[str]] = {}  # community_id -> set of device_ids

        self._build_topology()
        self._construct_communities()

    def _build_topology(self) -> None:
        rng = np.random.default_rng(self.random_seed)

        # Strategic 5-spot gateway distribution (4 quadrants + 1 center) with small jitter
        if self.num_gateways == 5:
            base_gw_coords = [
                (25.0, 25.0),
                (75.0, 25.0),
                (50.0, 50.0),
                (25.0, 75.0),
                (75.0, 75.0),
            ]
        else:
            # Generic grid distribution
            grid_dim = int(math.ceil(math.sqrt(self.num_gateways)))
            base_gw_coords = []
            step = self.area_size / (grid_dim + 1)
            for i in range(1, grid_dim + 1):
                for j in range(1, grid_dim + 1):
                    if len(base_gw_coords) < self.num_gateways:
                        base_gw_coords.append((i * step, j * step))

        for gw_idx, (bx, by) in enumerate(base_gw_coords):
            gx = bx + rng.uniform(-3.0, 3.0)
            gy = by + rng.uniform(-3.0, 3.0)
            gw_id = f"GW-{gw_idx+1}"
            self.gateways[gw_id] = IoTNode(
                node_id=gw_id,
                node_type="gateway",
                x=float(gx),
                y=float(gy),
                transmission_radius=self.gateway_tx_radius,
            )

        # Place devices uniformly
        for d_idx in range(self.num_devices):
            dx = rng.uniform(5.0, self.area_size - 5.0)
            dy = rng.uniform(5.0, self.area_size - 5.0)
            dev_id = f"DEV-{d_idx+1:03d}"
            enrolled_tx = f"TX-{(d_idx % 6) + 1}"  # 6 nominal transmitter identities
            self.devices[dev_id] = IoTNode(
                node_id=dev_id,
                node_type="device",
                x=float(dx),
                y=float(dy),
                transmission_radius=self.device_tx_radius,
                enrolled_identity=enrolled_tx,
            )
            self.device_gateway_edges[dev_id] = set()

        # Connect devices to in-range gateways
        for dev_id, dev in self.devices.items():
            for gw_id, gw in self.gateways.items():
                dist = math.hypot(dev.x - gw.x, dev.y - gw.y)
                if dist <= self.device_tx_radius:
                    self.device_gateway_edges[dev_id].add(gw_id)

    def _construct_communities(self) -> None:
        """Partition network into spatial communities based on primary gateway proximity."""
        self.communities.clear()
        for gw_id in self.gateways.keys():
            self.communities[f"COMM-{gw_id}"] = set()

        for dev_id, dev in self.devices.items():
            nearest_gw = min(
                self.gateways.values(),
                key=lambda g: math.hypot(dev.x - g.x, dev.y - g.y),
            )
            comm_id = f"COMM-{nearest_gw.node_id}"
            self.communities[comm_id].add(dev_id)
            dev.active_community_id = comm_id

    def get_witnesses_for_device(self, device_id: str) -> List[str]:
        return sorted(list(self.device_gateway_edges.get(device_id, set())))

    def evaluate_multi_witness_consensus(
        self,
        reports: List[WitnessReport],
        min_witnesses: int = 2,
        unanimous_conf_threshold: float = 0.85,
        majority_conf_threshold: float = 0.70,
    ) -> Dict[str, Any]:
        """Aggregate multiple independent gateway witness reports into a consensus decision."""
        if not reports:
            return {
                "decision": ConsensusDecision.INSUFFICIENT_WITNESS.value,
                "consensus_identity": None,
                "witness_count": 0,
                "agreement_ratio": 0.0,
                "mean_confidence": 0.0,
            }

        witness_count = len(reports)
        if witness_count < min_witnesses:
            rep = reports[0]
            return {
                "decision": ConsensusDecision.QUARANTINE_HOLD.value,
                "consensus_identity": rep.predicted_identity,
                "witness_count": 1,
                "agreement_ratio": 1.0,
                "mean_confidence": rep.rf_confidence,
                "reason": "Single witness; quarantined pending corroboration",
            }

        # Tabulate votes
        votes: Dict[str, List[float]] = {}
        for r in reports:
            votes.setdefault(r.predicted_identity, []).append(r.rf_confidence)

        # Find majority candidate
        best_candidate = max(votes.keys(), key=lambda c: len(votes[c]))
        best_votes = len(votes[best_candidate])
        agreement_ratio = best_votes / witness_count
        candidate_confs = votes[best_candidate]
        mean_conf = float(np.mean(candidate_confs))

        if agreement_ratio == 1.0 and mean_conf >= unanimous_conf_threshold:
            decision = ConsensusDecision.UNANIMOUS_ACCEPT
        elif agreement_ratio >= 0.60 and mean_conf >= majority_conf_threshold:
            decision = ConsensusDecision.MAJORITY_ACCEPT
        elif agreement_ratio >= 0.50:
            decision = ConsensusDecision.QUARANTINE_HOLD
        else:
            decision = ConsensusDecision.CONSENSUS_REJECT

        return {
            "decision": decision.value,
            "consensus_identity": best_candidate if decision != ConsensusDecision.CONSENSUS_REJECT else None,
            "witness_count": witness_count,
            "agreement_ratio": float(agreement_ratio),
            "mean_confidence": mean_conf,
            "vote_distribution": {k: len(v) for k, v in votes.items()},
        }
