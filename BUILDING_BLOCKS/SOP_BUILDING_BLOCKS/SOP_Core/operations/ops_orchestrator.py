"""Operations-side orchestration stub for SOP."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .audit_output import AuditOutputHook
from .ext_lib_importer import ExternalLibraryImporter
from .stasis_holding import StasisHoldingArea


class OpsOrchestrator:
    """Wires SOP core services without executing external actions."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.audit = AuditOutputHook(self.config.get("audit_path"))
        self.importer = ExternalLibraryImporter()
        self.stasis = StasisHoldingArea()

    def start(self) -> Dict[str, Any]:
        """Start the orchestration surface in a ready-but-idle state."""

        self.audit.emit("sop_orchestrator_start", {"status": "ready"})
        return {
            "status": "ready",
            "services": {
                "audit": "ready",
                "importer": "ready",
                "stasis": "ready",
            },
        }
