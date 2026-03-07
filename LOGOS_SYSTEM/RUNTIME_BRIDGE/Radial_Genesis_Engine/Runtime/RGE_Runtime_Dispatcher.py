"""RGE Stage 27 — Runtime Dispatcher.

Maintains a list of registered runtime subscribers and synchronously delivers
RGECognitionSignal objects to each one via dispatch().

No async logic; no external dependencies; stdlib only.
"""

from typing import List

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import (
    RGECognitionSignal,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Interface import (
    RGERuntimeInterface,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Subscriber import (
    RGERuntimeSubscriber,
)


class RGERuntimeDispatcher:
    """Dispatches cognition signals to all registered runtime subscribers.

    Runtime components register via register_runtime(). dispatch() delivers
    signals synchronously to every registered subscriber in registration order.
    """

    def __init__(self) -> None:
        self._subscribers: List[RGERuntimeSubscriber] = []

    def register_runtime(self, runtime_interface: RGERuntimeInterface) -> None:
        """Wrap interface in a subscriber and add to the dispatch list."""
        self._subscribers.append(RGERuntimeSubscriber(runtime_interface))

    def dispatch(self, signal: RGECognitionSignal) -> None:
        """Deliver signal to all registered runtime subscribers in order."""
        for subscriber in self._subscribers:
            subscriber.on_signal(signal)
