"""RGE Stage 15 — Graph Builder.

Controlled construction of topology graphs from an existing field topology.
No traversal, no routing.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Edge import (
    RGEFieldEdge,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import (
    RGEFieldGraph,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Topology import (
    RGEFieldTopology,
)


class RGEGraphBuilder:
    """Constructs graph edges from topology-validated node pairs."""

    def __init__(self, topology: RGEFieldTopology, graph: RGEFieldGraph) -> None:
        self._topology = topology
        self._graph = graph

    def connect_nodes(
        self, source_id: str, target_id: str, weight: float = 1.0
    ) -> None:
        """Create a directed edge from source to target after verifying both nodes exist.

        Raises:
            ValueError: If either node_id is not present in the topology.
        """
        if self._topology.get_node(source_id) is None:
            raise ValueError(f"Source node '{source_id}' not found in topology.")
        if self._topology.get_node(target_id) is None:
            raise ValueError(f"Target node '{target_id}' not found in topology.")

        edge = RGEFieldEdge(
            source_node=source_id,
            target_node=target_id,
            weight=weight,
        )
        self._graph.add_edge(edge)
