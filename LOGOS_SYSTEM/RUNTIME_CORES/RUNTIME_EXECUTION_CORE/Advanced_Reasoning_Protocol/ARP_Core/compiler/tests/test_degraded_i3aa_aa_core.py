import pytest
import time
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Advanced_Reasoning_Protocol.ARP_Core.compiler.arp_compiler_core import ARPCompilerCore
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I3_Agent.I3_Agent_Infra.config.hashing import safe_hash

def minimal_smp_core():
    return {"id": "SMP-003", "data": {"baz": "qux"}}

def test_degraded_i3aa_aa_core_compliance():
    core = ARPCompilerCore()
    smp_core = minimal_smp_core()
    aaced_packet = {"smp_id": smp_core["id"]}
    context = {}
    failure_stage = "base_reasoning"
    failure_reason = "test failure"
    aa = core._emit_degraded_i3aa(aaced_packet, context, failure_stage, failure_reason, smp_core=smp_core)
    required_keys = [
        "aa_id", "aa_type", "aa_origin_type", "originating_entity", "bound_smp_id", "bound_smp_hash", "creation_timestamp", "aa_hash", "classification_state", "promotion_context", "origin_signature", "cross_validation_signatures", "verification_stage", "metadata_header", "content", "diff_references"
    ]
    for k in required_keys:
        assert k in aa, f"Missing AA_CORE key: {k}"
    for k in ["aa_id", "aa_hash", "bound_smp_id", "bound_smp_hash", "origin_signature"]:
        assert aa[k], f"Required AA_CORE field {k} is empty"
    assert aa["aa_type"] == "I3AA"
    assert aa["classification_state"] == "rejected"
    assert isinstance(aa["content"], dict)
    assert "failure_stage" in aa["content"]
    assert "failure_reason" in aa["content"]
    assert "analysis_stack" in aa["content"]
    assert "meta_reasoning_flags" in aa["content"]
    assert "validation_conflicts" in aa["content"]
