# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-062
# module_name:          schema_registry
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/schema_registry.py
# responsibility:       Utility module: schema registry
# runtime_stage:        utility
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
schema_registry.py — Central registry for JSON schema definitions.

Loads JSON schemas from the orchestration/json_drivers/ directory and
validates configuration structures on demand. Designed as the authoritative
validation authority referenced by all other modules (M00).
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

_SCHEMA_DIR = (
    Path(__file__).resolve().parent.parent.parent / "orchestration" / "json_drivers"
)
_schema_cache: Dict[str, Dict[str, Any]] = {}


def _load_schema_from_file(schema_path: Path) -> Dict[str, Any]:
    """Load a single schema file and return its parsed content."""
    with open(schema_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_schema(name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a named schema from the registry.

    Attempts to load from the schema cache first; falls back to disk.
    Returns None if the schema cannot be found.

    Args:
        name: Schema name (filename without .json extension,
              or a dotpath like 'crawl_configs.crawl_config').

    Returns:
        Parsed schema dict, or None if not found.
    """
    if name in _schema_cache:
        return _schema_cache[name]

    candidate = _SCHEMA_DIR / f"{name}.json"
    if candidate.is_file():
        schema = _load_schema_from_file(candidate)
        _schema_cache[name] = schema
        return schema

    return None


def register_schema(name: str, schema: Dict[str, Any]) -> None:
    """
    Register a schema definition directly (without loading from disk).

    Args:
        name:   Unique schema identifier.
        schema: Schema dict to register.
    """
    _schema_cache[name] = schema


def validate(artifact: Any, schema_name: str) -> Dict[str, Any]:
    """
    Validate an artifact against a named schema.

    Performs structural key presence checks.  Full JSON-Schema validation
    requires the 'jsonschema' package; this implementation provides a
    lightweight fallback that checks required top-level keys when the
    schema declares them.

    Args:
        artifact:    The data structure to validate.
        schema_name: Name of the schema to validate against.

    Returns:
        Dict with keys:
            'valid' (bool)
            'errors' (list[str])
    """
    errors: list[str] = []
    schema = get_schema(schema_name)

    if schema is None:
        return {
            "valid": True,
            "errors": [],
            "warning": f"Schema '{schema_name}' not found; validation skipped",
        }

    required_keys = schema.get("required", [])
    if isinstance(artifact, dict):
        for key in required_keys:
            if key not in artifact:
                errors.append(f"Missing required key: '{key}'")
    elif required_keys:
        errors.append("Artifact is not a dict; cannot check required keys")

    return {"valid": len(errors) == 0, "errors": errors}


def list_registered_schemas() -> list[str]:
    """Return the names of all currently cached schemas."""
    return list(_schema_cache.keys())
