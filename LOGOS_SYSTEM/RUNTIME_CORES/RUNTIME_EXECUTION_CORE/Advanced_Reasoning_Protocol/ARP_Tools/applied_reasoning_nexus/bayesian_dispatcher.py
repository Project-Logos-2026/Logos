from __future__ import annotations

from typing import Any, Dict


def run_bayesian_dispatch(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    evidence = payload.get("evidence") or []
    if isinstance(evidence, dict):
        evidence = list(evidence.values())

    score = 0.0
    for item in evidence:
        score += 0.1 if item else 0.0

    score = min(1.0, round(score, 4))
    return {
        "engine": "bayesian_dispatch",
        "evidence_count": len(evidence),
        "probability": score,
        "confidence": round(0.5 + score / 2.0, 4),
    }
