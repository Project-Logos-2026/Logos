"""
Authoritative execution-side Nexus

Responsibilities:
- Participant registration
- Deterministic tick orchestration
- Mesh enforcement
- MRE (Metered Reasoning Enforcer) integration
- State routing and isolation

This module is EXECUTION INFRASTRUCTURE.
No agent reasoning lives here.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import uuid
import time

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
# Participant Interface (Protocol)
# =============================================================================

class NexusParticipant:
    """
    All agents and protocols MUST implement this interface.
    """

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
# Mesh Enforcement (Structural, Not Semantic)
# =============================================================================

class MeshEnforcer:
    """
    Enforces structural admissibility.
    Does NOT reason, infer, or evaluate truth.
    """

    def validate(self, packet: StatePacket) -> None:
        # HARD FAIL on malformed packets
        if not isinstance(packet.payload, dict):
            raise MeshRejection("Payload must be a dict")

        # Example structural guardrails (expand later)
        if "type" not in packet.payload:
            raise MeshRejection("Missing required field: type")

        if "content" not in packet.payload:
            raise MeshRejection("Missing required field: content")


# =============================================================================
# MRE Integration
# =============================================================================

class MREGovernor:
    """
    Wraps metered_reasoning_enforcer.py
    Enforces recursion, expansion, and budget limits.
    """

    def __init__(self, mre):
        self.mre = mre

    def pre_execute(self, participant_id: str) -> Dict[str, Any]:
        decision = self.mre.pre_tick(participant_id)
        if decision["state"] == "RED":
            raise MREHalt(f"MRE HALT (pre): {participant_id}")
        return decision

    def post_execute(self, participant_id: str) -> None:
        decision = self.mre.post_tick(participant_id)
        if decision["state"] == "RED":
            raise MREHalt(f"MRE HALT (post): {participant_id}")


# =============================================================================
# Nexus Handle (What Participants See)
# =============================================================================

class NexusHandle:
    """
    Restricted handle exposed to participants.
    """

    def __init__(self, nexus: "StandardNexus", participant_id: str):
        self._nexus = nexus
        self._pid = participant_id

    def emit(self, payload: Dict[str, Any], causal_intent: Optional[str] = None):
        packet = StatePacket(
            source_id=self._pid,
            payload=payload,
            timestamp=time.time(),
            causal_intent=causal_intent,
        )
        self._nexus.ingest(packet)


# =============================================================================
# Standard Nexus Core
# =============================================================================

class StandardNexus:
    """
    Canonical execution nexus.
    """

    def __init__(self, mesh: MeshEnforcer, mre_governor: MREGovernor):
        self.mesh = mesh
        self.mre = mre_governor

        self.participants: Dict[str, NexusParticipant] = {}
        self.handles: Dict[str, NexusHandle] = {}

        self.inbox: List[StatePacket] = []
        self.tick_counter: int = 0

    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------

    def register_participant(self, participant: NexusParticipant) -> None:
        pid = getattr(participant, "participant_id", None)
        if not pid:
            raise NexusViolation("Participant missing participant_id")

        if pid in self.participants:
            raise NexusViolation(f"Duplicate participant_id: {pid}")

        self.participants[pid] = participant
        handle = NexusHandle(self, pid)
        self.handles[pid] = handle

        participant.register(handle)

    # -------------------------------------------------------------------------
    # Ingress
    # -------------------------------------------------------------------------

    def ingest(self, packet: StatePacket) -> None:
        # Mesh validation at ingress
        self.mesh.validate(packet)
        self.inbox.append(packet)

    # -------------------------------------------------------------------------
    # Routing
    # -------------------------------------------------------------------------

    def _route(self, packets: List[StatePacket]) -> None:
        for packet in packets:
            for pid, participant in self.participants.items():
                if pid != packet.source_id:
                    participant.receive_state(packet)

    # -------------------------------------------------------------------------
    # Tick Loop
    # -------------------------------------------------------------------------

    def tick(self, causal_intent: Optional[str] = None) -> None:
        self.tick_counter += 1
        tick_id = self.tick_counter

        # Snapshot inbox
        inbound = self.inbox
        self.inbox = []

        # Route inbound packets
        self._route(inbound)

        # Execute participants deterministically (sorted by id)
        for pid in sorted(self.participants.keys()):
            participant = self.participants[pid]

            # MRE pre-check
            context = self.mre.pre_execute(pid)
            context.update({
                "tick_id": tick_id,
                "causal_intent": causal_intent,
            })

            # Execute
            participant.execute_tick(context)

            # MRE post-check
            self.mre.post_execute(pid)

        # Collect projections
        projections: List[StatePacket] = []
        for participant in self.participants.values():
            packet = participant.project_state()
            if packet:
                self.mesh.validate(packet)
                projections.append(packet)

        # Route projections
        self._route(projections)

    # -------------------------------------------------------------------------
    # Introspection (Safe)
    # -------------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        return {
            "participants": list(self.participants.keys()),
            "tick": self.tick_counter,
            "queued_packets": len(self.inbox),
        }
