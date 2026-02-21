"""
Radial_Genesis_Engine - Divergence_Metric (Triune-Integrated)
ScoringInterface implementation computing C_stab(ω; x).
References: Capability_Function_Spec.md §6

Implements the stability penalty:
    C_stab(ω; x) = μ · Σ_k w_k^prio(ω) · (1 - S_{A_ω(k)}(x))

Where:
    S_j(x) ∈ [0, 1] is the per-protocol stability scalar
    w_k^prio(ω) ∈ [0, 1] is the topology-derived priority for axis k
    Σ w_k^prio = 1 (normalized priority distribution)
    μ ≥ 0 is the stability weight

Bounded: C_stab ∈ [0, μ] with normalized priorities.
Stability scalars are produced by Logos from protocol telemetry.
RGE does not compute stability — it only consumes telemetry.

Replaces the original placeholder Divergence_Metric that returned 0.0.

No execution authority. No identity mutation. No spine mutation.
"""

from typing import Any, Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Scoring_Interface import (
    ScoringInterface,
)


class DivergenceMetric(ScoringInterface):
    """
    Scores topology configurations by protocol stability.

    Consumes per-protocol stability scalars (S_SCP, S_MTP, S_ARP)
    from Logos telemetry. Penalizes configurations that rely on
    unstable protocols by weighting instability by topology priority.

    If no stability data is injected, returns 0.0 (neutral, fail-closed).
    """

    def __init__(
        self,
        mu: float = 1.0,
        priority_weights: Optional[List[float]] = None,
        module_weight: float = 1.0,
    ) -> None:
        if mu < 0.0:
            raise ValueError("mu must be non-negative")

        self._mu = mu
        self._priority_weights = priority_weights or [0.25, 0.25, 0.25, 0.25]
        self._module_weight = module_weight
        self._stability: Dict[str, float] = {}

    def inject_stability(self, stability: Dict[str, float]) -> None:
        """
        Inject per-protocol stability scalars for current tick.

        Expected keys: "SCP", "MTP", "ARP". Values ∈ [0, 1].
        1.0 = fully stable. 0.0 = maximum instability.
        Missing protocols default to 1.0 (assumed stable, no penalty).
        """
        self._stability = {}
        for protocol, val in stability.items():
            if not (0.0 <= val <= 1.0):
                raise ValueError(
                    f"Stability for {protocol} must be in [0, 1], got {val}"
                )
            self._stability[protocol] = val

    def inject_from_telemetry(self, telemetry) -> None:
        """Inject stability from a TelemetrySnapshot object."""
        if telemetry.has_stability():
            self.inject_stability({
                "SCP": telemetry.stability.S_SCP,
                "MTP": telemetry.stability.S_MTP,
                "ARP": telemetry.stability.S_ARP,
            })

    def set_priority_weights(self, weights: List[float]) -> None:
        """
        Set topology-derived priority weights.

        Must sum to 1.0 (normalized distribution).
        """
        total = sum(weights)
        if abs(total - 1.0) > 0.01 and total > 0.0:
            raise ValueError(
                f"Priority weights must sum to 1.0, got {total:.4f}"
            )
        self._priority_weights = list(weights)

    def compute_score(self, snapshot: Dict[str, Any]) -> float:
        """
        Compute stability penalty for a topology configuration.

        For each axis k, computes (1 - S_j) for the assigned protocol,
        weights it by axis priority, and sums. Scaled by μ.

        Protocols not present in stability data are assumed stable (S=1.0),
        contributing 0 penalty. Fail-closed to no influence when no
        telemetry is available.
        """
        if not self.validate_snapshot(snapshot):
            return 0.0

        if not self._stability:
            return 0.0

        assignments = snapshot.get("agent_assignments", {})
        sorted_axes = sorted(assignments.keys())

        weighted_instability = 0.0
        for idx, axis_key in enumerate(sorted_axes):
            protocol = assignments[axis_key]
            w_prio = (
                self._priority_weights[idx]
                if idx < len(self._priority_weights)
                else 0.25
            )
            s_j = self._stability.get(protocol, 1.0)
            weighted_instability += w_prio * (1.0 - s_j)

        return self._mu * weighted_instability

    @property
    def name(self) -> str:
        return "divergence_metric"

    @property
    def weight(self) -> float:
        return self._module_weight

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def is_active(self) -> bool:
        return bool(self._stability)

    @property
    def mu(self) -> float:
        return self._mu
