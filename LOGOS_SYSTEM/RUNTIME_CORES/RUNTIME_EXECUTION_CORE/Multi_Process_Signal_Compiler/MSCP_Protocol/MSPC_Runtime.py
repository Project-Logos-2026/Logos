from __future__ import annotations
import uuid
from typing import Any, Dict, Optional

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.MSPC_Config import (
    ExecutionMode,
    MSPCConfig,
    load_config,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.MSPC_State import (
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

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Signals.Signal_Ingress import (
    SignalIngress,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Signals.Signal_Registry import (
    SignalRegistry,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Resolution.Conflict_Resolver import (
    ConflictResolver,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Dependency_Graph import (
    DependencyGraph,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Incremental_Compiler import (
    IncrementalCompiler,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Artifact_Emitter import (
    ArtifactEmitter,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Contracts.MSPC_Subscription_API import (
    MSPCSubscriptionAPI,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Diagnostics.MSPC_Telemetry import (
    MSPCTelemetry,
)

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Diagnostics.MSPC_Audit_Log import (
    MSPCAuditLog,
)

class MSPCBootError(Exception):
    pass

class MSPCRuntime:
    def register_mtp_egress(
        self,
        mtp_process_fn,
        smp_builder_fn=None,
    ) -> None:
        """
        Phase 6 explicit activation hook.

        Registers the MSPC → MTP egress router.
        Must be called after boot().
        """
        if self._subscription_api is None:
            raise MSPCBootError("Runtime not booted")

        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Contracts.MSPC_MTP_Router import (
            MSPCMTPRouter,
        )

        self._mtp_router = MSPCMTPRouter(
            mtp_process_fn=mtp_process_fn,
            smp_builder_fn=smp_builder_fn,
        )

        self._subscription_api.subscribe(self._mtp_router)

    def __init__(self, config_overrides: Optional[Dict[str, Any]]=None) -> None:
        self._config: MSPCConfig = load_config(config_overrides)
        self._state: MSPCState = MSPCState()
        self._ingress: Optional[SignalIngress] = None
        self._registry: Optional[SignalRegistry] = None
        self._resolver: Optional[ConflictResolver] = None
        self._graph: Optional[DependencyGraph] = None
        self._compiler: Optional[IncrementalCompiler] = None
        self._emitter: Optional[ArtifactEmitter] = None
        self._subscription_api: Optional[MSPCSubscriptionAPI] = None
        self._telemetry: Optional[MSPCTelemetry] = None
        self._audit: Optional[MSPCAuditLog] = None
        self._pipeline: Optional[MSPCPipeline] = None
        self._scheduler: Optional[MSPCScheduler] = None
        self._mtp_router = None
        self._topology_context = None
    def set_topology_context(self, topology_context) -> None:
        """
        Phase 6 topology activation hook.

        Sets the active TopologyContext used during compilation.
        """
        self._topology_context = topology_context

    def get_topology_context(self):
        return self._topology_context

    @property
    def config(self) -> MSPCConfig:
        return self._config

    @property
    def state(self) -> MSPCState:
        return self._state

    @property
    def ingress(self) -> SignalIngress:
        if self._ingress is None:
            raise MSPCBootError('Runtime not booted: ingress unavailable')
        return self._ingress

    @property
    def subscription_api(self) -> MSPCSubscriptionAPI:
        if self._subscription_api is None:
            raise MSPCBootError('Runtime not booted: subscription API unavailable')
        return self._subscription_api

    def boot(self) -> None:
        session_id = self._config.session_id or str(uuid.uuid4())
        self._state.initialize(session_id)
        try:
            self._ingress = SignalIngress(max_queue_size=self._config.max_pending_signals)
            self._registry = SignalRegistry()
            self._resolver = ConflictResolver()
            self._graph = DependencyGraph()
            self._compiler = IncrementalCompiler(max_depth=self._config.max_compilation_depth)
            self._emitter = ArtifactEmitter(version_prefix=self._config.artifact_version_prefix, hash_algorithm=self._config.artifact_hash_algorithm)
            self._subscription_api = MSPCSubscriptionAPI()

            # Phase 6: Optional MTP Router Registration
            try:
                from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Contracts.MSPC_MTP_Router import MSPCMTPRouter
            except Exception:
                MSPCMTPRouter = None

            if MSPCMTPRouter is not None:
                # mtp_process_fn must be injected externally later
                self._mtp_router = None

            self._telemetry = MSPCTelemetry(enabled=self._config.enable_telemetry)
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
            self._scheduler = MSPCScheduler(config=self._config, state=self._state, pipeline=self._pipeline)
            self._state.transition(RuntimePhase.READY)
        except Exception as exc:
            self._state.transition(RuntimePhase.ERROR)
            raise MSPCBootError(f'Boot failed: {exc}') from exc

    def start(self) -> None:
        if self._state.phase != RuntimePhase.READY:
            raise MSPCBootError(f'Cannot start from phase {self._state.phase.value}')
        self._state.transition(RuntimePhase.RUNNING)

    def tick(self) -> PipelineTickResult:
        if self._scheduler is None:
            raise MSPCBootError('Runtime not booted')
        return self._scheduler.tick_once()

    def run(self, max_ticks: Optional[int]=None) -> int:
        if self._scheduler is None:
            raise MSPCBootError('Runtime not booted')
        return self._scheduler.run_continuous(max_ticks=max_ticks)

    def halt(self) -> None:
        if self._scheduler is not None:
            self._scheduler.request_halt()
        if self._state.phase not in (RuntimePhase.HALTED, RuntimePhase.UNINITIALIZED):
            try:
                self._state.transition(RuntimePhase.HALTED)
            except RuntimeError:
                pass

    def snapshot(self) -> Dict[str, Any]:
        base = self._state.snapshot()
        if self._telemetry is not None:
            base['telemetry'] = self._telemetry.aggregate()
        if self._audit is not None:
            base['audit'] = self._audit.summary()
        if self._scheduler is not None:
            base['scheduler'] = self._scheduler.stats()
        if self._registry is not None:
            base['registry'] = self._registry.snapshot()
        if self._compiler is not None:
            base['compiler_cache_size'] = self._compiler.cache_size()
        if self._subscription_api is not None:
            base['subscriptions'] = self._subscription_api.stats()
        return base