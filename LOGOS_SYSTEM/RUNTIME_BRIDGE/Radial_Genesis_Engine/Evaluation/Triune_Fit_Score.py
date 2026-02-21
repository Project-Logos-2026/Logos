"""
Radial_Genesis_Engine - Triune_Fit_Score
ScoringInterface implementation computing C_fit(ω; t).
References: Capability_Function_Spec.md §5, Constraint_Taxonomy_Spec.md

Implements the triadic fit cost:
    C_fit(ω; t) = Σ_k w_k · d(t, p_{A_ω(k)}(R(t)))

Where:
    d(t, p) = α_E·|E_x - p_E| + α_G·|G_x - p_G| + α_T·|T_x - p_T|
    (weighted L1 distance on the simplex)

Bounded: C_fit ∈ [0, 2·α_max·W] with defaults C_fit ∈ [0, 2].
Deterministic. Static capability lookup. No learning.

No execution authority. No identity mutation. No spine mutation.
"""

import json
from typing import Any, Dict, List, Optional, Tuple

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Scoring_Interface import (
    ScoringInterface,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Triad_Region_Classifier import (
    classify_region,
)


class TriuneFitScore(ScoringInterface):
    """
    Scores topology configurations by triadic fit between task triad
    and protocol capability vectors.

    Requires:
        - A loaded capability table (from Triune_Capability_Table.json).
        - A task triad injected per evaluation cycle via inject_triad().
        - Topology configuration snapshots with agent_assignments mapping
          axis IDs to protocol names.

    Returns lower scores for better-fitting configurations.
    """

    def __init__(
        self,
        capability_table: Optional[Dict[str, Any]] = None,
        alpha_e: float = 1.0,
        alpha_g: float = 1.0,
        alpha_t: float = 1.0,
        axis_weights: Optional[List[float]] = None,
        module_weight: float = 1.0,
    ) -> None:
        self._capability: Dict[str, Dict[str, List[float]]] = {}
        self._alpha_e = alpha_e
        self._alpha_g = alpha_g
        self._alpha_t = alpha_t
        self._axis_weights = axis_weights or [0.25, 0.25, 0.25, 0.25]
        self._module_weight = module_weight

        self._triad: Optional[Tuple[float, float, float]] = None
        self._region: Optional[str] = None

        if capability_table is not None:
            self._load_table(capability_table)

    def load_from_json(self, json_path: str) -> None:
        """Load capability table from JSON file."""
        with open(json_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self._load_table(data)

    def _load_table(self, data: Dict[str, Any]) -> None:
        """Load capability vectors from parsed table data."""
        vectors = data.get("capability_vectors", {})
        for protocol, regions in vectors.items():
            self._capability[protocol] = {}
            for region_id, vec in regions.items():
                if not isinstance(vec, list) or len(vec) != 3:
                    raise ValueError(
                        f"Invalid capability vector for {protocol}/{region_id}: {vec}"
                    )
                self._capability[protocol][region_id] = vec

    def inject_triad(self, e: float, g: float, t: float) -> None:
        """
        Inject task triad for the current evaluation cycle.
        Must be called once per tick, before Genesis_Selector enumerates.
        Classifies the triad into a region for capability lookup.
        """
        self._triad = (e, g, t)
        self._region = classify_region(e, g, t)

    def inject_from_telemetry(self, telemetry) -> None:
        """Inject triad from a TelemetrySnapshot object."""
        triad = telemetry.triad
        self.inject_triad(triad.E, triad.G, triad.T)

    def compute_score(self, snapshot: Dict[str, Any]) -> float:
        """
        Compute triadic fit cost for a topology configuration.

        For each axis k in the configuration, computes weighted L1 distance
        between the task triad and the assigned protocol's capability vector
        in the classified region.

        Returns 0.0 (neutral) if triad is not injected or capability table
        is not loaded. Fail-closed to no influence.
        """
        if not self.validate_snapshot(snapshot):
            return 0.0

        if self._triad is None or self._region is None:
            return 0.0

        if not self._capability:
            return 0.0

        assignments = snapshot.get("agent_assignments", {})
        e_x, g_x, t_x = self._triad

        total_cost = 0.0
        sorted_axes = sorted(assignments.keys())

        for idx, axis_key in enumerate(sorted_axes):
            protocol = assignments[axis_key]
            w_k = self._axis_weights[idx] if idx < len(self._axis_weights) else 0.25

            cap_vector = self._get_capability(protocol, self._region)
            if cap_vector is None:
                continue

            p_e, p_g, p_t = cap_vector
            distance = (
                self._alpha_e * abs(e_x - p_e)
                + self._alpha_g * abs(g_x - p_g)
                + self._alpha_t * abs(t_x - p_t)
            )
            total_cost += w_k * distance

        return total_cost

    def _get_capability(
        self, protocol: str, region: str
    ) -> Optional[Tuple[float, float, float]]:
        """Lookup capability vector for protocol in region."""
        protocol_data = self._capability.get(protocol)
        if protocol_data is None:
            return None
        vec = protocol_data.get(region)
        if vec is None:
            return None
        return (vec[0], vec[1], vec[2])

    @property
    def name(self) -> str:
        return "triune_fit_score"

    @property
    def weight(self) -> float:
        return self._module_weight

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def is_configured(self) -> bool:
        return bool(self._capability) and self._triad is not None

    @property
    def current_region(self) -> Optional[str]:
        return self._region
