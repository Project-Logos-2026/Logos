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
module_name: bdn_types
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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_bdn_adapter/bdn_types.py
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
class BDNRequest:
    """
    Request for BDN analysis. Avoid raw unsafe content; use references/hashes when possible.
    """
    smp_id: str
    input_hash: str
    payload_ref: Any = None  # optional opaque handle (NOT required)
    selected_domains: List[str] = field(default_factory=list)
    hints: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class BDNResult:
    """
    Result of BDN analysis, intended for SCP findings.
    """
    available: bool
    summary: str
    stability_score: float = 0.0
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "available": self.available,
            "summary": self.summary,
            "stability_score": self.stability_score,
            "meta": self.meta,
        }
