# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Stability_Scalar_Producer
runtime_layer: logos_core_telemetry_production
role: Telemetry producer
responsibility: Aggregates per-protocol tick telemetry into bounded stability scalars for RGE consumption.
agent_binding: Logos_Agent
protocol_binding: None
runtime_classification: telemetry_production
boot_phase: Phase-A-Telemetry
expected_imports: [Telemetry_Snapshot.ProtocolStability]
provides: [produce_stability, ProtocolTickTelemetry]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Returns default stability (1.0, fully stable) on missing or malformed telemetry. No partial aggregation propagates."
rewrite_provenance:
  source: Capability_Function_Spec.md §6, Constraint_Taxonomy_Spec.md §7.2
  rewrite_phase: Phase_A_Telemetry_Producer
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Logos_Core - Stability_Scalar_Producer
Deterministic per-protocol stability scalar computation.
References: Capability_Function_Spec.md §6

Aggregates protocol tick telemetry into bounded stability scalars S_j.
S_j = 1.0 means fully stable (no penalty). S_j = 0.0 means maximum instability.
Per-tick only. No history. No smoothing. No learning.

Logos Core authority. RGE does not invoke this module.
No execution authority. No identity mutation. No spine mutation.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    ProtocolStability,
)

_KNOWN_PROTOCOLS = frozenset({"SCP", "MTP", "ARP"})
_DEFAULT_STABILITY: float = 1.0

@dataclass(frozen=True)
class ProtocolTickTelemetry:
    protocol_id: str
    packets_processed: int
    packets_rejected: int
    mre_budget_fraction: float
    mesh_violations: int

    def __post_init__(self) -> None:
        if self.protocol_id not in _KNOWN_PROTOCOLS:
            raise ValueError(
                f"Unknown protocol_id: {self.protocol_id}. "
                f"Expected one of {sorted(_KNOWN_PROTOCOLS)}"
            )
        if self.packets_processed < 0:
            raise ValueError(
                f"packets_processed must be >= 0, got {self.packets_processed}"
            )
        if self.packets_rejected < 0:
            raise ValueError(
                f"packets_rejected must be >= 0, got {self.packets_rejected}"
            )
        if not (0.0 <= self.mre_budget_fraction <= 1.0):
            raise ValueError(
                f"mre_budget_fraction must be in [0, 1], "
                f"got {self.mre_budget_fraction}"
            )
        if self.mesh_violations < 0:
            raise ValueError(
                f"mesh_violations must be >= 0, got {self.mesh_violations}"
            )

def _compute_single_stability(telemetry: ProtocolTickTelemetry) -> float:
    total_packets = telemetry.packets_processed + telemetry.packets_rejected
    if total_packets == 0:
        rejection_rate = 0.0
    else:
        rejection_rate = telemetry.packets_rejected / total_packets

    if total_packets == 0:
        violation_rate = 0.0
    else:
        violation_rate = min(telemetry.mesh_violations / total_packets, 1.0)

    budget_pressure = telemetry.mre_budget_fraction

    instability = (rejection_rate + violation_rate + budget_pressure) / 3.0

    stability = max(0.0, min(1.0, 1.0 - instability))

    return stability

def produce_stability(
    telemetry_reports: Optional[List[ProtocolTickTelemetry]],
) -> ProtocolStability:
    if telemetry_reports is None or len(telemetry_reports) == 0:
        return ProtocolStability(
            S_SCP=_DEFAULT_STABILITY,
            S_MTP=_DEFAULT_STABILITY,
            S_ARP=_DEFAULT_STABILITY,
        )

    stability_map: Dict[str, float] = {}
    for report in telemetry_reports:
        if report.protocol_id in stability_map:
            continue
        stability_map[report.protocol_id] = _compute_single_stability(report)

    return ProtocolStability(
        S_SCP=stability_map.get("SCP", _DEFAULT_STABILITY),
        S_MTP=stability_map.get("MTP", _DEFAULT_STABILITY),
        S_ARP=stability_map.get("ARP", _DEFAULT_STABILITY),
    )
