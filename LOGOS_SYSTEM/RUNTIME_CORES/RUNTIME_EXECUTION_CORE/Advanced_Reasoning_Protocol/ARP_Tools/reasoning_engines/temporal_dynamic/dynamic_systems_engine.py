from __future__ import annotations

from typing import Any, Callable, Dict


class DynamicSystemsEngine:
    def simulate(self, state: Dict[str, Any], step_fn: Callable[[Dict[str, Any]], Dict[str, Any]], steps: int = 3) -> Dict[str, Any]:
        current = dict(state)
        history = [current]
        for _ in range(max(0, steps)):
            current = step_fn(dict(current))
            history.append(current)
        return {"engine": "dynamic_systems", "history": history}
