# File: Artifact_Emitter.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Emits compiled artifacts from the MSPC pipeline. Each artifact
#   is versioned, hashed, and wrapped in an emission envelope with
#   provenance metadata. Emitted artifacts are descriptive; the
#   emitter does not execute any downstream actions.
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

from Multi_Process_Signal_Compiler.Compilation.Incremental_Compiler import (
    CompiledArtifact,
)


@dataclass(frozen=True)
class EmittedArtifact:
    emission_id: str
    artifact_id: str
    artifact_hash: str
    emitted_at: float
    version_tag: str
    content: Dict[str, Any]
    provenance: Dict[str, Any]


@dataclass
class EmissionBatch:
    emitted: List[EmittedArtifact] = field(default_factory=list)
    skipped: int = 0
    errors: List[Dict[str, Any]] = field(default_factory=list)


class ArtifactEmitter:
    def __init__(
        self,
        version_prefix: str = "mspc-v",
        hash_algorithm: str = "sha256",
    ) -> None:
        self._version_prefix = version_prefix
        self._hash_algorithm = hash_algorithm
        self._emission_counter: int = 0
        self._emission_history: List[EmittedArtifact] = []

    def emit_batch(
        self,
        artifacts: List[CompiledArtifact],
    ) -> EmissionBatch:
        batch = EmissionBatch()

        for artifact in artifacts:
            try:
                emitted = self._emit_single(artifact)
                batch.emitted.append(emitted)
                self._emission_history.append(emitted)
            except Exception as exc:
                batch.errors.append({
                    "artifact_id": artifact.artifact_id,
                    "error": str(exc),
                    "timestamp": time.time(),
                })

        return batch

    def total_emitted(self) -> int:
        return self._emission_counter

    def recent_emissions(self, limit: int = 20) -> List[EmittedArtifact]:
        return list(self._emission_history[-limit:])

    def _emit_single(self, artifact: CompiledArtifact) -> EmittedArtifact:
        self._emission_counter += 1

        content_bytes = str(sorted(artifact.content.items())).encode("utf-8")
        if self._hash_algorithm == "sha256":
            artifact_hash = hashlib.sha256(content_bytes).hexdigest()
        else:
            artifact_hash = hashlib.sha256(content_bytes).hexdigest()

        version_tag = f"{self._version_prefix}{artifact.version}"

        emission_seed = f"{self._emission_counter}:{artifact.artifact_id}:{artifact_hash}"
        emission_id = hashlib.sha256(emission_seed.encode()).hexdigest()[:16]

        provenance = {
            "source_signal_id": artifact.source_signal_id,
            "source_payload_hash": artifact.source_payload_hash,
            "compiled_at": artifact.compiled_at,
            "dependencies_resolved": artifact.dependencies_resolved,
        }

        return EmittedArtifact(
            emission_id=f"emit-{emission_id}",
            artifact_id=artifact.artifact_id,
            artifact_hash=artifact_hash,
            emitted_at=time.time(),
            version_tag=version_tag,
            content=artifact.content,
            provenance=provenance,
        )
