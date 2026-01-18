# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: logging_utils
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
  source: System_Stack/Logos_Agents/I1_Agent/config/logging_utils.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional


def log_event(
    *,
    event: str,
    level: str = "INFO",
    context: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Lightweight structured log record generator.

    Returns a dict; caller decides where to emit it.
    """
    record = {
        "ts": time.time(),
        "level": level,
        "event": event,
        "context": context or {},
        "data": data or {},
    }
    return record


def dumps_log(record: Dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=False)
