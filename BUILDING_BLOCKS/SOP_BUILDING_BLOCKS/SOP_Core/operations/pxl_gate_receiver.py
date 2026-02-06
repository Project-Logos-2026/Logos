"""PXL Gate receiver stub for SOP boot."""

from __future__ import annotations

from typing import Any, Dict


class PXLGateReceiver:
    """Accepts PXL gate payloads and enforces fail-closed defaults."""

    def accept(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        status = str(payload.get("status", "")).upper()
        kernel_hash = payload.get("kernel_hash")
        if status != "PASS":
            return {"ok": False, "reason": "pxl_gate_not_passed", "status": status}
        if not kernel_hash:
            return {"ok": False, "reason": "missing_kernel_hash", "status": status}
        return {"ok": True, "status": status, "kernel_hash": kernel_hash}
