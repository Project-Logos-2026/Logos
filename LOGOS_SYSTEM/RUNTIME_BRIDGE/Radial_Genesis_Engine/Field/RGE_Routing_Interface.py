"""
Radial_Genesis_Engine - RGE_Routing_Interface
Protocol defining the minimal routing contract for recursion field packets.

Interface only — no routing decisions implemented.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 7
"""

from typing import Optional, Protocol

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Registry import (
    RGEPacketRegistry,
)


class RGERoutingInterface(Protocol):
    """
    Protocol defining the routing contract for recursion field packets.

    Implementations determine how packets are directed within the field.
    This interface defines the contract only — no routing logic is prescribed.
    """

    def route_packet(
        self,
        packet: RGEPacketBase,
        registry: RGEPacketRegistry,
    ) -> Optional[str]:
        """
        Route a packet within the recursion field.

        Returns the packet_id on successful routing, or None.
        """
        ...
