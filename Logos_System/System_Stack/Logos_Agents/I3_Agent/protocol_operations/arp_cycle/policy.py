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
module_name: policy
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
  source: System_Stack/Logos_Agents/I3_Agent/protocol_operations/arp_cycle/policy.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ARPPolicyDecision:
    priority: str  # normal | high
    run_evaluation: bool
    reason: str


def decide_policy(*, task: Dict[str, Any]) -> ARPPolicyDecision:
    """
    Minimal metadata-only policy:
    - If task.kind is safety/alignment or explicit priority high -> high priority
    - Default run_evaluation=True unless disabled explicitly
    """
    kind = str(task.get("kind", "generic")).lower().strip()
    requested_priority = str(task.get("priority", "")).lower().strip()

    priority = "high" if requested_priority == "high" or kind in {"safety", "alignment"} else "normal"

    run_eval = task.get("run_evaluation")
    if isinstance(run_eval, bool):
        return ARPPolicyDecision(priority=priority, run_evaluation=run_eval, reason="Explicit run_evaluation flag.")
    return ARPPolicyDecision(priority=priority, run_evaluation=True, reason="Default evaluation enabled.")
