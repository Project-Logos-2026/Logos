"""
Radial_Genesis_Engine - Mode_Controller
Authoritative runtime mode management.
Only Logos Core should invoke mode transitions.
"""

from enum import Enum


class RuntimeMode(Enum):
    P1_INTERACTIVE_RADIAL = 1
    P2_AUTONOMOUS_RADIAL = 2
    P2_LOGOS_CENTRALIZED = 3
    P2_AGENT_AUTONOMOUS = 4


class ModeController:
    def __init__(self) -> None:
        self.current_mode = RuntimeMode.P1_INTERACTIVE_RADIAL

    def set_mode(self, new_mode: RuntimeMode) -> None:
        self.current_mode = new_mode

    def get_mode(self) -> RuntimeMode:
        return self.current_mode
