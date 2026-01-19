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
module_name: trajectory_types
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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_analysis/trajectory_types.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class RiskSignal:
    name: str
    weight: float
    notes: str = ""

@dataclass(frozen=True)
class TrajectoryEstimate:
    """
    Non-tactical risk/trajectory estimate. This is NOT a prediction of specific acts.
    It is a conservative outcome-risk summary used to decide routing and escalation.
    """
    overall_risk: float  # 0..1
    confidence: float    # 0..1 (confidence in the estimate, not in any act)
    category: str        # "low" | "medium" | "high" | "critical"
    signals: List[RiskSignal] = field(default_factory=list)
    recommended_route: str = "LOGOS"
    recommended_action: str = "review"  # review | escalate | quarantine | monitor
    rationale: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_risk": self.overall_risk,
            "confidence": self.confidence,
            "category": self.category,
            "signals": [s.__dict__ for s in self.signals],
            "recommended_route": self.recommended_route,
            "recommended_action": self.recommended_action,
            "rationale": self.rationale,
            "meta": self.meta,
        }
