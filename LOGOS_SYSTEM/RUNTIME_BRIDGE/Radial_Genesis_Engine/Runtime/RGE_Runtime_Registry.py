"""RGE Stage 28 — Runtime Registry.

Centralized access point for a single RGERuntimeDispatcher instance.

Provides register_runtime() and get_dispatcher() so that callers do not need
to hold a direct reference to the dispatcher.

Stdlib only; no async logic.
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Dispatcher import (
    RGERuntimeDispatcher,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Runtime.RGE_Runtime_Interface import (
    RGERuntimeInterface,
)


class RGERuntimeRegistry:
    """Holds and exposes a single RGERuntimeDispatcher.

    Callers may register runtime interfaces and retrieve the dispatcher
    through a stable access point without coupling to the dispatcher directly.
    """

    def __init__(self) -> None:
        self._dispatcher: RGERuntimeDispatcher = RGERuntimeDispatcher()

    def register_runtime(self, runtime_interface: RGERuntimeInterface) -> None:
        """Register a runtime interface with the held dispatcher."""
        self._dispatcher.register_runtime(runtime_interface)

    def get_dispatcher(self) -> RGERuntimeDispatcher:
        """Return the held dispatcher instance."""
        return self._dispatcher
