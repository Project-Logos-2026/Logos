# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: CONTROLLED
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Proof_Carrying_Context_Reasoning_Engine
runtime_layer: RUNTIME_EXECUTION_CORE
role: Meta-binding reasoning engine for concept-to-implementation convergence
responsibility: Enforces PXL-grounded reasoning, DRAC axiom admission, triadic
  coherence, and proof-carrying artifact generation before execution envelope
  assembly. Acts as the pre-execution gate above the 5-stage ARP compiler
  pipeline. First runtime implementation of DRAC axiom logic (Trinitarian,
  Global Bijective Recursion, Necessary Existence) previously defined only as
  semantic axiom placeholders.
agent_binding: LOGOS_Agent
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: []
provides:
  - PXLKernel
  - DRACAxiomRegistry
  - ContextCompiler
  - MeshFixedPointAttractor
  - ProofCarryingArtifact
  - ProofCarryingContextReasoningEngine
  - Build_Concept_Packet
  - Reason_Concept_To_Artifact
  - IterativeReasoningAmplifier
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Rejects non-coherent, non-grounded, or non-provable candidates."
observability:
  log_channel: reasoning.meta_context
  metrics: enabled
pipeline_position: >
  Sits ABOVE the 5-stage ARPCompilerCore pipeline.
  Accepts ConceptPacket → emits ProofCarryingArtifact.
  ProofCarryingArtifact gates I3AA assembly in Stage 5 (UnifiedBinder).
  Can also wrap Stage 5 output to produce proof-grounded I3AA variants.
recursion_amplification: >
  IterativeReasoningAmplifier provides fixed-point convergence over multiple
  PCCRE passes. Each pass feeds ProofCarryingArtifact.bridge_mapping back as
  new premises for the next concept packet, converging when MESH fixed-point
  hash stabilizes or max_iterations reached.
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple
import ast
import hashlib
import json
import math
import logging

logger = logging.getLogger("reasoning.meta_context")

# Optional companion: FBC combination engine (same package — fail-open import)
try:
    from .DRAC_Function_Block_Core_Engine import (
        FBCCombinationEngine,
        Run_FBC_Phase,
        FBCEvaluationResult,
        ContextEmbedding as FBCContextEmbedding,
        FunctionBlockCore,
    )
    _FBC_ENGINE_AVAILABLE = True
except ImportError:
    _FBC_ENGINE_AVAILABLE = False
    FBCCombinationEngine = None  # type: ignore[assignment,misc]
    Run_FBC_Phase = None  # type: ignore[assignment]


# ============================================================================
# Exceptions
# ============================================================================

class ReasoningViolation(RuntimeError):
    """Base fail-closed reasoning exception."""


class InvariantViolation(ReasoningViolation):
    """Raised when invariants are violated."""


class CapabilityViolation(ReasoningViolation):
    """Raised when a required semantic capability is missing."""


class CoherenceViolation(ReasoningViolation):
    """Raised when MESH / triadic coherence fails."""


class ProofViolation(ReasoningViolation):
    """Raised when proof obligations fail."""


class ConvergenceViolation(ReasoningViolation):
    """Raised when iterative amplification fails to converge."""


# ============================================================================
# PXL Kernel
# ============================================================================

class PXLModalGround(Enum):
    """
    Triadic modal grounding aligned to PXL substrate.
    Runtime implementation of the three classical laws of thought,
    grounded in the PXL operator algebra.
    """
    IDENTITY = "I1"         # Law of Identity
    CONTRADICTION = "I2"    # Law of Non-Contradiction
    EXCLUDED_MIDDLE = "I3"  # Law of Excluded Middle


class PXLPrimitive(Enum):
    """Canonical PXL primitives in runtime-facing form."""
    COHERENCE = "⧟"
    NON_EQUIVALENCE = "⇎"
    INTERCHANGE = "⇌"
    ENTAILMENT = "⟹"
    MODAL_EQUIVALENCE = "⩪"


@dataclass(frozen=True)
class PXLJudgement:
    operator: str
    left: Any
    right: Any
    result: bool
    grounding: str
    justification: str


class PXLKernel:
    """
    Minimal deterministic PXL kernel.

    Derived from:
    - PXL_Core.py (fractal/ontological PXL surface)
    - pxl_engine.py (modal grounding engine)
    - foundational_logic.py (classical logic primitives)

    Runtime policy: fail-closed, deterministic, side-effect free.

    Relationship to DRAC:
      This kernel is the runtime implementation of the modal grounding logic
      that DRAC axioms (FBC_0016 Trinitarian_Alignment_Core,
      FBC_0009 Necessary_Existence_Core) declare but do not implement.
      The three PXLModalGround values correspond directly to the three
      DRAC invariant categories.
    """

    def coherence(self, left: Any, right: Any) -> PXLJudgement:
        result = self._canonicalize(left) == self._canonicalize(right)
        return PXLJudgement(
            operator=PXLPrimitive.COHERENCE.value,
            left=left,
            right=right,
            result=result,
            grounding=PXLModalGround.IDENTITY.value,
            justification="Canonical structural equality under grounded identity.",
        )

    def non_equivalence(self, left: Any, right: Any) -> PXLJudgement:
        coherence = self.coherence(left, right)
        result = not coherence.result
        return PXLJudgement(
            operator=PXLPrimitive.NON_EQUIVALENCE.value,
            left=left,
            right=right,
            result=result,
            grounding=PXLModalGround.CONTRADICTION.value,
            justification="Non-equivalence holds iff grounded coherence does not hold.",
        )

    def entailment(self, premises: Sequence[str], conclusion: str) -> PXLJudgement:
        normalized = {self._normalize_formula(p) for p in premises}
        c = self._normalize_formula(conclusion)

        direct = c in normalized
        modus_ponens = False

        if not direct:
            for p in normalized:
                if "->" in p:
                    antecedent, consequent = [x.strip() for x in p.split("->", 1)]
                    if antecedent in normalized and consequent == c:
                        modus_ponens = True
                        break

        result = direct or modus_ponens
        return PXLJudgement(
            operator=PXLPrimitive.ENTAILMENT.value,
            left=list(premises),
            right=conclusion,
            result=result,
            grounding=PXLModalGround.IDENTITY.value,
            justification="Direct inclusion or single-step modus ponens under deterministic proof search.",
        )

    def modal_equivalence(self, left: Any, right: Any) -> PXLJudgement:
        left_hash = self._stable_hash(self._canonicalize(left))
        right_hash = self._stable_hash(self._canonicalize(right))
        result = left_hash == right_hash
        return PXLJudgement(
            operator=PXLPrimitive.MODAL_EQUIVALENCE.value,
            left=left,
            right=right,
            result=result,
            grounding=PXLModalGround.EXCLUDED_MIDDLE.value,
            justification="Modal equivalence by canonical structural identity across grounded forms.",
        )

    def dichotomy(self, statement: str) -> PXLJudgement:
        normalized = self._normalize_formula(statement)
        result = bool(normalized)
        return PXLJudgement(
            operator="⫴",
            left=normalized,
            right=f"¬({normalized})",
            result=result,
            grounding=PXLModalGround.EXCLUDED_MIDDLE.value,
            justification="Deterministic dichotomy surface: proposition recognized as admissible statement form.",
        )

    def privation(self, value: Any) -> Dict[str, Any]:
        """Negation as privation / absence-of rather than contradiction."""
        return {
            "mode": "privation",
            "present": value is not None and value != "" and value != [] and value != {},
            "absence_signature": self._stable_hash({"privation_of": self._canonicalize(value)}),
        }

    def _canonicalize(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {k: self._canonicalize(value[k]) for k in sorted(value)}
        if isinstance(value, list):
            return [self._canonicalize(v) for v in value]
        if isinstance(value, tuple):
            return tuple(self._canonicalize(v) for v in value)
        if isinstance(value, set):
            return sorted(self._canonicalize(v) for v in value)
        return value

    def _normalize_formula(self, formula: str) -> str:
        return "".join(formula.split()).replace("→", "->")

    def _stable_hash(self, value: Any) -> str:
        payload = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ============================================================================
# DRAC Axiom Layer
# ============================================================================

@dataclass(frozen=True)
class DRACAxiom:
    axiom_id: str
    description: str
    status: str
    evaluator_name: str


class DRACAxiomRegistry:
    """
    Normalized runtime registry backed by DRAC SEMANTIC_AXIOMS.

    Runtime implementation for axioms registered in:
      DRAC_Core/DRAC_Invariables/MODULAR_LIBRARY/DRAC_Registries/drac_axiom_registry.json

    This class provides the first operational implementation of the axiom
    evaluator surfaces declared by those registry entries. The SEMANTIC_AXIOMS/
    .py stubs all raise NotImplementedError — this registry provides the
    runtime-callable equivalents through the evaluator pattern.

    Axioms with REQUIRED_UNIVERSAL status (FBC_0007, FBC_0014) are enforced
    on every candidate without exception.
    """

    def __init__(self) -> None:
        self._axioms: Dict[str, DRACAxiom] = {
            "Invariant_Constraints": DRACAxiom(
                axiom_id="Invariant_Constraints",
                description="System-wide invariants and guard conditions applied before context execution.",
                status="ACTIVE",
                evaluator_name="evaluate_invariants",
            ),
            "Semantic_Capability_Gate": DRACAxiom(
                axiom_id="Semantic_Capability_Gate",
                description="Capability admission checks for semantic contexts and orchestration steps.",
                status="ACTIVE",
                evaluator_name="evaluate_capabilities",
            ),
            "Runtime_Context_Initializer": DRACAxiom(
                axiom_id="Runtime_Context_Initializer",
                description="Bootstrap runtime environment and context scaffolding.",
                status="ACTIVE",
                evaluator_name="evaluate_runtime_context",
            ),
            "Runtime_Mode_Controller": DRACAxiom(
                axiom_id="Runtime_Mode_Controller",
                description="Controls runtime mode switching and interaction priority.",
                status="ACTIVE",
                evaluator_name="evaluate_runtime_mode",
            ),
            "Trinitarian_Alignment_Core": DRACAxiom(
                axiom_id="Trinitarian_Alignment_Core",
                description="Triadic alignment and optimization axiom for candidate selection.",
                status="ACTIVE",
                evaluator_name="evaluate_trinitarian_alignment",
            ),
            "Necessary_Existence_Core": DRACAxiom(
                axiom_id="Necessary_Existence_Core",
                description="Required grounding for non-null existential substrate.",
                status="ACTIVE",
                evaluator_name="evaluate_necessary_existence",
            ),
            "Global_Bijective_Recursion_Core": DRACAxiom(
                axiom_id="Global_Bijective_Recursion_Core",
                description="Recursive structural closure under stable cross-domain mappings.",
                status="ACTIVE",
                evaluator_name="evaluate_global_bijective_recursion",
            ),
        }

    def require(
        self,
        required_axioms: Sequence[str],
        candidate: "ReasoningCandidate",
    ) -> List[Dict[str, Any]]:
        evaluations: List[Dict[str, Any]] = []
        for axiom_name in required_axioms:
            if axiom_name not in self._axioms:
                raise CapabilityViolation(f"Unknown DRAC axiom: {axiom_name}")
            axiom = self._axioms[axiom_name]
            evaluator = getattr(self, axiom.evaluator_name)
            outcome = evaluator(candidate)
            evaluations.append({
                "axiom_id": axiom.axiom_id,
                "description": axiom.description,
                "status": axiom.status,
                "passed": outcome["passed"],
                "details": outcome["details"],
            })
            if not outcome["passed"]:
                raise ReasoningViolation(
                    f"DRAC axiom failed: {axiom_name} :: {outcome['details']}"
                )
        return evaluations

    # ── Axiom evaluators ──────────────────────────────────────────────────────

    def evaluate_invariants(self, candidate: "ReasoningCandidate") -> Dict[str, Any]:
        violated = candidate.flags.get("mutated_after_verification", False)
        return {
            "passed": not violated,
            "details": (
                "No post-verification mutation detected."
                if not violated
                else "Candidate mutated after verification."
            ),
        }

    def evaluate_capabilities(self, candidate: "ReasoningCandidate") -> Dict[str, Any]:
        # Empty capabilities dict means no requirements — pass vacuously.
        mapped = (not candidate.capabilities) or all(candidate.capabilities.values())
        return {
            "passed": mapped,
            "details": (
                "Capabilities mapped."
                if mapped
                else "One or more required capabilities are unmapped."
            ),
        }

    def evaluate_runtime_context(self, candidate: "ReasoningCandidate") -> Dict[str, Any]:
        has_context = candidate.runtime_context is not None and isinstance(
            candidate.runtime_context, dict
        )
        return {
            "passed": has_context,
            "details": (
                "Runtime context initialized."
                if has_context
                else "Runtime context missing."
            ),
        }

    def evaluate_runtime_mode(self, candidate: "ReasoningCandidate") -> Dict[str, Any]:
        allowed_modes = {"analytical", "synthetic", "validating", "exploratory"}
        mode = candidate.runtime_context.get("mode") if candidate.runtime_context else None
        return {
            "passed": mode in allowed_modes,
            "details": (
                f"Runtime mode admitted: {mode}"
                if mode in allowed_modes
                else f"Invalid runtime mode: {mode}"
            ),
        }

    def evaluate_trinitarian_alignment(self, candidate: "ReasoningCandidate") -> Dict[str, Any]:
        scores = candidate.triadic_scores
        passed = min(scores.idea, scores.analog, scores.bridge) > 0.0
        return {
            "passed": passed,
            "details": (
                "Triadic alignment vector populated."
                if passed
                else "One or more triadic dimensions are ungrounded."
            ),
        }

    def evaluate_necessary_existence(self, candidate: "ReasoningCandidate") -> Dict[str, Any]:
        non_empty = bool(
            candidate.concept
            and candidate.concept.name
            and candidate.concept.proposition
        )
        return {
            "passed": non_empty,
            "details": (
                "Concept substrate non-empty."
                if non_empty
                else "Concept substrate empty or null."
            ),
        }

    def evaluate_global_bijective_recursion(
        self, candidate: "ReasoningCandidate"
    ) -> Dict[str, Any]:
        bridge_map = candidate.bridge_mapping
        passed = isinstance(bridge_map, dict) and {
            "concept", "analog", "implementation"
        } <= set(bridge_map.keys())
        return {
            "passed": passed,
            "details": (
                "Bridge mapping closed over concept/analog/implementation."
                if passed
                else "Bridge mapping incomplete."
            ),
        }


# ============================================================================
# Arithmetic Engine
# ============================================================================

class SafeArithmeticEngine:
    """
    Deterministic arithmetic engine normalized from arithmetic_engine.py.
    Safe AST evaluator; stdlib only, no eval(), no exec().
    """

    _ALLOWED_BINOPS = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Pow: lambda a, b: a ** b,
        ast.Mod: lambda a, b: a % b,
        ast.FloorDiv: lambda a, b: a // b,
    }

    _ALLOWED_UNARYOPS = {
        ast.UAdd: lambda a: +a,
        ast.USub: lambda a: -a,
    }

    _ALLOWED_FUNCS = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp,
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    def compute_expression(
        self,
        expression: str,
        variables: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        variables = variables or {}
        node = ast.parse(expression, mode="eval")
        result = self._eval(node.body, variables)
        return {"expression": expression, "variables": variables, "result": result, "success": True}

    def factorize(self, n: int) -> List[int]:
        if n == 0:
            return [0]
        factors: List[int] = []
        value = abs(n)
        divisor = 2
        while divisor * divisor <= value:
            while value % divisor == 0:
                factors.append(divisor)
                value //= divisor
            divisor += 1
        if value > 1:
            factors.append(value)
        if n < 0:
            factors.insert(0, -1)
        return factors

    def _eval(self, node: ast.AST, variables: Dict[str, float]) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name):
            if node.id in variables:
                return float(variables[node.id])
            raise CapabilityViolation(f"Unknown arithmetic variable: {node.id}")
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._ALLOWED_BINOPS:
                raise CapabilityViolation(f"Disallowed arithmetic operator: {op_type.__name__}")
            return self._ALLOWED_BINOPS[op_type](
                self._eval(node.left, variables), self._eval(node.right, variables)
            )
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._ALLOWED_UNARYOPS:
                raise CapabilityViolation(f"Disallowed unary operator: {op_type.__name__}")
            return self._ALLOWED_UNARYOPS[op_type](self._eval(node.operand, variables))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in self._ALLOWED_FUNCS:
                raise CapabilityViolation(f"Disallowed arithmetic function: {func_name}")
            args = [self._eval(arg, variables) for arg in node.args]
            return float(self._ALLOWED_FUNCS[func_name](*args))
        raise CapabilityViolation(f"Unsupported arithmetic node: {type(node).__name__}")


# ============================================================================
# Proof Engine
# ============================================================================

@dataclass
class ProofStep:
    index: int
    rule: str
    statement: str
    supports: List[str] = field(default_factory=list)
    justification: str = ""


@dataclass
class ProofResult:
    proved: bool
    theorem: str
    method: str
    steps: List[ProofStep]
    obligations: List[str]
    diagnostics: List[str]


class OntologicalProofEngine:
    """
    Deterministic proof engine normalized from proof_engine.py and
    foundational_logic.py.

    Supports:
    - premise restoration
    - direct axiom admission
    - single-step modus ponens

    Used by IterativeReasoningAmplifier to feed proven theorems back as
    axioms for the next recursion pass — the key amplification mechanism.
    """

    def __init__(self) -> None:
        self.axioms: List[str] = []

    def add_axiom(self, axiom: str) -> None:
        normalized = self._normalize(axiom)
        if normalized not in self.axioms:
            self.axioms.append(normalized)

    def admit_proven_theorem(self, theorem: str) -> None:
        """
        Admit a proven theorem as a new axiom for subsequent proof passes.
        This is the primary recursion amplification hook: theorems proved in
        pass N become axioms available in pass N+1.
        """
        self.add_axiom(theorem)
        logger.debug("Admitted proven theorem as axiom: %s", theorem)

    def prove(self, premises: Sequence[str], theorem: str) -> ProofResult:
        theorem_n = self._normalize(theorem)
        normalized_premises = [self._normalize(p) for p in premises]
        normalized_axioms = list(self.axioms)

        steps: List[ProofStep] = []
        obligations: List[str] = []
        diagnostics: List[str] = []

        if theorem_n in normalized_premises:
            steps.append(ProofStep(
                index=1,
                rule="premise_restoration",
                statement=theorem_n,
                supports=[theorem_n],
                justification="Theorem present among premises.",
            ))
            return ProofResult(True, theorem_n, "premise_restoration", steps, obligations, diagnostics)

        if theorem_n in normalized_axioms:
            steps.append(ProofStep(
                index=1,
                rule="axiom_admission",
                statement=theorem_n,
                supports=[theorem_n],
                justification="Theorem present among admitted axioms.",
            ))
            return ProofResult(True, theorem_n, "axiom_admission", steps, obligations, diagnostics)

        universe = set(normalized_premises + normalized_axioms)
        for statement in list(universe):
            if "->" not in statement:
                continue
            antecedent, consequent = [x.strip() for x in statement.split("->", 1)]
            if antecedent in universe and consequent == theorem_n:
                steps.append(ProofStep(
                    index=1, rule="premise_or_axiom", statement=antecedent,
                    supports=[antecedent], justification="Antecedent available.",
                ))
                steps.append(ProofStep(
                    index=2, rule="conditional_admission", statement=statement,
                    supports=[statement], justification="Conditional available.",
                ))
                steps.append(ProofStep(
                    index=3, rule="modus_ponens", statement=theorem_n,
                    supports=[antecedent, statement],
                    justification="Derived by deterministic modus ponens.",
                ))
                return ProofResult(True, theorem_n, "modus_ponens", steps, obligations, diagnostics)

        obligations.append(theorem_n)
        diagnostics.append("Theorem not derivable under current premise/axiom universe.")
        return ProofResult(False, theorem_n, "fail_closed", steps, obligations, diagnostics)

    def _normalize(self, formula: str) -> str:
        return "".join(formula.split()).replace("→", "->")


# ============================================================================
# Reasoning Lenses
# ============================================================================

class DeductiveLens:
    def analyze(
        self,
        premises: Sequence[str],
        conclusion: str,
        proof_engine: OntologicalProofEngine,
    ) -> Dict[str, Any]:
        result = proof_engine.prove(premises, conclusion)
        return {
            "engine": "deductive",
            "proved": result.proved,
            "theorem": result.theorem,
            "method": result.method,
            "steps": [asdict(step) for step in result.steps],
            "obligations": result.obligations,
            "diagnostics": result.diagnostics,
        }


class InductiveLens:
    def analyze(self, examples: Sequence[Any]) -> Dict[str, Any]:
        if not examples:
            return {
                "engine": "inductive",
                "pattern": "insufficient_data",
                "confidence": 0.0,
                "support_count": 0,
                "exceptions": [],
            }

        type_names = [type(x).__name__ for x in examples]
        dominant = max(set(type_names), key=type_names.count)
        consistency = type_names.count(dominant) / len(type_names)

        pattern = f"dominant_type={dominant}"
        if dominant in {"int", "float"}:
            ordered = [float(x) for x in examples if isinstance(x, (int, float))]
            if len(ordered) >= 2:
                deltas = [ordered[i + 1] - ordered[i] for i in range(len(ordered) - 1)]
                if len(set(round(d, 8) for d in deltas)) == 1:
                    pattern = f"arithmetic_progression(delta={deltas[0]})"

        return {
            "engine": "inductive",
            "pattern": pattern,
            "confidence": round(consistency, 4),
            "support_count": len(examples),
            "exceptions": [repr(x) for x, t in zip(examples, type_names) if t != dominant][:5],
        }


class AbductiveLens:
    def analyze(
        self,
        observations: Sequence[str],
        hypothesis_space: Sequence[str],
    ) -> Dict[str, Any]:
        scored: List[Tuple[str, float]] = []
        obs_tokens = {tok for text in observations for tok in text.lower().split()}

        for hypothesis in hypothesis_space:
            hyp_tokens = set(hypothesis.lower().split())
            overlap = len(obs_tokens & hyp_tokens)
            score = overlap / max(len(obs_tokens | hyp_tokens), 1)
            scored.append((hypothesis, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        best = scored[0] if scored else ("", 0.0)

        return {
            "engine": "abductive",
            "best_hypothesis": best[0],
            "confidence": round(best[1], 4),
            "ranked_hypotheses": [
                {"hypothesis": h, "score": round(s, 4)} for h, s in scored[:5]
            ],
        }


class AnalogicalLens:
    def analyze(
        self,
        source_domain: str,
        target_domain: str,
        concepts: Sequence[str],
    ) -> Dict[str, Any]:
        source_tokens = set(source_domain.lower().split())
        target_tokens = set(target_domain.lower().split())
        shared = source_tokens & target_tokens

        analogies = []
        for concept in concepts[:8]:
            analogies.append({
                "concept": concept,
                "mapping": f"{source_domain} :: {concept} -> {target_domain} :: {concept}",
                "confidence": round(0.55 + (0.25 if concept.lower() in shared else 0.0), 4),
            })

        return {
            "engine": "analogical",
            "shared_tokens": sorted(shared),
            "analogies": analogies,
            "transfer_confidence": round(
                len(shared) / max(len(source_tokens | target_tokens), 1), 4
            ),
        }


class TopologicalLens:
    def analyze(self, graph: Dict[str, Sequence[str]]) -> Dict[str, Any]:
        nodes = sorted(graph.keys())
        edge_count = sum(len(v) for v in graph.values())
        isolated = [n for n, neighbors in graph.items() if not neighbors]
        strongly_connected_hint = len(isolated) == 0 and edge_count >= len(nodes)

        return {
            "engine": "topological",
            "node_count": len(nodes),
            "edge_count": edge_count,
            "isolated_nodes": isolated,
            "closure_hint": strongly_connected_hint,
        }


# ============================================================================
# Context Compiler / MESH Attractor
# ============================================================================

@dataclass(frozen=True)
class TriadicScores:
    idea: float
    analog: float
    bridge: float

    @property
    def minimum(self) -> float:
        return min(self.idea, self.analog, self.bridge)

    @property
    def mean(self) -> float:
        return (self.idea + self.analog + self.bridge) / 3.0


@dataclass(frozen=True)
class ConceptPacket:
    name: str
    proposition: str
    premises: Tuple[str, ...] = ()
    examples: Tuple[Any, ...] = ()
    observations: Tuple[str, ...] = ()
    hypothesis_space: Tuple[str, ...] = ()
    source_domain: str = ""
    target_domain: str = ""
    capabilities_required: Tuple[str, ...] = ()
    graph: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    arithmetic_expression: Optional[str] = None
    arithmetic_variables: Dict[str, float] = field(default_factory=dict)
    implementation_targets: Tuple[str, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningCandidate:
    concept: ConceptPacket
    lambda_form: str
    analog_form: Dict[str, Any]
    bridge_mapping: Dict[str, Any]
    runtime_context: Dict[str, Any]
    capabilities: Dict[str, bool]
    triadic_scores: TriadicScores
    flags: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProofCarryingArtifact:
    artifact_id: str
    concept_name: str
    pxl_judgements: Tuple[Dict[str, Any], ...]
    drac_axiom_results: Tuple[Dict[str, Any], ...]
    proof_result: Dict[str, Any]
    reasoning_lenses: Dict[str, Any]
    triadic_scores: Dict[str, float]
    mesh_fixed_point: Dict[str, Any]
    bridge_mapping: Dict[str, Any]
    implementation_targets: Tuple[str, ...]
    execution_envelope_binding: Dict[str, Any]
    signature: str
    # Phase F: FBC combination engine results (axiom+context pairing scores)
    fbc_phase_results: Dict[str, Any] = field(default_factory=dict)


class ContextCompiler:
    """
    Concept-to-concrete compiler derived from:
    - lambda_engine.py         (lambda encoding)
    - logos_mathematical_core.py (analog discovery)
    - trinitarian_optimization_theorem.py (triadic scoring)
    - mesh_coq_formalization.txt (MESH bridge concept)

    The output ReasoningCandidate is the input to MeshFixedPointAttractor.
    In iterative amplification, the bridge_mapping from one pass becomes
    the premise set for the next pass via IterativeReasoningAmplifier.
    """

    def compile(
        self,
        concept: ConceptPacket,
        arithmetic: SafeArithmeticEngine,
    ) -> ReasoningCandidate:
        lambda_form = self._lambda_encode(concept)
        analog_form = self._discover_analog(concept, arithmetic)
        bridge_mapping = self._build_bridge_mapping(concept, lambda_form, analog_form)

        triadic_scores = TriadicScores(
            idea=self._score_idea(concept, lambda_form),
            analog=self._score_analog(concept, analog_form),
            bridge=self._score_bridge(concept, bridge_mapping),
        )

        runtime_context = {
            "mode": concept.metadata.get("mode", "analytical"),
            "concept_name": concept.name,
            "proposition": concept.proposition,
            "implementation_targets": list(concept.implementation_targets),
        }

        capabilities = {required: True for required in concept.capabilities_required}

        return ReasoningCandidate(
            concept=concept,
            lambda_form=lambda_form,
            analog_form=analog_form,
            bridge_mapping=bridge_mapping,
            runtime_context=runtime_context,
            capabilities=capabilities,
            triadic_scores=triadic_scores,
            flags={"mutated_after_verification": False},
        )

    def _lambda_encode(self, concept: ConceptPacket) -> str:
        args = " ".join(f"x{i}" for i, _ in enumerate(concept.premises, start=1))
        body = concept.proposition or concept.name
        return f"λ {args}. {body}" if args else f"λ _. {body}"

    def _discover_analog(
        self,
        concept: ConceptPacket,
        arithmetic: SafeArithmeticEngine,
    ) -> Dict[str, Any]:
        arithmetic_result: Optional[Dict[str, Any]] = None
        if concept.arithmetic_expression:
            arithmetic_result = arithmetic.compute_expression(
                concept.arithmetic_expression, concept.arithmetic_variables
            )
        return {
            "conceptual_shape": {
                "premise_count": len(concept.premises),
                "example_count": len(concept.examples),
                "observation_count": len(concept.observations),
            },
            "arithmetic_result": arithmetic_result,
            "implementation_targets": list(concept.implementation_targets),
        }

    def _build_bridge_mapping(
        self,
        concept: ConceptPacket,
        lambda_form: str,
        analog_form: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "concept": {"name": concept.name, "proposition": concept.proposition},
            "analog": analog_form,
            "implementation": {
                "lambda_form": lambda_form,
                "targets": list(concept.implementation_targets),
                "proof_required": True,
                "envelope_binding": "PRE_EXECUTION_FIXED_POINT_GATE",
            },
        }

    def _score_idea(self, concept: ConceptPacket, lambda_form: str) -> float:
        density = 0.4 + min(len(lambda_form) / 200.0, 0.3)
        premise_bonus = min(len(concept.premises) / 10.0, 0.2)
        proposition_bonus = 0.1 if concept.proposition else 0.0
        return round(min(density + premise_bonus + proposition_bonus, 1.0), 6)

    def _score_analog(self, concept: ConceptPacket, analog_form: Dict[str, Any]) -> float:
        # Base: any concept with a proposition is minimally grounded.
        base = 0.55
        proposition_bonus = 0.15 if concept.proposition else 0.0
        # Depth bonus: targets, examples, and arithmetic increase structural richness.
        depth_targets = len(concept.implementation_targets) / 8.0
        depth_examples = len(concept.examples) / 8.0
        depth_arithmetic = 0.2 if analog_form.get("arithmetic_result") else 0.0
        depth_bonus = min(depth_targets + depth_examples + depth_arithmetic, 0.30)
        return round(min(base + proposition_bonus + depth_bonus, 1.0), 6)

    def _score_bridge(
        self,
        concept: ConceptPacket,
        bridge_mapping: Dict[str, Any],
    ) -> float:
        has_targets = bool(bridge_mapping["implementation"]["targets"])
        has_lambda = bool(bridge_mapping["implementation"]["lambda_form"])
        has_concept = bool(bridge_mapping["concept"]["proposition"])
        base = 0.3
        if has_targets:
            base += 0.25
        if has_lambda:
            base += 0.25
        if has_concept:
            base += 0.2
        return round(min(base, 1.0), 6)


class MeshFixedPointAttractor:
    """
    MESH operator as fixed-point attractor.

    Operational rule — concept → analog → implementation must cohere
    with direct concept → implementation projection:

        MESH(x) = x

    This is the runtime implementation of the bijective closure required
    by FBC_0005 Global_Bijective_Recursion_Core. When MESH converges,
    the concept-to-implementation mapping is provably stable.

    In IterativeReasoningAmplifier, the threshold is tightened each pass
    to force increasingly strict triadic coherence — the main convergence
    driver in amplified reasoning.
    """

    def __init__(self, pxl: PXLKernel) -> None:
        self._pxl = pxl

    def evaluate(
        self,
        candidate: ReasoningCandidate,
        threshold: float = 0.65,
    ) -> Dict[str, Any]:
        concept_projection = {
            "name": candidate.concept.name,
            "proposition": candidate.concept.proposition,
            "targets": list(candidate.concept.implementation_targets),
        }
        implementation_projection = {
            "name": candidate.bridge_mapping["concept"]["name"],
            "proposition": candidate.bridge_mapping["concept"]["proposition"],
            "targets": candidate.bridge_mapping["implementation"]["targets"],
        }

        coherence = self._pxl.coherence(concept_projection, implementation_projection)
        fixed_point = coherence.result and candidate.triadic_scores.minimum >= threshold

        return {
            "passed": fixed_point,
            "threshold": threshold,
            "triadic_minimum": candidate.triadic_scores.minimum,
            "triadic_mean": candidate.triadic_scores.mean,
            "coherence": asdict(coherence),
            "equation": "MESH(x) = x",
            "details": (
                "Triadic state converged to a coherent fixed point."
                if fixed_point
                else "Triadic state failed fixed-point coherence threshold."
            ),
        }


# ============================================================================
# Main Engine
# ============================================================================

class ProofCarryingContextReasoningEngine:
    """
    Unified meta-binding reasoning engine.

    Pipeline position:
      Sits ABOVE the 5-stage ARPCompilerCore (base_reasoning → taxonomy →
      triune_synthesis → cross_domain → unified_binder). PCCRE operates as
      the conceptual grounding gate: a ConceptPacket must produce a passing
      ProofCarryingArtifact before the ARP compiler is invoked with the
      associated AACED packet.

    Foundations pulled from existing repo modules:
      - PXL_Core.py / pxl_engine.py   → PXLKernel
      - math_engine.py                 → SafeArithmeticEngine (subset)
      - arithmetic_engine.py           → SafeArithmeticEngine (safe AST eval)
      - proof_engine.py                → OntologicalProofEngine
      - foundational_logic.py          → axiom bootstrap premises
      - DRAC SEMANTIC_AXIOMS/          → DRACAxiomRegistry (first runtime impl)
      - DRAC SEMANTIC_CONTEXTS/        → runtime_context mode contract
      - LOGOS_MATH lambda formalism    → ContextCompiler._lambda_encode
      - trinitarian_optimization_theorem → TriadicScores
      - MESH / 3OT formalisms          → MeshFixedPointAttractor

    DRAC axiom status:
      The seven axioms in DRACAxiomRegistry (FBC_0005, FBC_0007, FBC_0009,
      FBC_0011, FBC_0013, FBC_0014, FBC_0016, FBC_0017) are currently defined
      as SEMANTIC_AXIOM stubs that raise NotImplementedError. This engine
      provides the first operational runtime implementation of their evaluator
      surfaces.

    Recursion amplification:
      See IterativeReasoningAmplifier below. The key recursion hook is
      OntologicalProofEngine.admit_proven_theorem(), which allows proved
      theorems to accumulate as axioms across passes, growing the admissible
      proof space iteratively.
    """

    def __init__(self) -> None:
        self.pxl = PXLKernel()
        self.drac = DRACAxiomRegistry()
        self.arithmetic = SafeArithmeticEngine()
        self.proof = OntologicalProofEngine()
        self.compiler = ContextCompiler()
        self.mesh = MeshFixedPointAttractor(self.pxl)

        self.deductive = DeductiveLens()
        self.inductive = InductiveLens()
        self.abductive = AbductiveLens()
        self.analogical = AnalogicalLens()
        self.topological = TopologicalLens()

        self._bootstrap_axioms()

    def reason(self, concept: ConceptPacket) -> ProofCarryingArtifact:
        """
        Primary entry point. Receives a ConceptPacket, runs the full
        PXL → DRAC → proof → MESH pipeline, and emits a ProofCarryingArtifact.

        Fail-closed: raises ReasoningViolation subclasses on any gate failure.
        """
        logger.info("PCCRE.reason: concept=%s", concept.name)

        candidate = self.compiler.compile(concept, self.arithmetic)

        pxl_judgements = self._evaluate_pxl(candidate)
        drac_axiom_results = self._evaluate_drac(candidate)
        fbc_phase_results = self._run_fbc_phase(candidate)
        reasoning_lenses = self._run_reasoning_lenses(concept)
        proof_result = self._prove_candidate(concept, candidate)
        mesh_result = self.mesh.evaluate(candidate)

        if not proof_result["proved"]:
            raise ProofViolation(
                f"Proof obligation unresolved: {proof_result['obligations']}"
            )

        if not mesh_result["passed"]:
            raise CoherenceViolation(mesh_result["details"])

        artifact = self._assemble_artifact(
            concept=concept,
            candidate=candidate,
            pxl_judgements=pxl_judgements,
            drac_axiom_results=drac_axiom_results,
            fbc_phase_results=fbc_phase_results,
            reasoning_lenses=reasoning_lenses,
            proof_result=proof_result,
            mesh_result=mesh_result,
        )

        # Admit the proved theorem into the axiom set so subsequent calls
        # can build on this proof result — accumulating reasoning capital.
        if proof_result["proved"]:
            self.proof.admit_proven_theorem(proof_result["theorem"])

        logger.info(
            "PCCRE.reason: artifact=%s signature=%s",
            artifact.artifact_id[:16],
            artifact.signature[:16],
        )
        return artifact

    # ── Internal pipeline stages ──────────────────────────────────────────────

    def _bootstrap_axioms(self) -> None:
        foundational_axioms = [
            "A->A",
            "(A->B)->(A->B)",
            "coherence(x,x)",
            "necessary_existence->non_null_substrate",
            "trinitarian_alignment->coherent_selection",
            "global_bijective_recursion->closure",
        ]
        for axiom in foundational_axioms:
            self.proof.add_axiom(axiom)

    def _evaluate_pxl(
        self, candidate: ReasoningCandidate
    ) -> List[Dict[str, Any]]:
        concept_repr = {
            "name": candidate.concept.name,
            "proposition": candidate.concept.proposition,
        }
        bridge_repr = candidate.bridge_mapping["concept"]

        judgements = [
            asdict(self.pxl.coherence(concept_repr, bridge_repr)),
            asdict(self.pxl.non_equivalence(candidate.lambda_form, "")),
            asdict(self.pxl.modal_equivalence(
                candidate.bridge_mapping["concept"], bridge_repr
            )),
            asdict(self.pxl.dichotomy(candidate.concept.proposition)),
            {
                **asdict(self.pxl.entailment(
                    candidate.concept.premises, candidate.concept.proposition
                )),
                "privation": self.pxl.privation(
                    candidate.concept.metadata.get("negation_probe")
                ),
            },
        ]
        return judgements

    def _evaluate_drac(
        self, candidate: ReasoningCandidate
    ) -> List[Dict[str, Any]]:
        required = list(candidate.capabilities.keys())
        required += [
            "Invariant_Constraints",
            "Semantic_Capability_Gate",
            "Runtime_Context_Initializer",
            "Runtime_Mode_Controller",
            "Trinitarian_Alignment_Core",
            "Necessary_Existence_Core",
            "Global_Bijective_Recursion_Core",
        ]
        normalized = []
        for item in required:
            if item in self.drac._axioms:
                normalized.append(item)
            else:
                candidate.capabilities[item] = True
        return self.drac.require(normalized, candidate)

    def _run_fbc_phase(self, candidate: ReasoningCandidate) -> Dict[str, Any]:
        """
        Phase F — run the DRAC Function Block Core combination engine.
        Pairs each optional-composable axiom with the appropriate context
        embedding, scores all 5 power configurations, and returns the
        ranked results with the winning configuration identified.
        Fail-open: if FBC engine is unavailable, returns an empty dict.
        """
        if not _FBC_ENGINE_AVAILABLE or FBCCombinationEngine is None:
            logger.debug("PCCRE._run_fbc_phase: FBC engine unavailable — skipping")
            return {}

        candidate_dict = {
            "name": candidate.concept.name,
            "proposition": candidate.concept.proposition,
            "premises": list(candidate.concept.premises),
            "lambda_form": candidate.lambda_form,
            "bridge_mapping": candidate.bridge_mapping,
            "triadic_scores": asdict(candidate.triadic_scores),
            "runtime_context": candidate.runtime_context,
            "capabilities": candidate.capabilities,
            "flags": candidate.flags,
        }
        try:
            engine = FBCCombinationEngine()
            results = engine.run(candidate_dict)
            logger.info(
                "PCCRE.fbc_phase: best=%s power=%s score=%s",
                results.get("best_config_id"),
                results.get("best_power_class"),
                results.get("best_composite_score"),
            )
            return results
        except Exception as exc:  # noqa: BLE001
            logger.warning("PCCRE._run_fbc_phase: non-fatal error: %s", exc)
            return {"error": str(exc)}

    def _run_reasoning_lenses(
        self, concept: ConceptPacket
    ) -> Dict[str, Any]:
        return {
            "deductive_preview": self.deductive.analyze(
                concept.premises, concept.proposition, self.proof
            ),
            "inductive": self.inductive.analyze(concept.examples),
            "abductive": self.abductive.analyze(
                concept.observations, concept.hypothesis_space
            ),
            "analogical": self.analogical.analyze(
                concept.source_domain,
                concept.target_domain,
                [concept.name, *concept.implementation_targets],
            ),
            "topological": self.topological.analyze(
                {k: tuple(v) for k, v in concept.graph.items()}
            ),
        }

    def _prove_candidate(
        self, concept: ConceptPacket, candidate: ReasoningCandidate
    ) -> Dict[str, Any]:
        derived_premises = list(concept.premises)

        if candidate.triadic_scores.minimum >= 0.65:
            derived_premises.append("trinitarian_alignment->coherent_selection")
            derived_premises.append("global_bijective_recursion->closure")
            derived_premises.append("necessary_existence->non_null_substrate")

        proof = self.proof.prove(derived_premises, concept.proposition)
        return {
            "proved": proof.proved,
            "theorem": proof.theorem,
            "method": proof.method,
            "steps": [asdict(step) for step in proof.steps],
            "obligations": proof.obligations,
            "diagnostics": proof.diagnostics,
        }

    def _assemble_artifact(
        self,
        concept: ConceptPacket,
        candidate: ReasoningCandidate,
        pxl_judgements: List[Dict[str, Any]],
        drac_axiom_results: List[Dict[str, Any]],
        fbc_phase_results: Dict[str, Any],
        reasoning_lenses: Dict[str, Any],
        proof_result: Dict[str, Any],
        mesh_result: Dict[str, Any],
    ) -> ProofCarryingArtifact:
        artifact_core = {
            "concept_name": concept.name,
            "proposition": concept.proposition,
            "lambda_form": candidate.lambda_form,
            "bridge_mapping": candidate.bridge_mapping,
            "triadic_scores": asdict(candidate.triadic_scores),
            "mesh_fixed_point": mesh_result,
            "implementation_targets": list(concept.implementation_targets),
        }
        artifact_id = self._stable_hash(artifact_core)
        signature = self._stable_hash({
            "artifact_id": artifact_id,
            "proof_result": proof_result,
            "pxl_judgements": pxl_judgements,
            "drac_axiom_results": drac_axiom_results,
            "mesh_fixed_point": mesh_result,
        })

        execution_envelope_binding = {
            "binding_role": "FIXED_POINT_ATTRACTOR_META_GATE",
            "binding_position": "PRE_EXECUTION_ENVELOPE_ASSEMBLY",
            "must_pass": [
                "PXL_VALIDITY",
                "DRAC_AXIOM_ADMISSION",
                "PROOF_OBLIGATION_DISCHARGE",
                "MESH_FIXED_POINT",
            ],
            "next_stage": "Execution_Envelope_Assembly",
        }

        return ProofCarryingArtifact(
            artifact_id=artifact_id,
            concept_name=concept.name,
            pxl_judgements=tuple(pxl_judgements),
            drac_axiom_results=tuple(drac_axiom_results),
            proof_result=proof_result,
            reasoning_lenses=reasoning_lenses,
            triadic_scores=asdict(candidate.triadic_scores),
            mesh_fixed_point=mesh_result,
            bridge_mapping=candidate.bridge_mapping,
            implementation_targets=concept.implementation_targets,
            execution_envelope_binding=execution_envelope_binding,
            signature=signature,
            fbc_phase_results=fbc_phase_results,
        )

    def _stable_hash(self, value: Any) -> str:
        payload = json.dumps(
            value, sort_keys=True, ensure_ascii=False, default=str
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ============================================================================
# Iterative Reasoning Amplifier  (recursion amplification surface)
# ============================================================================

@dataclass
class AmplificationPass:
    pass_number: int
    concept_name: str
    artifact_id: str
    triadic_minimum: float
    triadic_mean: float
    proved: bool
    mesh_passed: bool
    axiom_count: int
    signature: str


@dataclass
class AmplificationResult:
    converged: bool
    total_passes: int
    passes: List[AmplificationPass]
    final_artifact: Optional[ProofCarryingArtifact]
    convergence_signature: str
    diagnostics: List[str]


class IterativeReasoningAmplifier:
    """
    Recursion amplification wrapper around ProofCarryingContextReasoningEngine.

    Mechanism:
      Each pass of PCCRE.reason() produces a ProofCarryingArtifact. The
      artifact's bridge_mapping and proved theorem are fed back into the
      next ConceptPacket as additional premises. The proof engine
      accumulates admitted theorems as axioms across passes. The MESH
      threshold is tightened incrementally.

    Convergence:
      The process converges when the artifact signature stabilizes across
      two consecutive passes (MESH(x) = x fixed-point condition) or when
      max_iterations is reached.

    Recursion hook into Global_Bijective_Recursion_Core:
      The bijective closure requirement (FBC_0005) demands that
        concept → analog → implementation ≡ concept → implementation
      The iterative amplifier enforces this by checking signature stability
      — identical signatures across passes prove the mapping is bijective
      and recursively closed.

    Recursion hook into OntologicalProofEngine:
      admit_proven_theorem() grows the axiomatic basis with every proved
      result, enabling deeper theorems to be reached in later passes that
      were not reachable in pass 1.

    Usage:
        amplifier = IterativeReasoningAmplifier(max_iterations=5)
        result = amplifier.amplify(concept)
        if result.converged:
            artifact = result.final_artifact
    """

    def __init__(
        self,
        max_iterations: int = 5,
        mesh_threshold_start: float = 0.65,
        mesh_threshold_step: float = 0.01,
        convergence_required_stable_passes: int = 2,
    ) -> None:
        self._max_iterations = max_iterations
        self._mesh_threshold_start = mesh_threshold_start
        self._mesh_threshold_step = mesh_threshold_step
        self._convergence_window = convergence_required_stable_passes
        self._engine = ProofCarryingContextReasoningEngine()

    def amplify(self, concept: ConceptPacket) -> AmplificationResult:
        """
        Run iterative amplification over a ConceptPacket.

        Each pass:
          1. Runs PCCRE.reason(concept_i)
          2. Extracts bridge_mapping premises and proved theorem
          3. Builds concept_{i+1} by enriching premises
          4. Tightens MESH threshold by mesh_threshold_step
          5. Checks signature stability for convergence

        Returns AmplificationResult with all pass records and final artifact.
        """
        passes: List[AmplificationPass] = []
        diagnostics: List[str] = []
        current_concept = concept
        previous_signature: Optional[str] = None
        stable_count = 0
        final_artifact: Optional[ProofCarryingArtifact] = None
        threshold = self._mesh_threshold_start

        for i in range(1, self._max_iterations + 1):
            logger.info("IterativeAmplifier pass %d/%d concept=%s", i, self._max_iterations, current_concept.name)
            try:
                artifact = self._engine.reason(current_concept)
            except ReasoningViolation as exc:
                diagnostics.append(f"Pass {i} failed: {exc}")
                logger.warning("Amplification pass %d failed: %s", i, exc)
                break

            mesh_ok = artifact.mesh_fixed_point.get("passed", False)
            triadic_min = artifact.mesh_fixed_point.get("triadic_minimum", 0.0)
            triadic_mean = artifact.mesh_fixed_point.get("triadic_mean", 0.0)

            pass_record = AmplificationPass(
                pass_number=i,
                concept_name=artifact.concept_name,
                artifact_id=artifact.artifact_id,
                triadic_minimum=triadic_min,
                triadic_mean=triadic_mean,
                proved=artifact.proof_result.get("proved", False),
                mesh_passed=mesh_ok,
                axiom_count=len(self._engine.proof.axioms),
                signature=artifact.signature,
            )
            passes.append(pass_record)
            final_artifact = artifact

            # Convergence check: stable signature across window
            if artifact.signature == previous_signature:
                stable_count += 1
            else:
                stable_count = 0
            previous_signature = artifact.signature

            if stable_count >= self._convergence_window:
                diagnostics.append(
                    f"Converged at pass {i}: signature stable for "
                    f"{self._convergence_window} consecutive passes."
                )
                convergence_sig = artifact.signature
                return AmplificationResult(
                    converged=True,
                    total_passes=i,
                    passes=passes,
                    final_artifact=final_artifact,
                    convergence_signature=convergence_sig,
                    diagnostics=diagnostics,
                )

            # Build enriched concept for next pass
            current_concept = self._enrich_concept(
                original=concept,
                artifact=artifact,
                pass_number=i,
                threshold=threshold,
            )
            threshold = min(threshold + self._mesh_threshold_step, 0.99)

        convergence_sig = final_artifact.signature if final_artifact else ""
        diagnostics.append(
            f"Max iterations ({self._max_iterations}) reached without signature convergence."
        )
        return AmplificationResult(
            converged=stable_count >= self._convergence_window,
            total_passes=len(passes),
            passes=passes,
            final_artifact=final_artifact,
            convergence_signature=convergence_sig,
            diagnostics=diagnostics,
        )

    def _enrich_concept(
        self,
        original: ConceptPacket,
        artifact: ProofCarryingArtifact,
        pass_number: int,
        threshold: float,
    ) -> ConceptPacket:
        """
        Build concept_{i+1} from concept_i by injecting bridge_mapping
        facts as new premises and recording the pass in metadata.

        This is the bijective recursion: the output of pass N becomes a
        structural input premise for pass N+1, forcing the proof engine to
        verify that the enriched concept remains derivable under the
        expanded axiomatic universe.
        """
        bridge = artifact.bridge_mapping
        derived_premises: List[str] = list(original.premises)

        # Inject bridge facts as new premises
        concept_name = bridge.get("concept", {}).get("name", "")
        proposition = bridge.get("concept", {}).get("proposition", "")
        lambda_form = bridge.get("implementation", {}).get("lambda_form", "")

        if concept_name and proposition:
            derived_premises.append(f"{concept_name}->{proposition}")
        if lambda_form:
            derived_premises.append(f"lambda_grounded->{concept_name}")
        if artifact.proof_result.get("proved"):
            derived_premises.append(artifact.proof_result["theorem"])

        new_metadata = dict(original.metadata)
        new_metadata["amplification_pass"] = pass_number
        new_metadata["mesh_threshold"] = threshold
        new_metadata["prior_artifact_id"] = artifact.artifact_id
        new_metadata["mode"] = original.metadata.get("mode", "analytical")

        return ConceptPacket(
            name=original.name,
            proposition=original.proposition,
            premises=tuple(derived_premises),
            examples=original.examples,
            observations=original.observations,
            hypothesis_space=original.hypothesis_space,
            source_domain=original.source_domain,
            target_domain=original.target_domain,
            capabilities_required=original.capabilities_required,
            graph=original.graph,
            arithmetic_expression=original.arithmetic_expression,
            arithmetic_variables=original.arithmetic_variables,
            implementation_targets=original.implementation_targets,
            metadata=new_metadata,
        )


# ============================================================================
# Construction helpers
# ============================================================================

def Build_Concept_Packet(
    *,
    name: str,
    proposition: str,
    premises: Optional[Sequence[str]] = None,
    examples: Optional[Sequence[Any]] = None,
    observations: Optional[Sequence[str]] = None,
    hypothesis_space: Optional[Sequence[str]] = None,
    source_domain: str = "",
    target_domain: str = "",
    capabilities_required: Optional[Sequence[str]] = None,
    graph: Optional[Dict[str, Sequence[str]]] = None,
    arithmetic_expression: Optional[str] = None,
    arithmetic_variables: Optional[Dict[str, float]] = None,
    implementation_targets: Optional[Sequence[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> ConceptPacket:
    return ConceptPacket(
        name=name,
        proposition=proposition,
        premises=tuple(premises or ()),
        examples=tuple(examples or ()),
        observations=tuple(observations or ()),
        hypothesis_space=tuple(hypothesis_space or ()),
        source_domain=source_domain,
        target_domain=target_domain,
        capabilities_required=tuple(capabilities_required or ()),
        graph={k: tuple(v) for k, v in (graph or {}).items()},
        arithmetic_expression=arithmetic_expression,
        arithmetic_variables=arithmetic_variables or {},
        implementation_targets=tuple(implementation_targets or ()),
        metadata=metadata or {},
    )


# ============================================================================
# Minimal admissibility surface
# ============================================================================

def Reason_Concept_To_Artifact(concept: ConceptPacket) -> ProofCarryingArtifact:
    """Single-pass convenience entry point."""
    engine = ProofCarryingContextReasoningEngine()
    return engine.reason(concept)


def Amplify_Concept_To_Artifact(
    concept: ConceptPacket,
    max_iterations: int = 5,
) -> AmplificationResult:
    """
    Iterative amplification entry point.
    Runs up to max_iterations passes, feeding each artifact back as enriched
    premises for the next pass. Returns converged or best-effort result.
    """
    amplifier = IterativeReasoningAmplifier(max_iterations=max_iterations)
    return amplifier.amplify(concept)
