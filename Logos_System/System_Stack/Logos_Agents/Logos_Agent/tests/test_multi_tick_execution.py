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


@pytest.mark.skip(reason="Multi-tick governance not yet implemented")
def test_multi_tick_with_budget_and_attestation():
    """
    Expected future behavior:
    - Explicit multi-tick policy granted
    - Bounded tick budget (N)
    - Each tick audited
    - UWM commits append-only per tick
    """
    pass


@pytest.mark.skip(reason="Multi-tick governance not yet implemented")
def test_tick_budget_exhaustion_fails_closed():
    """
    When tick budget is exhausted, execution must halt
    and no further commits are allowed.
    """
    pass
