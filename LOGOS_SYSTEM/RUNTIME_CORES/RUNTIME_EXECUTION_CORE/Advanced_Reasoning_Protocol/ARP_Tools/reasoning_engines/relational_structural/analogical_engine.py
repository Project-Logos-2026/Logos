from __future__ import annotations

from typing import Any, Dict


class AnalogicalEngine:
    def compare(self, left: str, right: str) -> Dict[str, Any]:
        lset = set(left.lower().split())
        rset = set(right.lower().split())
        score = len(lset.intersection(rset)) / max(1, len(lset.union(rset)))
        return {"engine": "analogical", "score": round(score, 4)}
