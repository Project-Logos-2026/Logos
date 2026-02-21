"""
Radial_Genesis_Engine - Triad_Region_Classifier
Pure function: classifies a task triad into one of 7 simplex regions.
References: Capability_Function_Spec.md §3

Partition:
    R_E  — E-strong (E > 0.5)
    R_G  — G-strong (G > 0.5)
    R_T  — T-strong (T > 0.5)
    R_ET — E-T pair (max ≤ 0.5, min < 0.2, G is min)
    R_EG — E-G pair (max ≤ 0.5, min < 0.2, T is min)
    R_GT — G-T pair (max ≤ 0.5, min < 0.2, E is min)
    R_B  — Balanced (max ≤ 0.5, min ≥ 0.2)

Properties:
    - Complete: every normalized triad maps to exactly one region.
    - Deterministic: explicit tie-break by alphabetical axis precedence.
    - No state. No side effects. No imports beyond typing.

No execution authority. No identity mutation. No spine mutation.
"""

from typing import Tuple

REGION_E = "R_E"
REGION_G = "R_G"
REGION_T = "R_T"
REGION_ET = "R_ET"
REGION_EG = "R_EG"
REGION_GT = "R_GT"
REGION_B = "R_B"

ALL_REGIONS = (REGION_E, REGION_G, REGION_T, REGION_ET, REGION_EG, REGION_GT, REGION_B)

_DOMINANCE_THRESHOLD = 0.5
_WEAK_THRESHOLD = 0.2


def classify_region(e: float, g: float, t: float) -> str:
    """
    Classify a task triad (E, G, T) into one of 7 simplex regions.

    Args:
        e: Existence axis value ∈ [0, 1]
        g: Goodness axis value ∈ [0, 1]
        t: Truth axis value ∈ [0, 1]

    Returns:
        Region ID string (one of R_E, R_G, R_T, R_ET, R_EG, R_GT, R_B).

    Tie-breaking:
        For max-axis ties: E wins over G wins over T.
        For min-axis ties: E < G < T (E classified as min first).
    """
    axes = [("E", e), ("G", g), ("T", t)]

    max_val = max(v for _, v in axes)
    min_val = min(v for _, v in axes)

    if max_val > _DOMINANCE_THRESHOLD:
        max_axis = _find_max_axis(axes)
        if max_axis == "E":
            return REGION_E
        elif max_axis == "G":
            return REGION_G
        else:
            return REGION_T

    if min_val < _WEAK_THRESHOLD:
        min_axis = _find_min_axis(axes)
        if min_axis == "G":
            return REGION_ET
        elif min_axis == "T":
            return REGION_EG
        else:
            return REGION_GT

    return REGION_B


def _find_max_axis(axes: list) -> str:
    """
    Find the axis with the maximum value.
    Tie-break: E > G > T (alphabetical precedence for max).
    """
    max_val = max(v for _, v in axes)
    for name, val in axes:
        if val == max_val:
            return name
    return axes[0][0]


def _find_min_axis(axes: list) -> str:
    """
    Find the axis with the minimum value.
    Tie-break: E < G < T (E is classified as min first).
    """
    min_val = min(v for _, v in axes)
    for name, val in axes:
        if val == min_val:
            return name
    return axes[0][0]


def classify_from_triad(triad) -> str:
    """Convenience: classify from a Triad dataclass."""
    return classify_region(triad.E, triad.G, triad.T)
