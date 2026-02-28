import pytest
import time
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Advanced_Reasoning_Protocol.ARP_Core.engines.unified_binder import UnifiedBinder
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I3_Agent.I3_Agent_Infra.config.hashing import safe_hash

def minimal_smp_core():
    return {"id": "SMP-002", "data": {"bar": "baz"}}

def test_i3aa_aa_core_compliance():
    binder = UnifiedBinder()
    smp_core = minimal_smp_core()
    aaced_packet = {"smp_id": smp_core["id"]}
    context = {}
    base_packet = {"engine_results": {}, "provenance": [], "status": "success"}
    taxonomy_packet = {"taxonomies": {}, "status": "success"}
    synthesis_packet = {"synthesis_result": {}, "pxl_result": {}, "active_iel_domains": [], "active_math_categories": [], "status": "success"}
    aa = binder.bind(aaced_packet, context, base_packet, taxonomy_packet, synthesis_packet, smp_core=smp_core)
    required_keys = [
        "aa_id", "aa_type", "aa_origin_type", "originating_entity", "bound_smp_id", "bound_smp_hash", "creation_timestamp", "aa_hash", "classification_state", "promotion_context", "origin_signature", "cross_validation_signatures", "verification_stage", "metadata_header", "content", "diff_references"
    ]
    for k in required_keys:
        assert k in aa, f"Missing AA_CORE key: {k}"
    for k in ["aa_id", "aa_hash", "bound_smp_id", "bound_smp_hash", "origin_signature"]:
        assert aa[k], f"Required AA_CORE field {k} is empty"
    assert aa["aa_type"] == "I3AA"
    assert aa["classification_state"] == "provisional"
    assert isinstance(aa["content"], dict)
    assert "reasoning_domains_used" in aa["content"]
    assert "aggregation_summary" in aa["content"]
    assert "validation_conflicts" in aa["content"]
    assert "meta_reasoning_flags" in aa["content"]
    assert "analysis_stack" in aa["content"]
    assert "overall_confidence" in aa["content"]
    assert "provenance_trace" in aa["content"]
