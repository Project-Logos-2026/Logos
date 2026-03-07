"""
Radial_Genesis_Engine - RGE_Packet_Lifecycle
Handles lifecycle operations for packets in the recursion field.

Passive infrastructure only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 8
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Registry import (
    RGEPacketRegistry,
)


class RGEPacketLifecycleManager:
    """
    Handles lifecycle operations for packets in the recursion field.
    """

    def __init__(self, registry: RGEPacketRegistry) -> None:
        self.registry = registry

    def decay_packets(self) -> None:
        packets = list(self.registry.all_packets().values())

        for packet in packets:
            if len(packet.payload) == 0:
                self.registry.remove_packet(packet.packet_id)
