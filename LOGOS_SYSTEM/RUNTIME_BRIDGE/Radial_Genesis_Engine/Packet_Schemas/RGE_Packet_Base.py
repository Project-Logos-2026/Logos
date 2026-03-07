"""
Radial_Genesis_Engine - RGE_Packet_Base
Base packet structure circulated within the RGE recursion field.

Passive schema definition only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 3
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class RGEPacketBase:
    """
    Base packet structure circulated within the RGE recursion field.

    Packets represent structured artifacts exchanged between subsystems.
    """

    packet_id: str
    packet_type: str

    origin_system: str
    creation_timestamp: float

    payload: Dict[str, Any]

    tags: List[str]

    metadata: Dict[str, Any]
