# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Telemetry_Producer
runtime_layer: logos_core_telemetry_production
role: Telemetry assembly
responsibility: Orchestrates triad derivation, residual extraction, and stability aggregation into a single immutable TelemetrySnapshot for RGE consumption.
agent_binding: Logos_Agent
protocol_binding: None
runtime_classification: telemetry_production
boot_phase: Phase-A-Telemetry
expected_imports: [Telemetry_Snapshot.TelemetrySnapshot, Task_Triad_Derivation, Commutation_Residual_Producer, Stability_Scalar_Producer]
provides: [assemble_telemetry]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Produces valid snapshot on all paths. Missing optional inputs yield neutral defaults. Triad derivation failure yields zero triad triggering RGE default topology."
rewrite_provenance:
  source: Constraint_Taxonomy_Spec.md §7, Capability_Function_Spec.md §9
  rewrite_phase: Phase_A_Telemetry_Producer
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Logos_Core - Telemetry_Producer
Deterministic assembly of immutable TelemetrySnapshot.
References: Constraint_Taxonomy_Spec.md §7, Capability_Function_Spec.md §9

Calls triad derivation, residual production, and stability production.
Assembles results into a single TelemetrySnapshot (existing V2 class).
Pure assembly. No injection logic. No scoring. No topology selection.

Logos Core authority. RGE does not invoke this module.
No execution authority. No identity mutation. No spine mutation.
"""

from typing import List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    ProtocolResiduals,
    ProtocolStability,
    RecursionLayerTelemetry,
    TelemetrySnapshot,
)

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Task_Triad_Derivation import (
    Constraint,
    TriadDerivationResult,
    derive_triad,
)

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Commutation_Residual_Producer import (
    MeshCommutationOutput,
    produce_residuals,
)

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Stability_Scalar_Producer import (
    ProtocolTickTelemetry,
    produce_stability,
)

def assemble_telemetry(
    task_id: str,
    tick_id: str,
    constraints: List[Constraint],
    mesh_output: Optional[MeshCommutationOutput] = None,
    protocol_telemetry: Optional[List[ProtocolTickTelemetry]] = None,
    hysteresis_key: Optional[str] = None,
    recursion_telemetry: Optional[RecursionLayerTelemetry] = None,
) -> TelemetrySnapshot:
    derivation: TriadDerivationResult = derive_triad(constraints)

    residuals: ProtocolResiduals = produce_residuals(mesh_output)

    stability: ProtocolStability = produce_stability(protocol_telemetry)

    snapshot = TelemetrySnapshot(
        task_id=task_id,
        tick_id=tick_id,
        triad=derivation.triad,
        raw_counts=derivation.raw_counts,
        residuals=residuals,
        stability=stability,
        hysteresis_key=hysteresis_key,
        recursion_telemetry=recursion_telemetry,
    )

    return snapshot
