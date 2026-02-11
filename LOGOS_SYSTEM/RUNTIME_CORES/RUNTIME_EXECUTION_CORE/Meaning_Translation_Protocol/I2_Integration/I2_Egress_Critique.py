# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: I2_Egress_Critique
runtime_layer: language_egress
role: I2 Agent force multiplier for egress quality assurance
responsibility: Operates as I2's last-mile contribution at MTP egress.
    Three critique functions exercised on rendered output:
    1. Translatability Verification — can the NL be deterministically
       reverse-mapped to the source SMP without ambiguity?
    2. Privation Surface Check — does the NL surface introduce, mask,
       or transform privation states present in the source?
    3. Ontological Grounding Audit — do grounding references in the NL
       trace back to declared evidence in the SMP?
    I2 operates read-only. Does not mutate output. Does not infer.
    Does not form beliefs. Produces an I2AA critique artifact.
agent_binding: I2_Agent
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [hashlib, time, uuid, dataclasses, typing, enum]
provides: [I2EgressCritique, CritiqueResult, TranslatabilityCheck, PrivationSurfaceCheck, GroundingAudit]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Critique failure produces ABSTAIN, not PASS.
    I2 never blocks emission unilaterally; critique is advisory
    per SMP Pipeline Governance Addendum (enrichment protocols
    are non-authoritative). But FAIL triggers re-render consideration.
rewrite_provenance:
  source: new_module
  rewrite_phase: MTP_Egress_Enhancement
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: MTP
  metrics: critique_count, pass_count, fail_count, abstain_count, privation_detections
---------------------
"""

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


# =============================================================================
# Critique Verdicts (aligned with SMP Pipeline agent_verification_semantics)
# =============================================================================

class CritiqueVerdict(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSTAIN = "ABSTAIN"


class PrivationStatus(Enum):
    NONE_DETECTED = "none_detected"
    PRESERVED = "preserved"
    MASKED = "masked"
    INTRODUCED = "introduced"
    TRANSFORMED = "transformed"


# =============================================================================
# Individual Critique Check Results
# =============================================================================

@dataclass
class TranslatabilityCheck:
    total_sentences: int = 0
    reverse_mappable: int = 0
    ambiguous: List[int] = field(default_factory=list)
    untraceable: List[int] = field(default_factory=list)
    ratio: float = 0.0
    verdict: CritiqueVerdict = CritiqueVerdict.ABSTAIN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_sentences": self.total_sentences,
            "reverse_mappable": self.reverse_mappable,
            "ambiguous": self.ambiguous,
            "untraceable": self.untraceable,
            "ratio": round(self.ratio, 4),
            "verdict": self.verdict.value,
        }


@dataclass
class PrivationSurfaceCheck:
    source_privations: List[str] = field(default_factory=list)
    surface_privations: List[str] = field(default_factory=list)
    masked: List[str] = field(default_factory=list)
    introduced: List[str] = field(default_factory=list)
    transformed: List[str] = field(default_factory=list)
    status: PrivationStatus = PrivationStatus.NONE_DETECTED
    verdict: CritiqueVerdict = CritiqueVerdict.ABSTAIN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_privations": self.source_privations,
            "surface_privations": self.surface_privations,
            "masked": self.masked,
            "introduced": self.introduced,
            "transformed": self.transformed,
            "status": self.status.value,
            "verdict": self.verdict.value,
        }


@dataclass
class GroundingAudit:
    source_groundings: List[str] = field(default_factory=list)
    surface_groundings: List[str] = field(default_factory=list)
    ungrounded_claims: List[int] = field(default_factory=list)
    phantom_groundings: List[str] = field(default_factory=list)
    grounding_ratio: float = 0.0
    verdict: CritiqueVerdict = CritiqueVerdict.ABSTAIN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_groundings": self.source_groundings,
            "surface_groundings": self.surface_groundings,
            "ungrounded_claims": self.ungrounded_claims,
            "phantom_groundings": self.phantom_groundings,
            "grounding_ratio": round(self.grounding_ratio, 4),
            "verdict": self.verdict.value,
        }


# =============================================================================
# Composite Critique Result (I2AA-shaped)
# =============================================================================

@dataclass
class CritiqueResult:
    aa_id: str = ""
    aa_type: str = "I2AA"
    originating_entity: str = "I2_Agent"
    bound_render_id: str = ""
    bound_render_hash: str = ""
    translatability: TranslatabilityCheck = field(default_factory=TranslatabilityCheck)
    privation: PrivationSurfaceCheck = field(default_factory=PrivationSurfaceCheck)
    grounding: GroundingAudit = field(default_factory=GroundingAudit)
    overall_verdict: CritiqueVerdict = CritiqueVerdict.ABSTAIN
    critique_timestamp: float = 0.0
    critique_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "aa_id": self.aa_id,
            "aa_type": self.aa_type,
            "originating_entity": self.originating_entity,
            "bound_render_id": self.bound_render_id,
            "bound_render_hash": self.bound_render_hash,
            "translatability": self.translatability.to_dict(),
            "privation": self.privation.to_dict(),
            "grounding": self.grounding.to_dict(),
            "overall_verdict": self.overall_verdict.value,
            "critique_timestamp": self.critique_timestamp,
            "critique_time_ms": round(self.critique_time_ms, 2),
        }


# =============================================================================
# Privation Indicators
# =============================================================================

_PRIVATION_SURFACE_MARKERS = (
    "not ", "no ", "none", "never", "without", "lack", "absent",
    "missing", "denied", "impossible", "cannot", "unable", "fail",
    "unknown", "uncertain", "unresolved", "incomplete", "partial",
)

_GROUNDING_SURFACE_MARKERS = (
    "based on", "according to", "grounded in", "derived from",
    "evidence", "source", "reference", "citation", "per ",
    "as stated", "as defined", "comes from",
)


# =============================================================================
# I2 Egress Critique Engine
# =============================================================================

class I2EgressCritique:

    def critique(
        self,
        rendered: Any,
        plan: Any,
        graph: Any,
        smp_payload: Optional[Dict[str, Any]] = None,
    ) -> CritiqueResult:
        start = time.monotonic()

        render_hash = rendered.content_hash if hasattr(rendered, "content_hash") else ""

        result = CritiqueResult(
            aa_id=f"I2AA-{uuid.uuid4().hex[:12]}",
            bound_render_id=rendered.render_id,
            bound_render_hash=render_hash,
            critique_timestamp=time.time(),
        )

        try:
            result.translatability = self._check_translatability(rendered, plan)
            result.privation = self._check_privation_surface(rendered, plan, graph, smp_payload)
            result.grounding = self._check_grounding(rendered, plan, graph)

            verdicts = [
                result.translatability.verdict,
                result.privation.verdict,
                result.grounding.verdict,
            ]

            if CritiqueVerdict.FAIL in verdicts:
                result.overall_verdict = CritiqueVerdict.FAIL
            elif all(v == CritiqueVerdict.PASS for v in verdicts):
                result.overall_verdict = CritiqueVerdict.PASS
            else:
                result.overall_verdict = CritiqueVerdict.PASS

        except Exception:
            result.overall_verdict = CritiqueVerdict.ABSTAIN

        result.critique_time_ms = (time.monotonic() - start) * 1000.0
        return result

    # -----------------------------------------------------------------
    # Translatability: can NL reverse-map to source units?
    # -----------------------------------------------------------------

    def _check_translatability(
        self, rendered: Any, plan: Any
    ) -> TranslatabilityCheck:
        check = TranslatabilityCheck()
        check.total_sentences = len(rendered.l1.sentences)

        if check.total_sentences == 0:
            check.verdict = CritiqueVerdict.PASS
            return check

        for idx, sentence in enumerate(rendered.l1.sentences):
            if idx >= len(plan.units):
                check.untraceable.append(idx)
                continue

            unit = plan.units[idx]
            content_lower = unit.content.lower().strip()
            sentence_lower = sentence.lower().strip()

            if content_lower and content_lower in sentence_lower:
                check.reverse_mappable += 1
            elif self._content_overlap(content_lower, sentence_lower) > 0.6:
                check.reverse_mappable += 1
            else:
                check.ambiguous.append(idx)

        check.ratio = (
            check.reverse_mappable / check.total_sentences
            if check.total_sentences > 0 else 0.0
        )

        if check.ratio >= 0.95:
            check.verdict = CritiqueVerdict.PASS
        elif check.ratio >= 0.8:
            check.verdict = CritiqueVerdict.PASS
        else:
            check.verdict = CritiqueVerdict.FAIL

        return check

    # -----------------------------------------------------------------
    # Privation Surface: does NL mask or introduce privations?
    # -----------------------------------------------------------------

    def _check_privation_surface(
        self,
        rendered: Any,
        plan: Any,
        graph: Any,
        smp_payload: Optional[Dict[str, Any]],
    ) -> PrivationSurfaceCheck:
        check = PrivationSurfaceCheck()

        source_privation_nodes = [
            n for n in graph.nodes
            if n.primitive_type.value in ("SP-03", "SP-07", "SP-08")
        ]
        check.source_privations = [n.node_id for n in source_privation_nodes]

        surface_privation_indices: List[int] = []
        for idx, sentence in enumerate(rendered.l1.sentences):
            lower = sentence.lower()
            if any(marker in lower for marker in _PRIVATION_SURFACE_MARKERS):
                surface_privation_indices.append(idx)

        check.surface_privations = [f"sentence-{i}" for i in surface_privation_indices]

        source_set = set()
        for node in source_privation_nodes:
            for idx, unit in enumerate(plan.units):
                if unit.source_node_id == node.node_id:
                    source_set.add(idx)

        surface_set = set(surface_privation_indices)

        masked = source_set - surface_set
        introduced = surface_set - source_set

        check.masked = [f"unit-{i}" for i in sorted(masked)]
        check.introduced = [f"sentence-{i}" for i in sorted(introduced)]

        if check.masked:
            check.status = PrivationStatus.MASKED
            check.verdict = CritiqueVerdict.FAIL
        elif check.introduced:
            check.status = PrivationStatus.INTRODUCED
            check.verdict = CritiqueVerdict.FAIL
        elif check.source_privations:
            check.status = PrivationStatus.PRESERVED
            check.verdict = CritiqueVerdict.PASS
        else:
            check.status = PrivationStatus.NONE_DETECTED
            check.verdict = CritiqueVerdict.PASS

        return check

    # -----------------------------------------------------------------
    # Grounding Audit: do NL grounding claims trace to source?
    # -----------------------------------------------------------------

    def _check_grounding(
        self, rendered: Any, plan: Any, graph: Any
    ) -> GroundingAudit:
        audit = GroundingAudit()

        grounding_nodes = [
            n for n in graph.nodes
            if n.primitive_type.value == "SP-12"
        ]
        audit.source_groundings = [n.node_id for n in grounding_nodes]

        grounding_sentences: List[int] = []
        for idx, sentence in enumerate(rendered.l1.sentences):
            lower = sentence.lower()
            if any(marker in lower for marker in _GROUNDING_SURFACE_MARKERS):
                grounding_sentences.append(idx)

        audit.surface_groundings = [f"sentence-{i}" for i in grounding_sentences]

        source_grounding_indices = set()
        for node in grounding_nodes:
            for idx, unit in enumerate(plan.units):
                if unit.source_node_id == node.node_id:
                    source_grounding_indices.add(idx)

        phantoms = set(grounding_sentences) - source_grounding_indices
        audit.phantom_groundings = [f"sentence-{i}" for i in sorted(phantoms)]

        if audit.source_groundings:
            surface_set = set(grounding_sentences)
            matched = source_grounding_indices & surface_set
            audit.grounding_ratio = (
                len(matched) / len(source_grounding_indices)
                if source_grounding_indices else 1.0
            )
        else:
            audit.grounding_ratio = 1.0

        if audit.phantom_groundings:
            audit.verdict = CritiqueVerdict.FAIL
        elif audit.grounding_ratio >= 0.8:
            audit.verdict = CritiqueVerdict.PASS
        else:
            audit.verdict = CritiqueVerdict.FAIL

        return audit

    # -----------------------------------------------------------------
    # Utility
    # -----------------------------------------------------------------

    def _content_overlap(self, source: str, target: str) -> float:
        if not source or not target:
            return 0.0
        source_words = set(source.split())
        target_words = set(target.split())
        if not source_words:
            return 0.0
        overlap = source_words & target_words
        return len(overlap) / len(source_words)
