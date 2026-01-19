from __future__ import annotations
# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: plan_evaluator
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Logos_Agents/I3_Agent/protocol_operations/arp_planner/plan_evaluator.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from typing import Any, Dict, List

from ..arp_runtime.evaluation_packet import emit_evaluation_packet


def evaluate_plan_packet(*, plan_packet: Dict[str, Any]) -> Any:
    """
    Minimal evaluator:
    - checks plan exists and has steps
    - checks constraints list exists (can be empty)
    - emits a score for completeness
    """
    task_id = str(plan_packet.get("task_id", "")).strip()
    smp_id = plan_packet.get("smp_id")
    plan = plan_packet.get("plan")
    constraints = plan_packet.get("constraints")

    issues: List[str] = []
    score = 1.0

    if not task_id:
        issues.append("missing_task_id")
        score -= 0.4

    if not isinstance(plan, list) or len(plan) == 0:
        issues.append("missing_or_empty_plan")
        score -= 0.5

    if constraints is not None and not isinstance(constraints, list):
        issues.append("constraints_not_list")
        score -= 0.2

    score = max(0.0, min(1.0, score))
    status = "ok" if score >= 0.8 else ("partial" if score >= 0.5 else "blocked")

    summary = "Plan passes baseline checks." if status == "ok" else "Plan has baseline issues; review recommended."

    return emit_evaluation_packet(
        task_id=task_id or "unknown",
        smp_id=smp_id if isinstance(smp_id, str) else None,
        status=status,
        scores={"completeness": round(score, 2)},
        issues=issues,
        summary=summary,
        provenance={"evaluator": "plan_evaluator.v1"},
    )
