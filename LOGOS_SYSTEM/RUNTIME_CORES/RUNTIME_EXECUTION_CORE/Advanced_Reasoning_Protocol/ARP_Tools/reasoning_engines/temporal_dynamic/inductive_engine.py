from __future__ import annotations

from typing import Any, Dict, List


class InductiveEngine:
    def generalize(self, samples: List[str]) -> Dict[str, Any]:
        prefix = None
        for s in samples:
            s = str(s)
            prefix = s if prefix is None else self._common_prefix(prefix, s)
        return {"engine": "inductive", "generalization": prefix or ""}

    def _common_prefix(self, left: str, right: str) -> str:
        i = 0
        for a, b in zip(left, right):
            if a != b:
                break
            i += 1
        return left[:i]
