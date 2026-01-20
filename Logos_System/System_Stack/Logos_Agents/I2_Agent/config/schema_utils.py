# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
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
module_name: schema_utils
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
  source: System_Stack/Logos_Agents/I2_Agent/config/schema_utils.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from typing import Any, Dict, List, Optional

from .errors import SchemaError


def require_dict(obj: Any, name: str) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        raise SchemaError(f"{name} must be a dict")
    return obj


def require_str(obj: Any, name: str) -> str:
    if not isinstance(obj, str) or not obj.strip():
        raise SchemaError(f"{name} must be a non-empty string")
    return obj


def get_str(d: Dict[str, Any], key: str, default: str = "") -> str:
    v = d.get(key, default)
    return v if isinstance(v, str) else default


def get_dict(d: Dict[str, Any], key: str) -> Dict[str, Any]:
    v = d.get(key)
    return v if isinstance(v, dict) else {}


def get_list(d: Dict[str, Any], key: str) -> List[Any]:
    v = d.get(key)
    return v if isinstance(v, list) else []
