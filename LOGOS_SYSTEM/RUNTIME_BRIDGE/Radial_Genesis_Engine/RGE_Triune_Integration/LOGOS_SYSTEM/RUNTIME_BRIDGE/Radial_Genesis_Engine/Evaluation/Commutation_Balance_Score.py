"""
Radial_Genesis_Engine - Commutation_Balance_Score
ScoringInterface implementation computing C_comm(ω; x).
References: Capability_Function_Spec.md §6

Implements the commutation alignment penalty:
    C_comm(ω; x) = γ · Σ_k w_k^prio(ω) · R_{A_ω(k)}(x)

Where:
    R_j(x) ∈ [0, 1] is the per-protocol commutation residual
    w_k^prio(ω) ∈ [0, 1] is the topology-derived priority for axis k
    Σ w_k^prio = 1 (normalized priority distribution)
    γ ≥ 0 is the commutation weight

Bounded: C_comm ∈ [0, γ] with normalized priorities.
Residuals are produced by Logos from MESH validation.
RGE does not compute commutation — it only consumes residuals.

No execution authority. No identity mutation. No spine mutation.
"""

from typing import Any, Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Scoring_Interface import (
    ScoringInterface,
)


class CommutationBalanceScore(ScoringInterface):
    """
    Scores topology configurations by commutation preservation.

    Consumes per-protocol commutation residuals (R_SCP, R_MTP, R_ARP)
    from Logos telemetry. Weights them by topology-derived priority
    to make commutation pressure topology-dependent.

    If no residuals are injected, returns 0.0 (neutral, fail-closed).
    """

    def __init__(
        self,
        gamma: float = 1.0,
        priority_weights: Optional[List[float]] = None,
        module_weight: float = 1.0,
    ) -> None:
        if gamma < 0.0:
            raise ValueError("gamma must be non-negative")

        self._gamma = gamma
        self._priority_weights = priority_weights or [0.25, 0.25, 0.25, 0.25]
        self._module_weight = module_weight
        self._residuals: Dict[str, float] = {}

    def inject_residuals(self, residuals: Dict[str, float]) -> None:
        """
        Inject per-protocol commutation residuals for current tick.

        Expected keys: "SCP", "MTP", "ARP". Values ∈ [0, 1].
        Missing protocols default to 0.0 (no penalty).
        """
        self._residuals = {}
        for protocol, val in residuals.items():
            if not (0.0 <= val <= 1.0):
                raise ValueError(
                    f"Residual for {protocol} must be in [0, 1], got {val}"
                )
            self._residuals[protocol] = val

    def inject_from_telemetry(self, telemetry) -> None:
        """Inject residuals from a TelemetrySnapshot object."""
        if telemetry.has_residuals():
            self.inject_residuals({
                "SCP": telemetry.residuals.R_SCP,
                "MTP": telemetry.residuals.R_MTP,
                "ARP": telemetry.residuals.R_ARP,
            })

    def set_priority_weights(self, weights: List[float]) -> None:
        """
        Set topology-derived priority weights.

        Must sum to 1.0 (normalized distribution).
        Called per evaluation cycle based on topology structure.
        """
        total = sum(weights)
        if abs(total - 1.0) > 0.01 and total > 0.0:
            raise ValueError(
                f"Priority weights must sum to 1.0, got {total:.4f}"
            )
        self._priority_weights = list(weights)

    def compute_score(self, snapshot: Dict[str, Any]) -> float:
        """
        Compute commutation balance penalty for a topology configuration.

        For each axis k, weights the assigned protocol's commutation
        residual by the axis priority. Total is scaled by γ.

        Returns 0.0 if no residuals are injected (fail-closed to no influence).
        """
        if not self.validate_snapshot(snapshot):
            return 0.0

        if not self._residuals:
            return 0.0

        assignments = snapshot.get("agent_assignments", {})
        sorted_axes = sorted(assignments.keys())

        weighted_residual = 0.0
        for idx, axis_key in enumerate(sorted_axes):
            protocol = assignments[axis_key]
            w_prio = (
                self._priority_weights[idx]
                if idx < len(self._priority_weights)
                else 0.25
            )
            r_j = self._residuals.get(protocol, 0.0)
            weighted_residual += w_prio * r_j

        return self._gamma * weighted_residual

    @property
    def name(self) -> str:
        return "commutation_balance"

    @property
    def weight(self) -> float:
        return self._module_weight

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def is_configured(self) -> bool:
        return bool(self._residuals)

    @property
    def gamma(self) -> float:
        return self._gamma
