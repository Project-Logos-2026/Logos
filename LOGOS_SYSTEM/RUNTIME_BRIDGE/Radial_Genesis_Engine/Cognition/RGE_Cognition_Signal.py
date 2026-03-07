"""RGE Stage 21 — Cognition Signal.

Lightweight immutable value object representing a single propagation event.
No runtime logic; stdlib only.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RGECognitionSignal:
    """Immutable record of a packet propagation event."""

    packet_id: str
    source_node: str
    destination_node: str
    timestamp: float
