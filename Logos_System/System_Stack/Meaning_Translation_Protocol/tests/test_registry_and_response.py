from __future__ import annotations
# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_registry_and_response
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Meaning_Translation_Protocol/tests/test_registry_and_response.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""Smoke tests for UIP registry and response formatter."""


import pytest

from User_Interaction_Protocol.uip_protocol.core_processing.registry import (
    StepHandler,
    UIPRegistry,
    UIPStatus,
    UIPStep,
)
from User_Interaction_Protocol.uip_protocol.output.response_formatter import (
    ResponseFormatter,
)


@pytest.mark.asyncio
async def test_registry_process_step_success() -> None:
    registry = UIPRegistry()

    async def dummy_handler(context):
        return {"ok": True}

    registry.register_handler(
        StepHandler(step=UIPStep.STEP_0_PREPROCESSING, handler_func=dummy_handler)
    )

    context = registry.create_context("session-test", "hello")
    context = await registry.process_step(context, UIPStep.STEP_0_PREPROCESSING)

    assert context.status == UIPStatus.COMPLETED
    assert context.step_results[UIPStep.STEP_0_PREPROCESSING] == {"ok": True}


@pytest.mark.asyncio
async def test_response_formatter_basic() -> None:
    formatter = ResponseFormatter()

    response = await formatter.synthesize_response(
        context={"user_input": "hello"},
        adaptive_profile={"confidence_level": 0.5},
        iel_bundle=None,
    )

    assert response.response_text
    assert 0.0 <= response.confidence <= 1.0
