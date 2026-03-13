# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-010
# module_name:          file_scanner
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/crawler/utils/file_scanner.py
# responsibility:       Utility module: file scanner
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

"""
ARCHON PRIME — File Scanner Utility
Stage 4: Crawler System Implementation

Responsibilities:
  - Recursively scan directories for supported file types
  - Filter by extension (.py, .json, .yaml, .yml, .md)
  - Ignore hidden directories and build artifacts
  - Detect Python modules
  - Return structured file index
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

SUPPORTED_EXTENSIONS: Set[str] = {".py", ".json", ".yaml", ".yml", ".md"}

IGNORED_DIRS: Set[str] = {
    ".git",
    "__pycache__",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    ".eggs",
    ".idea",
    ".vscode",
    "*.egg-info",
}


def scan_directory(
    root: str,
    max_depth: int = 1000,
    extensions: Optional[Set[str]] = None,
    ignored_dirs: Optional[Set[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Recursively scan root for files matching extensions.
    Returns a structured file index. Read-only — no mutations.

    Parameters
    ----------
    root       : Absolute path to scan.
    max_depth  : Maximum directory descent depth (default: 1000).
    extensions : Set of lowercase extensions to include.
    ignored_dirs : Set of directory names to prune from traversal.

    Returns
    -------
    List of file records: {path, absolute_path, extension, type, depth, size_bytes}
    """
    if extensions is None:
        extensions = SUPPORTED_EXTENSIONS
    if ignored_dirs is None:
        ignored_dirs = IGNORED_DIRS

    root_path = Path(root)
    if not root_path.exists():
        return []

    base_depth = len(root_path.parts)
    file_index: List[Dict[str, Any]] = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        current_path = Path(dirpath)
        depth = len(current_path.parts) - base_depth

        if depth > max_depth:
            dirnames.clear()
            continue

        # Prune hidden and ignored directories in-place
        dirnames[:] = sorted(
            d for d in dirnames if d not in ignored_dirs and not d.startswith(".")
        )

        for filename in sorted(filenames):
            file_path = current_path / filename
            ext = file_path.suffix.lower()

            if ext not in extensions:
                continue

            try:
                size = file_path.stat().st_size
            except OSError:
                size = 0

            rel_path = str(file_path.relative_to(root_path))

            file_index.append(
                {
                    "path": rel_path,
                    "absolute_path": str(file_path),
                    "extension": ext,
                    "type": _classify(ext),
                    "is_python_module": ext == ".py",
                    "is_hidden": filename.startswith("."),
                    "depth": depth,
                    "size_bytes": size,
                }
            )

    return file_index


def filter_python_modules(file_index: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return only Python module entries from a file index."""
    return [f for f in file_index if f.get("is_python_module")]


def filter_by_extension(
    file_index: List[Dict[str, Any]], ext: str
) -> List[Dict[str, Any]]:
    """Return entries matching a specific extension (e.g. '.json')."""
    return [f for f in file_index if f["extension"] == ext.lower()]


def summarize_index(file_index: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Produce a statistical summary of a file index."""
    type_counts: Dict[str, int] = {}
    ext_counts: Dict[str, int] = {}
    total_bytes = 0

    for f in file_index:
        t = f.get("type", "unknown")
        e = f.get("extension", "")
        type_counts[t] = type_counts.get(t, 0) + 1
        ext_counts[e] = ext_counts.get(e, 0) + 1
        total_bytes += f.get("size_bytes", 0)

    return {
        "total_files": len(file_index),
        "total_bytes": total_bytes,
        "type_counts": type_counts,
        "extension_counts": ext_counts,
    }


def _classify(ext: str) -> str:
    if ext == ".py":
        return "python_module"
    if ext == ".json":
        return "config_json"
    if ext in {".yaml", ".yml"}:
        return "config_yaml"
    if ext == ".md":
        return "documentation"
    return "unknown"


if __name__ == "__main__":
    import json
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    index = scan_directory(root)
    summary = summarize_index(index)
    print(json.dumps(summary, indent=2))
