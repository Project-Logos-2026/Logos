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
module_name: predict_integration
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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_predict/predict_integration.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from typing import Any, Dict, Tuple

from .risk_estimator import estimate_trajectory


def attach_trajectory_estimate(
    *,
    smp: Dict[str, Any],
    findings: Dict[str, Any],
    recommended_next: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Attach non-tactical trajectory/risk estimate into findings and recommended_next.

    Returns updated (findings, recommended_next).
    """
    findings = dict(findings or {})
    recommended_next = dict(recommended_next or {})

    est = estimate_trajectory(smp=smp)
    findings["trajectory_estimate"] = est.to_dict()

    recommended_next.setdefault("route_to", est.recommended_route)
    recommended_next.setdefault("recommended_action", est.recommended_action)

    return findings, recommended_next
