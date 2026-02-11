# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
Consistency Engine - Contradiction detection
"""

from __future__ import annotations
from typing import Any, Dict, List


class ConsistencyEngine:
    """Detect contradictions and inconsistencies."""
    
    def analyze(self, statements: List[str]) -> Dict[str, Any]:
        """
        Detect contradictions in statements.
        
        Returns:
            {
                "engine": "consistency",
                "contradictions": List[Dict],
                "conflict_severity": float,
                "consistent_subset_size": int
            }
        """
        if not statements:
            return {"engine": "consistency", "contradictions": [], "conflict_severity": 0.0}
        
        contradictions = []
        
        # Simple heuristic: look for negation patterns
        for i, s1 in enumerate(statements):
            for s2 in statements[i+1:]:
                if self._check_negation(s1, s2):
                    contradictions.append({
                        "statement1": s1,
                        "statement2": s2,
                        "type": "negation",
                        "severity": 0.8
                    })
        
        severity = min(1.0, len(contradictions) / max(len(statements), 1))
        consistent_size = len(statements) - len(contradictions)
        
        return {
            "engine": "consistency",
            "contradictions": contradictions[:5],
            "conflict_severity": round(severity, 3),
            "consistent_subset_size": consistent_size
        }
    
    def _check_negation(self, s1: str, s2: str) -> bool:
        """Simple negation check"""
        negation_words = ["not", "no", "never", "false"]
        s1_lower = s1.lower()
        s2_lower = s2.lower()
        
        s1_has_neg = any(neg in s1_lower for neg in negation_words)
        s2_has_neg = any(neg in s2_lower for neg in negation_words)
        
        # If one has negation and they share keywords, likely contradiction
        if s1_has_neg != s2_has_neg:
            s1_words = set(s1_lower.split())
            s2_words = set(s2_lower.split())
            shared = s1_words.intersection(s2_words)
            return len(shared) > 2
        
        return False
