"""RGE Stage 26 — Runtime Subscriber.

Wraps a RGERuntimeInterface and exposes a callable-style on_signal method
compatible with RGECognitionChannel subscriber registration.

Stdlib only; no async logic.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import (
    RGECognitionSignal,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Interface import (
    RGERuntimeInterface,
)


class RGERuntimeSubscriber:
    """Adapts a RGERuntimeInterface into a simple callable subscriber.

    on_signal delegates to the wrapped interface's handle_signal method, keeping
    the interface contract decoupled from the channel's callback convention.
    """

    def __init__(self, runtime_interface: RGERuntimeInterface) -> None:
        self._interface = runtime_interface

    def on_signal(self, signal: RGECognitionSignal) -> None:
        """Deliver signal to the wrapped runtime interface."""
        self._interface.handle_signal(signal)
