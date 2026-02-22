from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.MSPC_State import MSPCState
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Signals.Signal_Ingress import SignalIngress
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Signals.Signal_Registry import SignalRegistry
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Resolution.Conflict_Resolver import ConflictResolver, ResolutionResult
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Dependency_Graph import DependencyGraph
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Incremental_Compiler import IncrementalCompiler, CompilationResult
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Compilation.Artifact_Emitter import ArtifactEmitter, EmissionBatch
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Contracts.MSPC_Subscription_API import MSPCSubscriptionAPI
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Diagnostics.MSPC_Telemetry import MSPCTelemetry
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Diagnostics.MSPC_Audit_Log import AuditEventType, MSPCAuditLog

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

    def __init__(self, state: MSPCState, ingress: SignalIngress, registry: SignalRegistry, resolver: ConflictResolver, graph: DependencyGraph, compiler: IncrementalCompiler, emitter: ArtifactEmitter, subscription_api: MSPCSubscriptionAPI, telemetry: MSPCTelemetry, audit_log: MSPCAuditLog) -> None:
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
            result.errors.append({'stage': 'pipeline_unhandled', 'error': str(exc)})
            result.halted = True
            self._state.record_error('pipeline', str(exc))
            self._audit.record(AuditEventType.RUNTIME_ERROR, tick_num, {'error': str(exc)})
        return self._finalize_tick(result, tick_num)

    def _stage_ingress(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage('ingress')
        batch = self._ingress.drain()
        result.signals_ingested = len(batch)
        self._state.tick.signals_ingested_this_tick = len(batch)
        self._telemetry.end_stage(items_processed=len(batch))
        self._state._ingested_batch = batch
        return result

    def _stage_registration(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage('registration')
        batch = getattr(self._state, '_ingested_batch', [])
        reg_results = self._registry.register_batch(batch)
        registered = sum((1 for v in reg_results.values() if v))
        result.signals_registered = registered
        for sid, accepted in reg_results.items():
            event = AuditEventType.SIGNAL_REGISTERED if accepted else AuditEventType.SIGNAL_REJECTED
            self._audit.record(event, tick_num, {'signal_id': sid})
        self._telemetry.end_stage(items_processed=registered)
        return result

    def _stage_conflict_resolution(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage('conflict_resolution')
        active = self._registry.active_signals()
        resolution: ResolutionResult = self._resolver.resolve(active)
        result.conflicts_detected = resolution.conflicts_detected
        result.conflicts_resolved = resolution.conflicts_resolved
        self._state.tick.conflicts_resolved_this_tick = resolution.conflicts_resolved
        for blocked in resolution.blocked:
            self._state.blocked_signals[blocked.signal_id] = blocked
            self._audit.record(AuditEventType.CONFLICT_RESOLVED, tick_num, {'blocked_id': blocked.signal_id})
        for esc in resolution.escalations:
            self._state.escalation_queue.append(esc)
            self._audit.record(AuditEventType.CONFLICT_ESCALATED, tick_num, esc)
        self._state._resolved_signals = resolution.resolved
        self._telemetry.end_stage(items_processed=len(active))
        return result

    def _stage_compilation(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage('compilation')
        resolved = getattr(self._state, '_resolved_signals', [])
        self._graph.build_from_signals(resolved)
        self._audit.record(AuditEventType.COMPILATION_STARTED, tick_num)
        comp_result: CompilationResult = self._compiler.compile_batch(resolved, self._graph)
        result.artifacts_compiled = len(comp_result.compiled)
        self._state.tick.signals_compiled_this_tick = len(comp_result.compiled)
        if comp_result.errors:
            result.halted = True
            result.errors.extend(comp_result.errors)
            self._audit.record(
                AuditEventType.COMPILATION_ERROR,
                tick_num,
                {'errors': comp_result.errors},
            )
        else:
            self._audit.record(
                AuditEventType.COMPILATION_COMPLETED,
                tick_num,
                {'artifact_count': len(comp_result.compiled)},
            )
        for err in comp_result.errors:
            self._state.record_error('compilation', str(err))
        self._state._compiled_artifacts = comp_result.compiled
        self._telemetry.end_stage(
            items_processed=len(comp_result.compiled),
            errors=len(comp_result.errors),
        )
        return result

    def _stage_emission(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage('emission')
        artifacts = getattr(self._state, '_compiled_artifacts', [])
        emission: EmissionBatch = self._emitter.emit_batch(artifacts)
        result.artifacts_emitted = len(emission.emitted)
        self._state.tick.artifacts_emitted_this_tick = len(emission.emitted)
        for emitted in emission.emitted:
            self._state.emitted_artifacts.append({'emission_id': emitted.emission_id, 'artifact_id': emitted.artifact_id, 'version_tag': emitted.version_tag})
            self._audit.record(AuditEventType.ARTIFACT_EMITTED, tick_num, {'emission_id': emitted.emission_id})
        self._state._emitted_batch = emission.emitted
        self._telemetry.end_stage(items_processed=len(emission.emitted), errors=len(emission.errors))
        return result

    def _stage_publication(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._telemetry.begin_stage('publication')
        emitted = getattr(self._state, '_emitted_batch', [])
        delivered = self._subscription_api.publish(emitted)
        result.artifacts_published = delivered
        self._telemetry.end_stage(items_processed=delivered)
        return result

    def _finalize_tick(self, result: PipelineTickResult, tick_num: int) -> PipelineTickResult:
        self._audit.record(AuditEventType.TICK_COMPLETED, tick_num, {'signals_ingested': result.signals_ingested, 'artifacts_emitted': result.artifacts_emitted, 'halted': result.halted})
        self._telemetry.end_tick()
        for attr in ('_ingested_batch', '_resolved_signals', '_compiled_artifacts', '_emitted_batch'):
            if hasattr(self._state, attr):
                delattr(self._state, attr)
        return result