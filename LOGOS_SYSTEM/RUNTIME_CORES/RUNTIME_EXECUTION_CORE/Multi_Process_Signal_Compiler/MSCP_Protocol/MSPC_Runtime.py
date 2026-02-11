# File: MSPC_Runtime.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Entrypoint for the MSPC standalone runtime protocol. Manages
#   boot sequence, component initialization, state lifecycle, and
#   the top-level runtime loop. MSPC does not wait on any external
#   protocol to start. It loads config, initializes state, assembles
#   the pipeline, and enters the scheduler.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from Multi_Process_Signal_Compiler.MSPC_Config import (
    ExecutionMode,
    MSPCConfig,
    load_config,
)
from Multi_Process_Signal_Compiler.MSPC_State import MSPCState, RuntimePhase
from Multi_Process_Signal_Compiler.MSPC_Pipeline import MSPCPipeline, PipelineTickResult
from Multi_Process_Signal_Compiler.MSPC_Scheduler import MSPCScheduler, SchedulerHalt
from Multi_Process_Signal_Compiler.Signals.Signal_Ingress import SignalIngress
from Multi_Process_Signal_Compiler.Signals.Signal_Registry import SignalRegistry
from Multi_Process_Signal_Compiler.Resolution.Conflict_Resolver import ConflictResolver
from Multi_Process_Signal_Compiler.Compilation.Dependency_Graph import DependencyGraph
from Multi_Process_Signal_Compiler.Compilation.Incremental_Compiler import (
    IncrementalCompiler,
)
from Multi_Process_Signal_Compiler.Compilation.Artifact_Emitter import ArtifactEmitter
from Multi_Process_Signal_Compiler.Contracts.MSPC_Subscription_API import (
    MSPCSubscriptionAPI,
)
from Multi_Process_Signal_Compiler.Diagnostics.MSPC_Telemetry import MSPCTelemetry
from Multi_Process_Signal_Compiler.Diagnostics.MSPC_Audit_Log import MSPCAuditLog


class MSPCBootError(Exception):
    pass


class MSPCRuntime:
    def __init__(self, config_overrides: Optional[Dict[str, Any]] = None) -> None:
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

    @property
    def config(self) -> MSPCConfig:
        return self._config

    @property
    def state(self) -> MSPCState:
        return self._state

    @property
    def ingress(self) -> SignalIngress:
        if self._ingress is None:
            raise MSPCBootError("Runtime not booted: ingress unavailable")
        return self._ingress

    @property
    def subscription_api(self) -> MSPCSubscriptionAPI:
        if self._subscription_api is None:
            raise MSPCBootError("Runtime not booted: subscription API unavailable")
        return self._subscription_api

    def boot(self) -> None:
        session_id = self._config.session_id or str(uuid.uuid4())
        self._state.initialize(session_id)

        try:
            self._ingress = SignalIngress(
                max_queue_size=self._config.max_pending_signals,
            )
            self._registry = SignalRegistry()
            self._resolver = ConflictResolver()
            self._graph = DependencyGraph()
            self._compiler = IncrementalCompiler(
                max_depth=self._config.max_compilation_depth,
            )
            self._emitter = ArtifactEmitter(
                version_prefix=self._config.artifact_version_prefix,
                hash_algorithm=self._config.artifact_hash_algorithm,
            )
            self._subscription_api = MSPCSubscriptionAPI()
            self._telemetry = MSPCTelemetry(
                enabled=self._config.enable_telemetry,
            )
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
            )

            self._scheduler = MSPCScheduler(
                config=self._config,
                state=self._state,
                pipeline=self._pipeline,
            )

            self._state.transition(RuntimePhase.READY)

        except Exception as exc:
            self._state.transition(RuntimePhase.ERROR)
            raise MSPCBootError(f"Boot failed: {exc}") from exc

    def start(self) -> None:
        if self._state.phase != RuntimePhase.READY:
            raise MSPCBootError(
                f"Cannot start from phase {self._state.phase.value}"
            )
        self._state.transition(RuntimePhase.RUNNING)

    def tick(self) -> PipelineTickResult:
        if self._scheduler is None:
            raise MSPCBootError("Runtime not booted")
        return self._scheduler.tick_once()

    def run(self, max_ticks: Optional[int] = None) -> int:
        if self._scheduler is None:
            raise MSPCBootError("Runtime not booted")
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
            base["telemetry"] = self._telemetry.aggregate()
        if self._audit is not None:
            base["audit"] = self._audit.summary()
        if self._scheduler is not None:
            base["scheduler"] = self._scheduler.stats()
        if self._registry is not None:
            base["registry"] = self._registry.snapshot()
        if self._compiler is not None:
            base["compiler_cache_size"] = self._compiler.cache_size()
        if self._subscription_api is not None:
            base["subscriptions"] = self._subscription_api.stats()
        return base
