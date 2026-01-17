# MODULE_META:
#   module_id: SCX-005
#   layer: SEMANTIC_CONTEXT
#   role: TRINITARIAN_OPTIMIZATION_CONTEXT
#   phase_origin: PHASE_CONTEXTUAL_EMBEDDING
#   description: Semantic context module defined in Trinitarian_Optimization_Context.py.
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
Semantic Context: Trinitarian_Optimization_Context

NOTE:
- Headers intentionally deferred.
- Metadata is authoritative in SEMANTIC_CONTEXTS_CATALOG.json.
"""

from PYTHON_MODULES.SEMANTIC_AXIOMS.Trinitarian_Alignment_Core import score_candidates
from PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints import enforce_invariants
from PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate import validate_capabilities


def run(context: dict) -> dict:
    """
    Trinitarian optimization semantic context.
    Scores and selects candidates under triadic governance constraints.
    """
    enforce_invariants(context)
    validate_capabilities(context)
    return score_candidates(context)
