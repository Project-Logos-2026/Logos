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

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


IGNORE_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv", ".mypy_cache", ".pytest_cache"}


def scan(root: Path) -> Iterator[Path]:
    """Yield all .py files under root, skipping ignored directories."""
    for path in root.rglob("*.py"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        yield path


def collect(root: Path) -> list[Path]:
    """Return sorted list of all scannable .py files."""
    return sorted(scan(root))
