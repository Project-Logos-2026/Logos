"""
MTP_Nexus

Authoritative execution-side Nexus for MTP (Meaning Translation Protocol).

Responsibilities:
- Deterministic tick orchestration
- IonMesh + PXL structural enforcement
- Participant isolation and routing
- Metered Reasoning Enforcement (MRE)

Execution infrastructure ONLY.
No interpretation, no semantics, no authority delegation.
"""

from typing import Dict, List, Any, Optional, Hashable
from dataclasses import dataclass
import time

from metered_reasoning_enforcer import MeteredReasoningEnforcer


# =============================================================================
# Exceptions (Fail-Closed)
# =============================================================================

class NexusViolation(Exception):
    pass


class MeshRejection(Exception):
    pass


class MREHalt(Exception):
    pass


# =============================================================================
# State Packets
# =============================================================================

@dataclass(frozen=True)
class StatePacket:
    source_id: str
    payload: Dict[str, Any]
    timestamp: float
    causal_intent: Optional[str] = None


# =============================================================================
# Participant Interface
# =============================================================================

class NexusParticipant:
    participant_id: str

    def register(self, nexus_handle: "NexusHandle") -> None:
        raise NotImplementedError

    def project_state(self) -> Optional[StatePacket]:
        raise NotImplementedError

    def receive_state(self, packet: StatePacket) -> None:
        raise NotImplementedError

    def execute_tick(self, context: Dict[str, Any]) -> None:
        raise NotImplementedError


# =============================================================================
# IonMesh + PXL Structural Enforcement
# =============================================================================

class IonMeshEnforcer:
    """
    Structural enforcement only.
    No reasoning, no semantics, no inference.
    """

    REQUIRED_FIELDS = {"type", "content"}

    def validate(self, packet: StatePacket) -> None:
        if not isinstance(packet.payload, dict):
            raise MeshRejection("Payload must be dict")

        missing = self.REQUIRED_FIELDS - packet.payload.keys()
        if missing:
            raise MeshRejection(f"Missing required fields: {missing}")

        # PXL structural admissibility only
        # No modal or semantic evaluation


# =============================================================================
# MRE Governor
# =============================================================================

class MREGovernor:
    def __init__(self, mre: MeteredReasoningEnforcer):
        self.mre = mre

    def pre_execute(self, signature: Hashable) -> None:
        self.mre.update(signature)
        if not self.mre.should_continue():
            raise MREHalt("MRE pre-execution halt")

    def post_execute(self, signature: Hashable) -> None:
        self.mre.update(signature)
        if not self.mre.should_continue():
            raise MREHalt("MRE post-execution halt")


# =============================================================================
# Nexus Handle
# =============================================================================

class NexusHandle:
    def __init__(self, nexus: "StandardNexus", participant_id: str):
        self._nexus = nexus
        self._pid = participant_id

    def emit(self, payload: Dict[str, Any], causal_intent: Optional[str] = None) -> None:
        packet = StatePacket(
            source_id=self._pid,
            payload=payload,
            timestamp=time.time(),
            causal_intent=causal_intent,
        )
        self._nexus.ingest(packet)


# =============================================================================
# Standard Execution Nexus
# =============================================================================

class StandardNexus:
    def __init__(self) -> None:
        self.mesh = IonMeshEnforcer()
        self.mre = MREGovernor(
            MeteredReasoningEnforcer(
                mre_level=0.45,
                max_iterations=500,
                max_time_seconds=5.0,
            )
        )

        self.participants: Dict[str, NexusParticipant] = {}
        self.handles: Dict[str, NexusHandle] = {}
        self.inbox: List[StatePacket] = []
        self.tick_counter: int = 0

    def register_participant(self, participant: NexusParticipant) -> None:
        pid = getattr(participant, "participant_id", None)
        if not pid:
            raise NexusViolation("participant_id required")

        if pid in self.participants:
            raise NexusViolation(f"Duplicate participant_id: {pid}")

        self.participants[pid] = participant
        handle = NexusHandle(self, pid)
        self.handles[pid] = handle
        participant.register(handle)

    def ingest(self, packet: StatePacket) -> None:
        self.mesh.validate(packet)
        self.inbox.append(packet)

    def _route(self, packets: List[StatePacket]) -> None:
        for packet in packets:
            for pid, participant in self.participants.items():
                if pid != packet.source_id:
                    participant.receive_state(packet)

    def tick(self, causal_intent: Optional[str] = None) -> None:
        self.tick_counter += 1

        inbound = self.inbox
        self.inbox = []

        self._route(inbound)

        for pid in sorted(self.participants.keys()):
            participant = self.participants[pid]

            self.mre.pre_execute(pid)
            participant.execute_tick(
                {
                    "tick": self.tick_counter,
                    "causal_intent": causal_intent,
                }
            )
            self.mre.post_execute(pid)

        projections: List[StatePacket] = []
        for participant in self.participants.values():
            packet = participant.project_state()
            if packet:
                self.mesh.validate(packet)
                projections.append(packet)

        self._route(projections)

    def status(self) -> Dict[str, Any]:
        return {
            "participants": list(self.participants.keys()),
            "tick": self.tick_counter,
            "queued_packets": len(self.inbox),
        }
