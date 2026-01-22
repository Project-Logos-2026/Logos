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
