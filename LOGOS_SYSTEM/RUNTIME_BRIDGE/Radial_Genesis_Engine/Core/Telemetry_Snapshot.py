"""
Radial_Genesis_Engine - Telemetry_Snapshot (V2)
Extends V1 with recursion-layer coupling telemetry.
References: Constraint_Taxonomy_Spec.md §7, Capability_Function_Spec.md §6

Additive extension only. All V1 fields preserved.
New: RecursionLayerTelemetry with validated layer registry,
shared delta vectors, layer magnitudes, and coupling weights.

Immutable once produced. RGE reads only. No mutation within a tick.
No execution authority. No identity mutation. No spine mutation.
No recursion execution. No projection matrices. No fractal math.
"""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Tuple


# ============================================================================
# V1 types (unchanged)
# ============================================================================

@dataclass(frozen=True)
class Triad:
    """Task Triad: normalized constraint mass across Three Pillars."""

    E: float
    G: float
    T: float

    def __post_init__(self) -> None:
        for name, val in [("E", self.E), ("G", self.G), ("T", self.T)]:
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"Triad.{name} must be in [0, 1], got {val}")
        total = self.E + self.G + self.T
        if total > 0.0 and abs(total - 1.0) > 0.01:
            raise ValueError(
                f"Triad components must sum to ≈1.0, got {total:.4f}"
            )

    def to_tuple(self) -> tuple:
        return (self.E, self.G, self.T)

    def to_dict(self) -> Dict[str, float]:
        return {"E": self.E, "G": self.G, "T": self.T}


@dataclass(frozen=True)
class RawCounts:
    """Raw constraint counts before normalization."""

    c_E: int
    c_G: int
    c_T: int

    def __post_init__(self) -> None:
        for name, val in [("c_E", self.c_E), ("c_G", self.c_G), ("c_T", self.c_T)]:
            if val < 0:
                raise ValueError(f"RawCounts.{name} must be ≥ 0, got {val}")

    def total(self) -> int:
        return self.c_E + self.c_G + self.c_T


@dataclass(frozen=True)
class ProtocolResiduals:
    """Per-protocol commutation residuals from MESH validation."""

    R_SCP: float = 0.0
    R_MTP: float = 0.0
    R_ARP: float = 0.0

    def __post_init__(self) -> None:
        for name, val in [
            ("R_SCP", self.R_SCP), ("R_MTP", self.R_MTP), ("R_ARP", self.R_ARP),
        ]:
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"ProtocolResiduals.{name} must be in [0, 1], got {val}")

    def for_protocol(self, protocol: str) -> float:
        return {"SCP": self.R_SCP, "MTP": self.R_MTP, "ARP": self.R_ARP}.get(protocol, 0.0)


@dataclass(frozen=True)
class ProtocolStability:
    """Per-protocol stability scalars from protocol telemetry."""

    S_SCP: float = 1.0
    S_MTP: float = 1.0
    S_ARP: float = 1.0

    def __post_init__(self) -> None:
        for name, val in [
            ("S_SCP", self.S_SCP), ("S_MTP", self.S_MTP), ("S_ARP", self.S_ARP),
        ]:
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"ProtocolStability.{name} must be in [0, 1], got {val}")

    def for_protocol(self, protocol: str) -> float:
        return {"SCP": self.S_SCP, "MTP": self.S_MTP, "ARP": self.S_ARP}.get(protocol, 1.0)


# ============================================================================
# V2 recursion-layer types
# ============================================================================

CANONICAL_RECURSION_LAYERS: Tuple[str, ...] = (
    "PROTOCOL_LOCAL",
    "AGENT_TRICORE",
    "TETRACONSCIOUS",
    "RUNTIME_BRIDGE_COMMUTATION",
    "SCP_BDN_DEEP",
)

_WEIGHT_SUM_TOLERANCE = 1e-9


def _validate_layer_keys(
    data: Dict[str, Any],
    expected_layers: Tuple[str, ...],
    field_name: str,
) -> None:
    """Validate that dict keys match the recursion layer registry exactly."""
    expected = set(expected_layers)
    actual = set(data.keys())
    if actual != expected:
        missing = expected - actual
        extra = actual - expected
        raise ValueError(
            f"{field_name}: key mismatch. "
            f"missing={missing or 'none'}, extra={extra or 'none'}"
        )


def _validate_finite_nonneg(
    data: Dict[str, float],
    field_name: str,
) -> None:
    """Validate all values are finite and ≥ 0."""
    for key, val in data.items():
        if not math.isfinite(val):
            raise ValueError(f"{field_name}[{key}] is not finite: {val}")
        if val < 0.0:
            raise ValueError(f"{field_name}[{key}] must be ≥ 0, got {val}")


def _generate_pair_key(layer_a: str, layer_b: str) -> str:
    """Canonical unordered pair key: alphabetically sorted, pipe-separated."""
    a, b = sorted([layer_a, layer_b])
    return f"{a}|{b}"


def _all_unordered_pairs(layers: Tuple[str, ...]) -> List[str]:
    """Generate all canonical unordered pair keys for a layer set."""
    pairs = []
    for i in range(len(layers)):
        for j in range(i + 1, len(layers)):
            pairs.append(_generate_pair_key(layers[i], layers[j]))
    return sorted(pairs)


@dataclass(frozen=True)
class RecursionLayerTelemetry:
    """
    Recursion-layer coupling telemetry. V2 extension.

    All fields are immutable. Validation is strict and fail-closed:
    any structural violation raises ValueError at construction time.
    Scoring modules return 0.0 if this object is absent from the snapshot.

    Fields:
        recursion_layers: Closed deterministic list of layer identifiers.
        layer_shared_delta: Per-layer shared delta vectors (all same dim D,
            each component ∈ [-1, +1], no NaN, no Inf).
        layer_residual: Per-layer residual magnitudes (≥ 0, finite).
        layer_stability: Per-layer stability magnitudes (≥ 0, finite).
        layer_throughput: Per-layer throughput magnitudes (≥ 0, finite).
        coupling_weights: Normalized pairwise coupling weights (sum = 1.0,
            keys are canonical unordered pairs "LAYER_A|LAYER_B").
    """

    recursion_layers: Tuple[str, ...]
    layer_shared_delta: Dict[str, Tuple[float, ...]]
    layer_residual: Dict[str, float]
    layer_stability: Dict[str, float]
    layer_throughput: Dict[str, float]
    coupling_weights: Dict[str, float]

    def __post_init__(self) -> None:
        layers = self.recursion_layers

        if len(layers) < 2:
            raise ValueError("At least 2 recursion layers required")

        # Validate layer_shared_delta keys and dimensionality
        _validate_layer_keys(self.layer_shared_delta, layers, "layer_shared_delta")
        dims = set()
        for layer, vec in self.layer_shared_delta.items():
            if not isinstance(vec, tuple):
                raise ValueError(
                    f"layer_shared_delta[{layer}] must be a tuple, got {type(vec)}"
                )
            dims.add(len(vec))
            for i, v in enumerate(vec):
                if not math.isfinite(v):
                    raise ValueError(
                        f"layer_shared_delta[{layer}][{i}] is not finite: {v}"
                    )
                if not (-1.0 <= v <= 1.0):
                    raise ValueError(
                        f"layer_shared_delta[{layer}][{i}] must be in [-1, 1], got {v}"
                    )
        if len(dims) != 1:
            raise ValueError(
                f"layer_shared_delta: inconsistent dimensionality {dims}"
            )
        if 0 in dims:
            raise ValueError("layer_shared_delta: zero-dimensional vectors not permitted")

        # Validate magnitude dicts
        _validate_layer_keys(self.layer_residual, layers, "layer_residual")
        _validate_finite_nonneg(self.layer_residual, "layer_residual")

        _validate_layer_keys(self.layer_stability, layers, "layer_stability")
        _validate_finite_nonneg(self.layer_stability, "layer_stability")

        _validate_layer_keys(self.layer_throughput, layers, "layer_throughput")
        _validate_finite_nonneg(self.layer_throughput, "layer_throughput")

        # Validate coupling weights
        expected_pairs = set(_all_unordered_pairs(layers))
        actual_pairs = set(self.coupling_weights.keys())
        if actual_pairs != expected_pairs:
            missing = expected_pairs - actual_pairs
            extra = actual_pairs - expected_pairs
            raise ValueError(
                f"coupling_weights: pair mismatch. "
                f"missing={missing or 'none'}, extra={extra or 'none'}"
            )
        for pair_key, w in self.coupling_weights.items():
            if not math.isfinite(w):
                raise ValueError(f"coupling_weights[{pair_key}] not finite: {w}")
            if w < 0.0:
                raise ValueError(f"coupling_weights[{pair_key}] must be ≥ 0, got {w}")
        w_sum = sum(self.coupling_weights.values())
        if abs(w_sum - 1.0) > _WEIGHT_SUM_TOLERANCE:
            raise ValueError(
                f"coupling_weights must sum to 1.0, got {w_sum:.12f}"
            )

    @property
    def delta_dimensionality(self) -> int:
        """Shared dimensionality D of all delta vectors."""
        if not self.layer_shared_delta:
            return 0
        first = next(iter(self.layer_shared_delta.values()))
        return len(first)

    @property
    def pair_count(self) -> int:
        return len(self.coupling_weights)

    def get_pair_weight(self, layer_a: str, layer_b: str) -> float:
        key = _generate_pair_key(layer_a, layer_b)
        return self.coupling_weights.get(key, 0.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recursion_layers": list(self.recursion_layers),
            "layer_shared_delta": {
                k: list(v) for k, v in self.layer_shared_delta.items()
            },
            "layer_residual": dict(self.layer_residual),
            "layer_stability": dict(self.layer_stability),
            "layer_throughput": dict(self.layer_throughput),
            "coupling_weights": dict(self.coupling_weights),
        }


# ============================================================================
# V2 snapshot (extends V1)
# ============================================================================

@dataclass(frozen=True)
class TelemetrySnapshot:
    """
    Complete Logos→RGE telemetry snapshot (V2).

    Extends V1 with optional recursion-layer coupling telemetry.
    All V1 fields preserved. Backward compatible: recursion_telemetry
    defaults to None.

    Immutable once produced. RGE reads only.
    No feedback loops within a single tick.
    """

    task_id: str
    tick_id: str
    triad: Triad
    raw_counts: RawCounts
    residuals: Optional[ProtocolResiduals] = None
    stability: Optional[ProtocolStability] = None
    hysteresis_key: Optional[str] = None
    recursion_telemetry: Optional[RecursionLayerTelemetry] = None

    def has_residuals(self) -> bool:
        return self.residuals is not None

    def has_stability(self) -> bool:
        return self.stability is not None

    def has_recursion_telemetry(self) -> bool:
        return self.recursion_telemetry is not None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "task_id": self.task_id,
            "tick_id": self.tick_id,
            "triad": self.triad.to_dict(),
            "raw_counts": {
                "c_E": self.raw_counts.c_E,
                "c_G": self.raw_counts.c_G,
                "c_T": self.raw_counts.c_T,
            },
            "immutable": True,
        }
        if self.residuals is not None:
            result["residuals"] = {
                "R_SCP": self.residuals.R_SCP,
                "R_MTP": self.residuals.R_MTP,
                "R_ARP": self.residuals.R_ARP,
            }
        if self.stability is not None:
            result["stability"] = {
                "S_SCP": self.stability.S_SCP,
                "S_MTP": self.stability.S_MTP,
                "S_ARP": self.stability.S_ARP,
            }
        if self.hysteresis_key is not None:
            result["hysteresis_key"] = self.hysteresis_key
        if self.recursion_telemetry is not None:
            result["recursion_telemetry"] = self.recursion_telemetry.to_dict()
        return result
