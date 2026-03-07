"""
Radial_Genesis_Engine - RGE_Circulation_Controller
Manages packet flow within the recursion field.

Passive infrastructure only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 6
"""

from typing import List

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Registry import (
    RGEPacketRegistry,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Validator import (
    RGEPacketValidator,
)


class RGECirculationController:
    """
    Manages packet flow within the recursion field.
    """

    def __init__(self, registry: RGEPacketRegistry) -> None:
        self.registry = registry

    def circulate(self, packets: List[RGEPacketBase]) -> None:

        for packet in packets:
            if RGEPacketValidator.validate(packet):
                self.registry.register_packet(packet)
