# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: tool_chain_executor
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
  source: System_Stack/System_Operations_Protocol/Optimization/tool_chain_executor.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Tool Chain Executor
===================

Derive Deterministic Tool Chain Executor to satisfy tool optimizer gap tool_chain_executor

Provides deterministic orchestration across validated tool steps.
"""

import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


class ToolChainExecutor:
    """Execute ordered tool callables with audit history."""

    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    def execute(
        self,
        steps: Iterable[Tuple[str, Callable[[Any], Any]]],
        payload: Any = None,
        allow_partial: bool = False,
    ) -> Dict[str, Any]:
        timeline: List[Dict[str, Any]] = []
        current = payload
        for index, (name, func) in enumerate(list(steps)):
            record = {
                "step": index,
                "name": name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            try:
                current = func(current)
                record["status"] = "ok"
            except Exception as exc:  # noqa: BLE001 - surface failure detail to caller
                record["status"] = "error"
                record["reason"] = str(exc)
                if not allow_partial:
                    timeline.append(record)
                    break
            timeline.append(record)
        outcome = {
            "status": "ok",
            "results": timeline,
            "final_payload": current,
        }
        if any(entry.get("status") == "error" for entry in timeline):
            outcome["status"] = "partial" if allow_partial else "error"
        self.history.append(
            {
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                "timeline": timeline,
                "status": outcome["status"],
            }
        )
        return outcome

    def last_run(self) -> Optional[Dict[str, Any]]:
        """Return the most recent execution record if available."""
        return self.history[-1] if self.history else None


EXECUTOR = ToolChainExecutor()


def run_chain(
    step_functions: Iterable[Tuple[str, Callable[[Any], Any]]],
    payload: Any = None,
    allow_partial: bool = False,
) -> Dict[str, Any]:
    """Execute a deterministic chain of tool callables."""

    return EXECUTOR.execute(step_functions, payload, allow_partial=allow_partial)


if __name__ == "__main__":
    def _echo(value: Any) -> Any:
        return value

    report = run_chain([("echo", _echo)], {"demo": True})
    print(json.dumps(report))
