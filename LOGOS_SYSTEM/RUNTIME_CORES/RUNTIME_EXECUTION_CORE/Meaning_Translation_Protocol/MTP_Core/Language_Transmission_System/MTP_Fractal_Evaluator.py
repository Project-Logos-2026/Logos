# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MTP_Fractal_Evaluator
runtime_layer: language_egress
role: AF-LANG-002 Fractal Evaluator
responsibility: Evaluates linearized semantic structures for pattern coherence,
    structural stability, and resonance across recursive dimensions.
    Detects imbalances in primitive distribution, identifies structural
    weaknesses, and produces stability scores for downstream rendering.
    Does not mutate meaning. Does not reassign authority. Does not signal execution.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [math, dataclasses, typing, enum]
provides: [FractalEvaluator, StabilityReport, PatternAnalysis, ResonanceScore]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Returns neutral stability score (0.5) on any evaluation failure.
    Never blocks pipeline progression. Evaluation is advisory.
rewrite_provenance:
  source: new_module
  rewrite_phase: MTP_Egress_Enhancement
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: MTP
  metrics: evaluation_count, stability_scores, pattern_detections
---------------------
"""

import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


# =============================================================================
# Stability Classifications
# =============================================================================

class StabilityLevel(Enum):
    UNSTABLE = "unstable"
    MARGINAL = "marginal"
    STABLE = "stable"
    RESONANT = "resonant"


class PatternType(Enum):
    ASSERTION_HEAVY = "assertion_heavy"
    NEGATION_HEAVY = "negation_heavy"
    UNCERTAINTY_DOMINANT = "uncertainty_dominant"
    BALANCED = "balanced"
    SCOPE_ANCHORED = "scope_anchored"
    GROUNDING_RICH = "grounding_rich"
    CONSTRAINT_DENSE = "constraint_dense"
    EVALUATION_FOCUSED = "evaluation_focused"
    SPARSE = "sparse"


# =============================================================================
# Triadic Axis Mapping (Sign / Bridge / Mind)
# =============================================================================

_TRIADIC_AXES: Dict[str, List[str]] = {
    "sign": ["SP-01", "SP-02", "SP-03", "SP-11"],
    "bridge": ["SP-04", "SP-05", "SP-10", "SP-12"],
    "mind": ["SP-06", "SP-07", "SP-08", "SP-09"],
}


# =============================================================================
# Report Structures
# =============================================================================

@dataclass
class PatternAnalysis:
    detected_patterns: List[PatternType] = field(default_factory=list)
    primitive_distribution: Dict[str, int] = field(default_factory=dict)
    dominant_primitive: Optional[str] = None
    dominance_ratio: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "detected_patterns": [p.value for p in self.detected_patterns],
            "primitive_distribution": self.primitive_distribution,
            "dominant_primitive": self.dominant_primitive,
            "dominance_ratio": self.dominance_ratio,
        }


@dataclass
class ResonanceScore:
    sign_axis: float = 0.0
    bridge_axis: float = 0.0
    mind_axis: float = 0.0
    triadic_balance: float = 0.0
    harmonic_mean: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sign_axis": round(self.sign_axis, 4),
            "bridge_axis": round(self.bridge_axis, 4),
            "mind_axis": round(self.mind_axis, 4),
            "triadic_balance": round(self.triadic_balance, 4),
            "harmonic_mean": round(self.harmonic_mean, 4),
        }


@dataclass
class StabilityReport:
    report_id: str
    source_plan_id: str
    overall_score: float = 0.5
    stability_level: StabilityLevel = StabilityLevel.MARGINAL
    pattern_analysis: PatternAnalysis = field(default_factory=PatternAnalysis)
    resonance: ResonanceScore = field(default_factory=ResonanceScore)
    structural_warnings: List[str] = field(default_factory=list)
    evaluation_timestamp: float = 0.0
    evaluation_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "source_plan_id": self.source_plan_id,
            "overall_score": round(self.overall_score, 4),
            "stability_level": self.stability_level.value,
            "pattern_analysis": self.pattern_analysis.to_dict(),
            "resonance": self.resonance.to_dict(),
            "structural_warnings": self.structural_warnings,
            "evaluation_timestamp": self.evaluation_timestamp,
            "evaluation_time_ms": round(self.evaluation_time_ms, 2),
        }


# =============================================================================
# Fractal Evaluator (AF-LANG-002)
# =============================================================================

class FractalEvaluator:

    def __init__(
        self,
        dominance_threshold: float = 0.5,
        sparsity_threshold: int = 2,
    ) -> None:
        self._dominance_threshold = dominance_threshold
        self._sparsity_threshold = sparsity_threshold

    def evaluate(self, plan: Any) -> StabilityReport:
        start = time.monotonic()

        report = StabilityReport(
            report_id=f"SR-{plan.plan_id}",
            source_plan_id=plan.plan_id,
            evaluation_timestamp=time.time(),
        )

        try:
            if not plan.units:
                report.overall_score = 0.0
                report.stability_level = StabilityLevel.UNSTABLE
                report.structural_warnings.append("Empty linearization plan")
                report.evaluation_time_ms = (time.monotonic() - start) * 1000.0
                return report

            distribution = self._compute_distribution(plan.units)
            patterns = self._detect_patterns(distribution, len(plan.units))
            resonance = self._compute_resonance(distribution, len(plan.units))
            warnings = self._detect_warnings(distribution, resonance, len(plan.units))

            report.pattern_analysis = patterns
            report.resonance = resonance
            report.structural_warnings = warnings

            report.overall_score = self._compute_overall_score(
                patterns, resonance, len(warnings)
            )

            if report.overall_score >= 0.8:
                report.stability_level = StabilityLevel.RESONANT
            elif report.overall_score >= 0.6:
                report.stability_level = StabilityLevel.STABLE
            elif report.overall_score >= 0.4:
                report.stability_level = StabilityLevel.MARGINAL
            else:
                report.stability_level = StabilityLevel.UNSTABLE

        except Exception:
            report.overall_score = 0.5
            report.stability_level = StabilityLevel.MARGINAL
            report.structural_warnings.append("Evaluation failed; neutral score applied")

        report.evaluation_time_ms = (time.monotonic() - start) * 1000.0
        return report

    def _compute_distribution(
        self, units: List[Any]
    ) -> Dict[str, int]:
        dist: Dict[str, int] = {}
        for unit in units:
            code = unit.primitive_code
            dist[code] = dist.get(code, 0) + 1
        return dist

    def _detect_patterns(
        self, distribution: Dict[str, int], total: int
    ) -> PatternAnalysis:
        analysis = PatternAnalysis(primitive_distribution=distribution)

        if total == 0:
            analysis.detected_patterns.append(PatternType.SPARSE)
            return analysis

        dominant_sp = max(distribution, key=distribution.get) if distribution else None
        dominant_count = distribution.get(dominant_sp, 0) if dominant_sp else 0
        dominance_ratio = dominant_count / total if total > 0 else 0.0

        analysis.dominant_primitive = dominant_sp
        analysis.dominance_ratio = dominance_ratio

        if total <= self._sparsity_threshold:
            analysis.detected_patterns.append(PatternType.SPARSE)

        if dominance_ratio >= self._dominance_threshold:
            if dominant_sp == "SP-01":
                analysis.detected_patterns.append(PatternType.ASSERTION_HEAVY)
            elif dominant_sp == "SP-03":
                analysis.detected_patterns.append(PatternType.NEGATION_HEAVY)
            elif dominant_sp in ("SP-07", "SP-08"):
                analysis.detected_patterns.append(PatternType.UNCERTAINTY_DOMINANT)
            elif dominant_sp == "SP-04":
                analysis.detected_patterns.append(PatternType.CONSTRAINT_DENSE)
            elif dominant_sp == "SP-06":
                analysis.detected_patterns.append(PatternType.EVALUATION_FOCUSED)

        if distribution.get("SP-11", 0) > 0 and distribution.get("SP-12", 0) > 0:
            scope_ground = (
                distribution.get("SP-11", 0) + distribution.get("SP-12", 0)
            )
            if scope_ground / total >= 0.3:
                analysis.detected_patterns.append(PatternType.SCOPE_ANCHORED)
                analysis.detected_patterns.append(PatternType.GROUNDING_RICH)

        if dominance_ratio < 0.35 and total >= 3:
            analysis.detected_patterns.append(PatternType.BALANCED)

        if not analysis.detected_patterns:
            analysis.detected_patterns.append(PatternType.BALANCED)

        return analysis

    def _compute_resonance(
        self, distribution: Dict[str, int], total: int
    ) -> ResonanceScore:
        if total == 0:
            return ResonanceScore()

        axis_scores: Dict[str, float] = {}
        for axis_name, sp_codes in _TRIADIC_AXES.items():
            axis_count = sum(distribution.get(sp, 0) for sp in sp_codes)
            axis_scores[axis_name] = axis_count / total

        sign = axis_scores.get("sign", 0.0)
        bridge = axis_scores.get("bridge", 0.0)
        mind = axis_scores.get("mind", 0.0)

        values = [sign, bridge, mind]
        mean = sum(values) / 3.0
        variance = sum((v - mean) ** 2 for v in values) / 3.0
        balance = max(0.0, 1.0 - math.sqrt(variance) * 3.0)

        nonzero = [v for v in values if v > 0]
        if nonzero:
            harmonic = len(nonzero) / sum(1.0 / v for v in nonzero)
        else:
            harmonic = 0.0

        return ResonanceScore(
            sign_axis=sign,
            bridge_axis=bridge,
            mind_axis=mind,
            triadic_balance=balance,
            harmonic_mean=harmonic,
        )

    def _detect_warnings(
        self,
        distribution: Dict[str, int],
        resonance: ResonanceScore,
        total: int,
    ) -> List[str]:
        warnings: List[str] = []

        if resonance.triadic_balance < 0.3:
            warnings.append("Severe triadic imbalance detected")

        if resonance.sign_axis == 0.0 and total > 2:
            warnings.append("No sign-axis primitives (assertion, distinction, negation, scope)")

        if resonance.bridge_axis == 0.0 and total > 2:
            warnings.append("No bridge-axis primitives (constraint, dependency, relation, grounding)")

        if resonance.mind_axis == 0.0 and total > 2:
            warnings.append("No mind-axis primitives (evaluation, uncertainty, unknown, commitment)")

        negation_count = distribution.get("SP-03", 0)
        assertion_count = distribution.get("SP-01", 0)
        if negation_count > assertion_count and assertion_count > 0:
            warnings.append("Negation exceeds assertion count; output may be predominantly negative")

        uncertainty_count = distribution.get("SP-07", 0) + distribution.get("SP-08", 0)
        if total > 0 and uncertainty_count / total > 0.5:
            warnings.append("Majority uncertainty/unknown content; output may lack substance")

        return warnings

    def _compute_overall_score(
        self,
        patterns: PatternAnalysis,
        resonance: ResonanceScore,
        warning_count: int,
    ) -> float:
        base = 0.5

        base += resonance.triadic_balance * 0.25

        base += resonance.harmonic_mean * 0.15

        if PatternType.BALANCED in patterns.detected_patterns:
            base += 0.1

        warning_penalty = min(warning_count * 0.05, 0.25)
        base -= warning_penalty

        return max(0.0, min(1.0, base))
