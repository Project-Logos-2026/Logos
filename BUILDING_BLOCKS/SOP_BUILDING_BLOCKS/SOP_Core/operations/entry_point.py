"""SOP core entry point stub (non-executing, fail-closed)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .ops_orchestrator import OpsOrchestrator
from .pxl_gate_receiver import PXLGateReceiver


class SOPStartupError(RuntimeError):
    """Raised when SOP startup invariants fail."""


def start_sop_core(
    *,
    config: Optional[Dict[str, Any]] = None,
    pxl_gate_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Start SOP core in a fail-closed, non-executing mode."""

    receiver = PXLGateReceiver()
    gate_result = receiver.accept(pxl_gate_payload or {})
    if not gate_result.get("ok", False):
        raise SOPStartupError(gate_result.get("reason", "PXL Gate denied"))

    orchestrator = OpsOrchestrator(config=config or {})
    status = orchestrator.start()
    return {
        "status": "SOP_CORE_READY",
        "pxl_gate": gate_result,
        "orchestrator": status,
    }
