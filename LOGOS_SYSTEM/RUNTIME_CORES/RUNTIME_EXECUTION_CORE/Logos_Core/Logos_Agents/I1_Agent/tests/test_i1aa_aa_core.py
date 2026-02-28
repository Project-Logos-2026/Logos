import pytest
import time
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.I1_Agent_Tools.scp_integrations.i1aa_binder import I1AABinder
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.I1_Agent_Infra.config.hashing import safe_hash

def minimal_smp_core():
    return {"id": "SMP-001", "data": {"foo": "bar"}}

def test_i1aa_aa_core_compliance():
    binder = I1AABinder()
    smp_core = minimal_smp_core()
    smp_id = smp_core["id"]
    mvs_result = {"meta": {}, "coherence_score": 0.9}
    bdn_result = {"meta": {}, "stability_score": 0.8}
    sign_grounding = {"epistemic_status": "good"}
    privation_profile = {"depth_level": 1}
    aa = binder.bind(smp_id, mvs_result, bdn_result, sign_grounding, privation_profile, smp_core=smp_core)
    required_keys = [
        "aa_id", "aa_type", "aa_origin_type", "originating_entity", "bound_smp_id", "bound_smp_hash", "creation_timestamp", "aa_hash", "classification_state", "promotion_context", "origin_signature", "cross_validation_signatures", "verification_stage", "metadata_header", "content", "diff_references"
    ]
    for k in required_keys:
        assert k in aa, f"Missing AA_CORE key: {k}"
    for k in ["aa_id", "aa_hash", "bound_smp_id", "bound_smp_hash", "origin_signature"]:
        assert aa[k], f"Required AA_CORE field {k} is empty"
    assert aa["aa_type"] == "I1AA"
    assert aa["classification_state"] == "provisional"
    assert isinstance(aa["content"], dict)
    assert "fractal_configuration" in aa["content"]
    assert "modal_analysis_summary" in aa["content"]
    assert "causal_chain_findings" in aa["content"]
    assert "salvageability_assessment" in aa["content"]
    assert "analysis_stack" in aa["content"]
    assert "validation_conflicts" in aa["content"]
    assert "meta_reasoning_flags" in aa["content"]
    assert "overall_confidence" in aa["content"]
    assert "provenance_trace" in aa["content"]
