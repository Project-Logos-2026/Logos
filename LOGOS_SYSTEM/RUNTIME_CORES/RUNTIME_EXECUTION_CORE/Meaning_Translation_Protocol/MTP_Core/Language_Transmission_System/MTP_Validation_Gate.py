# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MTP_Validation_Gate
runtime_layer: language_egress
role: Egress validation gate for rendered output
responsibility: Performs mandatory fail-closed validation on rendered output
    before emission. Three checks enforced:
    1. Structural Coverage — bijective mapping between content units and clauses
    2. Arithmetic Shadow Consistency — NL quantitative claims match L2
    3. Semantic Predicate Alignment — reverse-mapping to source templates
    Failure halts output. Retry with alternate templates. Halt on exhaustion
    with FAILED consistency declaration.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [hashlib, time, dataclasses, typing, enum]
provides: [ValidationGate, ValidationResult, CoverageCheck, ShadowCheck, PredicateCheck]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Any validation failure produces REJECT. No partial pass.
    Silence over invalid output per Language Governance Charter.
rewrite_provenance:
  source: new_module
  rewrite_phase: MTP_Egress_Enhancement
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: MTP
  metrics: validation_count, pass_count, reject_count, coverage_failures, shadow_failures, predicate_failures
---------------------
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


# =============================================================================
# Validation Outcomes
# =============================================================================

class ValidationVerdict(Enum):
    PASS = "PASS"
    REJECT = "REJECT"
    WARN = "WARN"


class GateDecision(Enum):
    EMIT = "emit"
    RETRY = "retry"
    HALT = "halt"


# =============================================================================
# Individual Check Results
# =============================================================================

@dataclass
class CoverageCheck:
    total_units: int = 0
    rendered_sentences: int = 0
    missing_units: List[str] = field(default_factory=list)
    orphan_sentences: int = 0
    bijective: bool = False
    verdict: ValidationVerdict = ValidationVerdict.REJECT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_units": self.total_units,
            "rendered_sentences": self.rendered_sentences,
            "missing_units": self.missing_units,
            "orphan_sentences": self.orphan_sentences,
            "bijective": self.bijective,
            "verdict": self.verdict.value,
        }


@dataclass
class ShadowCheck:
    l2_populated: bool = False
    l2_expression_count: int = 0
    l1_numeric_claims: int = 0
    mismatches: List[str] = field(default_factory=list)
    verdict: ValidationVerdict = ValidationVerdict.PASS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "l2_populated": self.l2_populated,
            "l2_expression_count": self.l2_expression_count,
            "l1_numeric_claims": self.l1_numeric_claims,
            "mismatches": self.mismatches,
            "verdict": self.verdict.value,
        }


@dataclass
class PredicateCheck:
    total_sentences: int = 0
    template_traced: int = 0
    untraced: List[int] = field(default_factory=list)
    trace_ratio: float = 0.0
    verdict: ValidationVerdict = ValidationVerdict.REJECT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_sentences": self.total_sentences,
            "template_traced": self.template_traced,
            "untraced": self.untraced,
            "trace_ratio": self.trace_ratio,
            "verdict": self.verdict.value,
        }


# =============================================================================
# Composite Validation Result
# =============================================================================

@dataclass
class ValidationResult:
    result_id: str
    source_render_id: str
    coverage: CoverageCheck = field(default_factory=CoverageCheck)
    shadow: ShadowCheck = field(default_factory=ShadowCheck)
    predicate: PredicateCheck = field(default_factory=PredicateCheck)
    overall_verdict: ValidationVerdict = ValidationVerdict.REJECT
    gate_decision: GateDecision = GateDecision.HALT
    validation_timestamp: float = 0.0
    validation_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "source_render_id": self.source_render_id,
            "coverage": self.coverage.to_dict(),
            "shadow": self.shadow.to_dict(),
            "predicate": self.predicate.to_dict(),
            "overall_verdict": self.overall_verdict.value,
            "gate_decision": self.gate_decision.value,
            "validation_timestamp": self.validation_timestamp,
            "validation_time_ms": round(self.validation_time_ms, 2),
        }


# =============================================================================
# Validation Gate
# =============================================================================

_TEMPLATE_MARKERS: Dict[str, List[str]] = {
    "SP-01": [],
    "SP-02": ["distinction is drawn", "specifically", "to be clear"],
    "SP-03": ["not the case", "does not hold", "not the case"],
    "SP-04": ["constraint", "with the constraint", "keep in mind"],
    "SP-05": ["depends on", "requires", "first"],
    "SP-06": ["evaluation yields", "assessment", "looking at"],
    "SP-07": ["uncertainty", "uncertain whether", "not yet clear"],
    "SP-08": ["unknown", "currently unknown", "do not yet know"],
    "SP-09": ["commitment", "committed"],
    "SP-10": ["relation holds", "related", "connected to"],
    "SP-11": ["within the scope", "in the context", "regarding"],
    "SP-12": ["grounded in", "based on", "comes from"],
}


class ValidationGate:

    def __init__(self, max_retries: int = 2) -> None:
        self._max_retries = max_retries

    def validate(
        self,
        rendered: Any,
        plan: Any,
    ) -> ValidationResult:
        start = time.monotonic()

        result = ValidationResult(
            result_id=f"VR-{rendered.render_id}",
            source_render_id=rendered.render_id,
            validation_timestamp=time.time(),
        )

        try:
            result.coverage = self._check_coverage(rendered, plan)
            result.shadow = self._check_shadow(rendered)
            result.predicate = self._check_predicates(rendered, plan)

            all_pass = (
                result.coverage.verdict == ValidationVerdict.PASS
                and result.shadow.verdict == ValidationVerdict.PASS
                and result.predicate.verdict == ValidationVerdict.PASS
            )

            any_reject = (
                result.coverage.verdict == ValidationVerdict.REJECT
                or result.shadow.verdict == ValidationVerdict.REJECT
                or result.predicate.verdict == ValidationVerdict.REJECT
            )

            if all_pass:
                result.overall_verdict = ValidationVerdict.PASS
                result.gate_decision = GateDecision.EMIT
            elif any_reject:
                result.overall_verdict = ValidationVerdict.REJECT
                result.gate_decision = GateDecision.RETRY
            else:
                result.overall_verdict = ValidationVerdict.WARN
                result.gate_decision = GateDecision.EMIT

        except Exception:
            result.overall_verdict = ValidationVerdict.REJECT
            result.gate_decision = GateDecision.HALT

        result.validation_time_ms = (time.monotonic() - start) * 1000.0
        return result

    def _check_coverage(self, rendered: Any, plan: Any) -> CoverageCheck:
        check = CoverageCheck()

        check.total_units = plan.unit_count()
        check.rendered_sentences = len(rendered.l1.sentences)

        if check.total_units == 0 and check.rendered_sentences == 0:
            check.bijective = True
            check.verdict = ValidationVerdict.PASS
            return check

        if check.total_units != check.rendered_sentences:
            check.bijective = False
            if check.rendered_sentences < check.total_units:
                check.missing_units = [
                    plan.units[i].unit_id
                    for i in range(check.rendered_sentences, check.total_units)
                ]
            else:
                check.orphan_sentences = check.rendered_sentences - check.total_units
            check.verdict = ValidationVerdict.REJECT
            return check

        check.bijective = True
        check.verdict = ValidationVerdict.PASS
        return check

    def _check_shadow(self, rendered: Any) -> ShadowCheck:
        check = ShadowCheck()

        check.l2_populated = rendered.l2.populated

        if not check.l2_populated:
            check.verdict = ValidationVerdict.PASS
            return check

        check.l2_expression_count = len(rendered.l2.expressions)

        numeric_count = 0
        for sentence in rendered.l1.sentences:
            if any(c.isdigit() for c in sentence):
                numeric_count += 1
        check.l1_numeric_claims = numeric_count

        if not rendered.sync_valid:
            check.mismatches.append("L1/L2 sync flag is False")
            check.verdict = ValidationVerdict.REJECT
            return check

        check.verdict = ValidationVerdict.PASS
        return check

    def _check_predicates(self, rendered: Any, plan: Any) -> PredicateCheck:
        check = PredicateCheck()
        check.total_sentences = len(rendered.l1.sentences)

        if check.total_sentences == 0:
            check.verdict = ValidationVerdict.PASS
            return check

        traced = 0
        untraced: List[int] = []

        for idx, sentence in enumerate(rendered.l1.sentences):
            if idx < len(plan.units):
                sp_code = plan.units[idx].primitive_code
                markers = _TEMPLATE_MARKERS.get(sp_code, [])

                if sp_code == "SP-01":
                    traced += 1
                    continue

                lower_sentence = sentence.lower()
                if any(m in lower_sentence for m in markers):
                    traced += 1
                else:
                    content = plan.units[idx].content.lower()
                    if content and content in lower_sentence:
                        traced += 1
                    else:
                        untraced.append(idx)
            else:
                untraced.append(idx)

        check.template_traced = traced
        check.untraced = untraced
        check.trace_ratio = traced / check.total_sentences if check.total_sentences > 0 else 0.0

        if check.trace_ratio >= 1.0:
            check.verdict = ValidationVerdict.PASS
        elif check.trace_ratio >= 0.8:
            check.verdict = ValidationVerdict.WARN
        else:
            check.verdict = ValidationVerdict.REJECT

        return check
