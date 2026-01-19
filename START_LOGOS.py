"""
===============================================================================
FILE: START_LOGOS.py
PATH: START_LOGOS.py
PROJECT: LOGOS System
PHASE: Phase-F (Prelude)
STEP: Canonical System Ignition
STATUS: GOVERNED - NON-BYPASSABLE

CLASSIFICATION:
- Authoritative Runtime Ignition
- External Invocation Boundary

GOVERNANCE:
- System_Entry_Point_Execution_Contract.md
- Runtime_Module_Header_Contract.md

ROLE:
Serves as the sole ignition point for the LOGOS system.
Delegates immediately and exclusively to LOGOS_SYSTEM.py.
Contains no system logic, governance logic, or agent logic.

ORDERING GUARANTEE:
1. START_LOGOS.py is invoked first.
2. Control is delegated to LOGOS_SYSTEM.py.
3. No other file may initiate runtime execution.

PROHIBITIONS:
- No runtime logic
- No agent creation
- No projection loading
- No epistemic mutation
- No execution on import

FAILURE SEMANTICS:
Any failure halts immediately with no side effects.
===============================================================================
"""

from LOGOS_SYSTEM import RUN_LOGOS_SYSTEM


def main() -> None:
    """Canonical ignition for LOGOS."""
    RUN_LOGOS_SYSTEM()


if __name__ == "__main__":
    main()
