"""RGE Stage 25 — Runtime Interface.

Protocol-style contract that runtime components must satisfy to receive
RGECognitionSignal objects from the RGE.

No runtime logic is implemented here; this module is purely definitional.
Stdlib only.
"""

from abc import ABC, abstractmethod

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Cognition.RGE_Cognition_Signal import (
    RGECognitionSignal,
)


class RGERuntimeInterface(ABC):
    """Abstract base defining the contract for RGE runtime observers.

    Any class that wants to receive cognition signals must inherit from this
    and implement handle_signal.
    """

    @abstractmethod
    def handle_signal(self, signal: RGECognitionSignal) -> None:
        """Handle an inbound cognition signal.

        Args:
            signal: The RGECognitionSignal emitted by the field engine.
        """
