# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-078
# module_name:          registry_writer
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/semantic_extraction/registry_writer.py
# responsibility:       Analysis module: registry writer
# runtime_stage:        analysis
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

"""
registry_writer.py — Write AF semantic registry entries to MODULAR_LIBRARY.
AF IDs are deterministic: AF_0001, AF_0002, …
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: registry_writer.py
tool_category: Report_Generation
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python registry_writer.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import json
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json

        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


DRAC_INVAR = Path(
    "/workspaces/ARCHON_PRIME/LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE"
    "/Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
    "/DRAC_Core/DRAC_Invariables"
)
MODLIB_DIR = DRAC_INVAR / "MODULAR_LIBRARY"
REGISTRY_PATH = MODLIB_DIR / "af_semantic_registry.json"


def build_entry(
    counter: int,
    record: dict,
    category: str,
    semantic_modifier: str,
) -> dict:
    """Construct a single AF registry entry."""
    return {
        "af_id": f"AF_{counter:04d}",
        "function_name": record["name"],
        "signature": record["signature"],
        "file_path": record["file_path"],
        "lineno": record["lineno"],
        "category": category,
        "semantic_modifier": semantic_modifier,
        "docstring": record["docstring"],
        "imports": record["imports"],
        "body_calls": record["body_calls"],
    }


def write_registry(
    entries: list[dict],
    pass_name: str,
    category_filter: str,
) -> Path:
    """
    Write the AF registry to MODULAR_LIBRARY/af_semantic_registry.json.
    Validates uniqueness of AF IDs before writing.
    Returns the output path.
    """
    MODLIB_DIR.mkdir(parents=True, exist_ok=True)

    # Validate unique IDs
    ids = [e["af_id"] for e in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate AF IDs detected — aborting write")

    registry = {
        "schema_version": "1.0.0",
        "pass_name": pass_name,
        "category_filter": category_filter,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_entries": len(entries),
        "entries": entries,
    }

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)

    return REGISTRY_PATH
