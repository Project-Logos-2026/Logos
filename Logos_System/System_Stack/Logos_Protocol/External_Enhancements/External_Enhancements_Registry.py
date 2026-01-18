# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: External_Enhancements_Registry
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
  source: System_Stack/Logos_Protocol/External_Enhancements/External_Enhancements_Registry.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Optional


@dataclass(frozen=True)
class Wrapper_Info:
    wrapper_id: str
    wraps: str
    role: str
    module_path: str
    factory: Callable[[], object]


_REGISTRY: Dict[str, Wrapper_Info] = {}


def register(info: Wrapper_Info) -> None:
    if info.wrapper_id in _REGISTRY:
        raise RuntimeError(f"Duplicate wrapper_id: {info.wrapper_id}")
    _REGISTRY[info.wrapper_id] = info


def list_wrappers() -> Dict[str, Wrapper_Info]:
    return dict(_REGISTRY)


def get_wrapper(wrapper_id: str) -> object:
    if wrapper_id not in _REGISTRY:
        raise KeyError(f"Unknown wrapper_id: {wrapper_id}")
    return _REGISTRY[wrapper_id].factory()
