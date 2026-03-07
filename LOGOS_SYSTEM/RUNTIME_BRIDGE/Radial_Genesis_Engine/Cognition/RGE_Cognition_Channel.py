"""RGE Stage 22 — Cognition Channel.

Simple synchronous subscriber channel for RGECognitionSignal objects.
No async logic; no external dependencies.
"""

from typing import TYPE_CHECKING, Callable, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import (
    RGECognitionSignal,
)

if TYPE_CHECKING:
    from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Dispatcher import (
        RGERuntimeDispatcher,
    )


class RGECognitionChannel:
    """Pub/sub channel for cognition signals.

    Subscribers are plain callables that accept a single RGECognitionSignal.
    emit() delivers signals synchronously to all registered subscribers and,
    if a runtime dispatcher is attached, forwards the signal through it.
    The dispatcher dependency is strictly optional — the channel operates
    identically without one.
    """

    def __init__(
        self,
        runtime_dispatcher: Optional["RGERuntimeDispatcher"] = None,
    ) -> None:
        self._subscribers: List[Callable[[RGECognitionSignal], None]] = []
        self._runtime_dispatcher: Optional["RGERuntimeDispatcher"] = runtime_dispatcher

    def set_runtime_dispatcher(
        self, dispatcher: "RGERuntimeDispatcher"
    ) -> None:
        """Attach or replace the optional runtime dispatcher."""
        self._runtime_dispatcher = dispatcher

    def register_subscriber(
        self, callback: Callable[[RGECognitionSignal], None]
    ) -> None:
        """Register a callable to receive future signals."""
        self._subscribers.append(callback)

    def emit(self, signal: RGECognitionSignal) -> None:
        """Deliver signal to every registered subscriber, then to the runtime dispatcher."""
        for subscriber in self._subscribers:
            subscriber(signal)
        if self._runtime_dispatcher is not None:
            self._runtime_dispatcher.dispatch(signal)
