# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Lem_Discharge
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/System_Entry_Point/Agent_Orchestration/Lem_Discharge.py.
agent_binding: None
protocol_binding: System_Entry_Point
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/System_Entry_Point/Agent_Orchestration/Lem_Discharge.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
System Entry Point LEM discharge adapter.

Provides a governed alias for LOGOS agent LEM discharge.
"""

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Core.Lem_Discharge import (
    LemDischargeHalt,
    discharge_lem,
)

__all__ = ["LemDischargeHalt", "discharge_lem"]
