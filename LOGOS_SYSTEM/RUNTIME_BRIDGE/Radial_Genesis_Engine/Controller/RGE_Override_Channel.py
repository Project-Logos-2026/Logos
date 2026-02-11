"""
Runtime_Bridge - RGE_Override_Channel
Runtime_Spine routed override signaling for RGE coordination.
References: RGE_SOVEREIGNTY_CONTRACT.md, GENESIS_SELECTOR_STATE_MACHINE.md
"""


class RGEOverrideChannel:
    """
    Override signaling channel for Runtime_Spine to control RGE yield behavior.
    References: RGE_SOVEREIGNTY_CONTRACT.md
    """

    def __init__(self) -> None:
        self._override_active = False
        self._hard_override_active = False

    def register_override(self, hard: bool = False) -> None:
        self._override_active = True
        self._hard_override_active = self._hard_override_active or hard

    def register_hard_override(self) -> None:
        self.register_override(hard=True)

    def should_yield(self) -> bool:
        return self._override_active

    def is_hard_override(self) -> bool:
        return self._hard_override_active

    def clear_override(self) -> None:
        self._override_active = False
        self._hard_override_active = False
