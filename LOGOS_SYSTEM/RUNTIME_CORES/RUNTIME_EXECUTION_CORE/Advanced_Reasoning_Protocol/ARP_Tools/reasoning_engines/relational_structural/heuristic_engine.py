from __future__ import annotations

from typing import Any, Dict


class HeuristicEngine:
    def score(self, signals: Dict[str, float]) -> Dict[str, Any]:
        total = sum(float(v) for v in signals.values()) if signals else 0.0
        return {"engine": "heuristic", "score": round(total, 4)}
