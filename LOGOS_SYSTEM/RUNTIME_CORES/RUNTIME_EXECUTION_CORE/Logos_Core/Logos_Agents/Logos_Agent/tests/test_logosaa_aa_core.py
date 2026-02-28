import pytest
import time
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Tools.logos_aa_builder import build_logos_aa

def minimal_smp():
    return {"id": "SMP-LOGOS-001", "data": {"foo": "bar"}}

def test_logosaa_promotion_and_rejection():
    smp = minimal_smp()
    bound_smp_id = smp["id"]
    bound_smp_hash = "dummyhash1234567890abcdef"
    source_aa_ids = ["AA-1", "AA-2"]
    # Promotion (CANONICAL)
    aa_prom = build_logos_aa(
        bound_smp_id=bound_smp_id,
        bound_smp_hash=bound_smp_hash,
        decision_type="promotion",
        source_aa_ids=source_aa_ids,
        resulting_state="CANONICAL",
        semantic_projection=[],
        proof_coverage="FULLY_PROVEN"
    )
    # Rejection (REJECTED)
    aa_rej = build_logos_aa(
        bound_smp_id=bound_smp_id,
        bound_smp_hash=bound_smp_hash,
        decision_type="rejection",
        source_aa_ids=source_aa_ids,
        resulting_state="REJECTED",
        semantic_projection=["EXAMPLE_FAMILY"],
        proof_coverage="PROVEN_FALSE"
    )
    required_keys = [
        "aa_id", "aa_type", "aa_origin_type", "originating_entity", "bound_smp_id", "bound_smp_hash", "creation_timestamp", "aa_hash", "classification_state", "promotion_context", "origin_signature", "cross_validation_signatures", "verification_stage", "metadata_header", "content", "diff_references"
    ]
    for aa, state, proof, sem_proj, vstage in [
        (aa_prom, "canonical", "FULLY_PROVEN", [], "pre-canonicalization"),
        (aa_rej, "rejected", "PROVEN_FALSE", ["EXAMPLE_FAMILY"], "pre-canonicalization")
    ]:
        for k in required_keys:
            assert k in aa, f"Missing AA_CORE key: {k}"
        assert aa["aa_type"] == "LogosAA"
        assert aa["classification_state"] == state
        assert aa["verification_stage"] == vstage
        header = aa["metadata_header"]
        assert header["epistemic_status"] == state.upper()
        assert header["proof_coverage"] == proof
        assert isinstance(header["semantic_projection"], list)
        if sem_proj:
            assert header["semantic_projection"] == [x.upper() for x in sem_proj]
        else:
            assert header["semantic_projection"] == []
