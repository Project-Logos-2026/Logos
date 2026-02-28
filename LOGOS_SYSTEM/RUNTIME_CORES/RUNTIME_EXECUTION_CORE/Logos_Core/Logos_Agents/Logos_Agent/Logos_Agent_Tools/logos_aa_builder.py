from typing import Dict, Any, List, Optional
import json, hashlib, time

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.I2_Agent_Tools.aa import build_append_artifact

ALLOWED_DECISION_TYPES = {"promotion", "rejection", "conflict_resolution"}
ALLOWED_RESULTING_STATES = {"CANONICAL", "REJECTED", "CONDITIONAL"}

def build_logos_aa(
    *,
    bound_smp_id: str,
    bound_smp_hash: str,
    decision_type: str,
    source_aa_ids: List[str],
    resulting_state: str,
    promotion_criteria: Optional[Dict[str, Any]] = None,
    cross_validation: Optional[Dict[str, Any]] = None,
    notes: Optional[str] = None,
    semantic_projection: Optional[List[str]] = None,
    dependency_shape: Optional[str] = None,
    proof_coverage: Optional[str] = None,
    creation_timestamp: Optional[float] = None
) -> Dict[str, Any]:

    if decision_type not in ALLOWED_DECISION_TYPES:
        raise Exception("Invalid LogosAA decision_type")

    if resulting_state.upper() not in ALLOWED_RESULTING_STATES:
        raise Exception("Invalid LogosAA resulting_state")

    if not isinstance(source_aa_ids, list) or not source_aa_ids:
        raise Exception("LogosAA requires non-empty source_aa_ids")

    resulting_state_upper = resulting_state.upper()
    classification_state = resulting_state_upper.lower()

    ts = creation_timestamp if creation_timestamp is not None else time.time()

    origin_sig_payload = {
        "originating_entity": "Logos_Agent",
        "aa_type": "LogosAA",
        "bound_smp_id": bound_smp_id,
        "bound_smp_hash": bound_smp_hash,
        "creation_timestamp": ts
    }

    origin_signature = "sha256:" + hashlib.sha256(
        json.dumps(origin_sig_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()

    metadata_header = {
        "epistemic_status": resulting_state_upper,
        "proof_coverage": proof_coverage or "UNPROVEN",
        "semantic_projection": semantic_projection or []
    }

    if dependency_shape:
        metadata_header["dependency_shape"] = dependency_shape

    content = {
        "decision_type": decision_type,
        "source_aa_ids": source_aa_ids,
        "promotion_criteria": promotion_criteria or {},
        "cross_validation": cross_validation or {},
        "resulting_state": resulting_state_upper,
        "notes": notes or ""
    }

    aa = build_append_artifact(
        aa_type="LogosAA",
        aa_origin_type="agent",
        originating_entity="Logos_Agent",
        bound_smp_id=bound_smp_id,
        bound_smp_hash=bound_smp_hash,
        classification_state=classification_state,
        promotion_context={},
        origin_signature=origin_signature,
        verification_stage="pre-canonicalization",
        content=content,
        cross_validation_signatures=[],
        metadata_header=metadata_header,
        creation_timestamp=ts
    )

    return aa.to_dict()
