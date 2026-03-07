"""RGE Stage 30 — Runtime Bootstrap.

Orchestrates the initialization sequence for the RGE runtime bridge:
  1. Creates RGEBridgeNexus (channel + dispatcher, already bound).
  2. Creates RGERuntimeRegistry.
  3. Registers the nexus dispatcher with the registry so that callers may
     register further runtime interfaces through the registry's stable API.

Returns the initialized RGEBridgeNexus from initialize_runtime().

Stdlib only; no async logic.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Bootstrap.RGE_Bridge_Nexus import (
    RGEBridgeNexus,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Registry import (
    RGERuntimeRegistry,
)


class RGERuntimeBootstrap:
    """Runs the bootstrap initialization sequence for the RGE runtime bridge.

    After initialize_runtime() completes:
      - nexus.get_channel() is bound to nexus.get_dispatcher().
      - The dispatcher is the same instance held by the registry.
      - External runtime components may register themselves via
        self.registry.register_runtime(interface).
    """

    def __init__(self) -> None:
        self.registry: RGERuntimeRegistry = RGERuntimeRegistry()

    def initialize_runtime(self) -> RGEBridgeNexus:
        """Create and wire the bridge nexus; register its dispatcher.

        Returns:
            The initialized RGEBridgeNexus instance.
        """
        nexus = RGEBridgeNexus()
        # Replace the registry's internal dispatcher with the nexus dispatcher
        # so that register_runtime() calls route to the same dispatcher the
        # channel is already bound to.
        self.registry._dispatcher = nexus.get_dispatcher()
        return nexus
