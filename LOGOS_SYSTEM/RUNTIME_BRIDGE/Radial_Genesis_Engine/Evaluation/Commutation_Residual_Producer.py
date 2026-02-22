# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Commutation_Residual_Producer
runtime_layer: logos_core_telemetry_production
role: Telemetry producer
responsibility: Extracts per-protocol commutation residuals from MESH validation output for RGE consumption.
agent_binding: Logos_Agent
protocol_binding: None
runtime_classification: telemetry_production
boot_phase: Phase-A-Telemetry
expected_imports: [Telemetry_Snapshot.ProtocolResiduals]
provides: [produce_residuals, MeshCommutationOutput, ProtocolCommutationResult]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Returns zero residuals (neutral) on missing or malformed MESH output. No partial extraction propagates."
rewrite_provenance:
  source: Constraint_Taxonomy_Spec.md §8.3, Capability_Function_Spec.md §6
  rewrite_phase: Phase_A_Telemetry_Producer
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Logos_Core - Commutation_Residual_Producer
Deterministic extraction of per-protocol commutation residuals.
References: Constraint_Taxonomy_Spec.md §8.3, Capability_Function_Spec.md §6

Consumes MESH bijection commutation validation output.
Extracts per-protocol residual magnitudes R_j.
Does NOT perform commutation validation itself.

Logos Core authority. RGE does not invoke this module.
No execution authority. No identity mutation. No spine mutation.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    ProtocolResiduals,
)

_KNOWN_PROTOCOLS = frozenset({"SCP", "MTP", "ARP"})
_NEUTRAL_RESIDUAL: float = 0.0

@dataclass(frozen=True)
class ProtocolCommutationResult:
    protocol_id: str
    residual_magnitude: float
    commutation_held: bool

    def __post_init__(self) -> None:
        if self.protocol_id not in _KNOWN_PROTOCOLS:
            raise ValueError(
                f"Unknown protocol_id: {self.protocol_id}. "
                f"Expected one of {sorted(_KNOWN_PROTOCOLS)}"
            )
        if not (0.0 <= self.residual_magnitude <= 1.0):
            raise ValueError(
                f"residual_magnitude must be in [0, 1], "
                f"got {self.residual_magnitude}"
            )

@dataclass(frozen=True)
class MeshCommutationOutput:
    results: tuple
    tick_id: str
    validation_complete: bool

    def __post_init__(self) -> None:
        for item in self.results:
            if not isinstance(item, ProtocolCommutationResult):
                raise TypeError(
                    f"results must contain ProtocolCommutationResult, "
                    f"got {type(item).__name__}"
                )
        seen: set = set()
        for item in self.results:
            if item.protocol_id in seen:
                raise ValueError(
                    f"Duplicate protocol_id in results: {item.protocol_id}"
                )
            seen.add(item.protocol_id)

def produce_residuals(
    mesh_output: Optional[MeshCommutationOutput],
) -> ProtocolResiduals:
    if mesh_output is None:
        return ProtocolResiduals(
            R_SCP=_NEUTRAL_RESIDUAL,
            R_MTP=_NEUTRAL_RESIDUAL,
            R_ARP=_NEUTRAL_RESIDUAL,
        )

    if not mesh_output.validation_complete:
        return ProtocolResiduals(
            R_SCP=_NEUTRAL_RESIDUAL,
            R_MTP=_NEUTRAL_RESIDUAL,
            R_ARP=_NEUTRAL_RESIDUAL,
        )

    residual_map: Dict[str, float] = {}
    for result in mesh_output.results:
        residual_map[result.protocol_id] = result.residual_magnitude

    return ProtocolResiduals(
        R_SCP=residual_map.get("SCP", _NEUTRAL_RESIDUAL),
        R_MTP=residual_map.get("MTP", _NEUTRAL_RESIDUAL),
        R_ARP=residual_map.get("ARP", _NEUTRAL_RESIDUAL),
    )
