from __future__ import annotations

from typing import Callable, Dict


class OptimizationEngine:
    def optimize(self, objective: Callable[[float], float], initial_guess: float) -> Dict[str, float]:
        x = float(initial_guess)
        best = objective(x)
        for step in range(10):
            candidate = x + 0.1
            score = objective(candidate)
            if score < best:
                x, best = candidate, score
        return {"best_x": x, "best_score": float(best)}
