"""
Radial_Genesis_Engine - RGE_Recursion_Field_Engine
Central container coordinating packet registry, validator, router, and circulation.

Structural orchestration only. No recursion behavior, no decay, no heuristics.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 9
"""

import time
from typing import List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Packet_Schemas.RGE_Packet_Base import (
    RGEPacketBase,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Registry import (
    RGEPacketRegistry,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Validator import (
    RGEPacketValidator,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Circulation_Controller import (
    RGECirculationController,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Routing_Interface import (
    RGERoutingInterface,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Default_Router import (
    RGEDefaultRouter,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Field.RGE_Packet_Propagator import (
    RGEPacketPropagator,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import (
    RGECognitionSignal,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Signal_Broadcaster import (
    RGESignalBroadcaster,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Dispatcher import (
    RGERuntimeDispatcher,
)


class RGERecursionFieldEngine:
    """
    Central container responsible for coordinating packet registry, validator,
    router, and circulation controller.

    Structural orchestration only — no recursion behavior, no decay, no routing
    heuristics introduced at this stage.
    """

    def __init__(
        self,
        registry: Optional[RGEPacketRegistry] = None,
        router: Optional[RGERoutingInterface] = None,
        propagator: Optional[RGEPacketPropagator] = None,
        broadcaster: Optional[RGESignalBroadcaster] = None,
        runtime_dispatcher: Optional[RGERuntimeDispatcher] = None,
    ) -> None:
        self.registry: RGEPacketRegistry = registry if registry is not None else RGEPacketRegistry()
        self.router: RGERoutingInterface = router if router is not None else RGEDefaultRouter()
        self.validator: RGEPacketValidator = RGEPacketValidator()
        self.circulator: RGECirculationController = RGECirculationController(self.registry)
        self.propagator: Optional[RGEPacketPropagator] = propagator
        self.broadcaster: Optional[RGESignalBroadcaster] = broadcaster
        self.runtime_dispatcher: Optional[RGERuntimeDispatcher] = runtime_dispatcher

    def ingest_packets(self, packets: List[RGEPacketBase]) -> List[str]:
        """
        Circulate packets through the field, route each one, and return
        the list of packet_ids successfully processed.
        """
        self.circulator.circulate(packets)

        processed_ids: List[str] = []
        for packet in packets:
            result = self.router.route_packet(packet, self.registry)
            if result is not None:
                processed_ids.append(result)

        return processed_ids

    def propagate_packet(self, packet_id: str) -> None:
        """Delegate propagation of packet_id to the injected propagator.

        After successful propagation, emits a RGECognitionSignal through the
        broadcaster if one is configured.

        Raises:
            RuntimeError: If no propagator has been configured.
        """
        if self.propagator is None:
            raise RuntimeError(
                "No propagator configured on RGERecursionFieldEngine."
            )

        # Capture source location before propagation.
        source_node = self.propagator._location_map.get_location(packet_id) or ""

        self.propagator.propagate(packet_id)

        # Emit cognition signal if broadcaster is present.
        if self.broadcaster is not None:
            destination_node = self.propagator._location_map.get_location(packet_id) or ""
            signal = RGECognitionSignal(
                packet_id=packet_id,
                source_node=source_node,
                destination_node=destination_node,
                timestamp=time.time(),
            )
            self.broadcaster.broadcast(signal)
            if self.runtime_dispatcher is not None:
                self.runtime_dispatcher.dispatch(signal)
