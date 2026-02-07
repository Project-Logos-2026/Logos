# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: logos_constructive_compile
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/Runtime_Spine/Logos_Constructive_Compile/logos_constructive_compile.py.
agent_binding: None
protocol_binding: Runtime_Spine
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/Runtime_Spine/Logos_Constructive_Compile/logos_constructive_compile.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Runtime Spine Logos Constructive Compile adapter.

Re-exports the governed constructive compile boundary.
"""

from LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT.Agent_Invocation.logos_constructive_compile import (
    ConstructiveCompileHalt,
    perform_constructive_compile,
)

__all__ = ["ConstructiveCompileHalt", "perform_constructive_compile"]
