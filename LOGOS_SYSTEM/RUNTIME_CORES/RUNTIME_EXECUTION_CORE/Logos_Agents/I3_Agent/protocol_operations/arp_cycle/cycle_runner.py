# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
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
module_name: cycle_runner
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
  source: System_Stack/Logos_Agents/I3_Agent/protocol_operations/arp_cycle/cycle_runner.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from typing import Any, Dict

from ..arp_runtime.task_intake import load_task
from ..arp_planner.baseline_planner import plan_task
from ..arp_planner.plan_evaluator import evaluate_plan_packet
from .policy import decide_policy


def run_arp_cycle(*, task: Dict[str, Any]) -> Dict[str, Any]:
    """
    One ARP cycle:
      - Validate/normalize task
      - Generate baseline plan packet
      - Optionally evaluate plan packet
      - Return JSON-serializable dict bundle
    """
    env = load_task(task=task)
    pol = decide_policy(task=env.raw)

    plan_pkt = plan_task(env=env)
    plan_dict = plan_pkt.to_dict() if hasattr(plan_pkt, "to_dict") else plan_pkt

    if pol.run_evaluation:
        eval_pkt = evaluate_plan_packet(plan_packet=plan_dict)
        eval_dict = eval_pkt.to_dict() if hasattr(eval_pkt, "to_dict") else eval_pkt
    else:
        eval_dict = {
            "task_id": env.task_id,
            "smp_id": env.smp_id,
            "status": "skipped",
            "scores": {},
            "issues": [],
            "summary": "Evaluation skipped by policy.",
            "provenance": {"evaluator": "none"},
        }

    return {
        "policy": {"priority": pol.priority, "run_evaluation": pol.run_evaluation, "reason": pol.reason},
        "plan": plan_dict,
        "evaluation": eval_dict,
    }
