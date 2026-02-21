"""
Radial_Genesis_Engine - Recursion_Coupling_Coherence_Score
ScoringInterface implementation computing C_cpl (recursion-layer coupling penalty).

Mathematical definition (locked):

    For each unordered layer pair (i, j):

    Raw residual:
        Res_ij = ||Δs~_i - Δs~_j||_1

    Normalized residual:
        Res^_ij = Res_ij / (ε + Res_ij)
        where ε = 1e-9

    Strain gate:
        g_i = (Layer_Residual_i + Layer_Stability_i) /
              (κ + Layer_Residual_i + Layer_Stability_i)
        where κ = 1.0

    Final coupling penalty:
        C_cpl = Σ_{i<j} w^cpl_ij · g_i · g_j · Res^_ij

Properties:
    - Bounded in [0, 1)
    - Deterministic
    - No recursion execution
    - No external calls
    - No projection matrices
    - No fractal math
    - Pure function

Optional instrumentation (toggle-controlled):
    - Captures per-pair breakdown from identical intermediate variables
    - No recomputation, no floating-point drift between score and report
    - Zero allocation overhead when disabled
    - Pure observer: never affects score output

Fail-closed: returns 0.0 if telemetry is missing, layers are absent,
or vector dimensions mismatch. No runtime exceptions during scoring.

No execution authority. No identity mutation. No spine mutation.
"""

import math
from typing import Any, Dict, List, Optional, Tuple

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Scoring_Interface import (
    ScoringInterface,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    RecursionLayerTelemetry,
    _generate_pair_key,
)


_EPSILON = 1e-9
_KAPPA = 1.0


class RecursionCouplingCoherenceScore(ScoringInterface):
    """
    Scores topology configurations by recursion-layer coupling coherence.

    Consumes RecursionLayerTelemetry from the telemetry snapshot.
    Measures how well recursion layers maintain commutation coherence
    by comparing shared delta vectors, weighted by per-layer strain
    and pairwise coupling weights.

    Optional instrumentation captures per-pair breakdown without
    affecting scoring math. Controlled by enable_instrumentation flag.

    If recursion telemetry is not injected, returns 0.0 (neutral).
    """

    def __init__(
        self,
        module_weight: float = 1.0,
        enable_instrumentation: bool = False,
    ) -> None:
        self._module_weight = module_weight
        self._enable_instrumentation = enable_instrumentation
        self._recursion_telemetry: Optional[RecursionLayerTelemetry] = None
        self._last_report: Optional[Dict[str, Any]] = None

    def inject_recursion_telemetry(
        self, telemetry: RecursionLayerTelemetry
    ) -> None:
        """
        Inject recursion-layer telemetry for current tick.

        Validation was already performed at RecursionLayerTelemetry
        construction time. This method stores the reference.
        """
        self._recursion_telemetry = telemetry

    def inject_from_telemetry(self, telemetry) -> None:
        """Inject recursion telemetry from a TelemetrySnapshot object."""
        if telemetry.has_recursion_telemetry():
            self.inject_recursion_telemetry(telemetry.recursion_telemetry)

    def compute_score(self, snapshot: Dict[str, Any]) -> float:
        """
        Compute recursion-layer coupling coherence penalty.

        For each unordered pair of recursion layers, computes the
        weighted product of strain gates and normalized delta residual.
        Sum is bounded in [0, 1).

        When instrumentation is enabled, captures per-pair breakdown
        from the same intermediate variables used in scoring. No
        separate recomputation. No floating-point drift.

        Returns 0.0 if:
            - No recursion telemetry injected
            - Snapshot validation fails
            - Any structural inconsistency detected at runtime

        Never raises during scoring. Fail-closed to neutral.
        """
        if self._enable_instrumentation:
            self._last_report = None

        if not self.validate_snapshot(snapshot):
            return 0.0

        rt = self._recursion_telemetry
        if rt is None:
            return 0.0

        try:
            return self._compute_coupling_penalty(rt)
        except Exception:
            return 0.0

    def _compute_coupling_penalty(
        self, rt: RecursionLayerTelemetry
    ) -> float:
        """
        Core computation. Single code path for both scoring and
        instrumentation. Intermediates captured from identical
        variables when instrumentation is enabled.

        C_cpl = Σ_{i<j} w^cpl_ij · g_i · g_j · Res^_ij
        """
        layers = rt.recursion_layers
        n = len(layers)
        instrument = self._enable_instrumentation

        if n < 2:
            return 0.0

        # Pre-compute strain gates for all layers
        strain_gates: Dict[str, float] = {}
        for layer in layers:
            r_i = rt.layer_residual.get(layer, 0.0)
            s_i = rt.layer_stability.get(layer, 0.0)
            numerator = r_i + s_i
            denominator = _KAPPA + numerator
            if denominator <= 0.0:
                strain_gates[layer] = 0.0
            else:
                strain_gates[layer] = numerator / denominator

        # Pre-compute shared delta vectors (as tuples for fast access)
        deltas: Dict[str, Tuple[float, ...]] = {}
        dim: Optional[int] = None
        for layer in layers:
            vec = rt.layer_shared_delta.get(layer)
            if vec is None:
                return 0.0
            if dim is None:
                dim = len(vec)
            elif len(vec) != dim:
                return 0.0
            deltas[layer] = vec

        if dim is None or dim == 0:
            return 0.0

        # Instrumentation: allocate pair list only when enabled
        pair_details: Optional[List[Dict[str, Any]]] = [] if instrument else None

        # Compute coupling penalty over all unordered pairs
        total = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                layer_i = layers[i]
                layer_j = layers[j]

                # L1 distance between shared delta vectors
                delta_i = deltas[layer_i]
                delta_j = deltas[layer_j]
                res_raw = 0.0
                for d in range(dim):
                    res_raw += abs(delta_i[d] - delta_j[d])

                # Normalized residual: Res^_ij = Res_ij / (ε + Res_ij)
                res_norm = res_raw / (_EPSILON + res_raw)

                # Strain gates
                g_i = strain_gates[layer_i]
                g_j = strain_gates[layer_j]

                # Coupling weight
                pair_key = _generate_pair_key(layer_i, layer_j)
                w_cpl = rt.coupling_weights.get(pair_key, 0.0)

                # Weighted contribution
                contribution = w_cpl * g_i * g_j * res_norm

                # Accumulate
                total += contribution

                # Capture from identical variables (no recomputation)
                if pair_details is not None:
                    pair_details.append({
                        "pair": pair_key,
                        "residual_raw": res_raw,
                        "residual_normalized": res_norm,
                        "g_i": g_i,
                        "g_j": g_j,
                        "weight": w_cpl,
                        "contribution": contribution,
                    })

        # Build instrumentation report from computed values
        if instrument:
            self._last_report = {
                "delta_dimensionality": dim,
                "pair_count": len(pair_details),
                "layers": list(layers),
                "strain_gates": dict(strain_gates),
                "pairs": pair_details,
                "total_coupling_penalty": total,
            }

        return total

    def get_last_instrumentation_report(self) -> Optional[Dict[str, Any]]:
        """
        Return the instrumentation report from the most recent
        compute_score call.

        Returns None if:
            - Instrumentation is disabled
            - No score has been computed yet
            - Telemetry was invalid (score returned 0.0)

        The report is replaced on each compute_score call.
        No cross-tick accumulation.
        """
        if not self._enable_instrumentation:
            return None
        return self._last_report

    @property
    def name(self) -> str:
        return "recursion_coupling_coherence"

    @property
    def weight(self) -> float:
        return self._module_weight

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def is_configured(self) -> bool:
        return self._recursion_telemetry is not None

    @property
    def instrumentation_enabled(self) -> bool:
        return self._enable_instrumentation
