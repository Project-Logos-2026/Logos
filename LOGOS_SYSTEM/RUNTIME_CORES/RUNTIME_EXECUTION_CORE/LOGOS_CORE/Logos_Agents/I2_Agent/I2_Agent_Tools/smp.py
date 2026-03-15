# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from __future__ import annotations
# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: smp
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Logos_Agents/I2_Agent/protocol_operations/smp.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Structured Meaning Packet (SMP) schema and builder for the I2 agent
termination stage.

This module is intentionally non-transformative. It only packages
already-evaluated metadata from the privation handler, bridge, benevolence
mediator, and Trinitarian mediator into a JSON-serializable record for
handoff to SCP (I1) or other agents.
"""


from dataclasses import dataclass, field
import json
from pathlib import Path
from LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.repo_root import _find_repo_root
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class TriageVector:
    """
    Minimal, non-transformative IEL orientation overlay applied in I2.
    Serves only to record directional deltas; no remediation is performed here.
    """

    applied_iel: Optional[str] = None
    purpose: Optional[str] = None  # e.g. "orientation", "stabilization"
    overlay_type: str = "soft"
    delta_profile: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "applied_iel": self.applied_iel,
            "purpose": self.purpose,
            "overlay_type": self.overlay_type,
            "delta_profile": self.delta_profile,
        }


@dataclass
class StructuredMeaningPacket:
    smp_id: str
    timestamp: float
    origin_agent: str
    parent_id: Optional[str]

    # References
    input_reference: Dict[str, Any]

    # Privation pipeline
    classification: Dict[str, Any]
    analysis: Dict[str, Any]
    transform_report: Dict[str, Any]

    # Constraint checks
    bridge_passed: bool
    benevolence: Dict[str, Any]

    # Trinitarian mediation
    triadic_scores: Dict[str, float]
    final_decision: str
    violations: List[str]
    route_to: str

    # Metadata header (standardized)
    metadata_header: Dict[str, Any]

    # Classification and AA catalog
    classification_state: Optional[str] = None
    append_artifacts: Dict[str, Any] = field(default_factory=dict)

    # Orientation overlay
    triage_vector: Optional[TriageVector] = None
    delta_profile: Dict[str, Any] = field(default_factory=dict)

    # Provenance
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        packet = {
            "smp_id": self.smp_id,
            "timestamp": self.timestamp,
            "origin_agent": self.origin_agent,
            "parent_id": self.parent_id,
            "input_reference": self.input_reference,
            "classification": self.classification,
            "analysis": self.analysis,
            "transform_report": self.transform_report,
            "bridge_passed": self.bridge_passed,
            "benevolence": self.benevolence,
            "triadic_scores": self.triadic_scores,
            "final_decision": self.final_decision,
            "violations": self.violations,
            "route_to": self.route_to,
            "metadata_header": self.metadata_header,
            "delta_profile": self.delta_profile or {},
            "provenance": self.provenance,
        }

        if self.classification_state:
            packet["classification_state"] = self.classification_state

        if self.append_artifacts:
            packet["append_artifacts"] = self.append_artifacts

        if self.triage_vector:
            packet["triage_vector"] = self.triage_vector.to_dict()
            if not self.delta_profile:
                packet["delta_profile"] = self.triage_vector.delta_profile

        return packet


# Factory function

def build_smp(
    *,
    origin_agent: str,
    input_reference: Dict[str, Any],
    classification: Dict[str, Any],
    analysis: Dict[str, Any],
    transform_report: Dict[str, Any],
    bridge_passed: bool,
    benevolence: Dict[str, Any],
    triadic_scores: Dict[str, float],
    final_decision: str,
    violations: List[str],
    route_to: str,
    metadata_header: Optional[Dict[str, Any]] = None,
    classification_state: Optional[str] = None,
    triage_vector: Optional[TriageVector] = None,
    delta_profile: Optional[Dict[str, Any]] = None,
    parent_id: Optional[str] = None,
    provenance: Optional[Dict[str, Any]] = None,
    append_artifacts: Optional[Dict[str, Any]] = None,
) -> StructuredMeaningPacket:
    """
    Package downstream-ready SMP metadata without altering or inferring content.
    """

    normalized_header = _normalize_metadata_header(metadata_header, classification_state)

    return StructuredMeaningPacket(
        smp_id=str(uuid.uuid4()),
        timestamp=time.time(),
        origin_agent=origin_agent,
        parent_id=parent_id,
        input_reference=input_reference,
        classification=classification,
        analysis=analysis,
        transform_report=transform_report,
        bridge_passed=bridge_passed,
        benevolence=benevolence,
        triadic_scores=triadic_scores,
        final_decision=final_decision,
        violations=violations,
        route_to=route_to,
        metadata_header=normalized_header,
        classification_state=classification_state,
        triage_vector=triage_vector,
        delta_profile=delta_profile or (triage_vector.delta_profile if triage_vector else {}),
        provenance=provenance or {},
        append_artifacts=append_artifacts or {},
    )


ALLOWED_EPISTEMIC_STATUS = {"REJECTED", "PROVISIONAL", "CONDITIONAL", "CANONICAL"}
ALLOWED_PROOF_COVERAGE = {"UNPROVEN", "PARTIALLY_PROVEN", "FULLY_PROVEN", "PROVEN_FALSE"}
ALLOWED_DEPENDENCY_SHAPE = {
    "LINGUISTIC_DEPENDENT",
    "INFERENTIAL_DEPENDENT",
    "EVIDENCE_DEPENDENT",
    "AXIOMATIC_DEPENDENT",
}


def _normalize_metadata_header(
    header: Optional[Dict[str, Any]],
    classification_state: Optional[str],
) -> Dict[str, Any]:
    if header is None:
        status = (classification_state or "PROVISIONAL").strip().upper()
        header = {"epistemic_status": status}

    if not isinstance(header, dict):
        raise ValueError("metadata_header must be a dict")

    status = header.get("epistemic_status")
    if not isinstance(status, str) or not status.strip():
        raise ValueError("metadata_header.epistemic_status is required")
    normalized_status = status.strip().upper()
    if normalized_status not in ALLOWED_EPISTEMIC_STATUS:
        raise ValueError("metadata_header.epistemic_status invalid")
    header["epistemic_status"] = normalized_status

    proof_coverage = header.get("proof_coverage")
    if proof_coverage is not None:
        if not isinstance(proof_coverage, str) or not proof_coverage.strip():
            raise ValueError("metadata_header.proof_coverage must be a non-empty string")
        proof_coverage = proof_coverage.strip().upper()
        if proof_coverage not in ALLOWED_PROOF_COVERAGE:
            raise ValueError("metadata_header.proof_coverage invalid")
        header["proof_coverage"] = proof_coverage

    dependency_shape = header.get("dependency_shape")
    if dependency_shape is not None:
        if not isinstance(dependency_shape, str) or not dependency_shape.strip():
            raise ValueError("metadata_header.dependency_shape must be a non-empty string")
        dependency_shape = dependency_shape.strip().upper()
        if dependency_shape not in ALLOWED_DEPENDENCY_SHAPE:
            raise ValueError("metadata_header.dependency_shape invalid")
        header["dependency_shape"] = dependency_shape

    semantic_projection = header.get("semantic_projection", [])
    header["semantic_projection"] = _normalize_semantic_projection(semantic_projection)

    return header


def _normalize_semantic_projection(value: Any) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("metadata_header.semantic_projection must be a list")
    projections = [str(item).strip().upper() for item in value if str(item).strip()]
    if not projections:
        return []
    registered = _load_semantic_projection_families()
    unregistered = [item for item in projections if item not in registered]
    if unregistered:
        raise ValueError(f"semantic_projection unregistered: {sorted(set(unregistered))}")
    return projections


def _load_semantic_projection_families() -> set[str]:
    root = _find_repo_root()
    manifest_path = root / "_Governance" / "Semantic_Projection_Manifest.json"
    if not manifest_path.is_file():
        raise ValueError("Semantic_Projection_Manifest.json missing")
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    families = payload.get("families") if isinstance(payload, dict) else None
    if not isinstance(families, dict):
        raise ValueError("Semantic_Projection_Manifest.json invalid")
    return {str(key).upper() for key in families.keys()}


...existing code...
