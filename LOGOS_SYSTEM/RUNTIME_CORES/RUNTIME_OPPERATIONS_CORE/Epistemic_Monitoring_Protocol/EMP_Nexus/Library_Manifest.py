# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Library_Manifest
runtime_layer: operations
role: Runtime module
responsibility: Declares allowed external libraries for EMP operations.
    Read-only registry. No execution logic.
agent_binding: None
protocol_binding: Epistemic_Monitoring_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides:
  - ALLOWED_LIBRARIES
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Registry is static and read-only.
rewrite_provenance:
  source: Epistemic_Monitoring_Protocol/EMP_Nexus/Library_Manifest.py
  rewrite_phase: Phase_E1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

ALLOWED_LIBRARIES = {
    "COQ": {"purpose": "Formal proof checking"},
    "LEAN4": {"purpose": "Secondary proof assistant"},
    "Z3": {"purpose": "Constraint solving"},
    "NETWORKX": {"purpose": "Proof graph analysis"},
    "SYMPY": {"purpose": "Symbolic math"},
    "CUSTOM_PXL_KERNEL": {"purpose": "Canonical logic validation"},
}
