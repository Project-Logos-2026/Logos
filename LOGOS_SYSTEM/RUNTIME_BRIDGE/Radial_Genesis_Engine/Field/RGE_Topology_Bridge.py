"""
Radial_Genesis_Engine - RGE_Topology_Bridge
Connects the packet registry with topology nodes.

Structural assignment only. No routing decisions, no topology physics.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 12
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Registry import (
    RGEPacketRegistry,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import (
    RGEFieldTopology,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Node import (
    RGEFieldNode,
)


class RGETopologyBridge:
    """
    Connects packet registry with topology nodes.

    Verifies packet existence in registry, creates node if absent,
    and appends packet_id to the node packet list.
    """

    def __init__(self, registry: RGEPacketRegistry, topology: RGEFieldTopology) -> None:
        self.registry = registry
        self.topology = topology

    def assign_packet_to_node(self, packet_id: str, node_id: str) -> None:
        if self.registry.get_packet(packet_id) is None:
            raise ValueError(f"Packet '{packet_id}' not found in registry")

        node = self.topology.get_node(node_id)
        if node is None:
            node = self.topology.create_node(node_id)

        if packet_id not in node.packets:
            node.packets.append(packet_id)
