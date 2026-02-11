# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
Inductive Reasoning Engine - Pattern generalization from examples
"""

from __future__ import annotations

from typing import Any, Dict, List
from collections import Counter


class InductiveEngine:
    """
    Inductive reasoning: generalize patterns from specific examples.
    
    Produces:
    - Pattern descriptions
    - Confidence based on example consistency
    - Exception detection
    """
    
    def analyze(self, examples: List[Any]) -> Dict[str, Any]:
        """
        Perform inductive reasoning on examples.
        
        Args:
            examples: List of examples to generalize from
            
        Returns:
            {
                "engine": "inductive",
                "pattern": str,
                "confidence": float,
                "example_count": int,
                "exceptions": List[Any],
                "consistency_score": float
            }
        """
        if not examples:
            return {
                "engine": "inductive",
                "pattern": "insufficient_data",
                "confidence": 0.0,
                "example_count": 0,
                "exceptions": [],
                "consistency_score": 0.0
            }
        
        # Analyze example types and structure
        example_types = [type(ex).__name__ for ex in examples]
        type_counter = Counter(example_types)
        most_common_type = type_counter.most_common(1)[0][0]
        
        # Calculate consistency
        consistency = type_counter[most_common_type] / len(examples)
        
        # Detect exceptions (examples not matching the dominant pattern)
        exceptions = [ex for ex in examples if type(ex).__name__ != most_common_type]
        
        # Generate pattern description
        if most_common_type == "str":
            pattern = self._analyze_string_pattern(
                [ex for ex in examples if isinstance(ex, str)]
            )
        elif most_common_type in ("int", "float"):
            pattern = self._analyze_numeric_pattern(
                [ex for ex in examples if isinstance(ex, (int, float))]
            )
        elif most_common_type == "dict":
            pattern = self._analyze_dict_pattern(
                [ex for ex in examples if isinstance(ex, dict)]
            )
        else:
            pattern = f"Dominant type: {most_common_type}"
        
        # Confidence based on consistency and sample size
        confidence = consistency * min(1.0, len(examples) / 10.0)
        
        return {
            "engine": "inductive",
            "pattern": pattern,
            "confidence": round(confidence, 3),
            "example_count": len(examples),
            "exceptions": exceptions[:5],  # Limit exceptions
            "consistency_score": round(consistency, 3)
        }
    
    def _analyze_string_pattern(self, strings: List[str]) -> str:
        """Analyze pattern in string examples"""
        if not strings:
            return "empty_string_set"
        
        # Check for common prefixes/suffixes
        common_prefix = self._find_common_prefix(strings)
        common_suffix = self._find_common_suffix(strings)
        
        avg_length = sum(len(s) for s in strings) / len(strings)
        
        pattern_parts = []
        if common_prefix:
            pattern_parts.append(f"prefix='{common_prefix}'")
        if common_suffix:
            pattern_parts.append(f"suffix='{common_suffix}'")
        pattern_parts.append(f"avg_length={avg_length:.1f}")
        
        return f"String pattern: {', '.join(pattern_parts)}"
    
    def _analyze_numeric_pattern(self, numbers: List[float]) -> str:
        """Analyze pattern in numeric examples"""
        if not numbers:
            return "empty_numeric_set"
        
        avg = sum(numbers) / len(numbers)
        min_val = min(numbers)
        max_val = max(numbers)
        
        # Check for arithmetic sequence
        if len(numbers) >= 3:
            diffs = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
            if len(set(diffs)) == 1:
                return f"Arithmetic sequence: step={diffs[0]}, range=[{min_val}, {max_val}]"
        
        return f"Numeric pattern: avg={avg:.2f}, range=[{min_val}, {max_val}]"
    
    def _analyze_dict_pattern(self, dicts: List[Dict]) -> str:
        """Analyze pattern in dictionary examples"""
        if not dicts:
            return "empty_dict_set"
        
        # Find common keys
        all_keys = [set(d.keys()) for d in dicts]
        common_keys = set.intersection(*all_keys) if all_keys else set()
        
        return f"Dict pattern: {len(common_keys)} common keys, avg_size={sum(len(d) for d in dicts) / len(dicts):.1f}"
    
    def _find_common_prefix(self, strings: List[str]) -> str:
        """Find longest common prefix"""
        if not strings:
            return ""
        
        prefix = strings[0]
        for s in strings[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix
    
    def _find_common_suffix(self, strings: List[str]) -> str:
        """Find longest common suffix"""
        if not strings:
            return ""
        
        # Reverse strings and find common prefix
        reversed_strings = [s[::-1] for s in strings]
        reversed_suffix = self._find_common_prefix(reversed_strings)
        return reversed_suffix[::-1]
