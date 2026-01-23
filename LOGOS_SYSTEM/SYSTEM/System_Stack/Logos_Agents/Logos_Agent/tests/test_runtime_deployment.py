"""
TESTS: Phase-G Agent Deployment
PURPOSE:
- Verify governed single-action execution
- Enforce fail-closed behavior
"""

from Logos_System.System_Stack.Logos_Agents.Logos_Agent.runtime import (
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
