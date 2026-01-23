"""
===============================================================================
FILE: LOGOS_SYSTEM.py
PATH: LOGOS_SYSTEM.py (root)
PROJECT: LOGOS System
PHASE: Phase-F (Prelude)
STEP: Runtime Spine Compatibility Wrapper
STATUS: GOVERNED - NON-BYPASSABLE

ROLE:
Compatibility shim that delegates to the canonical runtime spine at
Logos_System/LOGOS_SYSTEM.py. Contains no independent runtime logic.

FAILURE SEMANTICS:
Delegates fail-closed behavior to the canonical runtime spine.
===============================================================================
"""

# LEGACY / COMPATIBILITY: Use Logos_System.LOGOS_SYSTEM as canonical runtime spine
from Logos_System.LOGOS_SYSTEM import RUN_LOGOS_SYSTEM, RuntimeHalt  # re-export

__all__ = ["RUN_LOGOS_SYSTEM", "RuntimeHalt"]
