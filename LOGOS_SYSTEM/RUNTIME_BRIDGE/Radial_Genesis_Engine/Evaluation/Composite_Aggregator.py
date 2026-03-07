"""
Radial_Genesis_Engine - Composite_Aggregator
Weighted combination of scoring modules.
Deterministic evaluation order. Produces composite score for Genesis_Selector.
References: RGE_SOVEREIGNTY_CONTRACT.md
"""

import math
from typing import Any, Dict, List, Tuple

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Scoring_Interface import (
    ScoringInterface,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Contracts.RGE_Telemetry_Snapshot_V2 import (
    RGETelemetrySnapshotV2,
)


class CompositeAggregator(ScoringInterface):
    """
    Aggregates multiple scoring modules into a single composite score.

    Evaluation order is fixed at construction time and never reordered.
    Weights are normalized so that absent modules do not skew totals.
    Implements ScoringInterface so it can be passed directly to Genesis_Selector.
    """

    def __init__(self, modules: List[Tuple[ScoringInterface, float]]) -> None:
        """
        Args:
            modules: List of (scoring_module, weight) pairs.
                     Evaluation proceeds in list order. Deterministic.
                     Weights must be non-negative.
        """
        if not modules:
            raise ValueError("CompositeAggregator requires at least one scoring module")

        for module, weight in modules:
            if weight < 0:
                raise ValueError(f"Negative weight for {module.name}: {weight}")

        self._modules: List[Tuple[ScoringInterface, float]] = list(modules)
        total_weight = sum(w for _, w in self._modules)
        if total_weight <= 0:
            raise ValueError("Total weight must be positive")
        self._total_weight = total_weight

    @property
    def name(self) -> str:
        return "composite_aggregator"

    def compute_score(self, configuration: Dict[str, Any]) -> float:
        weighted_sum = 0.0

        for module, weight in self._modules:
            try:
                component_score = module.compute_score(configuration)
            except Exception as exc:
                raise RuntimeError(
                    f"Scoring module '{module.name}' failed during evaluation"
                ) from exc

            if not isinstance(component_score, (int, float)) or not math.isfinite(component_score):
                raise ValueError(
                    f"Scoring module '{module.name}' produced invalid score: {component_score}"
                )

            weighted_sum += component_score * weight

        return weighted_sum / self._total_weight

    def compute_score_breakdown(self, configuration: Dict[str, Any]) -> Dict[str, float]:
        """Return per-module score breakdown for audit and snapshot."""
        breakdown: Dict[str, float] = {}
        for module, weight in self._modules:
            breakdown[module.name] = module.compute_score(configuration)
        breakdown["composite"] = self.compute_score(configuration)
        return breakdown

    def generate_telemetry_snapshot(
        self, configuration_id: str, configuration: Dict[str, Any]
    ) -> RGETelemetrySnapshotV2:
        module_scores = self.compute_score_breakdown(configuration)
        composite_score = self.compute_score(configuration)

        snapshot = RGETelemetrySnapshotV2(
            configuration_id=configuration_id,
            composite_score=composite_score,
            module_scores=module_scores,
            completion_score=0.0,
            completion_potential=0.0,
            participant_count=len(module_scores),
            participant_diversity=float(len(module_scores)),
            resonance_score=0.0,
            novelty_score=0.0,
            telemetry_tags=["evaluation_cycle"],
            metadata={},
        )

        return snapshot

    @property
    def module_names(self) -> List[str]:
        return [m.name for m, _ in self._modules]
