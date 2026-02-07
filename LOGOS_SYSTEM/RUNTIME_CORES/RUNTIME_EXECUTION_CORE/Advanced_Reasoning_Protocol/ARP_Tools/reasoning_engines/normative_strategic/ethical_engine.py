# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: ethical_engine
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Tools/reasoning_engines/normative_strategic/ethical_engine.py.
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Tools/reasoning_engines/normative_strategic/ethical_engine.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _load_moral_validator() -> Optional[Any]:
    try:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.MVS_System.MVS_Core.mathematics.privation_mathematics import (
            MoralSetValidator,
        )

        return MoralSetValidator()
    except Exception:
        return None


class EthicalEngine:
    def __init__(self) -> None:
        self.moral_validator = _load_moral_validator()

    def evaluate(self, action: str, prohibited: List[str], entity: Optional[Any] = None) -> Dict[str, Any]:
        action = action.lower().strip()
        blocked = any(p.lower().strip() in action for p in prohibited)
        moral_validation = None
        if self.moral_validator:
            try:
                moral_validation = self.moral_validator.validate_moral_operation(entity or action, "evaluate")
            except Exception:
                moral_validation = {"status": "error", "reason": "moral_validation_failed"}
        return {
            "engine": "ethical",
            "action": action,
            "allowed": not blocked,
            "moral_validation": moral_validation,
        }
