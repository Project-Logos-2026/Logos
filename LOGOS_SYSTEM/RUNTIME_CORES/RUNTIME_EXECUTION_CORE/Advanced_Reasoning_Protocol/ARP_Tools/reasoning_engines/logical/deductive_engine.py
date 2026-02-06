from __future__ import annotations

from typing import Any, Dict, List


class DeductiveEngine:
    def analyze(self, premises: List[str], conclusion: str) -> Dict[str, Any]:
        premises = [str(p) for p in premises]
        conclusion = str(conclusion)
        valid = conclusion in premises or self._simple_entails(premises, conclusion)
        return {
            "engine": "deductive",
            "valid": valid,
            "premise_count": len(premises),
            "conclusion": conclusion,
        }

    def _simple_entails(self, premises: List[str], conclusion: str) -> bool:
        for premise in premises:
            if premise.lower() == conclusion.lower():
                return True
        return False
