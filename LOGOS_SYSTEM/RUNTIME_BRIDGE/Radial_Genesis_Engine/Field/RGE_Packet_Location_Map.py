"""RGE Stage 17 — Packet Location Tracker.

Tracks which topology node currently contains each packet.
Storage only — no routing logic.
"""

from typing import Dict, Optional


class RGEPacketLocationMap:
    """Maps packet IDs to their current node ID."""

    def __init__(self) -> None:
        self.locations: Dict[str, str] = {}

    def set_location(self, packet_id: str, node_id: str) -> None:
        """Record that packet_id currently resides in node_id."""
        self.locations[packet_id] = node_id

    def get_location(self, packet_id: str) -> Optional[str]:
        """Return the node_id for packet_id, or None if untracked."""
        return self.locations.get(packet_id)

    def remove(self, packet_id: str) -> None:
        """Remove packet_id from the location map if present."""
        self.locations.pop(packet_id, None)
