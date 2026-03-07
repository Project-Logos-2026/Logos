"""
Radial_Genesis_Engine - RGE_Completion_Metrics
Computes completion metrics for recursion field packets.

Passive computation only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 7
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)


class RGECompletionMetrics:
    """
    Computes completion metrics for recursion field packets.
    """

    @staticmethod
    def completion_score(packet: RGEPacketBase) -> float:
        return float(len(packet.payload))

    @staticmethod
    def completion_potential(packet: RGEPacketBase) -> float:
        return max(0.0, 1.0 - (len(packet.payload) / 100.0))
