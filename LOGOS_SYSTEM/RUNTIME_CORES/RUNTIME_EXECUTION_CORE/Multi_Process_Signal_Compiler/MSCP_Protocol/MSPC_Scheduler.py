from __future__ import annotations
import time
from typing import Any, Callable, Dict, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSPC_Config import ExecutionMode, MSPCConfig
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSPC_State import MSPCState, RuntimePhase
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSPC_Pipeline import MSPCPipeline, PipelineTickResult

class SchedulerHalt(Exception):
    pass

class MSPCScheduler:

    def __init__(self, config: MSPCConfig, state: MSPCState, pipeline: MSPCPipeline) -> None:
        self._config = config
        self._state = state
        self._pipeline = pipeline
        self._halt_requested: bool = False
        self._total_ticks: int = 0
        self._last_result: Optional[PipelineTickResult] = None

    def request_halt(self) -> None:
        self._halt_requested = True

    def is_halted(self) -> bool:
        return self._halt_requested or self._state.phase in (RuntimePhase.HALTED, RuntimePhase.ERROR)

    def tick_once(self) -> PipelineTickResult:
        if self.is_halted():
            raise SchedulerHalt('Scheduler is halted')
        if self._state.phase != RuntimePhase.RUNNING:
            raise SchedulerHalt(f'Cannot tick in phase {self._state.phase.value}')
        self._state.reset_tick()
        result = self._pipeline.execute_tick()
        self._total_ticks += 1
        self._last_result = result
        if result.halted:
            self._state.transition(RuntimePhase.ERROR)
        return result

    def run_continuous(self, max_ticks: Optional[int]=None) -> int:
        ticks_executed = 0
        while not self.is_halted():
            if max_ticks is not None and ticks_executed >= max_ticks:
                break
            self._apply_backpressure()
            result = self.tick_once()
            ticks_executed += 1
            if result.halted:
                break
            if self._config.execution_mode == ExecutionMode.CONTINUOUS:
                self._sleep_interval()
        return ticks_executed

    def run_on_demand(self) -> PipelineTickResult:
        return self.tick_once()

    def stats(self) -> Dict[str, Any]:
        return {'total_ticks': self._total_ticks, 'halt_requested': self._halt_requested, 'current_phase': self._state.phase.value, 'execution_mode': self._config.execution_mode.value, 'last_tick_halted': self._last_result.halted if self._last_result else None}

    def _sleep_interval(self) -> None:
        interval = self._config.tick_interval_seconds
        if interval > 0:
            time.sleep(interval)

    def _apply_backpressure(self) -> None:
        pending = len(self._state.active_signals)
        max_pending = self._config.max_pending_signals
        if max_pending > 0:
            ratio = pending / max_pending
            if ratio >= self._config.backpressure_threshold:
                extra_wait = (ratio - self._config.backpressure_threshold) * 2.0
                time.sleep(min(extra_wait, 5.0))