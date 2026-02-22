# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Topology_Context
runtime_layer: rge_integration
role: Topology state carrier
responsibility: Frozen dataclass carrying the active RGE topology configuration
    into MSPC compilation. Provides reverse-lookup helper for axis-to-protocol
    resolution. No side effects. No runtime dependencies beyond stdlib.
agent_binding: None
protocol_binding: Multi_Process_Signal_Compiler
runtime_classification: data_carrier
boot_phase: Phase-6-Integration
expected_imports: [dataclasses, typing]
provides: [TopologyContext]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Frozen dataclass. Construction-time validation only."
rewrite_provenance:
  source: Phase_6_MSPC_Topology_Enforcement
  rewrite_phase: Phase_6
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class TopologyContext:

    config_id: str
    rotation_index: int
    agent_assignments: Dict[str, str]

    def protocol_for_axis(self, axis: str) -> Optional[str]:
        for agent, assigned_axis in self.agent_assignments.items():
            if assigned_axis == axis:
                return agent
        return None

    def axis_for_protocol(self, protocol: str) -> Optional[str]:
        return self.agent_assignments.get(protocol)
