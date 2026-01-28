"""
LOGOS — SOP Dev Test Runtime State Telemetry Shim

Status: DEV_TEST_ONLY
Execution Impact: NONE
Authority: READ-ONLY EMISSION
Prometheus: NOT WIRED
Profile: Dev Test Sandbox Only

Purpose:
Expose SOP runtime state as a telemetry signal in strict compliance with:
- Design_Only_Telemetry_Emission_Contract
- Design_Only_Telemetry_Metric_Schema

This module:
- emits no decisions
- receives no inputs
- alters no control flow
- introduces no dependencies
"""

from enum import IntEnum


class RuntimeState(IntEnum):
    INIT = 0
    ACTIVE_LIMITED = 1
    HALT = 2
    INERT = 3


class DevTestRuntimeStateTelemetry:
    """
    Read-only holder for current runtime state.
    Intended to be set by SOP lifecycle transitions.
    """

    _state: RuntimeState = RuntimeState.INIT

    @classmethod
    def set_state(cls, state: RuntimeState) -> None:
        cls._state = state

    @classmethod
    def get_state(cls) -> int:
        return int(cls._state)
