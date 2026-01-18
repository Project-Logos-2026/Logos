# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: packet_types
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
  source: System_Stack/Logos_Agents/I3_Agent/config/packet_types.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class InputReference:
    """A safe reference to input payload (hash + minimal metadata)."""
    input_hash: str
    preview: str = ""
    kind: str = "opaque"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_hash": self.input_hash,
            "preview": self.preview,
            "kind": self.kind,
        }


@dataclass(frozen=True)
class MediationSummary:
    """Minimal mediation summary for routing."""
    final_decision: str
    route_to: str
    violations: Optional[list] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "final_decision": self.final_decision,
            "route_to": self.route_to,
            "violations": self.violations or [],
        }
