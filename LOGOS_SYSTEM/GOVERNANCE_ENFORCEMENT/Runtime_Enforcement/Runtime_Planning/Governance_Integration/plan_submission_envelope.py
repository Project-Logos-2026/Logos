# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: plan_submission_envelope
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Governance_Integration/plan_submission_envelope.py.
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
  source: LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Governance_Integration/plan_submission_envelope.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
MODULE: plan_submission_envelope
PHASE: Phase-Q (GOVERNANCE_INTEGRATION_NON_EXECUTABLE)
AUTHORITY: Protopraxic Logic (PXL)

PURPOSE:
Defines a pure data envelope for submitting planning artifacts
to governance review.

This module:
- does NOT submit plans
- does NOT approve plans
- does NOT invoke governance
- does NOT enable execution, autonomy, or activation

It defines structure ONLY.
"""

from dataclasses import dataclass
from typing import Dict, Any
from Logos_System.Planning_Runtime.Plan_Objects.plan_schema import PlanObject


class SubmissionEnvelopeError(ValueError):
    """Raised when a submission envelope is malformed."""
    pass


@dataclass(frozen=True)
class PlanSubmissionEnvelope:
    plan: PlanObject
    submitted_by: str
    submitted_at_utc: str
    declared_intent: str
    provenance: Dict[str, Any]

    def __post_init__(self):
        if not self.submitted_by:
            raise SubmissionEnvelopeError("submitted_by is required")

        if not self.submitted_at_utc:
            raise SubmissionEnvelopeError("submitted_at_utc is required")

        if not self.declared_intent:
            raise SubmissionEnvelopeError("declared_intent is required")

        if not isinstance(self.provenance, dict):
            raise SubmissionEnvelopeError("provenance must be a dictionary")
