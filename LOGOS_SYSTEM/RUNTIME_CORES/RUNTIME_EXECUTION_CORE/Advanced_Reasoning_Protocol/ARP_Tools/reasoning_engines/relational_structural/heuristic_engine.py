from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


class HeuristicEngine:
    def score(self, signals: Dict[str, float]) -> Dict[str, Any]:
        values = [float(v) for v in signals.values()] if signals else []
        total = sum(values) if values else 0.0
        entropy = self._shannon_entropy(values)
        compression_ratio = self._compression_ratio(values)
        return {
            "engine": "heuristic",
            "score": round(total, 4),
            "entropy": entropy,
            "compression_ratio": compression_ratio,
        }

    def _shannon_entropy(self, values: List[float]) -> float:
        if not values:
            return 0.0
        total = sum(abs(v) for v in values) or 1.0
        probs = [abs(v) / total for v in values if v]
        if not probs:
            return 0.0
        entropy = -sum(p * math.log(p, 2) for p in probs)
        return round(entropy, 4)

    def _compression_ratio(self, values: List[float]) -> float:
        if not values:
            return 0.0
        rounded = [round(v, 4) for v in values]
        compressed = self._simple_rle_compress(rounded)
        return round(len(compressed) / max(1, len(rounded)), 4)

    def _simple_rle_compress(self, values: List[float]) -> List[Tuple[float, int]]:
        compressed: List[Tuple[float, int]] = []
        current = values[0]
        count = 1
        for value in values[1:]:
            if value == current:
                count += 1
            else:
                compressed.append((current, count))
                current = value
                count = 1
        compressed.append((current, count))
        return compressed
