"""RGE Stage 29 — Bridge Nexus.

Central wiring point that creates and binds the cognition channel and runtime
dispatcher together.  All other bootstrap components obtain their channel and
dispatcher references through this class.

Stdlib only; no async logic.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Channel import (
    RGECognitionChannel,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Dispatcher import (
    RGERuntimeDispatcher,
)


class RGEBridgeNexus:
    """Creates and exposes a bound cognition channel and runtime dispatcher.

    On construction:
      - A fresh RGECognitionChannel is created.
      - A fresh RGERuntimeDispatcher is created.
      - The dispatcher is attached to the channel so that every call to
        channel.emit() automatically forwards to dispatcher.dispatch().

    Both objects are then available via their respective accessors.
    """

    def __init__(self) -> None:
        self._channel: RGECognitionChannel = RGECognitionChannel()
        self._dispatcher: RGERuntimeDispatcher = RGERuntimeDispatcher()
        # Bind dispatcher to channel so emit() triggers dispatch().
        self._channel.set_runtime_dispatcher(self._dispatcher)

    def get_channel(self) -> RGECognitionChannel:
        """Return the bound cognition channel."""
        return self._channel

    def get_dispatcher(self) -> RGERuntimeDispatcher:
        """Return the runtime dispatcher attached to the channel."""
        return self._dispatcher
