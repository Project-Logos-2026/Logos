# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: scp_nexus_orchestrator
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
  source: System_Stack/Synthetic_Cognition_Protocol/SCP_Nexus/scp_nexus_orchestrator.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

# === Canonical SCP Nexus Façade ===
# This file intentionally re-exports the public SCP execution surface.
# No execution logic lives here.

from Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.predictors.fractal_nexus import FractalNexus

__all__ = [
    "FractalNexus",
]
