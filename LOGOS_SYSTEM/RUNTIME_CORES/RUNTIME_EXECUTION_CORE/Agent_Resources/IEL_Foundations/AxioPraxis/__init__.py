# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: __init__
runtime_layer: inferred
role: Package initializer
responsibility: Defines package boundaries for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Agent_Resources/IEL_Foundations/AxioPraxis.
agent_binding: None
protocol_binding: None
runtime_classification: package_initializer
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Agent_Resources/IEL_Foundations/AxioPraxis/__init__.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Axiopraxis Domain: Axioms and Foundations Praxis

This domain focuses on the praxis of foundational systems, including:
- Axiom systems and their properties
- Logical foundations
- Consistency and completeness
- Meta-mathematical frameworks
"""

from .axiom_systems import AxiomSystem
from .foundational_logic import FoundationalLogic
from .consistency_checker import ConsistencyChecker

__all__ = ['AxiomSystem', 'FoundationalLogic', 'ConsistencyChecker']