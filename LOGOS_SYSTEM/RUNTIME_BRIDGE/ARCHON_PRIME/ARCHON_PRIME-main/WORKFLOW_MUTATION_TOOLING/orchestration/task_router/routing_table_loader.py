# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-011
# module_name:          routing_table_loader
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/orchestration/task_router/routing_table_loader.py
# responsibility:       Orchestration module: routing table loader
# runtime_stage:        orchestration
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
routing_table_loader.py — Load and expose the canonical artifact routing table (M01).

Loads orchestration/task_router/routing_table.json and returns its
parsed content as a dictionary mapping artifact type keys to their
canonical destination paths.  All artifact write operations must
resolve destinations via load_routing_table().
"""

import json
from pathlib import Path
from typing import Any, Dict

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_ROUTING_TABLE_PATH = (
    _REPO_ROOT / "orchestration" / "task_router" / "routing_table.json"
)

_routing_cache: Dict[str, Any] = {}


def load_routing_table(routing_table_path: str | Path | None = None) -> Dict[str, Any]:
    """
    Load and return the artifact routing table.

    Results are cached after the first load.  Pass an explicit
    *routing_table_path* to override the default location.

    Args:
        routing_table_path: Optional path to routing_table.json.
                            Defaults to orchestration/task_router/routing_table.json.

    Returns:
        Parsed routing table dictionary mapping artifact type → canonical path.

    Raises:
        FileNotFoundError: If the routing table file cannot be located.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    global _routing_cache

    if _routing_cache:
        return _routing_cache

    path = (
        Path(routing_table_path) if routing_table_path else _DEFAULT_ROUTING_TABLE_PATH
    )

    if not path.is_file():
        raise FileNotFoundError(
            f"[routing_table_loader] Routing table not found at: {path}"
        )

    with open(path, "r", encoding="utf-8") as fh:
        _routing_cache = json.load(fh)

    return _routing_cache


def resolve_destination(artifact_type: str) -> str | None:
    """
    Return the canonical destination path for a given artifact type key.

    Args:
        artifact_type: The artifact type key (e.g. 'module_index').

    Returns:
        Destination path string, or None if the key is not in the table.
    """
    table = load_routing_table()
    return table.get(artifact_type)


def reload_routing_table(
    routing_table_path: str | Path | None = None,
) -> Dict[str, Any]:
    """
    Force a fresh load of the routing table, bypassing the cache.

    Args:
        routing_table_path: Optional override path.

    Returns:
        Freshly loaded routing table dictionary.
    """
    global _routing_cache
    _routing_cache = {}
    return load_routing_table(routing_table_path)
