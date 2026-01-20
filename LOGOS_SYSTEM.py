"""
===============================================================================
FILE: LOGOS_SYSTEM.py
PATH: Logos_System/LOGOS_SYSTEM.py
PROJECT: LOGOS System
PHASE: Phase-F (Prelude)
STEP: Runtime Spine Initialization
STATUS: GOVERNED - NON-BYPASSABLE

CLASSIFICATION:
- Canonical Runtime Spine
- Post-Entry, Pre-Agent Execution Layer

GOVERNANCE:
- System_Entry_Point_Execution_Contract.md
- Runtime_Module_Header_Contract.md

ROLE:
Acts as the sole governed runtime spine downstream of System_Entry_Point.
Initializes lock-and-key orchestration and proof gate routing but performs
no agent activation and no epistemic scoping.

ORDERING GUARANTEE:
Executes only after System_Entry_Point.START_LOGOS authorization.
Executes before any agent startup, LEM discharge, or Phase-F enforcement.

PROHIBITIONS:
- No agent creation
- No projection loading
- No epistemic mutation
- No execution on import

FAILURE SEMANTICS:
Any invariant failure halts progression immediately (fail-closed).
===============================================================================
"""

from Logos_System.System_Entry_Point.System_Entry_Point import START_LOGOS, StartupHalt
from Logos_System.Runtime_Spine.Lock_And_Key.lock_and_key import execute_lock_and_key, LockAndKeyFailure


class RuntimeHalt(Exception):
    """Raised when the runtime spine fails an invariant."""
    pass


def RUN_LOGOS_SYSTEM(
    config_path: str | None = None,
    mode: str = "headless",
    diagnostic: bool = False,
):
    """Canonical runtime spine entry receiving handoff from START_LOGOS."""

    try:
        handoff = START_LOGOS(
            config_path=config_path,
            mode=mode,
            diagnostic=diagnostic,
        )
    except StartupHalt as exc:
        raise RuntimeHalt(f"Startup halted: {exc}")

    try:
        # Canonical first executable stage after System Entry Point
        lock_and_key_result = execute_lock_and_key(
            external_compile_artifact=b"STUB_COMPILE_ARTIFACT",
            internal_compile_artifact=b"STUB_COMPILE_ARTIFACT",
        )
    except LockAndKeyFailure as exc:
        raise RuntimeHalt(f"Lock-and-Key failed: {exc}")

    # Stub: downstream lock-and-key / proof gate logic is invoked after handoff.
    runtime_context = {
        "handoff": handoff,
        "lock_and_key": lock_and_key_result,
        "status": "RUNTIME_SPINE_READY",
    }

    return runtime_context
