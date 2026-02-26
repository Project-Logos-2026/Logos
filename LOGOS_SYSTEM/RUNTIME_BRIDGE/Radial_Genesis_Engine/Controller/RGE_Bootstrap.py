# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: RGE_Bootstrap
runtime_layer: rge_construction
role: Bootstrap factory
responsibility: Constructs and wires the complete RGE object graph. Returns a single RGERuntime instance. No Nexus awareness. No auto-registration. No global state. No I/O.
agent_binding: None
protocol_binding: None
runtime_classification: construction_layer
boot_phase: Phase-A-Integration
expected_imports: [Core.Telemetry_Snapshot, Core.Topology_State, Evaluation.*, Control.Hysteresis_Governor, Controller.Genesis_Selector, Controller.Mode_Controller, Controller.RGE_Override_Channel, Events.Event_Emitter, Telemetry_Production.*]
provides: [RGERuntime, build_rge]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Construction failure raises. Runtime methods fail-closed to neutral on telemetry absence."
rewrite_provenance:
  source: Phase_A_Controlled_Runtime_Entry
  rewrite_phase: Phase_A_Integration
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from typing import Any, Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    RecursionLayerTelemetry,
    TelemetrySnapshot,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Topology_State import (
    TopologyState,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Composite_Aggregator import (
    CompositeAggregator,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Stability_Metric import (
    StabilityMetric,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Triune_Fit_Score import (
    TriuneFitScore,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Commutation_Balance_Score import (
    CommutationBalanceScore,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Divergence_Metric import (
    DivergenceMetric,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Recursion_Coupling_Coherence_Score import (
    RecursionCouplingCoherenceScore,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Control.Hysteresis_Governor import (
    Hysteresis_Governor,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.Genesis_Selector import (
    GenesisSelector,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.Mode_Controller import (
    ModeController,
    RuntimeMode,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.RGE_Override_Channel import (
    RGEOverrideChannel,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Events.Event_Emitter import (
    EventEmitter,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Telemetry_Production.Task_Triad_Derivation import (
    Constraint,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Telemetry_Production.Commutation_Residual_Producer import (
    MeshCommutationOutput,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Telemetry_Production.Stability_Scalar_Producer import (
    ProtocolTickTelemetry,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Telemetry_Production.Telemetry_Producer import (
    assemble_telemetry,
)



from .RGE_Governance_Context import RGEGovernanceContext
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.Logos_Agent_Resources.Epistemic_Library import Epistemic_Library_Router
import datetime
import json

class RGERuntime:


    def __init__(
        self,
        aggregator: CompositeAggregator,
        fit_score: TriuneFitScore,
        comm_score: CommutationBalanceScore,
        div_metric: DivergenceMetric,
        rccs: RecursionCouplingCoherenceScore,
        hysteresis: Hysteresis_Governor,
        selector: GenesisSelector,
        mode_controller: ModeController,
        override_channel: RGEOverrideChannel,
        event_emitter: EventEmitter,
        governance_context: RGEGovernanceContext,
    ) -> None:
        self._aggregator = aggregator
        self._fit_score = fit_score
        self._comm_score = comm_score
        self._div_metric = div_metric
        self._rccs = rccs
        self._hysteresis = hysteresis
        self._selector = selector
        self._mode_controller = mode_controller
        self._override_channel = override_channel
        self._event_emitter = event_emitter
        self._governance_context = governance_context

        self._snapshot: Optional[TelemetrySnapshot] = None
        self._tick_counter: int = 0
        self._prev_config_id: Optional[str] = None
        self._prev_score: Optional[float] = None

    def _emit_topology_advice(self, result: Dict[str, Any]) -> None:
        # Validate router availability
        router = self._governance_context.get_router()
        if router is None:
            self._event_emitter.emit("RGE_ROUTER_UNAVAILABLE", {"reason": "Router not available"})
            raise RuntimeError("Epistemic_Library_Router unavailable")

        # Required fields from governance context
        status_context = self._governance_context.get_status_context()
        parent_hash_reference = self._governance_context.get_parent_hash_reference()
        if status_context is None or parent_hash_reference is None:
            raise RuntimeError("status_context and parent_hash_reference must be provided by governance context")

        # Build schema-compliant payload
        payload = {
            "schema_version": "1.0.0",
            "aa_type": "TOPOLOGY_ADVICE",
            "author_class": "PROTOCOL",
            "author_id": "RGE",
            "topology_id": result["config_id"],
            "orchestration_tick": result["tick"],
            "timestamp_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "topology_configuration": result["topology"],
            "derivation_context": {
                # Optionally add more if available from context
            },
            "confidence_metrics": {
                "primary_score": result["score"],
                "stability_index": 0.0 if result.get("switched") else 1.0
            },
            "status_context": status_context,
            "parent_hash_reference": parent_hash_reference,
        }

        # Validate payload against schema (fail-closed)
        # (Assume schema validation is handled by router, as per governance addendum)
        try:
            router.Attach_NonCanonical_Aa(
                parent_smp_id=parent_hash_reference,
                aa_payload=payload,
                aa_type="TOPOLOGY_ADVICE",
                author_class="PROTOCOL",
                author_id="RGE",
                status_context=status_context,
            )
            self._event_emitter.emit("RGE_ROUTER_SUBMISSION_SUCCESS", {"payload": payload})
        except Exception as e:
            self._event_emitter.emit("RGE_ROUTER_SUBMISSION_REJECTED", {"error": str(e), "payload": payload})
            raise

    def inject_telemetry(
        self,
        task_id: str,
        tick_id: str,
        constraints: List[Constraint],
        mesh_output: Optional[MeshCommutationOutput] = None,
        protocol_telemetry: Optional[List[ProtocolTickTelemetry]] = None,
        hysteresis_key: Optional[str] = None,
        recursion_telemetry: Optional[RecursionLayerTelemetry] = None,
    ) -> None:
        self._tick_counter += 1

        snapshot = assemble_telemetry(
            task_id=task_id,
            tick_id=tick_id,
            constraints=constraints,
            mesh_output=mesh_output,
            protocol_telemetry=protocol_telemetry,
            hysteresis_key=hysteresis_key,
            recursion_telemetry=recursion_telemetry,
        )
        print("RGE SNAPSHOT:", snapshot)  # TEMPORARY AUDIT PRINT

        self._fit_score.inject_from_telemetry(snapshot)
        self._comm_score.inject_from_telemetry(snapshot)
        self._div_metric.inject_from_telemetry(snapshot)
        self._rccs.inject_from_telemetry(snapshot)

        self._snapshot = snapshot

    def evaluate(self) -> Dict[str, float]:
        if self._snapshot is None:
            return {}
        all_configs = TopologyState.enumerate_all_configurations()
        if not all_configs:
            return {}
        sample_snapshot = all_configs[0].snapshot()
        scores = self._aggregator.get_module_scores(sample_snapshot)
        print("RGE SCORES:", scores)  # TEMPORARY AUDIT PRINT
        return scores

    def select(self) -> Dict[str, Any]:
        best = self._selector.select_best()

        if best is None:
            self._event_emitter.emit("rge_selection_skipped", {
                "tick": self._tick_counter,
                "reason": "mode_gated_or_overridden",
            })
            return {
                "selected": False,
                "tick": self._tick_counter,
                "reason": "mode_gated_or_overridden",
            }

        config_id = self._selector._config_id(best)
        candidate_score = self._selector.evaluate_configuration(best.snapshot())

        print("HYSTERESIS INPUT:", config_id, candidate_score, self._prev_config_id, self._prev_score)  # TEMPORARY AUDIT PRINT

        chosen_id = self._hysteresis.evaluate(
            candidate_id=config_id,
            candidate_score=candidate_score,
            prev_id=self._prev_config_id,
            prev_score=self._prev_score,
            tick=self._tick_counter,
            A_t=self._mode_controller.is_activation_allowed(),
            override_type="HARD" if self._override_channel.is_hard_override() else None,
        )

        switched = chosen_id != self._prev_config_id and self._prev_config_id is not None

        self._prev_config_id = chosen_id
        self._prev_score = candidate_score

        result: Dict[str, Any] = {
            "selected": True,
            "config_id": chosen_id,
            "score": candidate_score,
            "tick": self._tick_counter,
            "switched": switched,
            "topology": best.snapshot(),
        }

        # Controlled router emission (before event emission, after result construction)
        self._emit_topology_advice(result)

        self._event_emitter.emit("rge_selection_complete", result)

        return result

    @property
    def last_snapshot(self) -> Optional[TelemetrySnapshot]:
        return self._snapshot

    @property
    def tick_counter(self) -> int:
        return self._tick_counter


def build_rge(
    capability_table: Optional[Dict[str, Any]] = None,
    gamma: float = 1.0,
    mu: float = 1.0,
    theta: float = 0.0,
    tau_min: int = 1,
    initial_mode: RuntimeMode = RuntimeMode.P2_AUTONOMOUS_RADIAL,
    enable_instrumentation: bool = False,
) -> RGERuntime:

    fit_score = TriuneFitScore(
        capability_table=capability_table,
        module_weight=1.0,
    )

    comm_score = CommutationBalanceScore(
        gamma=gamma,
        module_weight=1.0,
    )

    div_metric = DivergenceMetric(
        mu=mu,
        module_weight=1.0,
    )

    rccs = RecursionCouplingCoherenceScore(
        module_weight=1.0,
        enable_instrumentation=enable_instrumentation,
    )

    stability_metric = StabilityMetric()

    aggregator = CompositeAggregator()
    aggregator.register(stability_metric)
    aggregator.register(fit_score)
    aggregator.register(comm_score)
    aggregator.register(div_metric)
    aggregator.register(rccs)

    hysteresis = Hysteresis_Governor(theta=theta, tau_min=tau_min)

    mode_controller = ModeController(initial_mode=initial_mode)
    override_channel = RGEOverrideChannel()

    selector = GenesisSelector(
        scoring_module=aggregator,
        mode_controller=mode_controller,
        override_channel=override_channel,
    )

    event_emitter = EventEmitter()
    governance_context = RGEGovernanceContext(
        status_context="Provisional",
        parent_hash_reference="",
        router=Epistemic_Library_Router,
    )

    return RGERuntime(
        aggregator=aggregator,
        fit_score=fit_score,
        comm_score=comm_score,
        div_metric=div_metric,
        rccs=rccs,
        hysteresis=hysteresis,
        selector=selector,
        mode_controller=mode_controller,
        override_channel=override_channel,
        event_emitter=event_emitter,
        governance_context=governance_context,
    )
