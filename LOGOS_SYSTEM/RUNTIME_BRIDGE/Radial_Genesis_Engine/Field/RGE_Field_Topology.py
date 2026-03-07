"""
Radial_Genesis_Engine - RGE_Field_Topology
Container for field nodes in the recursion field.

Container only. No adjacency logic, no routing logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 11
"""

from typing import Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Field_Node import (
    RGEFieldNode,
)


class RGEFieldTopology:
    """
    Container for RGEFieldNode instances representing the recursion field topology.

    Provides node creation and retrieval. No adjacency or routing logic.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, RGEFieldNode] = {}

    def create_node(self, node_id: str) -> RGEFieldNode:
        node = RGEFieldNode(node_id=node_id)
        self.nodes[node_id] = node
        return node

    def get_node(self, node_id: str) -> Optional[RGEFieldNode]:
        return self.nodes.get(node_id)

    def all_nodes(self) -> List[RGEFieldNode]:
        return list(self.nodes.values())
