# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: LOGOS_SYSTEM
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
===============================================================================
FILE: LOGOS_SYSTEM.py
PATH: Logos_System/LOGOS_SYSTEM.py
PROJECT: LOGOS System
PHASE: Phase-F
STEP: Runtime Spine Wiring → LOGOS Agent Startup → LEM Discharge
STATUS: GOVERNED — NON-BYPASSABLE

ROLE:
- Receives the governed handoff from System Entry Point
- Executes Lock-and-Key to derive the universal session id
- Starts the LOGOS agent session envelope
- Discharges LEM to derive the LOGOS agent identity

ORDERING GUARANTEE:
Executes strictly after System_Entry_Point.START_LOGOS and immediately before
any LOGOS agent execution or protocol activation.

FAILURE SEMANTICS:
Any invariant failure raises RuntimeHalt and halts progression (fail-closed).
No degraded modes or retries.
===============================================================================
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Literal, Optional

from LOGOS_SYSTEM.System_Entry_Point.System_Entry_Point import (
    START_LOGOS,
    StartupHalt,
)
from LOGOS_SYSTEM.System_Entry_Point.Agent_Orchestration.agent_orchestration import (
    OrchestrationHalt,
    prepare_agent_orchestration,
)
from LOGOS_SYSTEM.Runtime_Spine.Lock_And_Key.lock_and_key import (
    execute_lock_and_key,
    LockAndKeyFailure,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Core.Start_Logos_Agent import (
    LogosAgentStartupHalt,
    start_logos_agent,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Core.Lem_Discharge import (
    LemDischargeHalt,
    discharge_lem,
)


class RuntimeHalt(Exception):
    """Raised when the runtime spine fails an invariant."""


def _launch_gui() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    candidates = [Path.cwd(), Path(__file__).resolve().parent]
    explicit_paths = [
        repo_root / "LOGOS_GUI",
        repo_root / "LOGOS_SYSTEM" / "INTERFACES" / "LOGOS_GUI" / "LOGOS_GUI",
    ]
    gui_dir: Optional[Path] = None
    for base in candidates:
        for parent in [base, *base.parents]:
            candidate = parent / "LOGOS_GUI"
            if candidate.is_dir():
                gui_dir = candidate
                break
        if gui_dir is not None:
            break

    if gui_dir is None:
        for candidate in explicit_paths:
            if candidate.is_dir():
                gui_dir = candidate
                break

    if gui_dir is None:
        raise RuntimeHalt("LOGOS_GUI directory not found for GUI launch")

    env = dict(os.environ)
    env.setdefault("CI", "1")
    env.setdefault("NG_CLI_ANALYTICS", "ci")

    subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=str(gui_dir),
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env,
    )


def RUN_LOGOS_SYSTEM(
    config_path: Optional[str] = None,
    mode: Literal["headless", "interactive"] = "headless",
    diagnostic: bool = False,
) -> Dict[str, Any]:
    """Canonical runtime spine entry receiving handoff from START_LOGOS."""

    # M3: Import logger and Channel at top of function
    from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol.SOP_Tools.Operational_Log.Operational_Logger import (
        Operational_Logger,
        Channel,
    )

    # M3: Create provisional logger before any try blocks
    operational_logger = Operational_Logger(
        log_dir="_Reports/Operational_Logs",
        session_id="BOOTSTRAP",
    )

    try:
        handoff = START_LOGOS(
            config_path=config_path,
            mode=mode,
            diagnostic=diagnostic,
        )
    except StartupHalt as exc:
        operational_logger.halt(
            Channel.STARTUP,
            f"Startup halted: {exc}",
            error_type="StartupHalt",
            error_detail=str(exc),
        )
        raise RuntimeHalt(f"Startup halted: {exc}")
    operational_logger.status(Channel.STARTUP, "system_bootstrap_start")

    try:
        lock_and_key_result = execute_lock_and_key(
            external_compile_artifact=b"STUB_COMPILE_ARTIFACT",
            internal_compile_artifact=b"STUB_COMPILE_ARTIFACT",
        )
    except LockAndKeyFailure as exc:
        operational_logger.halt(
            Channel.STARTUP,
            f"Lock-and-Key failed: {exc}",
            error_type="LockAndKeyFailure",
            error_detail=str(exc),
        )
        raise RuntimeHalt(f"Lock-and-Key failed: {exc}")

    operational_logger.status(Channel.STARTUP, "lock_and_key_complete")

    verified_context = dict(handoff)
    verified_context["session_id"] = lock_and_key_result.get("session_id")
    verified_context["lock_and_key_status"] = lock_and_key_result.get("status")

    from typing import cast

    # Close provisional logger before session logger instantiation
    operational_logger.close()

    # Type-safe session_id binding after invariant check
    session_id = cast(str, verified_context["session_id"])
    operational_logger = Operational_Logger(
        log_dir="_Reports/Operational_Logs",
        session_id=session_id,
    )

    if not isinstance(verified_context["session_id"], str):
        operational_logger.halt(
            Channel.STARTUP,
            "Derived session_id is missing or invalid",
            error_type="MissingSessionId",
            error_detail="session_id missing or invalid",
        )
        raise RuntimeHalt("Derived session_id is missing or invalid")

    operational_logger.status(Channel.STARTUP, "governance_contracts_loaded")
    operational_logger.status(Channel.STARTUP, "operational_logger_initialized")

    try:
        logos_session = start_logos_agent(verified_context)
    except LogosAgentStartupHalt as exc:
        operational_logger.halt(
            Channel.STARTUP,
            f"LOGOS agent startup failed: {exc}",
            error_type="LogosAgentStartupHalt",
            error_detail=str(exc),
        )
        raise RuntimeHalt(f"LOGOS agent startup failed: {exc}")
    operational_logger.status(Channel.STARTUP, "logos_agent_started")

    try:
        logos_identity = discharge_lem(logos_session)
    except LemDischargeHalt as exc:
        operational_logger.halt(
            Channel.STARTUP,
            f"LEM discharge failed: {exc}",
            error_type="LemDischargeHalt",
            error_detail=str(exc),
        )
        raise RuntimeHalt(f"LEM discharge failed: {exc}")
    operational_logger.status(Channel.STARTUP, "lem_discharge_complete")

    constructive_compile_output = {
        "logos_agent_id": logos_identity.get("logos_agent_id"),
        "universal_session_id": logos_identity.get("session_id"),
        "prepared_bindings": {
            "issued_agents": logos_identity.get("issued_agents", {}),
            "issued_protocols": logos_identity.get("issued_protocols", {}),
            "authority": logos_identity.get("authority", {}),
        },
    }

    if not constructive_compile_output["logos_agent_id"] or not constructive_compile_output["universal_session_id"]:
        operational_logger.halt(
            Channel.STARTUP,
            "Missing identity context for orchestration",
            error_type="MissingIdentityContext",
            error_detail="identity context absent",
        )
        raise RuntimeHalt("Missing identity context for orchestration")

    try:
        orchestration_plan = prepare_agent_orchestration(constructive_compile_output)
    except OrchestrationHalt as exc:
        operational_logger.halt(
            Channel.STARTUP,
            f"Agent orchestration failed: {exc}",
            error_type="OrchestrationHalt",
            error_detail=str(exc),
        )
        raise RuntimeHalt(f"Agent orchestration failed: {exc}")

    if mode == "interactive":
        _launch_gui()



    result = {
        "status": "LOGOS_AGENT_READY",
        "logos_identity": logos_identity,
        "logos_session": logos_session,
        "constructive_compile_output": constructive_compile_output,
        "agent_orchestration_plan": orchestration_plan,
    }
    operational_logger.status(Channel.STARTUP, "agent_orchestration_complete")
    operational_logger.close()
    return result
