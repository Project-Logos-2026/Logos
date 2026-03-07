"""RGE Stage 23 — Signal Broadcaster.

Thin facade that forwards a RGECognitionSignal to a configured channel.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Channel import (
    RGECognitionChannel,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import (
    RGECognitionSignal,
)


class RGESignalBroadcaster:
    """Broadcasts cognition signals through a configured channel."""

    def __init__(self, broadcast_channel: RGECognitionChannel) -> None:
        self._channel = broadcast_channel

    def broadcast(self, signal: RGECognitionSignal) -> None:
        """Forward signal to the channel for delivery to all subscribers."""
        self._channel.emit(signal)
