"""RGE Stage 13 — Node Edge Structure.

Represents a directed connection between two field nodes.
Frozen dataclass; no traversal logic.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class RGEFieldEdge:
    """Immutable directed edge between two topology nodes."""

    source_node: str
    target_node: str
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
