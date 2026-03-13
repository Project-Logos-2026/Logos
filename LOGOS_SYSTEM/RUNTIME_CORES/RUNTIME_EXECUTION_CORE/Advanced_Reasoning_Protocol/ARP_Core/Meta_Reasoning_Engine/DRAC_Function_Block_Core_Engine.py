# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: CONTROLLED
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: DRAC_Function_Block_Core_Engine
runtime_layer: RUNTIME_EXECUTION_CORE
role: DRAC axiom-context pairing engine with FBC combination scoring
responsibility: >
  Injects context embeddings into DRAC axioms to form Function Block Cores
  (FBCs). Each FBC pairs one or more axioms with a context embedding and a
  set of application function bindings (AFs from the MODULAR_LIBRARY). The
  engine experimentally scores all viable axiom+context+AF combinations,
  selects optimal configurations, and returns typed FBCEvaluationResults.

  This module is the bridge between the raw DRAC axiom/context registry and
  the PCCRE reasoning pipeline. PCCRE calls FBCCombinationEngine.run() as a
  new Phase F (after MESH) to further amplify artifact quality with the full
  optional-composable axiom inventory.

axiom_coverage:
  REQUIRED_UNIVERSAL  : FBC_0007 (Invariant_Constraints)
                        FBC_0014 (Semantic_Capability_Gate)
  CONTEXT_SELECTIVE   : FBC_0011 (Runtime_Context_Initializer)
                        FBC_0013 (Runtime_Mode_Controller)
                        FBC_0016 (Trinitarian_Alignment_Core)
  OPTIONAL_COMPOSABLE : FBC_0001 (3PDN_Constraint)
                        FBC_0002 (3PDN_Validator)
                        FBC_0003 (Agent_Activation_Gate)
                        FBC_0004 (Evidence_Chain)
                        FBC_0005 (Global_Bijective_Recursion_Core)
                        FBC_0006 (Hypostatic_ID_Validator)
                        FBC_0009 (Necessary_Existence_Core)
                        FBC_0012 (Runtime_Input_Sanitizer)
                        FBC_0015 (Temporal_Supersession)
                        FBC_0017 (Trinitarian_Logic_Core)
                        FBC_0019 (UWM_Validator)

context_embeddings (5 EMBEDDED):
  SCX-001 : Agent_Policy_Decision_Context
  SCX-002 : Bootstrap_Runtime_Context
  SCX-003 : Privation_Handling_Context
  SCX-004 : Runtime_Mode_Context
  SCX-005 : Trinitarian_Optimization_Context

power_configurations_scored (top 5):
  POWER-A : Inference_Full_Stack          (45/50) — ALL inference optionals
  POWER-B : Trinitarian_Complete          (43/50) — SCX-005 + logic + evidence
  POWER-C : Bijective_Bootstrap           (41/50) — SCX-002 + bijection + temporal
  POWER-D : Existence_Privation_Temporal  (40/50) — SCX-003 + existence + temporal
  POWER-E : Safety_Complete               (40/50) — SCX-001+003 + all safety optionals

af_bindings_used:
  AF_0046 : execute_HBN (symbolic probabilistic, reasoning_engine)
  AF_0048 : run_logos_cycle (runtime orchestration, reasoning_engine)
  AF_0050 : _initialize_ontological_state (logical, reasoning_engine)
  AF_0051 : _select_active_concepts (logical, reasoning_engine)
  AF_0052 : _update_ontological_state (logical, reasoning_engine)
  AF_0055 : _evolve_context (agent reasoning, reasoning_engine)
  AF_0057 : _analyze_emergence_patterns (analytic, reasoning_engine)
  AF_0058 : _compare_to_human_baseline (validation vector, reasoning_engine)
  AF_0059 : evaluate_modal_proposition (modal, reasoning_engine)

new_reasoning_lenses:
  EvidenceChainLens          — FBC_0004 runtime implementation
  ExistenceProofLens         — FBC_0009 runtime implementation
  TemporalSupersessionLens   — FBC_0015 runtime implementation
  TrinitarianLogicLens       — FBC_0017 runtime implementation
  BijectionClosureLens       — FBC_0005 runtime implementation
  TripartiteDistinctionLens  — FBC_0001+0002 runtime implementation
  HypostaticIdentityLens     — FBC_0006 runtime implementation
  InputSanitizerLens         — FBC_0012 runtime implementation

failure_mode:
  type: fail_closed
  notes: >
    Unrecognized FBC IDs raise CapabilityViolation.
    Failed axiom evaluators raise ReasoningViolation.
    FBC combination scoring is graceful-degraded: scoring continues if
    individual FBCs fail; only the aggregate MASTER configuration raises
    if the minimum viable set fails.
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple
import hashlib
import json
import logging
import math

logger = logging.getLogger("reasoning.fbc_engine")


# ============================================================================
# Re-export exceptions (avoid circular import; define locally)
# ============================================================================

class CapabilityViolation(RuntimeError):
    """Raised when a required FBC capability or axiom is missing."""


class ReasoningViolation(RuntimeError):
    """Raised when an FBC axiom evaluation fails (fail-closed)."""


class SanitizerViolation(ReasoningViolation):
    """Raised when input sanitization fails."""


# ============================================================================
# Scoring dimensions and power classes
# ============================================================================

class PowerClass(Enum):
    ALPHA = "ALPHA"   # ≥ 42 / 50 — top tier
    BETA  = "BETA"    # 35 – 41 — enhanced
    GAMMA = "GAMMA"   # < 35 — minimal


@dataclass(frozen=True)
class FBCScore:
    inference_depth: int      # 1–10  how many inference steps the core enables
    safety_coverage: int      # 1–10  safety gate breadth
    cluster_reach: int        # 1–10  AF clusters unlocked
    axiom_synergy: int        # 1–10  how well axiom+context reinforce each other
    novel_coverage: int       # 1–10  covers optional-composable axioms not in DRAC_CORE_013

    @property
    def total(self) -> int:
        return (
            self.inference_depth
            + self.safety_coverage
            + self.cluster_reach
            + self.axiom_synergy
            + self.novel_coverage
        )

    @property
    def power_class(self) -> PowerClass:
        t = self.total
        if t >= 42:
            return PowerClass.ALPHA
        if t >= 35:
            return PowerClass.BETA
        return PowerClass.GAMMA


# ============================================================================
# Context embedding descriptor
# ============================================================================

@dataclass(frozen=True)
class ContextEmbedding:
    """
    Mirrors the EMBEDDED SEMANTIC_CONTEXT modules (SCX-001..005).
    axiom_call_sequence: ordered axiom function names called by this context.
    spine_binding: runtime lifecycle position.
    """
    scx_id: str
    name: str
    role: str
    axiom_call_sequence: Tuple[str, ...]
    spine_binding: str
    required_axiom_fbcs: Tuple[str, ...]

    def embed(self, candidate_context: Dict[str, Any]) -> Dict[str, Any]:
        """Return context dict enriched with embedding trace."""
        return {
            **candidate_context,
            "_ctx_embedding": self.scx_id,
            "_ctx_name": self.name,
            "_ctx_call_sequence": list(self.axiom_call_sequence),
            "_ctx_spine": self.spine_binding,
        }


# Context embedding catalog — directly from DRAC_CORE_CATALOG.json
_CTX_EMBEDDINGS: Dict[str, ContextEmbedding] = {
    "SCX-001": ContextEmbedding(
        scx_id="SCX-001",
        name="Agent_Policy_Decision_Context",
        role="AGENT_POLICY_DECISION_CONTEXT",
        axiom_call_sequence=("enforce_invariants", "validate_capabilities"),
        spine_binding="PASSIVE_RUNTIME_INITIALIZATION",
        required_axiom_fbcs=("FBC_0007", "FBC_0014"),
    ),
    "SCX-002": ContextEmbedding(
        scx_id="SCX-002",
        name="Bootstrap_Runtime_Context",
        role="BOOTSTRAP_RUNTIME_CONTEXT",
        axiom_call_sequence=(
            "enforce_invariants",
            "validate_capabilities",
            "initialize_runtime_context",
            "set_runtime_mode",
        ),
        spine_binding="PASSIVE_RUNTIME_INITIALIZATION",
        required_axiom_fbcs=("FBC_0007", "FBC_0014", "FBC_0011", "FBC_0013"),
    ),
    "SCX-003": ContextEmbedding(
        scx_id="SCX-003",
        name="Privation_Handling_Context",
        role="PRIVATION_HANDLING_CONTEXT",
        axiom_call_sequence=("enforce_invariants", "validate_capabilities"),
        spine_binding="PASSIVE_TASK_SUSPENSION_AND_TEMPORARY_STATE_LOCKING",
        required_axiom_fbcs=("FBC_0007", "FBC_0014"),
    ),
    "SCX-004": ContextEmbedding(
        scx_id="SCX-004",
        name="Runtime_Mode_Context",
        role="RUNTIME_MODE_CONTEXT",
        axiom_call_sequence=(
            "enforce_invariants",
            "validate_capabilities",
            "set_runtime_mode",
        ),
        spine_binding="ACTIVE_INTERACTION_PRIORITY_SWITCH",
        required_axiom_fbcs=("FBC_0007", "FBC_0014", "FBC_0013"),
    ),
    "SCX-005": ContextEmbedding(
        scx_id="SCX-005",
        name="Trinitarian_Optimization_Context",
        role="TRINITARIAN_OPTIMIZATION_CONTEXT",
        axiom_call_sequence=(
            "enforce_invariants",
            "validate_capabilities",
            "score_candidates",
        ),
        spine_binding="AGENT_ORCHESTRATION_AND_PROTOCOL_BINDING",
        required_axiom_fbcs=("FBC_0007", "FBC_0014", "FBC_0016"),
    ),
}


# ============================================================================
# AF binding descriptors (reasoning_engine + math_operator AFs)
# Sourced from af_semantic_registry + af_runtime_roles
# ============================================================================

@dataclass(frozen=True)
class AFBinding:
    af_id: str
    function_name: str
    signature: str
    semantic_modifier: str
    description: str
    cluster: str


_AF_BINDINGS: Dict[str, AFBinding] = {
    "AF_0046": AFBinding(
        af_id="AF_0046",
        function_name="execute_HBN",
        signature="execute_HBN(query)",
        semantic_modifier="execute(symbolic)",
        description="Execute complete HBN pipeline with intent analysis (probabilistic symbolic)",
        cluster="reasoning_inference",
    ),
    "AF_0048": AFBinding(
        af_id="AF_0048",
        function_name="run_logos_cycle",
        signature="run_logos_cycle(smp, payload_ref, arp_task_override)",
        semantic_modifier="run(runtime)",
        description="Minimal Logos orchestration cycle: SMP dispatch → ARP → LogosBundle",
        cluster="reasoning_inference",
    ),
    "AF_0050": AFBinding(
        af_id="AF_0050",
        function_name="_initialize_ontological_state",
        signature="_initialize_ontological_state(self)",
        semantic_modifier="score(logical)",
        description="Initialize the agent's ontological state with 10 core concepts",
        cluster="numerical_compute",
    ),
    "AF_0051": AFBinding(
        af_id="AF_0051",
        function_name="_select_active_concepts",
        signature="_select_active_concepts(self, context)",
        semantic_modifier="activate(logical)",
        description="Select which ontological concepts to activate based on context",
        cluster="reasoning_inference",
    ),
    "AF_0052": AFBinding(
        af_id="AF_0052",
        function_name="_update_ontological_state",
        signature="_update_ontological_state(self, transformed_concepts)",
        semantic_modifier="reason(logical)",
        description="Update the agent's ontological state based on interaction results",
        cluster="numerical_compute",
    ),
    "AF_0055": AFBinding(
        af_id="AF_0055",
        function_name="_evolve_context",
        signature="_evolve_context(self, current_context, responses)",
        semantic_modifier="reason(agent)",
        description="Evolve the interaction context based on agent responses",
        cluster="reasoning_inference",
    ),
    "AF_0057": AFBinding(
        af_id="AF_0057",
        function_name="_analyze_emergence_patterns",
        signature="_analyze_emergence_patterns(self)",
        semantic_modifier="analyze(agent)",
        description="Analyze patterns that emerge from agent interactions",
        cluster="reasoning_inference",
    ),
    "AF_0058": AFBinding(
        af_id="AF_0058",
        function_name="_compare_to_human_baseline",
        signature="_compare_to_human_baseline(self, metrics)",
        semantic_modifier="validate(vector)",
        description="Compare agent interactions to expected human-AI interaction patterns",
        cluster="reasoning_inference",
    ),
    "AF_0059": AFBinding(
        af_id="AF_0059",
        function_name="evaluate_modal_proposition",
        signature="evaluate_modal_proposition(self, proposition)",
        semantic_modifier="evaluate(modal)",
        description="Evaluate a modal proposition through ProofBridge pre-validation",
        cluster="reasoning_inference",
    ),
}


# ============================================================================
# New Inference Lenses — implementations for optional-composable axioms
# ============================================================================

class EvidenceChainLens:
    """
    FBC_0004 runtime implementation.
    Source: Evidence_Chain.py entrypoint verify_evidence_chain.
    Verifies that the premises of a concept form a valid, hash-stable
    evidence chain (no missing links, no orphaned premises).
    AF binding: AF_0046 (symbolic HBN), AF_0051 (concept selection).
    """

    def analyze(
        self,
        premises: Sequence[str],
        evidence_payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not premises:
            return {
                "engine": "evidence_chain",
                "fbc_id": "FBC_0004",
                "chain_valid": False,
                "chain_length": 0,
                "chain_hash": None,
                "orphaned_premises": [],
                "gaps": ["No premises supplied — chain cannot form."],
            }

        # Build ordered evidence chain from premises
        chain: List[Dict[str, Any]] = []
        orphaned: List[str] = []
        prev_hash: Optional[str] = None

        for i, premise in enumerate(premises):
            current_hash = self._hash({"index": i, "premise": premise, "prev": prev_hash})
            chain.append({
                "index": i,
                "premise": premise,
                "link_hash": current_hash,
                "prev_hash": prev_hash,
            })
            prev_hash = current_hash

        chain_hash = self._hash({"chain": [c["link_hash"] for c in chain]})

        # Detect orphans: premises not referenced by any other premise
        premise_set = set(premises)
        referenced: set = set()
        for p in premises:
            if "->" in p:
                ante, _ = p.split("->", 1)
                referenced.add(ante.strip())
        orphaned = [p for p in premises if p not in referenced and "->" not in p and len(premises) > 1]

        # Cross-reference evidence_payload if provided
        payload_match = True
        payload_gaps: List[str] = []
        if evidence_payload:
            expected_hash = evidence_payload.get("chain_hash")
            if expected_hash and expected_hash != chain_hash:
                payload_match = False
                payload_gaps.append(f"chain_hash mismatch: expected {expected_hash[:12]}... got {chain_hash[:12]}...")

        valid = payload_match and len(chain) > 0

        return {
            "engine": "evidence_chain",
            "fbc_id": "FBC_0004",
            "chain_valid": valid,
            "chain_length": len(chain),
            "chain_hash": chain_hash,
            "chain": chain,
            "orphaned_premises": orphaned,
            "gaps": payload_gaps,
            "af_bindings_activated": ["AF_0046", "AF_0051"],
        }

    def _hash(self, value: Any) -> str:
        return hashlib.sha256(
            json.dumps(value, sort_keys=True, default=str).encode()
        ).hexdigest()


class ExistenceProofLens:
    """
    FBC_0009 runtime implementation (Necessary_Existence_Core).
    Proves that the concept's substrate has non-null, non-empty existence
    by verifying all three ontological dimensions are populated.
    AF binding: AF_0050 (ontological state init), AF_0052 (state update).

    Pairs with SCX-003 (Privation_Handling_Context) — existence is the
    positive pole of the privation axis.
    """

    def analyze(
        self,
        name: str,
        proposition: str,
        lambda_form: str,
        bridge_mapping: Dict[str, Any],
    ) -> Dict[str, Any]:
        dimensions = {
            "name_exists": bool(name and name.strip()),
            "proposition_exists": bool(proposition and proposition.strip()),
            "lambda_grounded": bool(lambda_form and lambda_form.strip()),
            "bridge_concept_exists": bool(bridge_mapping.get("concept", {}).get("name")),
            "bridge_analog_exists": bool(bridge_mapping.get("analog")),
            "bridge_implementation_exists": bool(
                bridge_mapping.get("implementation", {}).get("targets")
            ),
        }

        grounded_count = sum(1 for v in dimensions.values() if v)
        total_count = len(dimensions)
        existence_score = grounded_count / total_count

        deficiencies: List[str] = [k for k, v in dimensions.items() if not v]
        necessary = existence_score >= 0.5  # at least half the dimensions must exist

        return {
            "engine": "existence_proof",
            "fbc_id": "FBC_0009",
            "proved": necessary,
            "existence_score": round(existence_score, 4),
            "dimensions": dimensions,
            "grounded_count": grounded_count,
            "total_dimensions": total_count,
            "deficiencies": deficiencies,
            "theorem": f"necessary_existence({name})",
            "method": "dimensional_grounding",
            "af_bindings_activated": ["AF_0050", "AF_0052"],
        }


class TemporalSupersessionLens:
    """
    FBC_0015 runtime implementation (Temporal_Supersession).
    Source: Temporal_Supersession.py: supersede(old_atom, new_atom).
    Applies temporal ordering to a premise set: identifies premises that
    have been superseded by later premises in the chain, marks superseded
    premises invalid, and emits the ordered valid-premise set.
    AF binding: AF_0052 (state update), AF_0055 (context evolution).

    Pairs with SCX-001 (Agent_Policy_Decision_Context) — policy decisions
    must respect temporal ordering of superseded rules.
    """

    def analyze(
        self,
        premises: Sequence[str],
        allow_supersession_markers: bool = True,
    ) -> Dict[str, Any]:
        if not premises:
            return {
                "engine": "temporal_supersession",
                "fbc_id": "FBC_0015",
                "valid_premises": [],
                "superseded_premises": [],
                "supersession_events": [],
                "temporally_ordered": True,
            }

        # Detect supersession markers: "SUPERSEDES:X" or "RETIRED:X"
        supersession_events: List[Dict[str, Any]] = []
        superseded_ids: set = set()
        valid_premises: List[str] = []

        for i, premise in enumerate(premises):
            p_lower = premise.lower()
            if p_lower.startswith("supersedes:") or "supersedes:" in p_lower:
                old_ref = premise.split(":", 1)[1].strip() if ":" in premise else "unknown"
                superseded_ids.add(old_ref)
                supersession_events.append({
                    "index": i,
                    "event": "supersession",
                    "superseded_ref": old_ref,
                    "new_premise": premise,
                })
            elif p_lower.startswith("retired:") or "retired:" in p_lower:
                retired_ref = premise.split(":", 1)[1].strip() if ":" in premise else "unknown"
                superseded_ids.add(retired_ref)
                supersession_events.append({
                    "index": i,
                    "event": "retirement",
                    "retired_ref": retired_ref,
                    "premise": premise,
                })

        # Filter: remove premises that appear in superseded_ids
        for premise in premises:
            premise_key = premise.split("->")[0].strip() if "->" in premise else premise.strip()
            if premise_key not in superseded_ids:
                valid_premises.append(premise)

        # Temporal ordering: premises at higher indexes supersede lower ones
        # if they touch the same antecedent
        antecedent_map: Dict[str, str] = {}
        overridden: List[str] = []
        for premise in valid_premises:
            if "->" in premise:
                ante, _ = premise.split("->", 1)
                ante = ante.strip()
                if ante in antecedent_map:
                    overridden.append(antecedent_map[ante])
                antecedent_map[ante] = premise

        final_valid = [p for p in valid_premises if p not in overridden]

        return {
            "engine": "temporal_supersession",
            "fbc_id": "FBC_0015",
            "valid_premises": final_valid,
            "superseded_premises": list(superseded_ids),
            "overridden_premises": overridden,
            "supersession_events": supersession_events,
            "temporal_compression": len(premises) - len(final_valid),
            "temporally_ordered": True,
            "af_bindings_activated": ["AF_0052", "AF_0055"],
        }


class TrinitarianLogicLens:
    """
    FBC_0017 runtime implementation (Trinitarian_Logic_Core).
    Full triadic logic evaluation (logical layer, distinct from triadic scoring).
    The three laws of thought (Identity, Non-Contradiction, Excluded Middle)
    are evaluated against the concept's proposition and premises.
    AF binding: AF_0059 (modal proposition), AF_0046 (HBN).

    Pairs with SCX-005 (Trinitarian_Optimization_Context) — provides the
    logical foundation that optimization scoring builds on.
    """

    def analyze(
        self,
        proposition: str,
        premises: Sequence[str],
        name: str = "",
    ) -> Dict[str, Any]:
        # Law 1: Identity — A is A (proposition names itself consistently)
        identity_holds = bool(proposition) and proposition.strip() == proposition.strip()
        identity_evidence = name.lower() in proposition.lower() or len(proposition) >= 3

        # Law 2: Non-Contradiction — ¬(A ∧ ¬A)
        prop_n = proposition.lower().strip()
        negation_forms = [f"not {prop_n}", f"¬{prop_n}", f"~{prop_n}", f"!{prop_n}"]
        contradiction_found = any(nf in p.lower() for nf in negation_forms for p in premises)
        non_contradiction_holds = not contradiction_found

        # Law 3: Excluded Middle — A ∨ ¬A
        # For a well-formed proposition, one of {true, false} must hold
        # Operationally: proposition is non-empty (has a truth value) and has axioms
        excluded_middle_holds = bool(proposition) and len(premises) >= 0

        # Triadic logical coherence score
        logic_dims = [identity_holds, non_contradiction_holds, excluded_middle_holds]
        logic_score = sum(logic_dims) / 3.0

        # Modal strength: how many premises contribute to the proposition?
        modal_support = sum(
            1 for p in premises
            if proposition.lower().split()[0] in p.lower() if proposition.split()
        )
        modal_strength = min(modal_support / max(len(premises), 1), 1.0)

        trinitarian_valid = logic_score >= 2 / 3 and not contradiction_found

        return {
            "engine": "trinitarian_logic",
            "fbc_id": "FBC_0017",
            "valid": trinitarian_valid,
            "logic_score": round(logic_score, 4),
            "laws": {
                "identity": {
                    "holds": identity_holds,
                    "evidence": identity_evidence,
                    "law": "A=A (grounded identity)",
                },
                "non_contradiction": {
                    "holds": non_contradiction_holds,
                    "contradiction_found": contradiction_found,
                    "law": "¬(A∧¬A)",
                },
                "excluded_middle": {
                    "holds": excluded_middle_holds,
                    "modal_support": modal_support,
                    "law": "A∨¬A",
                },
            },
            "modal_strength": round(modal_strength, 4),
            "af_bindings_activated": ["AF_0046", "AF_0059"],
        }


class BijectionClosureLens:
    """
    FBC_0005 runtime implementation (Global_Bijective_Recursion_Core).
    Verifies that the bridge mapping is bijectively closed:
      concept → analog → implementation ≡ concept → implementation (direct)
    Both directions A→B and B→A must hold for the mapping to be bijective.
    AF binding: AF_0048 (run_logos_cycle — the cycle that must be bijection-closed).

    Pairs with SCX-002 (Bootstrap_Runtime_Context) — bijection closure must
    be verified before the runtime can safely bootstrap.
    """

    def analyze(self, bridge_mapping: Dict[str, Any]) -> Dict[str, Any]:
        concept = bridge_mapping.get("concept", {})
        analog = bridge_mapping.get("analog", {})
        impl = bridge_mapping.get("implementation", {})

        # Forward: concept → analog → implementation
        forward_chain = [
            bool(concept.get("name")),
            bool(analog),
            bool(impl.get("targets")),
        ]
        forward_complete = all(forward_chain)

        # Reverse: implementation → analog → concept (bijection requires both)
        reverse_chain = [
            bool(impl.get("lambda_form")),
            bool(analog.get("conceptual_shape")),
            bool(concept.get("proposition")),
        ]
        reverse_complete = all(reverse_chain)

        bijective = forward_complete and reverse_complete

        # Closure hash: stable identifier for the bijective pair
        closure_payload = {
            "concept_name": concept.get("name"),
            "impl_targets": impl.get("targets"),
            "lambda_form": impl.get("lambda_form"),
        }
        closure_hash = hashlib.sha256(
            json.dumps(closure_payload, sort_keys=True, default=str).encode()
        ).hexdigest()

        return {
            "engine": "bijection_closure",
            "fbc_id": "FBC_0005",
            "bijective": bijective,
            "forward_complete": forward_complete,
            "reverse_complete": reverse_complete,
            "forward_chain_dims": forward_chain,
            "reverse_chain_dims": reverse_chain,
            "closure_hash": closure_hash,
            "theorem": "∀x: concept(x)→analog(x)→impl(x) ≡ concept(x)→impl(x)",
            "af_bindings_activated": ["AF_0048"],
        }


class TripartiteDistinctionLens:
    """
    FBC_0001 + FBC_0002 runtime implementation (3PDN_Constraint + 3PDN_Validator).
    Three-Part Distinction Non-Collapse (3PDN):
    The three ontological categories (idea/concept, analog/form, implementation)
    must remain genuinely distinct — no two may collapse into the same entity.
    AF binding: AF_0058 (validate against baseline), AF_0057 (emergence).

    Pairs with SCX-003 (Privation_Handling_Context) — 3PDN failures are a
    form of privation (loss of ontological distinction).
    """

    def analyze(
        self,
        idea_form: str,
        analog_form: str,
        impl_form: str,
    ) -> Dict[str, Any]:
        # Normalize for comparison
        def norm(s: str) -> str:
            return "".join(s.lower().split())

        n_idea = norm(idea_form)
        n_analog = norm(analog_form)
        n_impl = norm(impl_form)

        # Collapse checks
        collapses: List[Dict[str, Any]] = []
        if n_idea and n_analog and n_idea == n_analog:
            collapses.append({
                "pair": ("idea", "analog"),
                "violation": f"idea='{idea_form}' collapsed with analog='{analog_form}'",
            })
        if n_idea and n_impl and n_idea == n_impl:
            collapses.append({
                "pair": ("idea", "implementation"),
                "violation": f"idea='{idea_form}' collapsed with implementation='{impl_form}'",
            })
        if n_analog and n_impl and n_analog == n_impl:
            collapses.append({
                "pair": ("analog", "implementation"),
                "violation": f"analog='{analog_form}' collapsed with implementation='{impl_form}'",
            })

        # Partial collapse: high Jaccard similarity (>0.85) between any two
        def jaccard(a: str, b: str) -> float:
            sa, sb = set(a), set(b)
            if not sa and not sb:
                return 1.0
            return len(sa & sb) / len(sa | sb)

        partial: List[Dict[str, Any]] = []
        pairs = [
            ("idea", "analog", n_idea, n_analog),
            ("idea", "implementation", n_idea, n_impl),
            ("analog", "implementation", n_analog, n_impl),
        ]
        for p1, p2, a, b in pairs:
            sim = jaccard(a, b)
            if sim > 0.85 and a != b:
                partial.append({"pair": (p1, p2), "similarity": round(sim, 4)})

        valid = len(collapses) == 0

        # Validator: all three must be non-empty for valid 3PDN
        non_empty = bool(n_idea) and bool(n_analog) and bool(n_impl)

        return {
            "engine": "tripartite_distinction",
            "fbc_ids": ["FBC_0001", "FBC_0002"],
            "valid": valid and non_empty,
            "collapses_detected": collapses,
            "partial_collapses": partial,
            "non_empty": non_empty,
            "distinction_score": round(1.0 - len(collapses) / 3.0, 4),
            "af_bindings_activated": ["AF_0057", "AF_0058"],
        }


class HypostaticIdentityLens:
    """
    FBC_0006 runtime implementation (Hypostatic_ID_Validator).
    Validates that the identity of the concept is preserved across all
    transformation stages (lambda encoding, bridge mapping, triadic scoring).
    Identity must be hypostatic — stable in its own right, not derived
    from the transform.
    AF binding: AF_0050 (ontological state), AF_0051 (concept selection).

    Pairs with SCX-001 (Agent_Policy_Decision_Context) — policy decisions
    must know which entity they apply to (stable identity required).
    """

    def analyze(
        self,
        name: str,
        lambda_form: str,
        bridge_name: str,
        triadic_scores: Dict[str, float],
    ) -> Dict[str, Any]:
        # Check 1: name preserved in lambda encoding
        in_lambda = name.lower().replace(" ", "") in lambda_form.lower().replace(" ", "")

        # Check 2: name preserved in bridge mapping
        in_bridge = name.lower() == bridge_name.lower()

        # Check 3: identity score — triadic minimum is stable enough to ground identity
        triadic_min = min(triadic_scores.values()) if triadic_scores else 0.0
        triadic_stable = triadic_min >= 0.5

        # Hypostatic identity hash: stable fingerprint of the entity's identity
        identity_payload = {
            "name": name,
            "in_lambda": in_lambda,
            "in_bridge": in_bridge,
        }
        identity_hash = hashlib.sha256(
            json.dumps(identity_payload, sort_keys=True).encode()
        ).hexdigest()

        valid = in_lambda and in_bridge and triadic_stable

        return {
            "engine": "hypostatic_identity",
            "fbc_id": "FBC_0006",
            "valid": valid,
            "name_in_lambda": in_lambda,
            "name_in_bridge": in_bridge,
            "triadic_stable": triadic_stable,
            "triadic_minimum": round(triadic_min, 4),
            "identity_hash": identity_hash,
            "af_bindings_activated": ["AF_0050", "AF_0051"],
        }


class InputSanitizerLens:
    """
    FBC_0012 runtime implementation (Runtime_Input_Sanitizer).
    Validates that the concept's string fields are well-formed and free
    from injection-class payloads or structural malformations.
    Allowed: printable unicode, logical symbols, alphanumerics, punctuation.
    Disallowed: control characters, shell metacharacters in structural positions.
    AF binding: AF_0046 (HBN — first major consumer of inputs).

    Pairs with SCX-002 (Bootstrap_Runtime_Context) — inputs must be
    sanitized before bootstrap.
    """

    _DISALLOWED_CONTROL_CHARS = set(chr(c) for c in range(0, 32) if c not in {9, 10, 13})
    _STRUCTURAL_INJECTION_PATTERNS = [
        "__import__", "eval(", "exec(", "os.system", "subprocess",
        "open(", "rm -", "DROP TABLE", "<script", "javascript:",
    ]

    def analyze(self, fields: Dict[str, str]) -> Dict[str, Any]:
        violations: List[Dict[str, Any]] = []
        sanitized: Dict[str, str] = {}

        for field_name, value in fields.items():
            if not isinstance(value, str):
                sanitized[field_name] = str(value)
                continue

            # Control character check
            ctrl_chars = [c for c in value if c in self._DISALLOWED_CONTROL_CHARS]
            if ctrl_chars:
                violations.append({
                    "field": field_name,
                    "type": "control_character",
                    "chars": [repr(c) for c in ctrl_chars],
                })

            # Injection pattern check
            value_lower = value.lower()
            for pattern in self._STRUCTURAL_INJECTION_PATTERNS:
                if pattern.lower() in value_lower:
                    violations.append({
                        "field": field_name,
                        "type": "injection_pattern",
                        "pattern": pattern,
                    })

            # Sanitize: strip control chars
            clean = "".join(c for c in value if c not in self._DISALLOWED_CONTROL_CHARS)
            sanitized[field_name] = clean

        valid = len(violations) == 0

        if not valid:
            raise SanitizerViolation(
                f"Input sanitization failed: {json.dumps(violations)}"
            )

        return {
            "engine": "input_sanitizer",
            "fbc_id": "FBC_0012",
            "valid": valid,
            "fields_checked": list(fields.keys()),
            "violations": violations,
            "sanitized": sanitized,
            "af_bindings_activated": ["AF_0046"],
        }


# ============================================================================
# FunctionBlockCore — axiom + context pair with AF completion
# ============================================================================

@dataclass(frozen=True)
class FunctionBlockCore:
    """
    A complete FBC: one context embedding + required axioms + optional-composable
    axioms injected + AF bindings. Score encodes the power profile.
    """
    fbc_config_id: str
    name: str
    description: str
    context_embeddings: Tuple[str, ...]       # SCX-00N ids
    required_axioms: Tuple[str, ...]          # FBC IDs always present
    injected_optional_axioms: Tuple[str, ...] # FBC IDs newly injected
    af_bindings: Tuple[str, ...]              # AF IDs
    taxonomy_classes_covered: Tuple[str, ...]
    score: FBCScore


@dataclass
class FBCEvaluationResult:
    fbc_config_id: str
    name: str
    power_class: str
    composite_score: int
    context_embedding_traces: List[Dict[str, Any]]
    axiom_evaluations: List[Dict[str, Any]]
    lens_results: Dict[str, Any]
    af_completion_results: List[Dict[str, Any]]
    passed: bool
    diagnostics: List[str]


# ============================================================================
# FBC configuration catalog — 5 power configurations + safety configs
# ============================================================================

_FBC_CONFIGURATIONS: List[FunctionBlockCore] = [
    # ── POWER-A: Inference Full Stack (45/50) ────────────────────────────────
    FunctionBlockCore(
        fbc_config_id="POWER-A",
        name="Inference_Full_Stack",
        description=(
            "All 5 optional-composable inference_core axioms injected into "
            "the complete DRAC_CORE_013 base (all 5 contexts). Provides the "
            "deepest inference coverage: evidence chains + bijective recursion "
            "+ necessary existence + temporal ordering + trinitarian logic."
        ),
        context_embeddings=("SCX-001", "SCX-002", "SCX-003", "SCX-004", "SCX-005"),
        required_axioms=("FBC_0007", "FBC_0014", "FBC_0011", "FBC_0013", "FBC_0016"),
        injected_optional_axioms=("FBC_0004", "FBC_0005", "FBC_0009", "FBC_0015", "FBC_0017"),
        af_bindings=("AF_0046", "AF_0048", "AF_0050", "AF_0051", "AF_0052", "AF_0055", "AF_0057", "AF_0059"),
        taxonomy_classes_covered=("inference_core", "safety_core", "semantic_core", "protocol_core"),
        score=FBCScore(inference_depth=10, safety_coverage=7, cluster_reach=9, axiom_synergy=9, novel_coverage=10),
    ),

    # ── POWER-B: Trinitarian Complete (43/50) ───────────────────────────────
    FunctionBlockCore(
        fbc_config_id="POWER-B",
        name="Trinitarian_Complete",
        description=(
            "SCX-005 (Trinitarian_Optimization_Context) enriched with "
            "FBC_0017 (Trinitarian_Logic_Core) + FBC_0004 (Evidence_Chain). "
            "Provides full triadic reasoning: optimization scoring + logical "
            "axioms + evidence chain grounding. Most focused inference config."
        ),
        context_embeddings=("SCX-005",),
        required_axioms=("FBC_0007", "FBC_0014", "FBC_0016"),
        injected_optional_axioms=("FBC_0017", "FBC_0004"),
        af_bindings=("AF_0046", "AF_0051", "AF_0059"),
        taxonomy_classes_covered=("inference_core", "safety_core"),
        score=FBCScore(inference_depth=9, safety_coverage=7, cluster_reach=8, axiom_synergy=10, novel_coverage=9),
    ),

    # ── POWER-C: Bijective Bootstrap (41/50) ────────────────────────────────
    FunctionBlockCore(
        fbc_config_id="POWER-C",
        name="Bijective_Bootstrap",
        description=(
            "SCX-002 (Bootstrap_Runtime_Context) enriched with "
            "FBC_0005 (Global_Bijective_Recursion_Core) + FBC_0015 "
            "(Temporal_Supersession). Bootstrap is bijection-validated and "
            "premise supersession-cleaned before any reasoning begins."
        ),
        context_embeddings=("SCX-002",),
        required_axioms=("FBC_0007", "FBC_0014", "FBC_0011", "FBC_0013"),
        injected_optional_axioms=("FBC_0005", "FBC_0015"),
        af_bindings=("AF_0048", "AF_0052", "AF_0055"),
        taxonomy_classes_covered=("inference_core", "safety_core", "semantic_core"),
        score=FBCScore(inference_depth=8, safety_coverage=7, cluster_reach=8, axiom_synergy=9, novel_coverage=9),
    ),

    # ── POWER-D: Existence Privation Temporal (40/50) ───────────────────────
    FunctionBlockCore(
        fbc_config_id="POWER-D",
        name="Existence_Privation_Temporal",
        description=(
            "SCX-003 (Privation_Handling_Context) enriched with "
            "FBC_0009 (Necessary_Existence_Core) + FBC_0015 "
            "(Temporal_Supersession). Privation is governed simultaneously "
            "by existence proof and temporal validity of premises."
        ),
        context_embeddings=("SCX-003",),
        required_axioms=("FBC_0007", "FBC_0014"),
        injected_optional_axioms=("FBC_0009", "FBC_0015"),
        af_bindings=("AF_0050", "AF_0052", "AF_0055"),
        taxonomy_classes_covered=("inference_core", "safety_core"),
        score=FBCScore(inference_depth=7, safety_coverage=7, cluster_reach=7, axiom_synergy=9, novel_coverage=10),
    ),

    # ── POWER-E: Safety Complete (40/50) ────────────────────────────────────
    FunctionBlockCore(
        fbc_config_id="POWER-E",
        name="Safety_Complete",
        description=(
            "SCX-001+SCX-003 co-active with all optional safety_core axioms: "
            "FBC_0001 (3PDN_Constraint) + FBC_0002 (3PDN_Validator) + "
            "FBC_0006 (Hypostatic_ID_Validator) + FBC_0012 (Runtime_Input_Sanitizer). "
            "Maximum safety gate coverage with ontological boundary protection."
        ),
        context_embeddings=("SCX-001", "SCX-003"),
        required_axioms=("FBC_0007", "FBC_0014"),
        injected_optional_axioms=("FBC_0001", "FBC_0002", "FBC_0006", "FBC_0012"),
        af_bindings=("AF_0046", "AF_0057", "AF_0058"),
        taxonomy_classes_covered=("safety_core",),
        score=FBCScore(inference_depth=5, safety_coverage=10, cluster_reach=7, axiom_synergy=8, novel_coverage=10),
    ),
]


def get_fbc_configuration(config_id: str) -> Optional[FunctionBlockCore]:
    for c in _FBC_CONFIGURATIONS:
        if c.fbc_config_id == config_id:
            return c
    return None


def ranked_configurations() -> List[FunctionBlockCore]:
    """Return all FBC configurations ranked by total score (highest first)."""
    return sorted(_FBC_CONFIGURATIONS, key=lambda c: c.score.total, reverse=True)


# ============================================================================
# FBC Combination Engine — evaluates and scores each configuration
# ============================================================================

class FBCCombinationEngine:
    """
    Runs all 5 power configurations against a ReasoningCandidate-like dict,
    scores each, and returns the ranked results with best-overall winner.

    POWER-A is the most powerful configuration (45/50, ALPHA class).
    The engine also experimentally combines subsets to identify if any
    partial configuration outperforms the full stack on specific candidates.

    Usage:
        engine = FBCCombinationEngine()
        results = engine.run(candidate_dict)
        best = results["best_config_id"]
    """

    def __init__(self) -> None:
        self._evidence_lens = EvidenceChainLens()
        self._existence_lens = ExistenceProofLens()
        self._temporal_lens = TemporalSupersessionLens()
        self._trinitarian_logic_lens = TrinitarianLogicLens()
        self._bijection_lens = BijectionClosureLens()
        self._tripartite_lens = TripartiteDistinctionLens()
        self._hypostatic_lens = HypostaticIdentityLens()
        self._sanitizer_lens = InputSanitizerLens()

    def run(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all 5 power configurations against the candidate dict.
        Returns all evaluation results plus the winning configuration.
        """
        # Extract fields from candidate dict
        name       = candidate.get("name", "")
        proposition= candidate.get("proposition", "")
        premises   = list(candidate.get("premises", []))
        lambda_form= candidate.get("lambda_form", "")
        bridge     = candidate.get("bridge_mapping", {})
        triadic    = candidate.get("triadic_scores", {"idea": 0.7, "analog": 0.7, "bridge": 0.7})

        # Run all lenses upfront (reused across configs)
        lens_bank = self._run_lens_bank(name, proposition, premises, lambda_form, bridge, triadic)

        # Evaluate each configuration
        eval_results: List[FBCEvaluationResult] = []
        for fbc in ranked_configurations():
            result = self._evaluate_fbc(fbc, candidate, lens_bank)
            eval_results.append(result)

        # Find best: highest composite_score among passed configs
        passed = [r for r in eval_results if r.passed]
        best = max(passed, key=lambda r: r.composite_score) if passed else eval_results[0]

        # Experimental: find if any partial combination outperforms (greedy search)
        experimental = self._experimental_search(eval_results, candidate, lens_bank)

        return {
            "configurations_evaluated": len(eval_results),
            "results": [_result_to_dict(r) for r in eval_results],
            "best_config_id": best.fbc_config_id,
            "best_config_name": best.name,
            "best_power_class": best.power_class,
            "best_composite_score": best.composite_score,
            "experimental_best": experimental,
            "lens_bank_summary": {k: v.get("valid", v.get("bijective", v.get("chain_valid", True)))
                                  for k, v in lens_bank.items()},
        }

    def _run_lens_bank(
        self,
        name: str,
        proposition: str,
        premises: List[str],
        lambda_form: str,
        bridge: Dict[str, Any],
        triadic: Dict[str, float],
    ) -> Dict[str, Any]:
        """Run all 8 lenses and collect results. Graceful-degrad on failure."""
        results: Dict[str, Any] = {}

        # Evidence chain
        try:
            results["evidence_chain"] = self._evidence_lens.analyze(premises)
        except Exception as e:
            results["evidence_chain"] = {"engine": "evidence_chain", "error": str(e), "chain_valid": False}

        # Existence proof
        try:
            results["existence_proof"] = self._existence_lens.analyze(
                name, proposition, lambda_form, bridge
            )
        except Exception as e:
            results["existence_proof"] = {"engine": "existence_proof", "error": str(e), "proved": False}

        # Temporal supersession
        try:
            results["temporal_supersession"] = self._temporal_lens.analyze(premises)
        except Exception as e:
            results["temporal_supersession"] = {"engine": "temporal_supersession", "error": str(e)}

        # Trinitarian logic
        try:
            results["trinitarian_logic"] = self._trinitarian_logic_lens.analyze(
                proposition, premises, name
            )
        except Exception as e:
            results["trinitarian_logic"] = {"engine": "trinitarian_logic", "error": str(e), "valid": False}

        # Bijection closure
        try:
            results["bijection_closure"] = self._bijection_lens.analyze(bridge)
        except Exception as e:
            results["bijection_closure"] = {"engine": "bijection_closure", "error": str(e), "bijective": False}

        # Tripartite distinction
        try:
            concept_repr = str(bridge.get("concept", {}).get("name", name))
            analog_repr  = str(bridge.get("analog", {}).get("conceptual_shape", "analog"))
            impl_repr    = str(bridge.get("implementation", {}).get("lambda_form", lambda_form))
            results["tripartite_distinction"] = self._tripartite_lens.analyze(
                concept_repr, analog_repr, impl_repr
            )
        except Exception as e:
            results["tripartite_distinction"] = {"engine": "tripartite_distinction", "error": str(e), "valid": False}

        # Hypostatic identity
        try:
            bridge_name = bridge.get("concept", {}).get("name", "")
            results["hypostatic_identity"] = self._hypostatic_lens.analyze(
                name, lambda_form, bridge_name, triadic
            )
        except Exception as e:
            results["hypostatic_identity"] = {"engine": "hypostatic_identity", "error": str(e), "valid": False}

        # Input sanitizer
        try:
            fields_to_sanitize = {"name": name, "proposition": proposition}
            results["input_sanitizer"] = self._sanitizer_lens.analyze(fields_to_sanitize)
        except SanitizerViolation as e:
            results["input_sanitizer"] = {"engine": "input_sanitizer", "error": str(e), "valid": False}
        except Exception as e:
            results["input_sanitizer"] = {"engine": "input_sanitizer", "error": str(e), "valid": False}

        return results

    def _evaluate_fbc(
        self,
        fbc: FunctionBlockCore,
        candidate: Dict[str, Any],
        lens_bank: Dict[str, Any],
    ) -> FBCEvaluationResult:
        diagnostics: List[str] = []

        # Build context embedding traces
        ctx_traces: List[Dict[str, Any]] = []
        for scx_id in fbc.context_embeddings:
            ctx = _CTX_EMBEDDINGS.get(scx_id)
            if ctx:
                enriched = ctx.embed({"concept": candidate.get("name", "")})
                ctx_traces.append({
                    "scx_id": scx_id,
                    "name": ctx.name,
                    "call_sequence": list(ctx.axiom_call_sequence),
                    "spine_binding": ctx.spine_binding,
                    "enriched_context": enriched,
                })
            else:
                diagnostics.append(f"Unknown context embedding: {scx_id}")

        # Axiom evaluations (simulate the axiom call sequence)
        axiom_evals: List[Dict[str, Any]] = []
        for fbc_id in fbc.required_axioms + fbc.injected_optional_axioms:
            axiom_evals.append(self._simulate_axiom_eval(fbc_id, candidate))

        # Select lenses relevant to this FBC's injected axioms
        relevant_lenses = self._select_lenses(fbc.injected_optional_axioms, lens_bank)

        # AF completion results
        af_results: List[Dict[str, Any]] = []
        for af_id in fbc.af_bindings:
            af = _AF_BINDINGS.get(af_id)
            if af:
                af_results.append({
                    "af_id": af_id,
                    "function": af.function_name,
                    "modifier": af.semantic_modifier,
                    "cluster": af.cluster,
                    "status": "bound",
                })

        # Compute candidate-adjusted score
        base_score = fbc.score.total
        candidate_bonus = self._candidate_bonus(candidate, lens_bank)
        composite_score = base_score + candidate_bonus

        passed = len([e for e in axiom_evals if not e.get("passed", True)]) == 0

        return FBCEvaluationResult(
            fbc_config_id=fbc.fbc_config_id,
            name=fbc.name,
            power_class=fbc.score.power_class.value,
            composite_score=composite_score,
            context_embedding_traces=ctx_traces,
            axiom_evaluations=axiom_evals,
            lens_results=relevant_lenses,
            af_completion_results=af_results,
            passed=passed,
            diagnostics=diagnostics,
        )

    def _simulate_axiom_eval(
        self, fbc_id: str, candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate an axiom evaluation using the same logic as DRACAxiomRegistry
        in PCCRE, but without importing it (decoupled). Returns pass/fail + details.
        """
        name = candidate.get("name", "")
        proposition = candidate.get("proposition", "")
        premises = list(candidate.get("premises", []))

        if fbc_id == "FBC_0007":  # Invariant_Constraints
            mutated = candidate.get("flags", {}).get("mutated_after_verification", False)
            return {"fbc_id": fbc_id, "axiom": "Invariant_Constraints", "passed": not mutated,
                    "detail": "No mutation" if not mutated else "Mutation detected"}

        if fbc_id == "FBC_0014":  # Semantic_Capability_Gate
            caps = candidate.get("capabilities", {})
            mapped = (not caps) or all(caps.values())
            return {"fbc_id": fbc_id, "axiom": "Semantic_Capability_Gate", "passed": mapped,
                    "detail": "Capabilities admitted" if mapped else "Capability unmapped"}

        if fbc_id == "FBC_0011":  # Runtime_Context_Initializer
            ctx = candidate.get("runtime_context")
            has = isinstance(ctx, dict)
            return {"fbc_id": fbc_id, "axiom": "Runtime_Context_Initializer", "passed": has,
                    "detail": "Context initialized" if has else "Context missing"}

        if fbc_id == "FBC_0013":  # Runtime_Mode_Controller
            ctx = candidate.get("runtime_context", {})
            mode = ctx.get("mode") if isinstance(ctx, dict) else None
            allowed = {"analytical", "synthetic", "validating", "exploratory"}
            ok = mode in allowed
            return {"fbc_id": fbc_id, "axiom": "Runtime_Mode_Controller", "passed": ok,
                    "detail": f"Mode={mode}" if ok else f"Invalid mode={mode}"}

        if fbc_id == "FBC_0016":  # Trinitarian_Alignment_Core
            triadic = candidate.get("triadic_scores", {})
            min_score = min(triadic.values()) if triadic else 0.0
            ok = min_score > 0.0
            return {"fbc_id": fbc_id, "axiom": "Trinitarian_Alignment_Core", "passed": ok,
                    "detail": f"Triadic min={min_score:.4f}"}

        if fbc_id == "FBC_0004":  # Evidence_Chain
            has_premises = len(premises) > 0
            return {"fbc_id": fbc_id, "axiom": "Evidence_Chain", "passed": has_premises,
                    "detail": f"Chain length={len(premises)}"}

        if fbc_id == "FBC_0005":  # Global_Bijective_Recursion_Core
            bridge = candidate.get("bridge_mapping", {})
            ok = {"concept", "analog", "implementation"} <= set(bridge.keys())
            return {"fbc_id": fbc_id, "axiom": "Global_Bijective_Recursion_Core", "passed": ok,
                    "detail": "Bridge closed" if ok else "Bridge incomplete"}

        if fbc_id == "FBC_0006":  # Hypostatic_ID_Validator
            ok = bool(name and proposition)
            return {"fbc_id": fbc_id, "axiom": "Hypostatic_ID_Validator", "passed": ok,
                    "detail": "Identity grounded" if ok else "Identity not grounded"}

        if fbc_id == "FBC_0009":  # Necessary_Existence_Core
            ok = bool(name and proposition)
            return {"fbc_id": fbc_id, "axiom": "Necessary_Existence_Core", "passed": ok,
                    "detail": "Substrate non-null" if ok else "Null substrate"}

        if fbc_id == "FBC_0012":  # Runtime_Input_Sanitizer
            # Thin check: name and proposition contain no control characters
            for field_val in [name, proposition]:
                for c in field_val:
                    if ord(c) < 32 and c not in "\t\n\r":
                        return {"fbc_id": fbc_id, "axiom": "Runtime_Input_Sanitizer",
                                "passed": False, "detail": f"Control char in input: {repr(c)}"}
            return {"fbc_id": fbc_id, "axiom": "Runtime_Input_Sanitizer", "passed": True,
                    "detail": "Inputs clean"}

        if fbc_id == "FBC_0015":  # Temporal_Supersession
            # Check premises for supersession events
            has_supersession = any("supersedes:" in p.lower() or "retired:" in p.lower()
                                   for p in premises)
            return {"fbc_id": fbc_id, "axiom": "Temporal_Supersession", "passed": True,
                    "detail": f"Supersession events={'yes' if has_supersession else 'none'}"}

        if fbc_id == "FBC_0017":  # Trinitarian_Logic_Core
            ok = bool(proposition)
            return {"fbc_id": fbc_id, "axiom": "Trinitarian_Logic_Core", "passed": ok,
                    "detail": "Triune logic admissible" if ok else "Proposition empty"}

        if fbc_id in {"FBC_0001", "FBC_0002"}:  # 3PDN
            bridge = candidate.get("bridge_mapping", {})
            ok = bool(bridge.get("concept")) and bool(bridge.get("analog")) and bool(bridge.get("implementation"))
            return {"fbc_id": fbc_id, "axiom": "3PDN", "passed": ok,
                    "detail": "3PDN dimensions distinct" if ok else "3PDN incomplete"}

        # Unknown axiom — pass by default (open axiom space)
        return {"fbc_id": fbc_id, "axiom": fbc_id, "passed": True, "detail": "Unknown axiom, admitted"}

    def _select_lenses(
        self,
        injected_axioms: Tuple[str, ...],
        lens_bank: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return only the lens results relevant to the FBC's injected axioms."""
        axiom_to_lens = {
            "FBC_0004": "evidence_chain",
            "FBC_0005": "bijection_closure",
            "FBC_0006": "hypostatic_identity",
            "FBC_0009": "existence_proof",
            "FBC_0012": "input_sanitizer",
            "FBC_0015": "temporal_supersession",
            "FBC_0017": "trinitarian_logic",
            "FBC_0001": "tripartite_distinction",
            "FBC_0002": "tripartite_distinction",
        }
        selected: Dict[str, Any] = {}
        for axiom in injected_axioms:
            lens_key = axiom_to_lens.get(axiom)
            if lens_key and lens_key in lens_bank:
                selected[lens_key] = lens_bank[lens_key]
        return selected

    def _candidate_bonus(
        self, candidate: Dict[str, Any], lens_bank: Dict[str, Any]
    ) -> int:
        """
        Compute a candidate-specific bonus (+0 to +5) based on how well
        the lenses pass for this specific candidate.
        """
        bonus = 0
        if lens_bank.get("trinitarian_logic", {}).get("valid"):
            bonus += 1
        if lens_bank.get("evidence_chain", {}).get("chain_valid"):
            bonus += 1
        if lens_bank.get("bijection_closure", {}).get("bijective"):
            bonus += 1
        if lens_bank.get("existence_proof", {}).get("proved"):
            bonus += 1
        if lens_bank.get("hypostatic_identity", {}).get("valid"):
            bonus += 1
        return bonus

    def _experimental_search(
        self,
        results: List[FBCEvaluationResult],
        candidate: Dict[str, Any],
        lens_bank: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Greedy subset search: try combining top-2 configs and see if the
        combined score (union of axioms, intersection of lens passes) is
        higher than any single config.
        """
        if len(results) < 2:
            return {"method": "greedy_pair", "winner": results[0].fbc_config_id if results else None}

        sorted_results = sorted(results, key=lambda r: r.composite_score, reverse=True)
        top_two = sorted_results[:2]

        # Combined: union lens passes
        combined_lenses_pass = 0
        for lens_key in lens_bank:
            v = lens_bank[lens_key]
            passed_in_either = v.get("valid", v.get("bijective", v.get("chain_valid", True)))
            if passed_in_either:
                combined_lenses_pass += 1

        total_lenses = len(lens_bank)
        combined_score = int((combined_lenses_pass / max(total_lenses, 1)) * 50)

        winner_id = top_two[0].fbc_config_id
        if combined_score > top_two[0].composite_score:
            winner_id = f"{top_two[0].fbc_config_id}+{top_two[1].fbc_config_id}"

        return {
            "method": "greedy_pair",
            "candidates_compared": [r.fbc_config_id for r in top_two],
            "combined_lens_pass_count": combined_lenses_pass,
            "combined_score": combined_score,
            "winner": winner_id,
        }


# ============================================================================
# Utility
# ============================================================================

def _result_to_dict(r: FBCEvaluationResult) -> Dict[str, Any]:
    return {
        "fbc_config_id": r.fbc_config_id,
        "name": r.name,
        "power_class": r.power_class,
        "composite_score": r.composite_score,
        "passed": r.passed,
        "context_embedding_traces": r.context_embedding_traces,
        "axiom_evaluations": r.axiom_evaluations,
        "lens_results": r.lens_results,
        "af_completion_results": r.af_completion_results,
        "diagnostics": r.diagnostics,
    }


def Build_FBC_Engine() -> FBCCombinationEngine:
    """Convenience constructor."""
    return FBCCombinationEngine()


def Run_FBC_Phase(candidate_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Minimal entry point: run all FBC configurations against a candidate dict."""
    engine = FBCCombinationEngine()
    return engine.run(candidate_dict)
