from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class ProofStatus(Enum):
    PROVEN = "proven"
    DISPROVEN = "disproven"
    UNKNOWN = "unknown"


@dataclass
class ProofResult:
    status: ProofStatus
    proof_steps: List[str]
    confidence: float
    premises: List[str]
    conclusion: str


class ProofAttestationEngine:
    def verify(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        valid_steps = [s for s in steps if isinstance(s, dict) and s.get("statement")]
        return {
            "engine": "proof_attestation",
            "step_count": len(steps),
            "valid_steps": len(valid_steps),
            "verified": len(valid_steps) == len(steps),
        }

    def verify_proof(self, premises: List[str], conclusion: str) -> ProofResult:
        normalized = [p.strip() for p in premises]
        conclusion = conclusion.strip()
        steps: List[str] = []

        if conclusion in normalized:
            steps.append("Conclusion appears directly in premises")
            return ProofResult(ProofStatus.PROVEN, steps, 0.9, premises, conclusion)

        for premise in normalized:
            if "->" in premise:
                left, right = [part.strip() for part in premise.split("->", 1)]
                if left in normalized and right == conclusion:
                    steps.append(f"Applied implication: {premise}")
                    return ProofResult(ProofStatus.PROVEN, steps, 0.75, premises, conclusion)
            if "implies" in premise:
                left, right = [part.strip() for part in premise.split("implies", 1)]
                if left in normalized and right == conclusion:
                    steps.append(f"Applied implication: {premise}")
                    return ProofResult(ProofStatus.PROVEN, steps, 0.7, premises, conclusion)

        steps.append("No direct implication found")
        return ProofResult(ProofStatus.UNKNOWN, steps, 0.4, premises, conclusion)
