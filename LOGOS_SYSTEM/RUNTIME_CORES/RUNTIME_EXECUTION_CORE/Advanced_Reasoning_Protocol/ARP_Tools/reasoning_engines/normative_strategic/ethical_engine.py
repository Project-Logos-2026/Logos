from __future__ import annotations

from typing import Any, Dict, List


class EthicalEngine:
    def evaluate(self, action: str, prohibited: List[str]) -> Dict[str, Any]:
        action = action.lower().strip()
        blocked = any(p.lower().strip() in action for p in prohibited)
        return {
            "engine": "ethical",
            "action": action,
            "allowed": not blocked,
        }
