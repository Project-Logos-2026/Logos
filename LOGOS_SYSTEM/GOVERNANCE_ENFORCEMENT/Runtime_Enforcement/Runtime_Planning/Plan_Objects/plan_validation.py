# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: plan_validation
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Plan_Objects/plan_validation.py.
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
  source: LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Plan_Objects/plan_validation.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
MODULE: plan_validation
PHASE: Phase-P (IMPLEMENTATION_NON_EXECUTABLE)
AUTHORITY: Protopraxic Logic (PXL)

PURPOSE:
Provides pure validation logic for planning plan objects.
This module performs structural and governance-invariant checks only.

CONSTRAINTS:
- NO execution
- NO scheduling
- NO autonomy
- NO runtime activation
- NO approval or authorization effects
- Fail-closed on any violation
"""

from typing import Iterable
from .plan_schema import PlanObject, PlanStep


class PlanValidationError(ValueError):
    """Raised when a plan fails validation."""
    pass


def validate_plan(plan: PlanObject, *, allowed_permissions: Iterable[str]) -> None:
    """
    Validate a PlanObject against governance invariants.

    This function:
    - raises PlanValidationError on failure
    - returns None on success
    - has no side effects
    """

    # Metadata checks
    if not plan.metadata.plan_id:
        raise PlanValidationError("Missing plan_id")

    if not plan.metadata.domain:
        raise PlanValidationError("Missing domain")

    if plan.metadata.tick_budget <= 0:
        raise PlanValidationError("Tick budget must be positive")

    # Step checks
    if not plan.steps:
        raise PlanValidationError("Plan must contain at least one step")

    for step in plan.steps:
        _validate_step(step)

    # Permission checks
    allowed = set(allowed_permissions)
    declared = set(plan.declared_permissions)

    if not declared.issubset(allowed):
        raise PlanValidationError(
            f"Plan declares permissions not allowed: {declared - allowed}"
        )


def _validate_step(step: PlanStep) -> None:
    if not step.step_id:
        raise PlanValidationError("Step missing step_id")

    if not step.description:
        raise PlanValidationError("Step missing description")

    if not isinstance(step.constraints, dict):
        raise PlanValidationError("Step constraints must be a dictionary")
