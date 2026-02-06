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
module_name: aa
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
  source: System_Stack/Logos_Agents/I2_Agent/protocol_operations/aa.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-02-06T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Append Artifact (AA) schema and builder for the I2 agent context.

This module is intentionally non-transformative. It packages AA metadata
and content for downstream governance evaluation without mutating SMPs.
"""


from dataclasses import dataclass, field
import json
import time
import uuid
from typing import Any, Dict, List, Optional

from I2_Agent.config.hashing import safe_hash
from I2_Agent.diagnostics.errors import SchemaError


ALLOWED_AA_TYPES = {"I1AA", "I2AA", "I3AA", "LogosAA", "ProtocolAA"}
ALLOWED_ORIGIN_TYPES = {"agent", "protocol"}
ALLOWED_CLASSIFICATION = {"rejected", "conditional", "provisional", "canonical"}
ALLOWED_VERIFICATION_STAGE = {"ingress", "post-triune", "pre-canonicalization"}


@dataclass(frozen=True)
class AppendArtifact:
    aa_id: str
    aa_type: str
    aa_origin_type: str
    originating_entity: str
    bound_smp_id: str
    bound_smp_hash: str
    creation_timestamp: float
    aa_hash: str
    classification_state: str
    promotion_context: Dict[str, Any]
    origin_signature: str
    cross_validation_signatures: List[str]
    verification_stage: str
    content: Dict[str, Any] = field(default_factory=dict)
    diff_references: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "aa_id": self.aa_id,
            "aa_type": self.aa_type,
            "aa_origin_type": self.aa_origin_type,
            "originating_entity": self.originating_entity,
            "bound_smp_id": self.bound_smp_id,
            "bound_smp_hash": self.bound_smp_hash,
            "creation_timestamp": self.creation_timestamp,
            "aa_hash": self.aa_hash,
            "classification_state": self.classification_state,
            "promotion_context": self.promotion_context,
            "origin_signature": self.origin_signature,
            "cross_validation_signatures": list(self.cross_validation_signatures),
            "verification_stage": self.verification_stage,
            "content": self.content,
            "diff_references": self.diff_references,
        }


def _normalize_list(values: Optional[List[Any]]) -> List[str]:
    if not values:
        return []
    return [str(v) for v in values if v is not None]


def _stable_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _validate_required(value: Any, field_name: str) -> None:
    if value is None or (isinstance(value, str) and not value.strip()):
        raise SchemaError(f"AA missing {field_name}")


def _validate_enum(value: str, allowed: set, field_name: str) -> None:
    if value not in allowed:
        raise SchemaError(f"AA {field_name} must be one of: {sorted(allowed)}")


def _build_aa_hash(payload: Dict[str, Any]) -> str:
    return safe_hash(_stable_json(payload))


def build_append_artifact(
    *,
    aa_type: str,
    aa_origin_type: str,
    originating_entity: str,
    bound_smp_id: str,
    bound_smp_hash: str,
    classification_state: str,
    promotion_context: Optional[Dict[str, Any]] = None,
    origin_signature: str = "",
    verification_stage: str = "ingress",
    content: Optional[Dict[str, Any]] = None,
    diff_references: Optional[Dict[str, Any]] = None,
    cross_validation_signatures: Optional[List[Any]] = None,
    aa_id: Optional[str] = None,
    creation_timestamp: Optional[float] = None,
) -> AppendArtifact:
    """
    Build a non-authoritative AA record with a stable AA hash.
    """

    _validate_required(aa_type, "aa_type")
    _validate_required(aa_origin_type, "aa_origin_type")
    _validate_required(originating_entity, "originating_entity")
    _validate_required(bound_smp_id, "bound_smp_id")
    _validate_required(bound_smp_hash, "bound_smp_hash")
    _validate_required(classification_state, "classification_state")
    _validate_required(verification_stage, "verification_stage")

    _validate_enum(aa_type, ALLOWED_AA_TYPES, "aa_type")
    _validate_enum(aa_origin_type, ALLOWED_ORIGIN_TYPES, "aa_origin_type")
    _validate_enum(classification_state, ALLOWED_CLASSIFICATION, "classification_state")
    _validate_enum(verification_stage, ALLOWED_VERIFICATION_STAGE, "verification_stage")

    aa_id = aa_id or str(uuid.uuid4())
    ts = float(creation_timestamp) if creation_timestamp is not None else time.time()
    promotion_context = promotion_context or {}
    content = content or {}
    diff_references = diff_references or {}
    cross_validation_signatures = _normalize_list(cross_validation_signatures)

    if not isinstance(promotion_context, dict):
        raise SchemaError("AA promotion_context must be a dict")
    if not isinstance(content, dict):
        raise SchemaError("AA content must be a dict")
    if not isinstance(diff_references, dict):
        raise SchemaError("AA diff_references must be a dict")

    canonical_payload = {
        "aa_id": aa_id,
        "aa_type": aa_type,
        "aa_origin_type": aa_origin_type,
        "originating_entity": originating_entity,
        "bound_smp_id": bound_smp_id,
        "bound_smp_hash": bound_smp_hash,
        "creation_timestamp": ts,
        "classification_state": classification_state,
        "promotion_context": promotion_context,
        "origin_signature": origin_signature,
        "cross_validation_signatures": cross_validation_signatures,
        "verification_stage": verification_stage,
        "content": content,
        "diff_references": diff_references,
    }

    aa_hash = _build_aa_hash(canonical_payload)

    return AppendArtifact(
        aa_id=aa_id,
        aa_type=aa_type,
        aa_origin_type=aa_origin_type,
        originating_entity=originating_entity,
        bound_smp_id=bound_smp_id,
        bound_smp_hash=bound_smp_hash,
        creation_timestamp=ts,
        aa_hash=aa_hash,
        classification_state=classification_state,
        promotion_context=promotion_context,
        origin_signature=origin_signature,
        cross_validation_signatures=cross_validation_signatures,
        verification_stage=verification_stage,
        content=content,
        diff_references=diff_references,
    )
