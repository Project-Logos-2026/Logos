# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-044
# module_name:          scanner
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/scanner.py
# responsibility:       Inspection module: scanner
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

"""
scanner.py — Repository Python source file scanner
Recursively finds all .py files, ignoring non-source trees.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: scanner.py
tool_category: Repo_Audit
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python scanner.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

from pathlib import Path
from typing import Iterator

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


IGNORE_DIRS = {
    "__pycache__",
    ".git",
    "node_modules",
    "venv",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
}


def scan(root: Path) -> Iterator[Path]:
    """Yield all .py files under root, skipping ignored directories."""
    for path in root.rglob("*.py"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        yield path


def collect(root: Path) -> list[Path]:
    """Return sorted list of all scannable .py files."""
    return sorted(scan(root))
