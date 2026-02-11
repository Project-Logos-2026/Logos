# File: MSPC_State.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Internal state container for the MSPC protocol. Holds active signals,
#   the dependency graph, compilation cache, emitted artifact history,
#   and tick metadata. State is session-scoped and does not persist
#   across sessions.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class RuntimePhase(Enum):
    UNINITIALIZED = "uninitialized"
    BOOTING = "booting"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    HALTED = "halted"
    ERROR = "error"


@dataclass
class TickMetadata:
    tick_number: int = 0
    last_tick_timestamp: float = 0.0
    signals_ingested_this_tick: int = 0
    signals_compiled_this_tick: int = 0
    artifacts_emitted_this_tick: int = 0
    conflicts_resolved_this_tick: int = 0


@dataclass
class MSPCState:
    phase: RuntimePhase = RuntimePhase.UNINITIALIZED
    session_id: Optional[str] = None
    boot_timestamp: float = 0.0
    tick: TickMetadata = field(default_factory=TickMetadata)
    active_signals: Dict[str, Any] = field(default_factory=dict)
    blocked_signals: Dict[str, Any] = field(default_factory=dict)
    dependency_graph: Dict[str, Set[str]] = field(default_factory=dict)
    compilation_cache: Dict[str, Any] = field(default_factory=dict)
    emitted_artifacts: List[Dict[str, Any]] = field(default_factory=list)
    escalation_queue: List[Dict[str, Any]] = field(default_factory=list)
    error_log: List[Dict[str, Any]] = field(default_factory=list)

    def initialize(self, session_id: str) -> None:
        if self.phase != RuntimePhase.UNINITIALIZED:
            raise RuntimeError(
                f"Cannot initialize from phase {self.phase.value}"
            )
        self.session_id = session_id
        self.boot_timestamp = time.time()
        self.phase = RuntimePhase.BOOTING

    def transition(self, target: RuntimePhase) -> None:
        allowed = _TRANSITIONS.get(self.phase)
        if allowed is None or target not in allowed:
            raise RuntimeError(
                f"Illegal state transition: {self.phase.value} -> {target.value}"
            )
        self.phase = target

    def reset_tick(self) -> None:
        self.tick.tick_number += 1
        self.tick.last_tick_timestamp = time.time()
        self.tick.signals_ingested_this_tick = 0
        self.tick.signals_compiled_this_tick = 0
        self.tick.artifacts_emitted_this_tick = 0
        self.tick.conflicts_resolved_this_tick = 0

    def record_error(self, source: str, message: str) -> None:
        self.error_log.append({
            "source": source,
            "message": message,
            "tick": self.tick.tick_number,
            "timestamp": time.time(),
        })

    def snapshot(self) -> Dict[str, Any]:
        return {
            "phase": self.phase.value,
            "session_id": self.session_id,
            "boot_timestamp": self.boot_timestamp,
            "tick_number": self.tick.tick_number,
            "active_signal_count": len(self.active_signals),
            "blocked_signal_count": len(self.blocked_signals),
            "cached_compilations": len(self.compilation_cache),
            "total_emitted_artifacts": len(self.emitted_artifacts),
            "pending_escalations": len(self.escalation_queue),
            "error_count": len(self.error_log),
        }


_TRANSITIONS: Dict[RuntimePhase, Set[RuntimePhase]] = {
    RuntimePhase.UNINITIALIZED: {RuntimePhase.BOOTING},
    RuntimePhase.BOOTING: {RuntimePhase.READY, RuntimePhase.ERROR},
    RuntimePhase.READY: {RuntimePhase.RUNNING, RuntimePhase.HALTED},
    RuntimePhase.RUNNING: {RuntimePhase.PAUSED, RuntimePhase.HALTED, RuntimePhase.ERROR},
    RuntimePhase.PAUSED: {RuntimePhase.RUNNING, RuntimePhase.HALTED},
    RuntimePhase.HALTED: set(),
    RuntimePhase.ERROR: {RuntimePhase.HALTED},
}
