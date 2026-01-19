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
module_name: work_order
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
  source: System_Stack/Logos_Agents/I3_Agent/protocol_operations/arp_runtime/work_order.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from I3_Agent.protocol_operations.arp_runtime.task_intake import TaskEnvelope


@dataclass(frozen=True)
class ARPWorkOrder:
    """ARP work order derived from a TaskEnvelope (Advanced Reasoning Protocol).

    Keeps ARP-bound intent separate from SCP; avoids execution and stays append-only.
    """

    task_id: str
    smp_id: Optional[str]
    priority: str
    objectives: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    hints: Dict[str, Any] = field(default_factory=dict)


def build_work_order(*, envelope: TaskEnvelope) -> ARPWorkOrder:
    """Convert TaskEnvelope -> ARPWorkOrder with light, deterministic mapping."""
    kind = (envelope.kind or "").lower().strip()
    priority = "high" if kind in {"safety", "alignment", "escalation"} else "normal"

    constraints: List[str] = []
    raw_constraints = envelope.raw.get("constraints") if isinstance(envelope.raw, dict) else None
    if isinstance(raw_constraints, list):
        constraints = [str(item) for item in raw_constraints]

    objectives = [
        "normalize_task",
        "derive_baseline_plan",
        "evaluate_plan_if_requested",
    ]

    hints: Dict[str, Any] = {
        "origin": envelope.origin,
        "kind": envelope.kind,
        "has_payload": bool(envelope.raw),
    }

    directives = envelope.raw.get("directives") if isinstance(envelope.raw, dict) else None
    if isinstance(directives, dict):
        hints["directives"] = directives
        route_to = directives.get("route_to")
        if isinstance(route_to, str) and route_to.strip():
            hints["route_to"] = route_to.strip()

    policy = envelope.raw.get("policy") if isinstance(envelope.raw, dict) else None
    if isinstance(policy, dict):
        run_eval = policy.get("run_evaluation")
        if isinstance(run_eval, bool):
            hints["run_evaluation"] = run_eval

    return ARPWorkOrder(
        task_id=envelope.task_id,
        smp_id=envelope.smp_id,
        priority=priority,
        objectives=objectives,
        constraints=constraints,
        hints=hints,
    )
