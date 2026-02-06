from __future__ import annotations

from typing import Any, Dict


class GameTheoreticEngine:
    def select_strategy(self, payoffs: Dict[str, float]) -> Dict[str, Any]:
        if not payoffs:
            return {"engine": "game_theoretic", "strategy": None}
        strategy = max(payoffs.items(), key=lambda item: item[1])[0]
        return {"engine": "game_theoretic", "strategy": strategy, "payoff": payoffs[strategy]}
