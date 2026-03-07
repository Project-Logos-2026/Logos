"""
Radial_Genesis_Engine - RGE_Field_Stability_Index
Computes stability indicators for the recursion field.

Passive computation only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 9
"""

from typing import Dict

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)


class RGEFieldStabilityIndex:
    """
    Computes stability indicators for the recursion field.
    """

    @staticmethod
    def stability_score(packets: Dict[str, RGEPacketBase]) -> float:

        if not packets:
            return 0.0

        packet_count = len(packets)

        total_payload = sum(len(packet.payload) for packet in packets.values())

        return total_payload / packet_count
