from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


class SemanticRelationMappingEngine:
    def map_relations(
        self,
        items: List[str],
        trinity_vectors: Optional[Dict[str, Tuple[float, float, float]]] = None,
    ) -> Dict[str, Any]:
        relations = []
        for i, left in enumerate(items):
            for right in items[i + 1 :]:
                if left == right:
                    continue
                coherence = self._coherence(left, right, trinity_vectors)
                relations.append(
                    {
                        "source": left,
                        "target": right,
                        "relation": "related",
                        "coherence": coherence,
                    }
                )
        return {"engine": "semantic_relation_mapping", "relations": relations}

    def _coherence(
        self,
        left: str,
        right: str,
        trinity_vectors: Optional[Dict[str, Tuple[float, float, float]]],
    ) -> float:
        if not trinity_vectors:
            return 0.0
        left_vec = trinity_vectors.get(left)
        right_vec = trinity_vectors.get(right)
        if not left_vec or not right_vec:
            return 0.0
        dot = sum(l * r for l, r in zip(left_vec, right_vec))
        norm_left = sum(l * l for l in left_vec) ** 0.5
        norm_right = sum(r * r for r in right_vec) ** 0.5
        if not norm_left or not norm_right:
            return 0.0
        return round(dot / (norm_left * norm_right), 4)
