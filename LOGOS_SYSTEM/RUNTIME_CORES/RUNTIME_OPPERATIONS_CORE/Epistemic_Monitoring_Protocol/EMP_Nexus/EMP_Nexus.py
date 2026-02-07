# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
CSP / EXECUTION-SIDE STANDARD NEXUS

Responsibilities:
- Participant registration
- Deterministic tick orchestration
- Explicit Pre / Post Process Gates
- Mesh enforcement (structural only)
- MRE (Metered Reasoning Enforcer) integration
- State routing and isolation

NO AGENT REASONING LIVES HERE.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
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
# Pre / Post Process Gates (EXPLICIT)
# =============================================================================

class PreProcessGate:
    """
    Ingress gate.
    Structural admissibility ONLY.
    No reasoning. No mutation.
    """

    def apply(self, packet: StatePacket) -> StatePacket:
        if not isinstance(packet.payload, dict):
            raise NexusViolation("Ingress payload must be dict")
        return packet


class PostProcessGate:
    """
    Egress gate.
    Tagging, redaction, classification ONLY.
    No routing. No feedback.
    """

    def apply(self, packet: StatePacket) -> StatePacket:
        payload = packet.payload
        payload = _apply_provisional_proof_tagging(payload)
        return StatePacket(
            source_id=packet.source_id,
            payload=payload,
            timestamp=packet.timestamp,
            causal_intent=packet.causal_intent,
        )


# =============================================================================
# Provisional PXL Proof Tagging (EGRESS ONLY)
# =============================================================================

PROVISIONAL_STATUS = "PROVISIONAL"
PROVISIONAL_DISCLAIMER = "Requires EMP compilation"

def _apply_provisional_proof_tagging(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return payload

    if "PROVISIONAL_PROOF_TAG" in payload:
        return payload

    text = str(payload).lower()
    if not any(t in text for t in ("pxl", "proof", "axiom", "wff")):
        return payload

    payload["PROVISIONAL_PROOF_TAG"] = {
        "status": PROVISIONAL_STATUS,
        "disclaimer": PROVISIONAL_DISCLAIMER,
        "confidence_uplift": 0.05,
    }
    return payload


# =============================================================================
# Mesh Enforcement (STRUCTURAL ONLY)
# =============================================================================

class MeshEnforcer:
    def validate(self, packet: StatePacket) -> None:
        if not isinstance(packet.payload, dict):
            raise MeshRejection("Mesh violation: payload must be dict")
        if "content" not in packet.payload:
            raise MeshRejection("Mesh violation: missing 'content'")


# =============================================================================
# MRE Governor
# =============================================================================

class MREGovernor:
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
# Participant Interface
# =============================================================================

class NexusParticipant:
    participant_id: str

    def register(self, nexus_handle: "NexusHandle") -> None:
        raise NotImplementedError

    def receive_state(self, packet: StatePacket) -> None:
        raise NotImplementedError

    def execute_tick(self, context: Dict[str, Any]) -> None:
        raise NotImplementedError

    def project_state(self) -> Optional[StatePacket]:
        raise NotImplementedError


# =============================================================================
# Restricted Handle
# =============================================================================

class NexusHandle:
    def __init__(self, nexus: "StandardNexus", pid: str):
        self._nexus = nexus
        self._pid = pid

    def emit(self, payload: Dict[str, Any], causal_intent: Optional[str] = None):
        packet = StatePacket(
            source_id=self._pid,
            payload=payload,
            timestamp=time.time(),
            causal_intent=causal_intent,
        )
        self._nexus.ingest(packet)


# =============================================================================
# STANDARD EXECUTION NEXUS
# =============================================================================

class StandardNexus:
    """
    Canonical execution nexus with explicit gates.
    """

    def __init__(
        self,
        mesh: MeshEnforcer,
        mre_governor: MREGovernor,
        pre_gate: PreProcessGate,
        post_gate: PostProcessGate,
    ):
        self.mesh = mesh
        self.mre = mre_governor
        self.pre_gate = pre_gate
        self.post_gate = post_gate

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
        packet = self.pre_gate.apply(packet)
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

        inbound = self.inbox
        self.inbox = []

        self._route(inbound)

        for pid in sorted(self.participants.keys()):
            participant = self.participants[pid]

            context = self.mre.pre_execute(pid)
            context.update({"tick_id": tick_id, "causal_intent": causal_intent})

            participant.execute_tick(context)

            self.mre.post_execute(pid)

        projections: List[StatePacket] = []
        for participant in self.participants.values():
            packet = participant.project_state()
            if packet:
                packet = self.post_gate.apply(packet)
                self.mesh.validate(packet)
                projections.append(packet)

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
