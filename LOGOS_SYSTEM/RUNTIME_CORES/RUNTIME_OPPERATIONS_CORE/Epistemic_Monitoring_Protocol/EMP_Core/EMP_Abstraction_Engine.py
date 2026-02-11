# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: EMP_Abstraction_Engine
runtime_layer: operations
role: Runtime module
responsibility: Mechanical abstraction operations on verified proofs. Proposes
    generalizations, suggests intermediate lemmas, mines cross-module patterns,
    and measures proof complexity. All candidates are tagged UNVERIFIED until
    passed through EMP_Coq_Bridge. Not inference in the epistemic sense —
    structural pattern operations only.
agent_binding: None
protocol_binding: Epistemic_Monitoring_Protocol
runtime_classification: runtime_module
boot_phase: E6
expected_imports:
  - typing
  - dataclasses
  - re
  - collections
provides:
  - GeneralizationCandidate
  - LemmaCandidate
  - ProofPattern
  - ComplexityReport
  - EMP_Abstraction_Engine
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: All candidates tagged UNVERIFIED until re-verified. Candidates that
    fail verification are discarded, not stored.
rewrite_provenance:
  source: EMP_NATIVE_COQ_PROOF_ENGINE_BLUEPRINT_AND_ROADMAP.md
  rewrite_phase: Phase_E6
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: EMP
  metrics: disabled
---------------------
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from collections import Counter
import re


# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class GeneralizationCandidate:
    original_theorem: str
    generalized_name: str
    generalized_source: str
    substitutable_parameters: List[str]
    verified: bool = False
    verification_error: Optional[str] = None


@dataclass
class LemmaCandidate:
    parent_theorem: str
    lemma_name: str
    lemma_source: str
    rationale: str
    verified: bool = False
    verification_error: Optional[str] = None


@dataclass
class ProofPattern:
    pattern_name: str
    tactic_sequence: List[str]
    occurrence_count: int
    example_theorems: List[str]
    average_proof_length: float


@dataclass
class ComplexityReport:
    theorem_name: str
    total_tactics: int
    unique_tactics: int
    max_nesting_depth: int
    axiom_count: int
    import_count: int
    branching_factor: float
    complexity_score: float


# =============================================================================
# Tactic and Structure Parsers
# =============================================================================

_TACTIC_PATTERN = re.compile(
    r"\b(intros?|apply|exact|destruct|split|exists|rewrite|unfold|"
    r"simpl|auto|trivial|assumption|contradiction|induction|"
    r"inversion|discriminate|subst|reflexivity|symmetry|"
    r"transitivity|assert|pose|specialize|generalize|"
    r"clear|rename|replace|change|pattern|case|elim|"
    r"repeat|try|first|solve|now|eauto|omega|lia|ring|field)\b"
)

_PROOF_BLOCK = re.compile(
    r"(?:Theorem|Lemma|Corollary|Proposition)\s+(\w+)\b.*?Proof\.(.*?)(?:Qed\.|Defined\.|Admitted\.)",
    re.DOTALL,
)

_FORALL_PARAMS = re.compile(r"forall\s*\(([^)]+)\)")
_SIMPLE_FORALL = re.compile(r"forall\s+([\w\s]+?)(?:\s*:)")


def _extract_tactics(proof_body: str) -> List[str]:
    return _TACTIC_PATTERN.findall(proof_body)


def _count_nesting(proof_body: str) -> int:
    depth = 0
    max_depth = 0
    for char in proof_body:
        if char == "(":
            depth += 1
            max_depth = max(max_depth, depth)
        elif char == ")":
            depth = max(0, depth - 1)
    return max_depth


# =============================================================================
# EMP Abstraction Engine
# =============================================================================

class EMP_Abstraction_Engine:
    """
    Mechanical abstraction operations on verified proofs.

    Not inference in the epistemic sense — structural pattern operations only.
    All candidates are tagged UNVERIFIED until passed through EMP_Coq_Bridge.
    Candidates that fail verification are discarded, not stored.

    NO REASONING. NO EPISTEMIC INFERENCE. STRUCTURAL OPERATIONS ONLY.
    """

    def __init__(self, coq_bridge=None, proof_index=None):
        self._coq_bridge = coq_bridge
        self._proof_index = proof_index

    # -------------------------------------------------------------------------
    # Generalization
    # -------------------------------------------------------------------------

    def generalize(self, proof_entry: Any) -> List[GeneralizationCandidate]:
        candidates = []

        theorem_name = getattr(proof_entry, "theorem_name", "")
        file_path = getattr(proof_entry, "file_path", "")

        if not theorem_name or not file_path:
            return candidates

        try:
            from pathlib import Path
            source = Path(file_path).read_text(encoding="utf-8", errors="replace")
        except Exception:
            return candidates

        block_match = re.search(
            rf"((?:Theorem|Lemma|Corollary|Proposition)\s+{re.escape(theorem_name)}\b.*?"
            r"(?:Qed\.|Defined\.|Admitted\.))",
            source,
            re.DOTALL,
        )
        if block_match is None:
            return candidates

        proof_block = block_match.group(1)

        param_matches = _FORALL_PARAMS.findall(proof_block)
        if not param_matches:
            param_matches_simple = _SIMPLE_FORALL.findall(proof_block)
            if not param_matches_simple:
                return candidates

        specific_types = re.findall(r":\s*(Obj|Prop|nat|bool|Type)\b", proof_block)
        for specific_type in set(specific_types):
            gen_name = f"{theorem_name}_gen_{specific_type}"
            gen_source = proof_block.replace(
                f": {specific_type}", ": {$T}"
            )
            gen_source = gen_source.replace(theorem_name, gen_name)

            candidates.append(
                GeneralizationCandidate(
                    original_theorem=theorem_name,
                    generalized_name=gen_name,
                    generalized_source=gen_source,
                    substitutable_parameters=[specific_type],
                )
            )

        return candidates

    # -------------------------------------------------------------------------
    # Lemma Suggestion
    # -------------------------------------------------------------------------

    def suggest_lemmas(self, goal: str) -> List[LemmaCandidate]:
        candidates = []

        if "->" in goal or "⟹" in goal:
            parts = re.split(r"->|⟹", goal, maxsplit=1)
            if len(parts) == 2:
                antecedent = parts[0].strip()
                consequent = parts[1].strip()
                candidates.append(
                    LemmaCandidate(
                        parent_theorem="goal",
                        lemma_name="intermediate_step",
                        lemma_source=f"Lemma intermediate_step : {antecedent} -> (* intermediate *) -> {consequent}.",
                        rationale="Decompose implication into two steps",
                    )
                )

        if "/\\" in goal or "∧" in goal:
            candidates.append(
                LemmaCandidate(
                    parent_theorem="goal",
                    lemma_name="left_conjunct",
                    lemma_source="(* Prove left conjunct independently *)",
                    rationale="Split conjunction and prove each side",
                )
            )

        if "forall" in goal:
            candidates.append(
                LemmaCandidate(
                    parent_theorem="goal",
                    lemma_name="specialized_instance",
                    lemma_source="(* Prove for a specific instance first *)",
                    rationale="Prove specific case before generalizing",
                )
            )

        return candidates

    # -------------------------------------------------------------------------
    # Cross-Module Pattern Mining
    # -------------------------------------------------------------------------

    def mine_patterns(self, proof_entries: List[Any]) -> List[ProofPattern]:
        tactic_sequences: Dict[str, List[str]] = {}
        tactic_counts: Counter = Counter()

        for entry in proof_entries:
            if not getattr(entry, "proven", False):
                continue

            file_path = getattr(entry, "file_path", "")
            theorem_name = getattr(entry, "theorem_name", "")

            try:
                from pathlib import Path
                source = Path(file_path).read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            for match in _PROOF_BLOCK.finditer(source):
                name = match.group(1)
                body = match.group(2)
                tactics = _extract_tactics(body)
                if tactics:
                    key = " ".join(tactics[:5])
                    tactic_counts[key] += 1
                    if key not in tactic_sequences:
                        tactic_sequences[key] = []
                    tactic_sequences[key].append(name)

        patterns = []
        for seq_key, count in tactic_counts.most_common(20):
            if count < 2:
                continue
            tactics = seq_key.split()
            examples = tactic_sequences.get(seq_key, [])[:5]
            patterns.append(
                ProofPattern(
                    pattern_name=f"pattern_{tactics[0]}_{tactics[-1] if len(tactics) > 1 else 'single'}",
                    tactic_sequence=tactics,
                    occurrence_count=count,
                    example_theorems=examples,
                    average_proof_length=float(len(tactics)),
                )
            )

        return patterns

    # -------------------------------------------------------------------------
    # Complexity Analysis
    # -------------------------------------------------------------------------

    def complexity(self, proof_entry: Any) -> ComplexityReport:
        theorem_name = getattr(proof_entry, "theorem_name", "unknown")
        file_path = getattr(proof_entry, "file_path", "")
        axiom_footprint = getattr(proof_entry, "axiom_footprint", [])
        imports = getattr(proof_entry, "imports", [])

        try:
            from pathlib import Path
            source = Path(file_path).read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ComplexityReport(
                theorem_name=theorem_name,
                total_tactics=0,
                unique_tactics=0,
                max_nesting_depth=0,
                axiom_count=len(axiom_footprint),
                import_count=len(imports),
                branching_factor=0.0,
                complexity_score=0.0,
            )

        block_match = re.search(
            rf"Proof\.(.*?)(?:Qed\.|Defined\.|Admitted\.)",
            source,
            re.DOTALL,
        )
        proof_body = block_match.group(1) if block_match else ""

        tactics = _extract_tactics(proof_body)
        unique_tactics = set(tactics)
        nesting = _count_nesting(proof_body)

        destruct_count = tactics.count("destruct") + tactics.count("case")
        split_count = tactics.count("split")
        branching = float(destruct_count + split_count)

        score = (
            len(tactics) * 1.0
            + nesting * 2.0
            + len(axiom_footprint) * 1.5
            + branching * 1.0
        )

        return ComplexityReport(
            theorem_name=theorem_name,
            total_tactics=len(tactics),
            unique_tactics=len(unique_tactics),
            max_nesting_depth=nesting,
            axiom_count=len(axiom_footprint),
            import_count=len(imports),
            branching_factor=branching,
            complexity_score=round(score, 2),
        )

    # -------------------------------------------------------------------------
    # Introspection (Safe)
    # -------------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        return {
            "coq_bridge_available": self._coq_bridge is not None,
            "proof_index_available": self._proof_index is not None,
        }
