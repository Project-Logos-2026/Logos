# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: plan_governance_interface
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Governance_Integration/plan_governance_interface.py.
agent_binding: None
protocol_binding: None
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Governance_Integration/plan_governance_interface.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

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
