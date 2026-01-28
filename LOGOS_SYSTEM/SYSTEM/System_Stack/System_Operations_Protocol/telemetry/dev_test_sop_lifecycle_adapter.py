"""
LOGOS — SOP Dev Test Lifecycle Adapter

Status: DEV_TEST_ONLY
Execution Impact: NONE
Authority: NONE
Role: Telemetry State Setter Only

Purpose:
Provide a single, explicit adapter for SOP lifecycle transitions
to update dev-test telemetry state without altering control flow.

This module:
- defines no lifecycle logic
- emits no decisions
- introduces no dependencies
- is inert unless explicitly called

Approved use:
SOP code MAY call these functions at lifecycle boundaries.
"""

from SYSTEM.System_Stack.System_Operations_Protocol.telemetry.dev_test_runtime_state import (
    DevTestRuntimeStateTelemetry,
    RuntimeState,
)


def sop_init() -> None:
    DevTestRuntimeStateTelemetry.set_state(RuntimeState.INIT)


def sop_active_limited() -> None:
    DevTestRuntimeStateTelemetry.set_state(RuntimeState.ACTIVE_LIMITED)


def sop_halt() -> None:
    DevTestRuntimeStateTelemetry.set_state(RuntimeState.HALT)


def sop_inert() -> None:
    DevTestRuntimeStateTelemetry.set_state(RuntimeState.INERT)
