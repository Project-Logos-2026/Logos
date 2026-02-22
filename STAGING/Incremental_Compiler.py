# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.1.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Incremental_Compiler
runtime_layer: compilation
role: Signal compiler
responsibility: Compiles resolved signals into artifacts. Phase 6 addition:
    accepts optional TopologyContext and tags compiled artifact content with
    topology_routing metadata when present. Backward compatible — callers
    not passing topology_context see identical behavior to pre-Phase-6.
agent_binding: None
protocol_binding: Multi_Process_Signal_Compiler
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [hashlib, time, dataclasses, typing, Topology_Context]
provides: [IncrementalCompiler, CompiledArtifact, CompilationResult]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Compilation errors captured per-artifact. Batch returns partial."
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

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Topology_Context import (
    TopologyContext,
)


@dataclass
class CompiledArtifact:
    artifact_id: str = ""
    source_signal_id: str = ""
    source_payload_hash: str = ""
    compiled_at: float = 0.0
    content: Dict[str, Any] = field(default_factory=dict)
    dependencies_resolved: List[str] = field(default_factory=list)
    version: int = 1


@dataclass
class CompilationResult:
    compiled: List[CompiledArtifact] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)


class IncrementalCompiler:

    def __init__(self, max_depth: int = 64) -> None:
        self._max_depth = max_depth
        self._cache: Dict[str, CompiledArtifact] = {}
        self._version_counter: Dict[str, int] = {}

    def compile_batch(
        self,
        envelopes: Any,
        graph: Any,
        topology_context: Optional[TopologyContext] = None,
    ) -> CompilationResult:
        result = CompilationResult()
        if envelopes is None:
            return result
        for envelope in envelopes:
            try:
                artifact = self._compile_single(envelope, graph)

                if topology_context is not None:
                    artifact.content["topology_routing"] = topology_context.config_id

                self._cache[envelope.payload_hash] = artifact
                result.compiled.append(artifact)
            except Exception as exc:
                result.errors.append({
                    "signal_id": getattr(envelope, "signal_id", ""),
                    "error": str(exc),
                })
        return result

    def _compile_single(self, envelope: Any, graph: Any) -> CompiledArtifact:
        version = self._version_counter.get(envelope.signal_id, 0) + 1
        self._version_counter[envelope.signal_id] = version
        dep_ids = list(getattr(graph, "_adjacency", {}).get(envelope.signal_id, set()))
        content: Dict[str, Any] = {
            "type": envelope.payload.get("type", "unknown"),
            "domain": envelope.payload.get("domain"),
            "target": envelope.payload.get("target"),
            "data": envelope.payload.get("data"),
            "source": str(getattr(envelope.source, "value", "")),
            "authority": str(getattr(envelope.authority, "value", "")),
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

    def invalidate(self, payload_hash: str) -> bool:
        return self._cache.pop(payload_hash, None) is not None

    def clear_cache(self) -> int:
        count = len(self._cache)
        self._cache.clear()
        self._version_counter.clear()
        return count

    def cache_size(self) -> int:
        return len(self._cache)
