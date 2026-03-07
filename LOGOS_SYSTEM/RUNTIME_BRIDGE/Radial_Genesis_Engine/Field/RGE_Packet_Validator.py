"""
Radial_Genesis_Engine - RGE_Packet_Validator
Structural validator for recursion field packets.

Passive infrastructure only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 5
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)


class RGEPacketValidator:
    """
    Structural validator for recursion field packets.
    """

    @staticmethod
    def validate(packet: RGEPacketBase) -> bool:

        if not packet.packet_id:
            raise ValueError("Packet missing packet_id")

        if not packet.packet_type:
            raise ValueError("Packet missing packet_type")

        if not isinstance(packet.payload, dict):
            raise ValueError("Packet payload must be a dictionary")

        return True
