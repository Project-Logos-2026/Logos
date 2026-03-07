"""
Scoring interface for pluggable evaluation modules.
"""

from typing import Any, Dict, Protocol


class ScoringInterface(Protocol):

    @property
    def name(self) -> str:
        """Unique identifier for scoring module."""
        ...

    def compute_score(self, configuration: Dict[str, Any]) -> float:
        """Return score for candidate configuration."""
        ...
