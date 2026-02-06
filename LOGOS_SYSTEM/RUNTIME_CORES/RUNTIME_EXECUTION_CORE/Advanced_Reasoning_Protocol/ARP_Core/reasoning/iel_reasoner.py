from __future__ import annotations

from typing import Any, Dict, Optional


class IELReasoner:
    def analyze(
        self,
        packet: Dict[str, Any],
        context: Dict[str, Any],
        pxl_out: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        iel_domains = packet.get("iel_domains") or context.get("iel_domains") or []
        if isinstance(iel_domains, str):
            iel_domains = [iel_domains]

        return {
            "engine": "iel",
            "domains": list(iel_domains),
            "pxl_coherence": (pxl_out or {}).get("coherence_score", 0.0),
            "domain_count": len(iel_domains),
        }
