# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: EMP_Template_Engine
runtime_layer: operations
role: Runtime module
responsibility: Extracts reusable proof templates from verified proofs. Produces
    parameterized proof skeletons, validates instantiations via re-verification,
    and maintains a session-scoped template catalog. All templates are
    non-authoritative derived artifacts per Phase-3.1 Derived Policy Compiler
    Charter, bound to source proofs via cryptographic hash.
agent_binding: None
protocol_binding: Epistemic_Monitoring_Protocol
runtime_classification: runtime_module
boot_phase: E5
expected_imports:
  - typing
  - dataclasses
  - hashlib
  - re
  - time
provides:
  - ProofTemplate
  - TemplateInstantiation
  - EMP_Template_Engine
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Templates that fail validation are discarded. Source hash mismatch
    triggers DENY. No partial templates.
rewrite_provenance:
  source: EMP_NATIVE_COQ_PROOF_ENGINE_BLUEPRINT_AND_ROADMAP.md
  rewrite_phase: Phase_E5
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: EMP
  metrics: disabled
---------------------
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
import hashlib
import time
import re


# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class ProofTemplate:
    template_id: str
    name: str
    pattern_type: str
    parameters: List[str]
    skeleton: str
    source_theorem: str
    source_file: str
    source_hash: str
    extracted_at: float = field(default_factory=time.time)

    def instantiate(self, bindings: Dict[str, str]) -> str:
        result = self.skeleton
        for param, value in bindings.items():
            result = result.replace(f"{{${param}}}", value)
        return result


@dataclass
class TemplateInstantiation:
    template_id: str
    bindings: Dict[str, str]
    instantiated_source: str
    verified: bool = False
    verification_error: Optional[str] = None


# =============================================================================
# Pattern Detectors
# =============================================================================

_MODUS_PONENS_PATTERN = re.compile(
    r"intro\s+\w+\.\s*(?:apply|exact)\s+\w+",
    re.DOTALL,
)

_CASE_ANALYSIS_PATTERN = re.compile(
    r"destruct\s+\w+(?:\s+as\s+\[.*?\])?",
    re.DOTALL,
)

_INDUCTION_PATTERN = re.compile(
    r"induction\s+\w+",
    re.DOTALL,
)

_REWRITE_CHAIN_PATTERN = re.compile(
    r"(?:rewrite\s+\w+\.\s*){2,}",
    re.DOTALL,
)

_SPLIT_CONJ_PATTERN = re.compile(
    r"(?:split|repeat\s+split)",
    re.DOTALL,
)

PATTERN_REGISTRY = {
    "modus_ponens": _MODUS_PONENS_PATTERN,
    "case_analysis": _CASE_ANALYSIS_PATTERN,
    "induction": _INDUCTION_PATTERN,
    "rewrite_chain": _REWRITE_CHAIN_PATTERN,
    "conjunction_split": _SPLIT_CONJ_PATTERN,
}


def _compute_source_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]


def _extract_proof_body(source: str, theorem_name: str) -> Optional[str]:
    pattern = re.compile(
        rf"((?:Theorem|Lemma|Corollary|Proposition)\s+{re.escape(theorem_name)}\b.*?)"
        r"(?:Qed\.|Defined\.|Admitted\.)",
        re.DOTALL,
    )
    match = pattern.search(source)
    if match:
        return match.group(0)
    return None


# =============================================================================
# EMP Template Engine
# =============================================================================

class EMP_Template_Engine:
    """
    Extracts reusable proof templates from verified proofs.

    Templates are non-authoritative derived artifacts per Phase-3.1.
    All templates bind to source proofs via cryptographic hash.
    Any mismatch between template and source triggers DENY.

    NO REASONING. NO AUTHORITY. MECHANICAL EXTRACTION ONLY.
    """

    def __init__(self, coq_bridge=None):
        self._coq_bridge = coq_bridge
        self._catalog: Dict[str, ProofTemplate] = {}
        self._template_counter: int = 0

    # -------------------------------------------------------------------------
    # Template Extraction
    # -------------------------------------------------------------------------

    def extract_templates(self, proof_entries: List[Any]) -> List[ProofTemplate]:
        extracted = []

        for entry in proof_entries:
            if not getattr(entry, "proven", False):
                continue
            if getattr(entry, "admitted", False):
                continue

            file_path = getattr(entry, "file_path", None)
            if file_path is None:
                continue

            try:
                from pathlib import Path
                source = Path(file_path).read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            theorem_name = getattr(entry, "theorem_name", "")
            proof_body = _extract_proof_body(source, theorem_name)
            if proof_body is None:
                continue

            source_hash = _compute_source_hash(proof_body)

            for pattern_name, pattern_re in PATTERN_REGISTRY.items():
                if pattern_re.search(proof_body):
                    self._template_counter += 1
                    tid = f"tmpl_{self._template_counter:04d}"

                    parameters = self._detect_parameters(proof_body, theorem_name)

                    skeleton = self._generalize_proof(proof_body, theorem_name, parameters)

                    template = ProofTemplate(
                        template_id=tid,
                        name=f"{theorem_name}_{pattern_name}",
                        pattern_type=pattern_name,
                        parameters=parameters,
                        skeleton=skeleton,
                        source_theorem=theorem_name,
                        source_file=file_path,
                        source_hash=source_hash,
                    )

                    self._catalog[tid] = template
                    extracted.append(template)
                    break

        return extracted

    # -------------------------------------------------------------------------
    # Template Instantiation
    # -------------------------------------------------------------------------

    def instantiate(
        self, template: ProofTemplate, params: Dict[str, str]
    ) -> TemplateInstantiation:
        instantiated = template.instantiate(params)
        return TemplateInstantiation(
            template_id=template.template_id,
            bindings=params,
            instantiated_source=instantiated,
        )

    def validate_instantiation(
        self, instantiation: TemplateInstantiation
    ) -> TemplateInstantiation:
        if self._coq_bridge is None:
            instantiation.verified = False
            instantiation.verification_error = "No Coq bridge available"
            return instantiation

        result = self._coq_bridge.verify(instantiation.instantiated_source)
        instantiation.verified = result.verified
        if not result.verified:
            instantiation.verification_error = result.error_message
        return instantiation

    # -------------------------------------------------------------------------
    # Catalog
    # -------------------------------------------------------------------------

    def catalog(self) -> List[ProofTemplate]:
        return list(self._catalog.values())

    def get_template(self, template_id: str) -> Optional[ProofTemplate]:
        return self._catalog.get(template_id)

    def verify_source_binding(self, template: ProofTemplate) -> bool:
        try:
            from pathlib import Path
            source = Path(template.source_file).read_text(
                encoding="utf-8", errors="replace"
            )
        except Exception:
            return False

        proof_body = _extract_proof_body(source, template.source_theorem)
        if proof_body is None:
            return False

        current_hash = _compute_source_hash(proof_body)
        return current_hash == template.source_hash

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _detect_parameters(proof_body: str, theorem_name: str) -> List[str]:
        forall_match = re.search(
            r"forall\s+\(([^)]+)\)", proof_body
        )
        if forall_match:
            raw = forall_match.group(1)
            params = re.findall(r"(\w+)\s*:", raw)
            return params

        forall_simple = re.search(
            r"forall\s+([\w\s]+?)(?:\s*:|\s*,)", proof_body
        )
        if forall_simple:
            return forall_simple.group(1).split()

        return []

    @staticmethod
    def _generalize_proof(
        proof_body: str, theorem_name: str, parameters: List[str]
    ) -> str:
        skeleton = proof_body
        skeleton = skeleton.replace(theorem_name, "{$THEOREM_NAME}")
        for i, param in enumerate(parameters):
            skeleton = re.sub(
                rf"\b{re.escape(param)}\b",
                f"{{$PARAM_{i}}}",
                skeleton,
            )
        return skeleton

    # -------------------------------------------------------------------------
    # Introspection (Safe)
    # -------------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        pattern_counts: Dict[str, int] = {}
        for t in self._catalog.values():
            pattern_counts[t.pattern_type] = pattern_counts.get(t.pattern_type, 0) + 1

        return {
            "templates_count": len(self._catalog),
            "pattern_distribution": pattern_counts,
            "coq_bridge_available": self._coq_bridge is not None,
        }
