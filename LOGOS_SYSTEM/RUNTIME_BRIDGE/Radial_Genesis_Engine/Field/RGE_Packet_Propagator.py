"""RGE Stage 19 — Packet Propagation Primitive.

Moves a packet from its current node to the first deterministic neighbor.
No scoring, no decay, no multi-hop traversal.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import (
    RGEFieldGraph,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import (
    RGEFieldTopology,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Graph_Traversal import (
    RGEGraphTraversal,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Node_Packet_Accessor import (
    RGENodePacketAccessor,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Location_Map import (
    RGEPacketLocationMap,
)


class RGEPacketPropagator:
    """Moves a packet one hop to the first neighbor of its current node."""

    def __init__(
        self,
        topology: RGEFieldTopology,
        graph: RGEFieldGraph,
        accessor: RGENodePacketAccessor,
        location_map: RGEPacketLocationMap,
    ) -> None:
        self._topology = topology
        self._traversal = RGEGraphTraversal(graph)
        self._accessor = accessor
        self._location_map = location_map

    def propagate(self, packet_id: str) -> None:
        """Move packet_id from its current node to the first neighbor.

        Raises:
            ValueError: If packet_id has no recorded location.
            ValueError: If the current node has no outgoing neighbors.
        """
        source_id = self._location_map.get_location(packet_id)
        if source_id is None:
            raise ValueError(
                f"packet '{packet_id}' has no recorded location in the location map."
            )

        neighbors = self._traversal.neighbors(source_id)
        if not neighbors:
            raise ValueError(
                f"Node '{source_id}' has no outgoing neighbors; cannot propagate '{packet_id}'."
            )

        target_id = neighbors[0]  # deterministic: always first neighbor

        # Move the packet
        self._accessor.remove_packet(source_id, packet_id)
        self._accessor.add_packet(target_id, packet_id)
        self._location_map.set_location(packet_id, target_id)
