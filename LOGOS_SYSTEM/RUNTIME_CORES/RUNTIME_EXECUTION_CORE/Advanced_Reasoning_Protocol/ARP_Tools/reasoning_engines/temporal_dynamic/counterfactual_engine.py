from __future__ import annotations

from typing import Any, Dict


class CounterfactualEngine:
    def evaluate(self, base: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(base)
        result.update(changes)
        return {"engine": "counterfactual", "result": result}
