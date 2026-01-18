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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_cycle/policy.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class SCPPolicyDecision:
    run_loop: bool
    reason: str


def decide_policy(*, smp: Dict[str, Any]) -> SCPPolicyDecision:
    """
    Minimal policy for whether SCP should run the stabilization loop.
    This is NOT moral/policy enforcement; it's a compute routing decision.
    """
    fd = str(smp.get("final_decision", "")).lower().strip()
    if fd in {"escalate", "quarantine"}:
        return SCPPolicyDecision(run_loop=True, reason=f"final_decision={fd}")
    analysis = smp.get("analysis")
    sev = 0.0
    if isinstance(analysis, dict):
        try:
            sev = float(analysis.get("severity_score", 0.0))
        except Exception:
            sev = 0.0
    if sev >= 0.85:
        return SCPPolicyDecision(run_loop=True, reason="severity>=0.85")
    return SCPPolicyDecision(run_loop=False, reason="No trigger for SCP loop.")
