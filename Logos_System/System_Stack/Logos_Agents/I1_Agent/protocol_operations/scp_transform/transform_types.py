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
module_name: transform_types
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
  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_transform/transform_types.py
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
class TransformStep:
    name: str
    applied: bool
    notes: str = ""
    delta: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class TransformOutcome:
    # Payload is treated as opaque; SCP should avoid emitting raw harmful content.
    payload: Any
    steps: List[TransformStep]
    score_vector: Dict[str, float] = field(default_factory=dict)
    status: str = "partial"  # ok | partial | blocked | error
    summary: str = ""
