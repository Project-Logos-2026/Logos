"""
MODULE: pipeline_runner
PHASE: Phase-E (Execution Grounding)
PURPOSE:
- Execute a single activation plan under a tick budget
"""

from Logos_System.System_Stack.Logos_Protocol.Phase_E_Tick_Engine import (
    PhaseETickEngine,
    TickHalt,
)


class PipelineRunner:
    def run(self, fn, *, ticks: int = 1):
        engine = PhaseETickEngine(max_ticks=ticks)
        engine.start()
        try:
            engine.tick(fn)
        except TickHalt:
            pass
        return engine.audit_log


def run_scp_pipeline(*, smp=None, payload_ref=None):
    """Legacy-compatible stub that executes a single no-op under a tick budget."""

    def noop():
        return {"status": "OK", "smp": smp, "payload_ref": payload_ref}

    runner = PipelineRunner()
    audit = runner.run(noop, ticks=1)
    return {"audit": audit, "status": "OK"}
