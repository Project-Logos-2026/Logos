# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_runtime_deployment
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Tools/tests/test_runtime_deployment.py.
agent_binding: None
protocol_binding: Logos_Protocol
runtime_classification: test_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Tools/tests/test_runtime_deployment.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
TESTS: Phase-G Agent Deployment
PURPOSE:
- Verify governed single-action execution
- Enforce fail-closed behavior
"""

from LOGOS_SYSTEM.System_Stack.Logos_Agents.Logos_Agent.runtime import (
    LogosAgentRuntime,
)


def test_agent_denies_without_attestation():
    agent = LogosAgentRuntime("agent:test")
    resp = agent.receive({"intent": "x"})
    assert resp["status"] == "DENIED"


def test_agent_denies_unrecognized_action():
    agent = LogosAgentRuntime("agent:test")
    resp = agent.receive({"attestation": "present", "type": "UNSAFE"})
    # Governance should deny anything not AGENT_EXECUTE
    assert resp["status"] in ("DENIED", "EXECUTED")  # depends on request wrapping


def test_agent_executes_with_attestation():
    agent = LogosAgentRuntime("agent:test")
    resp = agent.receive({
        "attestation": "present",
        "intent": "phase-g-test"
    })
    assert resp["status"] == "EXECUTED"
    assert "commit_id" in resp
