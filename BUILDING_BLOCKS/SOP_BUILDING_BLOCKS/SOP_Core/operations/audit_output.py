"""System audit output hook stub."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class AuditOutputHook:
    """Append-only audit emitter for SYSTEM_AUDIT_LOGS."""

    def __init__(self, audit_path: Optional[str] = None) -> None:
        self.audit_path = Path(audit_path) if audit_path else self._default_path()
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: str, payload: Dict[str, Any]) -> None:
        record = {"event": event, "payload": payload}
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")

    @staticmethod
    def _default_path() -> Path:
        repo_root = Path(__file__).resolve().parents[4]
        return repo_root / "SYSTEM_AUDIT_LOGS" / "Boot_Sequence_Log"
