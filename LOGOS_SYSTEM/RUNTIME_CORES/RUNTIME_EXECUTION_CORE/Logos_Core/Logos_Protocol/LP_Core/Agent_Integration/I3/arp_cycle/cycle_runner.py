# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: cycle_runner
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Core/Agent_Integration/I3/arp_cycle/cycle_runner.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Core/Agent_Integration/I3/arp_cycle/cycle_runner.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
MODULE: cycle_runner
PHASE: Phase-E (Execution Grounding)
PURPOSE:
- Execute a single ARP cycle under a tick budget
"""

from Logos_System.System_Stack.Logos_Protocol.Phase_E_Tick_Engine import (
    PhaseETickEngine,
    TickHalt,
)


class CycleRunner:
    def run(self, fn, *, ticks: int = 1):
        engine = PhaseETickEngine(max_ticks=ticks)
        engine.start()
        try:
            engine.tick(fn)
        except TickHalt:
            pass
        return engine.audit_log


def run_arp_cycle(*, task=None, payload_ref=None):
    """Legacy-compatible stub that executes a single no-op under a tick budget."""

    def noop():
        return {"status": "OK", "task": task, "payload_ref": payload_ref}

    runner = CycleRunner()
    audit = runner.run(noop, ticks=1)
    return {"audit": audit, "status": "OK"}
