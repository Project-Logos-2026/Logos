# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.1.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MSPC_Pipeline
runtime_layer: protocol_runtime
role: Pipeline stage executor
responsibility: Executes MSPC pipeline stages in deterministic sequence per tick.
    Phase 6 addition: accepts optional runtime_ref at construction. When present,
    queries active topology context and passes it to IncrementalCompiler during
    compilation stage. No behavior change when runtime_ref is None or when
    no active topology exists.
agent_binding: None
protocol_binding: Multi_Process_Signal_Compiler
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [MSPC_State, Signal_Ingress, Signal_Registry, Conflict_Resolver,
    Dependency_Graph, Incremental_Compiler, Artifact_Emitter, MSPC_Subscription_API,
    MSPCTelemetry, MSPCAuditLog]
provides: [MSPCPipeline, PipelineTickResult]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Any stage halt propagates. Tick cleanup always runs."
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

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSPC_State import (
    MSPCState,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Signals.Signal_Ingress import (
    SignalIngress,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Signals.Signal_Registry import (
    SignalRegistry,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Resolution.Conflict_Resolver import (
    ConflictResolver,
    ResolutionResult,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Compilation.Dependency_Graph import (
    DependencyGraph,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Incremental_Compiler import (
    IncrementalCompiler,
    CompilationResult,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Compilation.Artifact_Emitter import (
    ArtifactEmitter,
    EmissionBatch,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Contracts.MSPC_Subscription_API import (
    MSPCSubscriptionAPI,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Diagnostics.MSPC_Telemetry import (
    MSPCTelemetry,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.Diagnostics.MSPC_Audit_Log import (
    AuditEventType,
    MSPCAuditLog,
)


@dataclass
class PipelineTickResult:
    tick_number: int = 0
    signals_ingested: int = 0
    signals_registered: int = 0
    conflicts_detected: int = 0
    conflicts_resolved: int = 0
    artifacts_compiled: int = 0
    artifacts_emitted: int = 0
    artifacts_published: int = 0
    errors: List[Dict[str, Any]] = field(default_factory=list)
    halted: bool = False


class MSPCPipeline:

    def __init__(
        self,
        state: MSPCState,
        ingress: SignalIngress,
        registry: SignalRegistry,
        resolver: ConflictResolver,
        graph: DependencyGraph,
        compiler: IncrementalCompiler,
        emitter: ArtifactEmitter,
        subscription_api: MSPCSubscriptionAPI,
        telemetry: MSPCTelemetry,
        audit_log: MSPCAuditLog,
        runtime_ref: Any = None,
    ) -> None:
        self._state = state
        self._ingress = ingress
        self._registry = registry
        self._resolver = resolver
        self._graph = graph
        self._compiler = compiler
        self._emitter = emitter
        self._subscription_api = subscription_api
        self._telemetry = telemetry
        self._audit = audit_log
        self._runtime_ref = runtime_ref

    def execute_tick(self) -> PipelineTickResult:
        result = PipelineTickResult(tick_number=self._state.tick.tick_number)
        tick_num = result.tick_number
        self._telemetry.begin_tick(tick_num)
        self._audit.record(AuditEventType.TICK_STARTED, tick_num)
        try:
            result = self._stage_ingress(result, tick_num)
            if result.halted:
                return self._finalize_tick(result, tick_num)
            result = self._stage_registration(result, tick_num)
            if result.halted:
                return self._finalize_tick(result, tick_num)
            result = self._stage_conflict_resolution(result, tick_num)
            if result.halted:
                return self._finalize_tick(result, tick_num)
            result = self._stage_compilation(result, tick_num)
            if result.halted:
                return self._finalize_tick(result, tick_num)
            result = self._stage_emission(result, tick_num)
            if result.halted:
                return self._finalize_tick(result, tick_num)
            result = self._stage_publication(result, tick_num)
        except Exception as exc:
            result.errors.append({"stage": "pipeline", "error": str(exc)})
            result.halted = True
        return self._finalize_tick(result, tick_num)

    def _stage_ingress(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage("ingestion")
        ingested = self._ingress.ingest(None)
        result.signals_ingested = len(ingested)
        self._state._ingested_batch = ingested
        self._telemetry.end_stage(items_processed=len(ingested))
        return result

    def _stage_registration(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage("registration")
        ingested = getattr(self._state, "_ingested_batch", [])
        registered = 0
        for envelope in ingested:
            if self._registry.register(envelope):
                registered += 1
        result.signals_registered = registered
        self._telemetry.end_stage(items_processed=registered)
        return result

    def _stage_conflict_resolution(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage("conflict_resolution")
        ingested = getattr(self._state, "_ingested_batch", [])
        resolution: ResolutionResult = self._resolver.resolve(ingested)
        result.conflicts_detected = resolution.conflicts
        result.conflicts_resolved = resolution.conflicts
        self._state._resolved_signals = resolution.resolved
        self._telemetry.end_stage(items_processed=resolution.conflicts)
        return result

    def _stage_compilation(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage("compilation")
        resolved = getattr(self._state, "_resolved_signals", [])

        topology_context = None
        if self._runtime_ref is not None:
            accessor = getattr(self._runtime_ref, "get_active_topology_context", None)
            if accessor is not None:
                topology_context = accessor()

        compilation: CompilationResult = self._compiler.compile_batch(
            resolved,
            self._graph,
            topology_context=topology_context,
        )

        result.artifacts_compiled = len(compilation.compiled)
        self._state._compiled_artifacts = compilation.compiled
        if compilation.errors:
            for err in compilation.errors:
                self._audit.record(AuditEventType.COMPILATION_ERROR, tick_num, err)
        self._telemetry.end_stage(
            items_processed=len(compilation.compiled),
            errors=len(compilation.errors),
        )
        return result

    def _stage_emission(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage("emission")
        artifacts = getattr(self._state, "_compiled_artifacts", [])
        emission: EmissionBatch = self._emitter.emit_batch(artifacts)
        result.artifacts_emitted = len(emission.emitted)
        self._state.tick.artifacts_emitted_this_tick = len(emission.emitted)
        for emitted in emission.emitted:
            self._state.emitted_artifacts.append({
                "emission_id": emitted.emission_id,
                "artifact_id": emitted.artifact_id,
                "version_tag": emitted.version_tag,
            })
            self._audit.record(AuditEventType.ARTIFACT_EMITTED, tick_num, {
                "emission_id": emitted.emission_id,
            })
        self._state._emitted_batch = emission.emitted
        self._telemetry.end_stage(
            items_processed=len(emission.emitted),
            errors=len(emission.errors),
        )
        return result

    def _stage_publication(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage("publication")
        emitted = getattr(self._state, "_emitted_batch", [])
        delivered = self._subscription_api.publish(emitted)
        result.artifacts_published = delivered
        self._telemetry.end_stage(items_processed=delivered)
        return result

    def _finalize_tick(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._audit.record(AuditEventType.TICK_COMPLETED, tick_num, {
            "signals_ingested": result.signals_ingested,
            "artifacts_emitted": result.artifacts_emitted,
            "halted": result.halted,
        })
        self._telemetry.end_tick()
        for attr in ("_ingested_batch", "_resolved_signals", "_compiled_artifacts", "_emitted_batch"):
            if hasattr(self._state, attr):
                delattr(self._state, attr)
        return result
