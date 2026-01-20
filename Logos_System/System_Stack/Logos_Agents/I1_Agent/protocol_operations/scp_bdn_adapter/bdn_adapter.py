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
module_name: bdn_adapter
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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_bdn_adapter/bdn_adapter.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from typing import Protocol

from .bdn_types import BDNRequest, BDNResult


class IBDNAdapter(Protocol):
    """
    Contract for BDN integration.
    Real implementations may call external/SCP engines, but SCP should depend only on this interface.
    """
    def analyze(self, req: BDNRequest) -> BDNResult:
        ...


class StubBDNAdapter:
    """
    Safe default: indicates BDN is not wired yet.
    """
    def analyze(self, req: BDNRequest) -> BDNResult:
        return BDNResult(
            available=False,
            summary="BDN adapter not configured; returning stub result.",
            stability_score=0.0,
            meta={"reason": "stub"},
        )
