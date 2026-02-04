# MODULE_META:
#   module_id: SCX-002
#   layer: SEMANTIC_CONTEXT
#   role: BOOTSTRAP_RUNTIME_CONTEXT
#   phase_origin: PHASE_CONTEXTUAL_EMBEDDING
#   description: Semantic context module defined in Bootstrap_Runtime_Context.py.
#   contracts: []
#   allowed_imports: [SEMANTIC_AXIOMS]
#   prohibited_behaviors: [IO, NETWORK, TIME, RANDOM]
#   entrypoints: [run]
#   callable_surface: INTERNAL
#   state_mutation: CONTEXT_ONLY
#   runtime_spine_binding: NONE
#   depends_on_contexts: []
#   invoked_by: [Canonical_System_Bootstrap_Pipeline]

"""
Semantic Context: Bootstrap_Runtime_Context

NOTE:
- Headers intentionally deferred.
- Metadata is authoritative in SEMANTIC_CONTEXTS_CATALOG.json.
"""

from PYTHON_MODULES.SEMANTIC_AXIOMS.Runtime_Context_Initializer import initialize_runtime_context
from PYTHON_MODULES.SEMANTIC_AXIOMS.Runtime_Mode_Controller import set_runtime_mode
from PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints import enforce_invariants
from PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate import validate_capabilities


def run(context: dict) -> dict:
    """
    Bootstrap semantic context.
    Prepares runtime state prior to active interaction.
    """
    enforce_invariants(context)
    validate_capabilities(context)
    initialized = initialize_runtime_context(context)
    return set_runtime_mode(initialized)
