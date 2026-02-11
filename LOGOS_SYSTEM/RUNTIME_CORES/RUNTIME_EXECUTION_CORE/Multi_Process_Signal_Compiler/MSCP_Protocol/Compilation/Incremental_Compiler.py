# File: Incremental_Compiler.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Incremental compiler for the MSPC pipeline. Processes resolved
#   signals in dependency order, produces compiled semantic artifacts,
#   and maintains a compilation cache to avoid redundant work across
#   ticks. Compilation is delta-based: only new or changed signals
#   are recompiled.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from Multi_Process_Signal_Compiler.Signals.Signal_Envelope import SignalEnvelope
from Multi_Process_Signal_Compiler.Compilation.Dependency_Graph import (
    CyclicDependencyError,
    DependencyGraph,
)


@dataclass(frozen=True)
class CompiledArtifact:
    artifact_id: str
    source_signal_id: str
    source_payload_hash: str
    compiled_at: float
    content: Dict[str, Any]
    dependencies_resolved: List[str]
    version: int


@dataclass
class CompilationResult:
    artifacts: List[CompiledArtifact] = field(default_factory=list)
    cache_hits: int = 0
    cache_misses: int = 0
    errors: List[Dict[str, Any]] = field(default_factory=list)
    halted: bool = False


class IncrementalCompiler:
    def __init__(self, max_depth: int = 64) -> None:
        self._cache: Dict[str, CompiledArtifact] = {}
        self._version_counter: Dict[str, int] = {}
        self._max_depth = max_depth

    def compile(
        self,
        signals: List[SignalEnvelope],
        graph: DependencyGraph,
    ) -> CompilationResult:
        result = CompilationResult()

        try:
            order = graph.topological_order()
        except CyclicDependencyError as exc:
            result.errors.append({
                "stage": "dependency_resolution",
                "error": str(exc),
                "timestamp": time.time(),
            })
            result.halted = True
            return result

        if len(order) > self._max_depth:
            result.errors.append({
                "stage": "depth_check",
                "error": f"Compilation depth {len(order)} exceeds max {self._max_depth}",
                "timestamp": time.time(),
            })
            result.halted = True
            return result

        signal_map = {s.signal_id: s for s in signals}

        for signal_id in order:
            envelope = signal_map.get(signal_id)
            if envelope is None:
                envelope = graph.get_envelope(signal_id)
            if envelope is None:
                continue

            cached = self._cache.get(envelope.payload_hash)
            if cached is not None:
                result.artifacts.append(cached)
                result.cache_hits += 1
                continue

            result.cache_misses += 1

            try:
                artifact = self._compile_single(envelope, graph)
            except Exception as exc:
                result.errors.append({
                    "stage": "compile_single",
                    "signal_id": signal_id,
                    "error": str(exc),
                    "timestamp": time.time(),
                })
                continue

            self._cache[envelope.payload_hash] = artifact
            result.artifacts.append(artifact)

        return result

    def invalidate(self, payload_hash: str) -> bool:
        return self._cache.pop(payload_hash, None) is not None

    def clear_cache(self) -> int:
        count = len(self._cache)
        self._cache.clear()
        self._version_counter.clear()
        return count

    def cache_size(self) -> int:
        return len(self._cache)

    def _compile_single(
        self,
        envelope: SignalEnvelope,
        graph: DependencyGraph,
    ) -> CompiledArtifact:
        version = self._version_counter.get(envelope.signal_id, 0) + 1
        self._version_counter[envelope.signal_id] = version

        dep_ids = list(graph._adjacency.get(envelope.signal_id, set()))

        content = {
            "type": envelope.payload.get("type", "unknown"),
            "domain": envelope.payload.get("domain"),
            "target": envelope.payload.get("target"),
            "data": envelope.payload.get("data"),
            "source": envelope.source.value,
            "authority": envelope.authority.value,
            "confidence": envelope.confidence,
        }

        artifact_seed = f"{envelope.signal_id}:{envelope.payload_hash}:{version}"
        artifact_id = hashlib.sha256(artifact_seed.encode()).hexdigest()[:16]

        return CompiledArtifact(
            artifact_id=f"mspc-{artifact_id}",
            source_signal_id=envelope.signal_id,
            source_payload_hash=envelope.payload_hash,
            compiled_at=time.time(),
            content=content,
            dependencies_resolved=dep_ids,
            version=version,
        )
