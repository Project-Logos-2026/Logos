# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Phase_E_Tick_Engine
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Tools/Recursion_Grounding/Phase_E_Tick_Engine.py.
agent_binding: None
protocol_binding: Logos_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Tools/Recursion_Grounding/Phase_E_Tick_Engine.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

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
        self.policy_context = None
        self.plan_context = None

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
            self._audit("TICK", {
                "remaining": self.remaining,
                "policy": self.policy_context,
                "plan": self.plan_context,
            })
        except Exception as e:
            self._audit("ERROR", {"error": repr(e)})
            self.halt("EXCEPTION")

    def halt(self, reason: str):
        self._audit("HALT", {"reason": reason})
        self.active = False
        raise TickHalt(reason)

    def run_multi_tick(self, max_ticks: int, fn: Callable[[], None]):
        """
        Phase-J (controlled): Run multiple ticks under an explicit tick budget.

        Preconditions:
        - max_ticks > 0
        - Caller has already passed governance authorization
        - No planning, no reentry, no autonomy

        This method is opt-in and introduces no behavior change unless invoked.
        """
        from LOGOS_SYSTEM.Governance.exceptions import GovernanceDenied

        if not isinstance(max_ticks, int) or max_ticks <= 0:
            raise GovernanceDenied("Invalid multi-tick budget")

        # Reset budget for this controlled run.
        self.max_ticks = max_ticks
        self.remaining = max_ticks

        if not self.active:
            self.start()

        try:
            while True:
                self.tick(fn)
        except TickHalt:
            return self.audit_log

    # -----------------------------
    # Governance (Audit-Only)
    # -----------------------------
    def attach_policy_context(self, policy: dict):
        """
        Attach policy provenance for audit purposes only.

        This does not authorize execution or alter tick behavior.
        Caller must already have passed governance checks.
        """

        self.policy_context = policy
        self._audit("POLICY_ATTACHED", {"policy": policy})

    def attach_plan_context(self, plan: dict):
        """
        Attach planning provenance for audit purposes only.

        This does not authorize execution or alter tick behavior.
        Caller must already have passed governance checks.
        """

        self.plan_context = plan
        self._audit("PLAN_ATTACHED", {"plan": plan})

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
