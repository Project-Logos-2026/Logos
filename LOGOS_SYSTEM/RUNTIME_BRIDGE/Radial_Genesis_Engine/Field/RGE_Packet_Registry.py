"""
Radial_Genesis_Engine - RGE_Packet_Registry
Registry maintaining packets currently circulating within the recursion field.

Passive infrastructure only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 4
"""

from typing import Dict, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)


class RGEPacketRegistry:
    """
    Registry maintaining packets currently circulating within the recursion field.
    """

    def __init__(self) -> None:
        self._packets: Dict[str, RGEPacketBase] = {}

    def register_packet(self, packet: RGEPacketBase) -> None:
        self._packets[packet.packet_id] = packet

    def remove_packet(self, packet_id: str) -> None:
        if packet_id in self._packets:
            del self._packets[packet_id]

    def get_packet(self, packet_id: str) -> Optional[RGEPacketBase]:
        return self._packets.get(packet_id)

    def all_packets(self) -> Dict[str, RGEPacketBase]:
        return dict(self._packets)
