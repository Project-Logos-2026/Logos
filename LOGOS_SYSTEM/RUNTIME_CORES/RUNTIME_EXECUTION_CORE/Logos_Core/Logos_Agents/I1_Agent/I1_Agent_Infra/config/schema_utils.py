from __future__ import annotations
'\nLOGOS_MODULE_METADATA\n---------------------\nmodule_name: schema_utils\nruntime_layer: inferred\nrole: inferred\nagent_binding: None\nprotocol_binding: None\nboot_phase: inferred\nexpected_imports: []\nprovides: []\ndepends_on_runtime_state: False\nfailure_mode:\n  type: unknown\n  notes: ""\nrewrite_provenance:\n  source: System_Stack/Logos_Agents/I1_Agent/config/schema_utils.py\n  rewrite_phase: Phase_B\n  rewrite_timestamp: 2026-01-18T23:03:31.726474\nobservability:\n  log_channel: None\n  metrics: disabled\n---------------------\n'
from typing import Any, Dict, List, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.diagnostics.errors import SchemaError

def require_dict(obj: Any, name: str) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        raise SchemaError(f'{name} must be a dict')
    return obj

def require_str(obj: Any, name: str) -> str:
    if not isinstance(obj, str) or not obj.strip():
        raise SchemaError(f'{name} must be a non-empty string')
    return obj

def get_str(d: Dict[str, Any], key: str, default: str='') -> str:
    v = d.get(key, default)
    return v if isinstance(v, str) else default

def get_dict(d: Dict[str, Any], key: str) -> Dict[str, Any]:
    v = d.get(key)
    return v if isinstance(v, dict) else {}

def get_list(d: Dict[str, Any], key: str) -> List[Any]:
    v = d.get(key)
    return v if isinstance(v, list) else []