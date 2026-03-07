"""RGE Stage 31 — Activation Manager.

System entry point for activating the RGE runtime bridge.

activate() runs the bootstrap sequence and returns the initialized nexus,
making both the cognition channel and runtime dispatcher accessible to the
calling context.

Stdlib only; no async logic.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Bootstrap.RGE_Bridge_Nexus import (
    RGEBridgeNexus,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Bootstrap.RGE_Runtime_Bootstrap import (
    RGERuntimeBootstrap,
)


class RGEActivationManager:
    """Entry point for activating the RGE runtime bridge.

    Calling activate() runs the full bootstrap sequence and stores references
    to the initialized nexus, channel, and dispatcher so that runtime systems
    can retrieve them after activation.

    A single RGEActivationManager instance should be used per activation
    lifecycle; calling activate() a second time creates a fresh nexus.
    """

    def __init__(self) -> None:
        self._nexus: RGEBridgeNexus | None = None
        self._bootstrap: RGERuntimeBootstrap = RGERuntimeBootstrap()

    def activate(self) -> RGEBridgeNexus:
        """Activate the RGE runtime bridge.

        Steps:
          1. Run RGERuntimeBootstrap.initialize_runtime().
          2. Store and return the initialized RGEBridgeNexus.

        Returns:
            The initialized RGEBridgeNexus exposing get_channel() and
            get_dispatcher().
        """
        self._nexus = self._bootstrap.initialize_runtime()
        return self._nexus

    def get_nexus(self) -> RGEBridgeNexus | None:
        """Return the nexus from the most recent activate() call, or None."""
        return self._nexus
