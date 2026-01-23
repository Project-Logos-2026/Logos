
'''
MODULE: plan_schema
PHASE: Phase-P (IMPLEMENTATION_NON_EXECUTABLE)
AUTHORITY: Protopraxic Logic (PXL)

PURPOSE:
Defines inert planning plan object schemas.
This module contains NO execution logic, NO scheduling,
NO autonomy, and NO runtime activation pathways.

GOVERNANCE:
- Importing this module must not cause side effects.
- Any misuse must fail closed.
- This file is schema-only.
'''

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class PlanMetadata:
    plan_id: str
    domain: str
    created_at_utc: str
    tick_budget: int


@dataclass(frozen=True)
class PlanStep:
    step_id: str
    description: str
    constraints: Dict[str, Any]


@dataclass(frozen=True)
class PlanObject:
    metadata: PlanMetadata
    steps: List[PlanStep]
    declared_permissions: List[str]

    def __post_init__(self):
        # Fail closed if implicit permissions exist
        if any(p.strip() == "" for p in self.declared_permissions):
            raise ValueError("Invalid permission declaration")
