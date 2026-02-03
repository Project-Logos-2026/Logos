
"""
I₂ External Ingress Adapter (Canonical)

Purpose:
- Sole external entry point for human-originated input
- Performs admissibility checks
- Hands off to MTP for SMP generation

Constraints:
- No reasoning
- No persistence
- Fail-closed
"""

from LOGOS_SYSTEM.SYSTEM.System_Stack.MTP.mtp_pipeline import (
    process_raw_text_to_response
)

def process_external_input(raw_text: str) -> str:
    if not isinstance(raw_text, str):
        raise ValueError("Invalid input type")

    if not raw_text.strip():
        raise ValueError("Empty input")

    return process_raw_text_to_response(raw_text)
