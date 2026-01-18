# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: types
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
  source: System_Stack/Logos_Protocol/Activation_Sequencer/Agent_Integration/types.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class LogosBundle:
    """
    Aggregate output from Logos orchestration.
    - smp: Structured Meaning Packet from I2 (input to this bundle)
    - scp_result: append-only packet from I1 (optional)
    - arp_result: plan/eval bundle from I3 (optional)
    """

    smp: Dict[str, Any]
    scp_result: Optional[Dict[str, Any]] = None
    arp_result: Optional[Dict[str, Any]] = None
    route_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "smp": self.smp,
            "scp_result": self.scp_result,
            "arp_result": self.arp_result,
            "route_summary": self.route_summary,
        }
