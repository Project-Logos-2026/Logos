from __future__ import annotations

from typing import Any, Dict


class MetaStrategyEngine:
    def choose(self, options: Dict[str, float]) -> Dict[str, Any]:
        if not options:
            return {"engine": "meta_strategy", "choice": None}
        choice = max(options.items(), key=lambda item: item[1])[0]
        return {"engine": "meta_strategy", "choice": choice, "score": options[choice]}
