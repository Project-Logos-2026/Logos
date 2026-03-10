# File: MSPC_Telemetry.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Telemetry collector for the MSPC runtime. Aggregates per-tick
#   metrics, pipeline stage durations, error rates, and throughput
#   statistics. Telemetry is read-only and does not affect pipeline
#   behavior.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StageMetric:
    stage_name: str
    started_at: float = 0.0
    ended_at: float = 0.0
    items_processed: int = 0
    errors: int = 0

    @property
    def duration_seconds(self) -> float:
        if self.ended_at > self.started_at:
            return self.ended_at - self.started_at
        return 0.0


@dataclass
class TickTelemetry:
    tick_number: int
    started_at: float
    ended_at: float = 0.0
    stages: List[StageMetric] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        if self.ended_at > self.started_at:
            return self.ended_at - self.started_at
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tick_number": self.tick_number,
            "total_duration_seconds": self.total_duration,
            "stages": [
                {
                    "name": s.stage_name,
                    "duration_seconds": s.duration_seconds,
                    "items_processed": s.items_processed,
                    "errors": s.errors,
                }
                for s in self.stages
            ],
        }


class MSPCTelemetry:
    def __init__(self, enabled: bool = True) -> None:
        self._enabled = enabled
        self._tick_history: List[TickTelemetry] = []
        self._current_tick: Optional[TickTelemetry] = None
        self._current_stage: Optional[StageMetric] = None

    @property
    def enabled(self) -> bool:
        return self._enabled

    def begin_tick(self, tick_number: int) -> None:
        if not self._enabled:
            return
        self._current_tick = TickTelemetry(
            tick_number=tick_number,
            started_at=time.time(),
        )

    def begin_stage(self, stage_name: str) -> None:
        if not self._enabled or self._current_tick is None:
            return
        self._current_stage = StageMetric(
            stage_name=stage_name,
            started_at=time.time(),
        )

    def end_stage(self, items_processed: int = 0, errors: int = 0) -> None:
        if not self._enabled or self._current_stage is None:
            return
        self._current_stage.ended_at = time.time()
        self._current_stage.items_processed = items_processed
        self._current_stage.errors = errors
        if self._current_tick is not None:
            self._current_tick.stages.append(self._current_stage)
        self._current_stage = None

    def end_tick(self) -> Optional[TickTelemetry]:
        if not self._enabled or self._current_tick is None:
            return None
        self._current_tick.ended_at = time.time()
        completed = self._current_tick
        self._tick_history.append(completed)
        self._current_tick = None
        return completed

    def recent_ticks(self, limit: int = 10) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._tick_history[-limit:]]

    def aggregate(self) -> Dict[str, Any]:
        if not self._tick_history:
            return {"total_ticks": 0}

        total_duration = sum(t.total_duration for t in self._tick_history)
        total_items = sum(
            s.items_processed
            for t in self._tick_history
            for s in t.stages
        )
        total_errors = sum(
            s.errors
            for t in self._tick_history
            for s in t.stages
        )

        return {
            "total_ticks": len(self._tick_history),
            "total_duration_seconds": total_duration,
            "total_items_processed": total_items,
            "total_errors": total_errors,
            "avg_tick_duration": total_duration / len(self._tick_history),
        }
