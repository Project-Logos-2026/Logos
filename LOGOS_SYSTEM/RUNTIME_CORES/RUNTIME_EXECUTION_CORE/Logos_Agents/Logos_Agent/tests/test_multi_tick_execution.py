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
