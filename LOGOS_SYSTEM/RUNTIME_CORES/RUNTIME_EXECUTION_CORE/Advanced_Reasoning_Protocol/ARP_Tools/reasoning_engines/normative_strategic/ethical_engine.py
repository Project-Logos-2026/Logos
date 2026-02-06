from __future__ import annotations

from typing import Any, Dict, List, Optional


def _load_moral_validator() -> Optional[Any]:
    try:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.MVS_System.MVS_Core.mathematics.privation_mathematics import (
            MoralSetValidator,
        )

        return MoralSetValidator()
    except Exception:
        return None


class EthicalEngine:
    def __init__(self) -> None:
        self.moral_validator = _load_moral_validator()

    def evaluate(self, action: str, prohibited: List[str], entity: Optional[Any] = None) -> Dict[str, Any]:
        action = action.lower().strip()
        blocked = any(p.lower().strip() in action for p in prohibited)
        moral_validation = None
        if self.moral_validator:
            try:
                moral_validation = self.moral_validator.validate_moral_operation(entity or action, "evaluate")
            except Exception:
                moral_validation = {"status": "error", "reason": "moral_validation_failed"}
        return {
            "engine": "ethical",
            "action": action,
            "allowed": not blocked,
            "moral_validation": moral_validation,
        }
