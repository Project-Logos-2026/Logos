"""RGE Stage 16 — Graph Traversal Primitive.

Minimal inspection utilities for the recursion field graph.
No search algorithms, no pathfinding, no routing decisions.
"""

from typing import List

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Graph import (
    RGEFieldGraph,
)


class RGEGraphTraversal:
    """Read-only traversal primitives over an RGEFieldGraph."""

    def __init__(self, graph: RGEFieldGraph) -> None:
        self._graph = graph

    def neighbors(self, node_id: str) -> List[str]:
        """Return the target_node values for all edges originating from node_id."""
        return [e.target_node for e in self._graph.get_edges_from(node_id)]
