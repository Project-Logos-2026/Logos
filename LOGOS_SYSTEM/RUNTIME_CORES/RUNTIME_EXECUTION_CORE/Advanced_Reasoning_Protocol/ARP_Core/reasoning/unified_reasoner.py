from __future__ import annotations

from typing import Any, Dict, Optional


class UnifiedReasoner:
    def analyze(
        self,
        packet: Dict[str, Any],
        context: Dict[str, Any],
        pxl_out: Optional[Dict[str, Any]] = None,
        iel_out: Optional[Dict[str, Any]] = None,
        math_out: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        pxl_score = (pxl_out or {}).get("coherence_score", 0.0)
        iel_count = (iel_out or {}).get("domain_count", 0)
        math_ready = bool((math_out or {}).get("lambda_ready"))

        aggregate = (pxl_score + float(iel_count) * 0.05 + (0.1 if math_ready else 0.0))
        aggregate = min(1.0, round(aggregate, 4))

        return {
            "engine": "unified",
            "aggregate_score": aggregate,
            "pxl_score": pxl_score,
            "iel_domains": iel_count,
            "math_ready": math_ready,
        }
