# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: ARP_Nexus
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Nexus/ARP_Nexus.py.
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Nexus/ARP_Nexus.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
ARP_Nexus

Authoritative execution-side Nexus for ARP (Advanced Reasoning Protocol).

Responsibilities:
- Deterministic tick orchestration
- IonMesh + PXL structural enforcement
- Participant isolation and routing
- Metered Reasoning Enforcement (MRE)

Execution infrastructure ONLY.
No reasoning, no semantics, no authority delegation.
"""

from typing import Dict, List, Any, Optional, Hashable
from dataclasses import dataclass
import time

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Advanced_Reasoning_Protocol.ARP_Core.metered_reasoning_enforcer import MeteredReasoningEnforcer


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
# Provisional PXL Proof Tagging (Egress Only)
# =============================================================================

PROVISIONAL_DISCLAIMER = "Requires EMP compilation"
PROVISIONAL_STATUS = "PROVISIONAL"


def _payload_is_smp(payload: Dict[str, Any]) -> bool:
    return any(key in payload for key in ("smp_id", "smp", "raw_input", "header"))


def _contains_pxl_fragments(obj: Any) -> bool:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if _pxl_key_match(str(key)) or _contains_pxl_fragments(value):
                return True
        return False
    if isinstance(obj, list):
        return any(_contains_pxl_fragments(item) for item in obj)
    if isinstance(obj, str):
        return _pxl_key_match(obj)
    return False


def _pxl_key_match(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("pxl", "formal_logic", "wff", "axiom", "proof"))


def _extract_proof_refs(obj: Dict[str, Any]) -> Dict[str, Optional[str]]:
    proof_id = obj.get("proof_id") or obj.get("pxl_proof_id")
    proof_hash = obj.get("proof_hash") or obj.get("pxl_proof_hash")
    proof_index = obj.get("proof_index") or obj.get("pxl_proof_index")
    proof_refs = obj.get("proof_refs") or obj.get("pxl_refs")

    if not proof_id and isinstance(proof_index, dict):
        proof_id = proof_index.get("proof_id")
        proof_hash = proof_hash or proof_index.get("proof_hash")

    if not proof_id and isinstance(proof_refs, dict):
        proof_id = proof_refs.get("proof_id")
        proof_hash = proof_hash or proof_refs.get("proof_hash")

    return {
        "proof_id": str(proof_id) if proof_id else None,
        "proof_hash": str(proof_hash) if proof_hash else None,
    }


def _build_span_mapping(obj: Dict[str, Any]) -> Dict[str, Any]:
    if "span_mapping" in obj and isinstance(obj["span_mapping"], dict):
        return obj["span_mapping"]
    return {
        "smp_section": obj.get("smp_section", "unknown"),
        "clause_range": obj.get("clause_range", "unknown"),
    }


def _derive_polarity(obj: Dict[str, Any]) -> str:
    candidate = str(obj.get("polarity") or obj.get("verdict") or "proven_true").lower()
    if candidate in {"proven_true", "true", "yes"}:
        return "proven_true"
    if candidate in {"proven_false", "false", "no"}:
        return "proven_false"
    return "proven_true"


def _tag_append_artifact(aa_payload: Dict[str, Any]) -> Dict[str, Any]:
    if "PROVISIONAL_PROOF_TAG" in aa_payload:
        return aa_payload

    content = aa_payload.get("content") if isinstance(aa_payload.get("content"), dict) else {}
    if not _contains_pxl_fragments(content) and not _contains_pxl_fragments(aa_payload):
        return aa_payload

    refs = _extract_proof_refs(content) if content else _extract_proof_refs(aa_payload)
    if not refs.get("proof_id") and not refs.get("proof_hash"):
        return aa_payload

    tag = {
        "proof_id": refs.get("proof_id"),
        "proof_hash": refs.get("proof_hash"),
        "polarity": _derive_polarity(content or aa_payload),
        "span_mapping": _build_span_mapping(content or aa_payload),
        "confidence_uplift": 0.05,
        "status": PROVISIONAL_STATUS,
        "disclaimer": PROVISIONAL_DISCLAIMER,
    }

    aa_payload["PROVISIONAL_PROOF_TAG"] = tag
    return aa_payload


def _apply_provisional_proof_tagging(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if not isinstance(payload, dict):
            return payload
        if _payload_is_smp(payload):
            return payload

        if {"aa_id", "aa_type"}.issubset(payload.keys()):
            return _tag_append_artifact(payload)

        for key in ("append_artifact", "append_artifacts", "aa", "aa_list"):
            if key in payload:
                aa_block = payload.get(key)
                if isinstance(aa_block, dict):
                    payload[key] = _tag_append_artifact(aa_block)
                elif isinstance(aa_block, list):
                    payload[key] = [
                        _tag_append_artifact(item) if isinstance(item, dict) else item
                        for item in aa_block
                    ]
        return payload
    except Exception:
        return payload


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
        tagged_payload = _apply_provisional_proof_tagging(payload)
        packet = StatePacket(
            source_id=self._pid,
            payload=tagged_payload,
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
                mre_level=0.6,
                max_iterations=400,
                max_time_seconds=4.0,
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
                tagged_packet = StatePacket(
                    source_id=packet.source_id,
                    payload=_apply_provisional_proof_tagging(packet.payload),
                    timestamp=packet.timestamp,
                    causal_intent=packet.causal_intent,
                )
                self.mesh.validate(tagged_packet)
                projections.append(tagged_packet)

        self._route(projections)

    def status(self) -> Dict[str, Any]:
        return {
            "participants": list(self.participants.keys()),
            "tick": self.tick_counter,
            "queued_packets": len(self.inbox),
        }
