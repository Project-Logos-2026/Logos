"""
MODULE: Phase_E_Tick_Engine
PHASE: Phase-E (Execution Grounding)
PURPOSE:
- Bounded tick execution
- Deterministic lifecycle
- Auditable state transitions
FAILURE MODE:
- Fail-closed on exception or budget exhaustion
"""

import time
from typing import Callable, Optional


class TickHalt(Exception):
    """Raised when the tick engine halts execution."""


class PhaseETickEngine:
    def __init__(self, max_ticks: int):
        if not isinstance(max_ticks, int) or max_ticks <= 0:
            raise ValueError("max_ticks must be a positive integer")

        self.max_ticks = max_ticks
        self.remaining = max_ticks
        self.active = False
        self.audit_log = []

    # -----------------------------
    # Lifecycle
    # -----------------------------
    def start(self):
        if self.active:
            raise RuntimeError("Tick engine already started")

        self.active = True
        self._audit("START", {"max_ticks": self.max_ticks})

    def tick(self, fn: Callable[[], None]):
        if not self.active:
            raise RuntimeError("Tick engine not active")

        if self.remaining <= 0:
            self.halt("TICK_BUDGET_EXHAUSTED")

        try:
            fn()
            self.remaining -= 1
            self._audit("TICK", {"remaining": self.remaining})
        except Exception as e:
            self._audit("ERROR", {"error": repr(e)})
            self.halt("EXCEPTION")

    def halt(self, reason: str):
        self._audit("HALT", {"reason": reason})
        self.active = False
        raise TickHalt(reason)

    # -----------------------------
    # Audit
    # -----------------------------
    def _audit(self, event: str, data: dict):
        self.audit_log.append({
            "timestamp": time.time(),
            "event": event,
            "data": data,
        })


def run_with_ticks(max_ticks: int, fn: Callable[[], None]):
    """
    Convenience wrapper for single-function execution under a tick budget.
    """
    engine = PhaseETickEngine(max_ticks)
    engine.start()
    try:
        while True:
            engine.tick(fn)
    except TickHalt:
        return engine.audit_log
