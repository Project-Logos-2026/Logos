# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-040
# module_name:          repair_registry_loader
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/repair_registry_loader.py
# responsibility:       Inspection module: repair registry loader
# runtime_stage:        audit
# execution_entry:      None
# allowed_targets:      []
# forbidden_targets:    ["SYSTEM", "WORKFLOW_NEXUS"]
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-AP-V2.1]
# implementation_phase: PHASE_2
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate

enforce_runtime_gate()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

# ARCHON_PRIME MODULE
# Created by remediation stage AP-REM-001
# Purpose: Foundation configuration loader

"""
repair_registry_loader.py — Load and expose the repair registry (M02).

Loads configs/repair_registry/repair_registry.json and returns its
parsed content as a dictionary.  All modules that need to consult
the failure-class → remediation-behaviour mapping must call
load_repair_registry() from this module.
"""

import json
from pathlib import Path
from typing import Any, Dict

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_REGISTRY_PATH = (
    _REPO_ROOT / "configs" / "repair_registry" / "repair_registry.json"
)

_registry_cache: Dict[str, Any] = {}


def load_repair_registry(registry_path: str | Path | None = None) -> Dict[str, Any]:
    """
    Load and return the repair registry.

    Results are cached after the first load.  Pass an explicit
    *registry_path* to override the default location.

    Args:
        registry_path: Optional path to repair_registry.json.
                       Defaults to configs/repair_registry/repair_registry.json.

    Returns:
        Parsed repair registry dictionary.

    Raises:
        FileNotFoundError: If the registry file cannot be located.
        json.JSONDecodeError: If the registry file contains invalid JSON.
    """
    global _registry_cache

    if _registry_cache:
        return _registry_cache

    path = Path(registry_path) if registry_path else _DEFAULT_REGISTRY_PATH

    if not path.is_file():
        raise FileNotFoundError(
            f"[repair_registry_loader] Registry not found at: {path}"
        )

    with open(path, "r", encoding="utf-8") as fh:
        _registry_cache = json.load(fh)

    return _registry_cache


def get_repair_action(failure_class: str) -> str | None:
    """
    Look up the repair action for a given failure class.

    Args:
        failure_class: The failure class key (e.g. 'syntax_error').

    Returns:
        Repair action string, or None if the class is unknown.
    """
    registry = load_repair_registry()
    return registry.get("repair_types", {}).get(failure_class)


def reload_repair_registry(registry_path: str | Path | None = None) -> Dict[str, Any]:
    """
    Force a fresh load of the registry, bypassing the cache.

    Args:
        registry_path: Optional override path.

    Returns:
        Freshly loaded registry dictionary.
    """
    global _registry_cache
    _registry_cache = {}
    return load_repair_registry(registry_path)
