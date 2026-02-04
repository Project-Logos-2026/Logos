"""
MODULE: plan_governance_interface
PHASE: Phase-Q (GOVERNANCE_INTEGRATION_NON_EXECUTABLE)
AUTHORITY: Protopraxic Logic (PXL)

PURPOSE:
Defines the sole governance review interface stub for planning artifacts
and explicitly denies all invocation attempts.

This module MUST fail closed.
"""

from typing import Any


class GovernanceInvocationError(RuntimeError):
    """Raised on any unauthorized or premature governance invocation."""
    pass


class GovernanceReviewInterface:
    """
    Canonical governance review interface stub.

    This interface:
    - defines the ONLY allowed conceptual governance entrypoint
    - does NOT implement approval
    - MUST deny all calls in Phase-Q
    """

    def submit_for_review(self, plan: Any) -> None:
        raise GovernanceInvocationError(
            "Governance review is not enabled. Phase-Q permits interface definition only."
        )


# Explicit denial for any accidental direct invocation

def _deny_direct_call(*args, **kwargs):
    raise GovernanceInvocationError("Direct governance invocation is forbidden.")
