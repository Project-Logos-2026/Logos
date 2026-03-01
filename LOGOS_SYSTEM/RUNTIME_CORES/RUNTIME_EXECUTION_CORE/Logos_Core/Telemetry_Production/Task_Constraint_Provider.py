# LOGOS SYSTEM — Canonical Runtime Header
# Module: Task_Constraint_Provider (M6A)
# Phase: M6A Constraint Ingress and Context Injection
# Governance: Fail-closed, advisory-only, deterministic

from typing import Any, Dict, List, Protocol
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Task_Triad_Derivation import Constraint

class ConstraintProvider(Protocol):
    def get_constraints_for_tick(self, task_context: Dict[str, Any]) -> List[Constraint]: ...

class DeclaredConstraintProvider:
    """
    Pass-through provider: reads pre-declared constraints from task_context.
    M6 implementation. Future phases may replace with governance-inference provider.
    """
    CONTEXT_KEY: str = "declared_constraints"

    def get_constraints_for_tick(self, task_context: Dict[str, Any]) -> List[Constraint]:
        raw = task_context.get(self.CONTEXT_KEY, [])
        if isinstance(raw, list):
            return [c for c in raw if isinstance(c, Constraint)]
        return []
