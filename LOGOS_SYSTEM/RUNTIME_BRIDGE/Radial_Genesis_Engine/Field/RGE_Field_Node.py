"""
Radial_Genesis_Engine - RGE_Field_Node
Represents a structural node in the recursion field topology.

Passive data structure only. No routing logic, no scoring logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 10
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RGEFieldNode:
    """
    Structural node in the recursion field topology.

    Tracks packet IDs registered within this node and optional
    structural metadata annotations.
    """

    node_id: str
    packets: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
