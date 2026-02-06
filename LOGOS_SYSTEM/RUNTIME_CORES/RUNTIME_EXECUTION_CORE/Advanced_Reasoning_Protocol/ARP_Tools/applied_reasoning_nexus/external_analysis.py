from __future__ import annotations

from typing import Any, Dict


def run_external_analysis(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "engine": "external_analysis",
        "status": "skipped",
        "reason": "external hooks disabled in runtime",
    }
