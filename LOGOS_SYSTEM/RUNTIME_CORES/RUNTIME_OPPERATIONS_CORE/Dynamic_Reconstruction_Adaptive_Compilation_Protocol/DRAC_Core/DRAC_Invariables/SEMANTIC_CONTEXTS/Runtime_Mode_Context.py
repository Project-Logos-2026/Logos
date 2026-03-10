# MODULE_META:
#   module_id: SCX-004
#   layer: SEMANTIC_CONTEXT
#   role: RUNTIME_MODE_CONTEXT
#   phase_origin: PHASE_CONTEXTUAL_EMBEDDING
#   description: Semantic context module defined in Runtime_Mode_Context.py.
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
Semantic Context: Runtime_Mode_Context

NOTE:
- Headers intentionally deferred.
- Metadata is authoritative in SEMANTIC_CONTEXTS_CATALOG.json.
"""

from logos.imports.drac_axioms import set_runtime_mode
from logos.imports.drac_axioms import enforce_invariants
from logos.imports.drac_axioms import validate_capabilities


def run(context: dict) -> dict:
    """
    Runtime mode semantic context.
    Controls execution behavior based on active runtime mode.
    """
    enforce_invariants(context)
    validate_capabilities(context)
    return set_runtime_mode(context)
