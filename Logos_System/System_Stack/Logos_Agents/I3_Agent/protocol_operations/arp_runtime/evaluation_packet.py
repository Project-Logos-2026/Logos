# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: evaluation_packet
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
  source: System_Stack/Logos_Agents/I3_Agent/protocol_operations/arp_runtime/evaluation_packet.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass(frozen=True)
class EvaluationPacket:
    task_id: str
    created_at: float
    smp_id: Optional[str]
    status: str  # ok | partial | blocked
    scores: Dict[str, float] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    summary: str = ""
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "created_at": self.created_at,
            "smp_id": self.smp_id,
            "status": self.status,
            "scores": self.scores,
            "issues": self.issues,
            "summary": self.summary,
            "provenance": self.provenance,
        }


def emit_evaluation_packet(
    *,
    task_id: str,
    smp_id: Optional[str],
    status: str,
    scores: Optional[Dict[str, float]] = None,
    issues: Optional[List[str]] = None,
    summary: str = "",
    provenance: Optional[Dict[str, Any]] = None,
) -> EvaluationPacket:
    return EvaluationPacket(
        task_id=task_id,
        created_at=time.time(),
        smp_id=smp_id,
        status=status,
        scores=scores or {},
        issues=issues or [],
        summary=summary,
        provenance=provenance or {},
    )
