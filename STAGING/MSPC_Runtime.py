# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.1.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MSPC_Runtime
runtime_layer: protocol_runtime
role: MSPC lifecycle owner
responsibility: Instantiates and wires the MSPC pipeline, scheduler, and all
    subsystems. Phase 6 additions: holds active RGE topology state, processes
    topology advisory packets, exposes topology context for pipeline consumption,
    registers MTP egress router as a publication subscriber.
agent_binding: None
protocol_binding: Multi_Process_Signal_Compiler
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [MSPC_Config, MSPC_State, MSPC_Pipeline, MSPC_Scheduler,
    Signal_Ingress, Signal_Registry, Conflict_Resolver, Dependency_Graph,
    Incremental_Compiler, Artifact_Emitter, MSPC_Subscription_API,
    MSPCTelemetry, MSPCAuditLog, Topology_Context]
provides: [MSPCRuntime]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Advisory validation returns False on structural violation. No raise."
rewrite_provenance:
  source: Phase_6_MSPC_Topology_Enforcement
  rewrite_phase: Phase_6
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

import uuid
from typing import Any, Callable, Dict, Optional

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSPC_Config import (
    MSPCConfig,
    load_config,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSPC_State import (
    MSPCState,
    RuntimePhase,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.MSPC_Pipeline import (
    MSPCPipeline,
    PipelineTickResult,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.MSPC_Scheduler import (
    MSPCScheduler,
    SchedulerHalt,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Signals.Signal_Ingress import (
    SignalIngress,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Signals.Signal_Registry import (
    SignalRegistry,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Resolution.Conflict_Resolver import (
    ConflictResolver,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Compilation.Dependency_Graph import (
    DependencyGraph,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Incremental_Compiler import (
    IncrementalCompiler,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Compilation.Artifact_Emitter import (
    ArtifactEmitter,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Contracts.MSPC_Subscription_API import (
    MSPCSubscriptionAPI,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Diagnostics.MSPC_Telemetry import (
    MSPCTelemetry,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Diagnostics.MSPC_Audit_Log import (
    MSPCAuditLog,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Topology_Context import (
    TopologyContext,
)


class MSPCRuntime:

    def __init__(
        self,
        config: Optional[MSPCConfig] = None,
        mtp_process_fn: Optional[Callable[[Dict[str, Any]], Any]] = None,
        smp_builder_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> None:
        self._config = config or load_config()
        session_id = self._config.session_id or str(uuid.uuid4())

        self._state = MSPCState(session_id=session_id)
        self._ingress = SignalIngress()
        self._registry = SignalRegistry()
        self._resolver = ConflictResolver()
        self._graph = DependencyGraph()
        self._compiler = IncrementalCompiler(max_depth=self._config.max_compilation_depth)
        self._emitter = ArtifactEmitter(
            version_prefix=self._config.artifact_version_prefix,
            hash_algorithm=self._config.artifact_hash_algorithm,
        )
        self._subscription_api = MSPCSubscriptionAPI()
        self._telemetry = MSPCTelemetry()
        self._audit = MSPCAuditLog(session_id=session_id)

        self._pipeline = MSPCPipeline(
            state=self._state,
            ingress=self._ingress,
            registry=self._registry,
            resolver=self._resolver,
            graph=self._graph,
            compiler=self._compiler,
            emitter=self._emitter,
            subscription_api=self._subscription_api,
            telemetry=self._telemetry,
            audit_log=self._audit,
            runtime_ref=self,
        )

        self._scheduler = MSPCScheduler(
            config=self._config,
            state=self._state,
            pipeline=self._pipeline,
        )

        self._active_topology_config_id: Optional[str] = None
        self._active_topology: Optional[Dict[str, Any]] = None
        self._topology_tick: int = 0

        self._mtp_router_subscription_id: Optional[str] = None
        if mtp_process_fn is not None:
            self._register_mtp_router(mtp_process_fn, smp_builder_fn)

    # -----------------------------------------------------------------
    # Phase 6: MTP Router Registration
    # -----------------------------------------------------------------

    def _register_mtp_router(
        self,
        mtp_process_fn: Callable[[Dict[str, Any]], Any],
        smp_builder_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> None:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Contracts.MSPC_MTP_Router import (
            MSPCMTPRouter,
        )

        router = MSPCMTPRouter(
            mtp_process_fn=mtp_process_fn,
            smp_builder_fn=smp_builder_fn,
        )
        self._mtp_router_subscription_id = self._subscription_api.subscribe(router)

    # -----------------------------------------------------------------
    # Phase 6: Topology Advisory Processing
    # -----------------------------------------------------------------

    def apply_topology_advisory(self, advisory: Dict[str, Any]) -> bool:
        if not isinstance(advisory, dict):
            return False

        if advisory.get("type") != "rge_topology_recommendation":
            return False

        content = advisory.get("content")
        if not isinstance(content, dict):
            return False

        selected = content.get("selected")
        config_id = content.get("config_id")
        topology = content.get("topology")
        switched = content.get("switched")

        if not isinstance(selected, bool):
            return False
        if not isinstance(config_id, str):
            return False
        if not isinstance(topology, dict):
            return False
        if not isinstance(switched, bool):
            return False

        if not selected:
            return True

        tick = content.get("tick", 0)

        if config_id == self._active_topology_config_id:
            self._topology_tick = tick
            return True

        if not switched:
            self._topology_tick = tick
            return True

        self._active_topology_config_id = config_id
        self._active_topology = topology
        self._topology_tick = tick
        return True

    # -----------------------------------------------------------------
    # Phase 6: Topology Context Accessor
    # -----------------------------------------------------------------

    def get_active_topology_context(self) -> Optional[TopologyContext]:
        if self._active_topology_config_id is None:
            return None
        if self._active_topology is None:
            return None
        rotation_index = self._active_topology.get("rotation_index", 0)
        agent_assignments = self._active_topology.get("agent_assignments", {})
        if not isinstance(agent_assignments, dict):
            return None
        return TopologyContext(
            config_id=self._active_topology_config_id,
            rotation_index=rotation_index,
            agent_assignments=agent_assignments,
        )

    # -----------------------------------------------------------------
    # Existing Interface
    # -----------------------------------------------------------------

    @property
    def config(self) -> MSPCConfig:
        return self._config

    @property
    def state(self) -> MSPCState:
        return self._state

    @property
    def scheduler(self) -> MSPCScheduler:
        return self._scheduler

    @property
    def subscription_api(self) -> MSPCSubscriptionAPI:
        return self._subscription_api

    def initialize(self) -> None:
        self._state.transition(RuntimePhase.RUNNING)

    def shutdown(self) -> None:
        self._scheduler.request_halt()
        self._state.transition(RuntimePhase.HALTED)

    def tick(self) -> PipelineTickResult:
        return self._scheduler.tick_once()
