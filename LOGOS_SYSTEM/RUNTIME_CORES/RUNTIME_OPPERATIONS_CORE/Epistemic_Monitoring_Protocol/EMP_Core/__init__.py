# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 2.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: __init__
runtime_layer: operations
role: Package initializer
responsibility: Establishes import boundaries and package identity for EMP_Core.
    Exports all EMP_Core modules for downstream consumption.
agent_binding: None
protocol_binding: Epistemic_Monitoring_Protocol
runtime_classification: package_init
boot_phase: E1
expected_imports: []
provides:
  - EMP_Coq_Bridge
  - EMP_Meta_Reasoner
  - EMP_Proof_Index
  - EMP_Template_Engine
  - EMP_Abstraction_Engine
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Import failures propagate. No silent suppression.
rewrite_provenance:
  source: EMP_NATIVE_COQ_PROOF_ENGINE_BLUEPRINT_AND_ROADMAP.md
  rewrite_phase: Phase_E1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

__all__ = [
    "EMP_Coq_Bridge",
    "EMP_Meta_Reasoner",
    "EMP_Proof_Index",
    "EMP_Template_Engine",
    "EMP_Abstraction_Engine",
]
