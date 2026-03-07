"""RGE Stage 14 — Topology Graph Storage.

Stores node adjacency relationships for the recursion field.
Storage only — no pathfinding, no routing.
"""

from typing import Dict, List

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Node import (
    RGEFieldNode,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Edge import (
    RGEFieldEdge,
)


class RGEFieldGraph:
    """Adjacency store for recursion field nodes and edges."""

    def __init__(self) -> None:
        self.nodes: Dict[str, RGEFieldNode] = {}
        self.edges: List[RGEFieldEdge] = []

    def add_node(self, node: RGEFieldNode) -> None:
        """Register a node in the graph by its node_id."""
        self.nodes[node.node_id] = node

    def add_edge(self, edge: RGEFieldEdge) -> None:
        """Append an edge to the adjacency list."""
        self.edges.append(edge)

    def get_edges_from(self, node_id: str) -> List[RGEFieldEdge]:
        """Return all edges whose source_node matches node_id."""
        return [e for e in self.edges if e.source_node == node_id]
