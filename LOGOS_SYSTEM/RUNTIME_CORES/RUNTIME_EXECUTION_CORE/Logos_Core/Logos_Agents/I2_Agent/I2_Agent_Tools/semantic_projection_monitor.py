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
module_name: semantic_projection_monitor
runtime_layer: inferred
role: inferred
agent_binding: I2
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Halts on missing metadata header or unregistered semantic projection."
rewrite_provenance:
  source: None
  rewrite_phase: Phase_I
  rewrite_timestamp: 2026-02-06T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
I2 Semantic Projection Monitor

Tracks SMPs and AAs by semantic projection family and performs I2-exclusive
cluster decomposition/recomposition when epistemic exhaustion is detected.

Design-first, fail-closed, non-executing by default. All actions are local
and require I2 authorization.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
import time
import uuid
from typing import Any, Dict, List, Optional

from I2_Agent.config.constants import AGENT_I2
from I2_Agent.config.hashing import safe_hash
from I2_Agent.diagnostics.errors import SchemaError
from I2_Agent.protocol_operations.aa import build_append_artifact


ALLOWED_PROOF_COVERAGE = {"UNPROVEN", "PARTIALLY_PROVEN", "FULLY_PROVEN", "PROVEN_FALSE"}


@dataclass
class Segment:
    segment_id: str
    segment_type: str
    proof_coverage: Optional[str]
    metadata_header: Dict[str, Any]
    span_mapping: Dict[str, Any]
    provenance: Dict[str, Any]
    payload: Dict[str, Any]


@dataclass
class Cluster:
    family: str
    segments: List[Segment] = field(default_factory=list)
    retired: bool = False


@dataclass
class RecompositionResult:
    family: str
    smp_t: Dict[str, Any]
    aa_f: Dict[str, Any]
    retired_segment_ids: List[str]
    timestamp: float


class I2SemanticClusterMonitor:
    """
    I2-only semantic cluster monitor for decomposition/recomposition.
    """

    def __init__(self, actor_id: str = AGENT_I2) -> None:
        self.actor_id = actor_id
        self._clusters: Dict[str, Cluster] = {}

    def register_payload(self, payload: Dict[str, Any], actor: str) -> List[RecompositionResult]:
        self._require_i2(actor)
        recompositions: List[RecompositionResult] = []
        for item in _extract_payload_items(payload):
            segment = self._build_segment(item)
            if not segment.metadata_header.get("semantic_projection"):
                continue
            families = segment.metadata_header.get("semantic_projection", [])
            for family in families:
                cluster = self._clusters.setdefault(family, Cluster(family=family))
                if cluster.retired:
                    continue
                cluster.segments.append(segment)
                result = self._check_exhaustion(cluster)
                if result:
                    recompositions.append(result)
        return recompositions

    def _check_exhaustion(self, cluster: Cluster) -> Optional[RecompositionResult]:
        if cluster.retired:
            return None
        if len(cluster.segments) <= 1:
            return None

        decided = [seg for seg in cluster.segments if _is_decided(seg.proof_coverage)]
        if len(decided) != len(cluster.segments):
            return None

        bucket_t = [seg for seg in cluster.segments if seg.proof_coverage == "FULLY_PROVEN"]
        bucket_f = [seg for seg in cluster.segments if seg.proof_coverage == "PROVEN_FALSE"]
        if not bucket_t or not bucket_f:
            return None

        smp_t = _build_recomposed_smp(cluster.family, bucket_t)
        aa_f = _build_recomposed_aa(cluster.family, smp_t, bucket_f, actor_id=self.actor_id)

        cluster.retired = True
        retired_ids = [seg.segment_id for seg in cluster.segments]

        return RecompositionResult(
            family=cluster.family,
            smp_t=smp_t,
            aa_f=aa_f,
            retired_segment_ids=retired_ids,
            timestamp=time.time(),
        )

    def _build_segment(self, payload: Dict[str, Any]) -> Segment:
        metadata_header = _extract_metadata_header(payload)
        proof_coverage = _normalize_proof_coverage(metadata_header.get("proof_coverage"))
        span_mapping = _extract_span_mapping(payload)
        provenance = _extract_provenance(payload)
        segment_id, segment_type = _extract_segment_identity(payload)

        return Segment(
            segment_id=segment_id,
            segment_type=segment_type,
            proof_coverage=proof_coverage,
            metadata_header=metadata_header,
            span_mapping=span_mapping,
            provenance=provenance,
            payload=payload,
        )

    def _require_i2(self, actor: str) -> None:
        if actor != self.actor_id:
            raise SchemaError("Recomposition restricted to I2")


def _extract_payload_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []

    if isinstance(payload.get("mtp_smp"), dict):
        items.append(payload["mtp_smp"])
    if isinstance(payload.get("smp"), dict):
        items.append(payload["smp"])

    if _is_smp_payload(payload) or _is_aa_payload(payload):
        items.append(payload)

    append_artifacts = payload.get("append_artifacts")
    if isinstance(append_artifacts, dict):
        items.append(append_artifacts)
    elif isinstance(append_artifacts, list):
        items.extend([item for item in append_artifacts if isinstance(item, dict)])

    return items


def _extract_metadata_header(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise SchemaError("metadata_header missing")

    if isinstance(payload.get("metadata_header"), dict):
        header = payload["metadata_header"]
    elif isinstance(payload.get("header"), dict) and "epistemic_status" in payload["header"]:
        header = payload["header"]
    else:
        raise SchemaError("metadata_header missing")

    if "epistemic_status" not in header:
        raise SchemaError("metadata_header.epistemic_status missing")

    header = dict(header)
    header["semantic_projection"] = _normalize_semantic_projection(header.get("semantic_projection", []))
    return header


def _normalize_semantic_projection(value: Any) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise SchemaError("metadata_header.semantic_projection must be a list")
    projections = [str(item).strip().upper() for item in value if str(item).strip()]
    if not projections:
        return []
    registered = _load_semantic_projection_families()
    unregistered = [item for item in projections if item not in registered]
    if unregistered:
        raise SchemaError(f"semantic_projection unregistered: {sorted(set(unregistered))}")
    return projections


def _normalize_proof_coverage(value: Any) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise SchemaError("metadata_header.proof_coverage must be a non-empty string")
    normalized = value.strip().upper()
    if normalized not in ALLOWED_PROOF_COVERAGE:
        raise SchemaError("metadata_header.proof_coverage invalid")
    return normalized


def _extract_span_mapping(payload: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(payload.get("PROVISIONAL_PROOF_TAG"), dict):
        tag = payload["PROVISIONAL_PROOF_TAG"]
        if isinstance(tag.get("span_mapping"), dict):
            return tag["span_mapping"]
    content = payload.get("content") if isinstance(payload.get("content"), dict) else {}
    if isinstance(content.get("span_mapping"), dict):
        return content["span_mapping"]
    return {}


def _extract_provenance(payload: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(payload.get("provenance"), dict):
        return payload["provenance"]
    if isinstance(payload.get("header"), dict):
        return {"processing_history": payload["header"].get("processing_history", [])}
    return {}


def _extract_segment_identity(payload: Dict[str, Any]) -> tuple[str, str]:
    if _is_aa_payload(payload):
        return str(payload.get("aa_id")), "aa"
    if _is_smp_payload(payload):
        return str(_extract_smp_id(payload)), "smp"
    raise SchemaError("segment identity missing")


def _extract_smp_id(payload: Dict[str, Any]) -> str:
    if isinstance(payload.get("smp_id"), str):
        return payload["smp_id"]
    if isinstance(payload.get("header"), dict) and payload["header"].get("smp_id"):
        return str(payload["header"].get("smp_id"))
    return f"SMP-UNKNOWN-{uuid.uuid4().hex[:8]}"


def _is_smp_payload(payload: Dict[str, Any]) -> bool:
    return any(key in payload for key in ("smp_id", "raw_input", "header"))


def _is_aa_payload(payload: Dict[str, Any]) -> bool:
    return {"aa_id", "aa_type"}.issubset(payload.keys())


def _is_decided(proof_coverage: Optional[str]) -> bool:
    return proof_coverage in {"FULLY_PROVEN", "PROVEN_FALSE"}


def _build_recomposed_smp(family: str, bucket_t: List[Segment]) -> Dict[str, Any]:
    smp_id = f"SMP-RECOMPOSED-{uuid.uuid4().hex}"
    span_mappings = [seg.span_mapping for seg in bucket_t if seg.span_mapping]
    source_segments = [
        {
            "segment_id": seg.segment_id,
            "segment_type": seg.segment_type,
            "provenance": seg.provenance,
            "span_mapping": seg.span_mapping,
        }
        for seg in bucket_t
    ]

    return {
        "smp_id": smp_id,
        "timestamp": time.time(),
        "origin_agent": AGENT_I2,
        "metadata_header": {
            "epistemic_status": "PROVISIONAL",
            "proof_coverage": "FULLY_PROVEN",
            "semantic_projection": [family],
        },
        "recomposition": {
            "family": family,
            "bucket": "T",
            "source_segments": source_segments,
            "span_mappings": span_mappings,
        },
        "provenance": {
            "actor": AGENT_I2,
            "action": "recompose_true_bucket",
            "timestamp": time.time(),
        },
    }


def _build_recomposed_aa(
    family: str,
    smp_t: Dict[str, Any],
    bucket_f: List[Segment],
    actor_id: str,
) -> Dict[str, Any]:
    span_mappings = [seg.span_mapping for seg in bucket_f if seg.span_mapping]
    source_segments = [
        {
            "segment_id": seg.segment_id,
            "segment_type": seg.segment_type,
            "provenance": seg.provenance,
            "span_mapping": seg.span_mapping,
        }
        for seg in bucket_f
    ]

    aa = build_append_artifact(
        aa_type="I2AA",
        aa_origin_type="agent",
        originating_entity=actor_id,
        bound_smp_id=str(smp_t.get("smp_id")),
        bound_smp_hash=safe_hash(smp_t),
        classification_state="rejected",
        promotion_context={
            "recomposition_family": family,
            "bucket": "F",
            "source_segments": [seg.segment_id for seg in bucket_f],
        },
        verification_stage="post-triune",
        metadata_header={
            "epistemic_status": "REJECTED",
            "proof_coverage": "PROVEN_FALSE",
            "semantic_projection": [family],
        },
        content={
            "negative_baseline": True,
            "span_mappings": span_mappings,
            "source_segments": source_segments,
        },
    )

    return aa.to_dict()


def _load_semantic_projection_families() -> set[str]:
    root = _find_repo_root()
    manifest_path = root / "_Governance" / "Semantic_Projection_Manifest.json"
    if not manifest_path.is_file():
        raise SchemaError("Semantic_Projection_Manifest.json missing")
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    families = payload.get("families") if isinstance(payload, dict) else None
    if not isinstance(families, dict):
        raise SchemaError("Semantic_Projection_Manifest.json invalid")
    return {str(key).upper() for key in families.keys()}


def _find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "_Governance").is_dir():
            return parent
    raise SchemaError("Repository root with _Governance not found")
