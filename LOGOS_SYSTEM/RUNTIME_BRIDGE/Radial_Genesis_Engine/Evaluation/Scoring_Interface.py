"""
Scoring interface placeholder for pluggable evaluation modules.
"""


class ScoringInterface:
    def compute_score(self, configuration) -> float:
        raise NotImplementedError("Scoring modules must implement compute_score()")
