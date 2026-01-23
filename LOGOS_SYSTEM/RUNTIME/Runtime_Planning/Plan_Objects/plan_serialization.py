
"""
MODULE: plan_serialization
PHASE: Phase-P (IMPLEMENTATION_NON_EXECUTABLE)
AUTHORITY: Protopraxic Logic (PXL)

PURPOSE:
Provides pure serialization and deserialization utilities
for plan object schemas.

CONSTRAINTS:
- NO execution
- NO scheduling
- NO autonomy
- NO runtime activation
- Deterministic, side-effect free
"""

from typing import Dict, Any, List
from .plan_schema import PlanObject, PlanMetadata, PlanStep


def serialize_plan(plan: PlanObject) -> Dict[str, Any]:
    """Serialize a PlanObject into a JSON-safe dictionary."""
    return {
        "metadata": {
            "plan_id": plan.metadata.plan_id,
            "domain": plan.metadata.domain,
            "created_at_utc": plan.metadata.created_at_utc,
            "tick_budget": plan.metadata.tick_budget,
        },
        "steps": [
            {
                "step_id": step.step_id,
                "description": step.description,
                "constraints": step.constraints,
            }
            for step in plan.steps
        ],
        "declared_permissions": list(plan.declared_permissions),
    }


def deserialize_plan(data: Dict[str, Any]) -> PlanObject:
    """Deserialize a JSON-safe dictionary into a PlanObject.
    Fails closed on malformed input.
    """
    try:
        metadata = PlanMetadata(
            plan_id=data["metadata"]["plan_id"],
            domain=data["metadata"]["domain"],
            created_at_utc=data["metadata"]["created_at_utc"],
            tick_budget=int(data["metadata"]["tick_budget"]),
        )

        steps: List[PlanStep] = [
            PlanStep(
                step_id=s["step_id"],
                description=s["description"],
                constraints=dict(s.get("constraints", {})),
            )
            for s in data.get("steps", [])
        ]

        permissions = list(data.get("declared_permissions", []))

        return PlanObject(
            metadata=metadata,
            steps=steps,
            declared_permissions=permissions,
        )
    except Exception as e:
        raise ValueError("Invalid serialized plan data") from e
