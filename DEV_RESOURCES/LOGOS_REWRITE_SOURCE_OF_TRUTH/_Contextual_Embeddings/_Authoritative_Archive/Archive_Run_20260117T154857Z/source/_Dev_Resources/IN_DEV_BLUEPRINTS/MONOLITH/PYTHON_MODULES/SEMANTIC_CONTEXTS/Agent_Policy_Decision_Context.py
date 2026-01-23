# MODULE_META:
#   module_id: SCX-001
#   layer: SEMANTIC_CONTEXT
#   role: AGENT_POLICY_DECISION_CONTEXT
#   phase_origin: PHASE_CONTEXTUAL_EMBEDDING
#   description: Semantic context module defined in Agent_Policy_Decision_Context.py.
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
Semantic Context: Agent_Policy_Decision_Context

NOTE:
- Headers intentionally deferred.
- Metadata is authoritative in SEMANTIC_CONTEXTS_CATALOG.json.
"""

from PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints import enforce_invariants
from PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate import validate_capabilities


def run(context: dict) -> dict:
    """
    Agent policy decision semantic context.
    Determines whether an agent should act, pause, or stabilize.
    """
    enforce_invariants(context)
    validate_capabilities(context)
    return context
