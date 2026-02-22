# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Task_Triad_Derivation
runtime_layer: logos_core_telemetry_production
role: Telemetry producer
responsibility: Classifies task constraints into Three Pillars axes (E, G, T) and normalizes to bounded triad vector for RGE consumption.
agent_binding: Logos_Agent
protocol_binding: None
runtime_classification: telemetry_production
boot_phase: Phase-A-Telemetry
expected_imports: [Telemetry_Snapshot.Triad, Telemetry_Snapshot.RawCounts]
provides: [derive_triad, Constraint, TriadDerivationResult]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Returns zero triad on empty or invalid constraint sets. No partial derivation propagates."
rewrite_provenance:
  source: Constraint_Taxonomy_Spec.md §4-§6
  rewrite_phase: Phase_A_Telemetry_Producer
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Logos_Core - Task_Triad_Derivation
Deterministic constraint classification and triad normalization.
References: Constraint_Taxonomy_Spec.md §4-§6

Classifies task constraints into Three Pillars axes (E, G, T),
applies deterministic framing detection with total precedence
ordering (G > T > E), and normalizes to a bounded triad vector.

Logos Core authority. RGE does not invoke this module.
No execution authority. No identity mutation. No spine mutation.
No learning. No NLP. No stochastic behavior.
"""

from dataclasses import dataclass
from typing import FrozenSet, List, Tuple

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    Triad,
    RawCounts,
)

_EPSILON: float = 1e-10

_NORMATIVE_INDICATORS: FrozenSet[str] = frozenset({
    "goal",
    "purpose",
    "preference",
    "harm",
    "benefit",
    "ought",
    "should",
    "value",
    "agency",
    "obligation",
    "teleological",
    "normative",
    "ethical",
    "aligned",
})

_EPISTEMIC_INDICATORS: FrozenSet[str] = frozenset({
    "consistent",
    "valid",
    "provable",
    "coherent",
    "contradicts",
    "complete",
    "deterministic",
    "identity-preserving",
    "verified",
    "truthful",
    "proof",
    "logical",
    "sound",
})

@dataclass(frozen=True)
class Constraint:
    constraint_id: str
    framing_tags: FrozenSet[str]
    weight: float = 1.0
    critical: bool = False

    def __post_init__(self) -> None:
        if not self.constraint_id:
            raise ValueError("constraint_id must be non-empty")
        if self.weight <= 0.0:
            raise ValueError(
                f"Constraint weight must be > 0, got {self.weight}"
            )

@dataclass(frozen=True)
class TriadDerivationResult:
    triad: Triad
    raw_counts: RawCounts
    constraint_count: int
    classification_log: Tuple[Tuple[str, str, float], ...]

def _effective_weight(constraint: Constraint) -> float:
    base = constraint.weight
    if constraint.critical:
        return base * 2.0
    return base

def _classify_single(tags: FrozenSet[str]) -> str:
    if tags & _NORMATIVE_INDICATORS:
        return "G"
    if tags & _EPISTEMIC_INDICATORS:
        return "T"
    return "E"

def derive_triad(constraints: List[Constraint]) -> TriadDerivationResult:
    c_e: float = 0.0
    c_g: float = 0.0
    c_t: float = 0.0
    log_entries: List[Tuple[str, str, float]] = []

    sorted_constraints = sorted(constraints, key=lambda c: c.constraint_id)

    for constraint in sorted_constraints:
        axis = _classify_single(constraint.framing_tags)
        w = _effective_weight(constraint)

        if axis == "G":
            c_g += w
        elif axis == "T":
            c_t += w
        else:
            c_e += w

        log_entries.append((constraint.constraint_id, axis, w))

    total_weight = c_e + c_g + c_t

    if total_weight == 0.0:
        triad = Triad(E=0.0, G=0.0, T=0.0)
    else:
        s = total_weight + _EPSILON
        triad = Triad(
            E=c_e / s,
            G=c_g / s,
            T=c_t / s,
        )

    raw_counts = RawCounts(
        c_E=round(c_e),
        c_G=round(c_g),
        c_T=round(c_t),
    )

    return TriadDerivationResult(
        triad=triad,
        raw_counts=raw_counts,
        constraint_count=len(sorted_constraints),
        classification_log=tuple(log_entries),
    )
