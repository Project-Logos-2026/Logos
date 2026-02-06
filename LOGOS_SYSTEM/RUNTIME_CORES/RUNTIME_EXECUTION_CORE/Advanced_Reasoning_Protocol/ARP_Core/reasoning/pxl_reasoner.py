from __future__ import annotations

from typing import Any, Dict, List


class PXLReasoner:
    def __init__(self) -> None:
        self.thresholds = {
            "high": 0.8,
            "medium": 0.5,
        }

    def analyze(self, packet: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        claims = packet.get("claims") or []
        if not isinstance(claims, list):
            claims = [claims]

        relations = self._map_relations(claims)
        score = self._score_relations(relations)
        return {
            "engine": "pxl",
            "relations": relations,
            "coherence_score": score,
            "claim_count": len(claims),
        }

    def _map_relations(self, claims: List[Any]) -> List[Dict[str, Any]]:
        relations = []
        for i, left in enumerate(claims):
            for right in claims[i + 1 :]:
                ltxt = str(left)
                rtxt = str(right)
                overlap = self._token_overlap(ltxt, rtxt)
                if overlap > 0:
                    relations.append(
                        {
                            "source": ltxt,
                            "target": rtxt,
                            "overlap": overlap,
                        }
                    )
        return relations

    def _token_overlap(self, left: str, right: str) -> float:
        lset = set(left.lower().split())
        rset = set(right.lower().split())
        if not lset or not rset:
            return 0.0
        return len(lset.intersection(rset)) / max(len(lset), len(rset))

    def _score_relations(self, relations: List[Dict[str, Any]]) -> float:
        if not relations:
            return 0.0
        avg = sum(r["overlap"] for r in relations) / len(relations)
        return round(avg, 4)
