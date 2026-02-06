from __future__ import annotations

from typing import Any, Dict, List


class AbductiveEngine:
    def analyze(self, observations: List[str], rules: List[str]) -> Dict[str, Any]:
        observations = [str(o) for o in observations]
        rules = [str(r) for r in rules]
        hypotheses = []
        for rule in rules:
            for obs in observations:
                if obs.lower() in rule.lower():
                    hypotheses.append(rule)
        return {
            "engine": "abductive",
            "hypotheses": hypotheses[:5],
            "observation_count": len(observations),
        }
