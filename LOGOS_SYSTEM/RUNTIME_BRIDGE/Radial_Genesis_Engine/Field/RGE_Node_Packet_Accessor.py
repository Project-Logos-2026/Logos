"""RGE Stage 18 — Node Packet Accessor.

Provides controlled access to packet ID lists stored on topology nodes.
No routing logic — only manipulates node.packets lists.
"""

from typing import List

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import (
    RGEFieldTopology,
)


class RGENodePacketAccessor:
    """Controlled read/write access to the packet list of topology nodes."""

    def __init__(self, topology: RGEFieldTopology) -> None:
        self._topology = topology

    def get_packets(self, node_id: str) -> List[str]:
        """Return the list of packet IDs stored in node_id.

        Returns an empty list if the node does not exist.
        """
        node = self._topology.get_node(node_id)
        if node is None:
            return []
        return list(node.packets)

    def add_packet(self, node_id: str, packet_id: str) -> None:
        """Append packet_id to node_id's packet list.

        Auto-creates the node if it does not already exist.
        Does nothing if packet_id is already present.
        """
        node = self._topology.get_node(node_id)
        if node is None:
            node = self._topology.create_node(node_id)
        if packet_id not in node.packets:
            node.packets.append(packet_id)

    def remove_packet(self, node_id: str, packet_id: str) -> None:
        """Remove packet_id from node_id's packet list if present.

        Does nothing if the node does not exist or the packet is not listed.
        """
        node = self._topology.get_node(node_id)
        if node is None:
            return
        try:
            node.packets.remove(packet_id)
        except ValueError:
            pass
