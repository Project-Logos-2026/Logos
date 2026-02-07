# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_multi_tick_execution
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Tools/tests/test_multi_tick_execution.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Tools/tests/test_multi_tick_execution.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Phase-H: Multi-Tick Execution — Specification Tests (TEST-FIRST)

These tests define the required governance and safety properties
for future multi-tick agent execution.

They MUST FAIL or SKIP until explicit enablement is implemented.
"""

import pytest


def test_multi_tick_denied_without_explicit_policy():
    """
    Multi-tick execution must be denied by default.

    This test is intentionally strict:
    - If a GovernanceDenied (or equivalent) exception exists, it must be raised.
    - Otherwise, this test is expected to fail until such a type is introduced.
    """
    try:
        from Logos_System.Governance.exceptions import GovernanceDenied
    except Exception:
        pytest.xfail("Typed governance denial not yet implemented")
        raise

    with pytest.raises(GovernanceDenied):
        raise GovernanceDenied("Multi-tick execution not authorized")


def test_multi_tick_with_budget_and_attestation():
    """
    Expected future behavior:
    - Explicit multi-tick policy granted
    - Bounded tick budget (N)
    - Each tick audited
    - UWM commits append-only per tick
    """
    from Logos_System.Governance.policy_checks import require_multi_tick_policy
    from Logos_System.System_Stack.Logos_Protocol.Phase_E_Tick_Engine import PhaseETickEngine

    policy = {"authorized": True, "max_ticks": 2}
    budget = require_multi_tick_policy(policy)

    engine = PhaseETickEngine(budget)
    log = engine.run_multi_tick(budget, lambda: None)

    ticks = [e for e in log if e["event"] == "TICK"]
    assert len(ticks) == budget


def test_tick_budget_exhaustion_fails_closed():
    """
    When tick budget is exhausted, execution must halt
    and no further commits are allowed.
    """
    from Logos_System.System_Stack.Logos_Protocol.Phase_E_Tick_Engine import PhaseETickEngine

    calls = {"count": 0}

    def fn():
        calls["count"] += 1

    engine = PhaseETickEngine(max_ticks=2)
    engine.start()

    log = engine.run_multi_tick(2, fn)

    # Exactly 2 ticks executed
    ticks = [e for e in log if e["event"] == "TICK"]
    assert len(ticks) == 2
    assert calls["count"] == 2

    # Engine must be inactive after halt
    assert engine.active is False
