"""
PACKAGE: Synthetic_Cognition_Protocol.core
STATUS: STRUCTURAL STUB (SCP PHASE-INCOMPLETE)

Purpose:
Defines the minimal public surface for Synthetic Cognition Protocol (SCP)
expected by tests and downstream imports.

No cognition, planning, or inference logic is implemented.
"""

__all__ = [
    "CognitionContext",
    "CognitionResult",
    "run_cognition",
]


class CognitionContext:
    def __init__(self, *args, **kwargs):
        pass


class CognitionResult:
    def __init__(self, *args, **kwargs):
        self.output = None


def run_cognition(*args, **kwargs):
    raise NotImplementedError(
        "run_cognition is not implemented (SCP stub)."
    )
