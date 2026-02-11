"""
Runtime_Bridge - Mode_Controller
Placeholder interface surface for runtime mode checks.
References: MODE_CONTROLLER_INTERFACE_SPEC.md, RGE_SOVEREIGNTY_CONTRACT.md
"""

from enum import Enum


class RuntimeMode(Enum):
    P1_INTERACTIVE_RADIAL = 1
    P2_AUTONOMOUS_RADIAL = 2
    P2_LOGOS_CENTRALIZED = 3
    P2_AGENT_AUTONOMOUS = 4


class ModeController:
    """
    Minimal mode query surface.
    References: MODE_CONTROLLER_INTERFACE_SPEC.md
    """

    def __init__(self, initial_mode: RuntimeMode = RuntimeMode.P1_INTERACTIVE_RADIAL) -> None:
        self._current_mode = initial_mode

    def set_mode(self, new_mode: RuntimeMode) -> None:
        self._current_mode = new_mode

    def get_mode(self) -> RuntimeMode:
        return self._current_mode

    def is_activation_allowed(self) -> bool:
        return True
