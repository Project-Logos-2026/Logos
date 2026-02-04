"""
MODULE: governance_review_response
PHASE: Phase-Q (GOVERNANCE_INTEGRATION_NON_EXECUTABLE)
AUTHORITY: Protopraxic Logic (PXL)

PURPOSE:
Defines the canonical data structure for governance review outcomes.

This module:
- does NOT perform governance review
- does NOT approve or deny plans
- does NOT trigger execution or activation
- encodes review outcomes as inert data only
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, Literal


class GovernanceResponseError(ValueError):
    """Raised when a governance response is malformed."""
    pass


GovernanceDecision = Literal[
    "APPROVED",
    "DENIED",
    "DEFERRED",
    "REQUIRES_REVISION",
]


@dataclass(frozen=True)
class GovernanceReviewResponse:
    plan_id: str
    decision: GovernanceDecision
    reviewed_at_utc: str
    reviewer_id: str
    rationale: str
    conditions: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.plan_id:
            raise GovernanceResponseError("plan_id is required")

        if not self.reviewed_at_utc:
            raise GovernanceResponseError("reviewed_at_utc is required")

        if not self.reviewer_id:
            raise GovernanceResponseError("reviewer_id is required")

        if not self.rationale:
            raise GovernanceResponseError("rationale is required")

        if self.conditions is not None and not isinstance(self.conditions, dict):
            raise GovernanceResponseError("conditions must be a dictionary if provided")
