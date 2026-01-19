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
module_name: mvs_adapter
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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_mvs_adapter/mvs_adapter.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from typing import Protocol

from .mvs_types import MVSRequest, MVSResult


class IMVSAdapter(Protocol):
    """
    Contract for MVS integration.
    Real implementations may call external/ARP engines, but SCP should depend only on this interface.
    """
    def analyze(self, req: MVSRequest) -> MVSResult:
        ...


class StubMVSAdapter:
    """
    Safe default: indicates MVS is not wired yet.
    """
    def analyze(self, req: MVSRequest) -> MVSResult:
        return MVSResult(
            available=False,
            summary="MVS adapter not configured; returning stub result.",
            coherence_score=0.0,
            meta={"reason": "stub"},
        )
