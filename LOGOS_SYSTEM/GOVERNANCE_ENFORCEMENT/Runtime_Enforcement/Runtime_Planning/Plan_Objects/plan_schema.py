# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: plan_schema
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Plan_Objects/plan_schema.py.
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
  source: LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Planning/Plan_Objects/plan_schema.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


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
