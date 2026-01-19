#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from _common import iter_files, parse_python_imports, looks_like_stdlib, write_json
try:
    from ._diagnostic_record import diag
except ImportError:  # script execution fallback
    from _diagnostic_record import diag

def scan_python_dependencies(repo: Path, targets: List[Path] | None = None) -> Dict[str, Any]:
    third_party: Set[str] = set()
    stdlib: Set[str] = set()
    local_like: Set[str] = set()
    diagnostics: List[Dict[str, Any]] = []

    py_files = list(targets) if targets else list(iter_files(repo, suffix=".py"))
    for p in py_files:
        for imp in parse_python_imports(p, repo):
            if imp.level:
                continue
            mod = (imp.module.split(".")[0] if imp.module else "")
            if not mod:
                continue
            if looks_like_stdlib(mod):
                stdlib.add(mod)
            else:
                # Heuristic: if top-level module name matches a first-party top directory, mark local-like
                local_like.add(mod)

    # We cannot reliably disambiguate third-party vs local without import resolution + sys.path.
    # Provide both sets; automation can refine later.
    return {
        "stdlib_candidates": sorted(stdlib),
        "top_level_non_stdlib_candidates": sorted(local_like),
        "diagnostics": diagnostics,
        "notes": {
            "classification": "stdlib is heuristic; non-stdlib includes both first-party and third-party. Refine via runtime import resolution if needed."
        }
    }

def scan_toolchain(repo: Path, targets: List[Path] | None = None) -> Dict[str, Any]:
    # Collect common dependency surfaces (requirements, pyproject, environment hints)
    candidates = []
    diagnostics: List[Dict[str, Any]] = []
    for p in iter_files(repo):
        rel = str(p.relative_to(repo))
        if p.name in {"requirements.txt", "requirements-dev.txt", "pyproject.toml", "Pipfile", "environment.yml"}:
            candidates.append(rel)
            diagnostics.append({**diag(error_type="DependencyManifest", line=1, char_start=0, char_end=len(p.name), details=rel, source="scan_dependencies"), "file": rel})
    return {"files": sorted(candidates), "diagnostics": diagnostics}

def scan_inter_system(repo: Path, targets: List[Path] | None = None) -> Dict[str, Any]:
    # Capture known cross-system dependencies based on repository structure
    # This is structural; import_graph covers code-level coupling.
    surfaces = []
    diagnostics: List[Dict[str, Any]] = []
    for d in ["PXL_Gate", "System_Stack", "LOGOS_SYSTEM", "System_Entry_Point", "System_Audit_Logs"]:
        p = repo / d
        if p.exists():
            surfaces.append(d)
            diagnostics.append({**diag(error_type="InterSystemSurface", line=1, char_start=0, char_end=len(d), details=d, source="scan_dependencies"), "file": d})
    return {"top_level_system_surfaces": surfaces, "diagnostics": diagnostics}

def main(argv=None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    repo = Path("/workspaces/Logos_System").resolve()
    if args:
        targets = [Path(a).resolve() for a in args]
        deps = scan_python_dependencies(repo, targets)
        # Emit only diagnostics for CLI use (schema-style). Currently only populated for severe issues.
        print(json.dumps(deps.get("diagnostics", []), indent=2))
        return 0

    out_base = Path("/workspaces/Logos_System/_Reports/SYSTEM_AUDIT/02_dependencies")
    write_json(out_base / "python_dependencies.json", scan_python_dependencies(repo))
    write_json(out_base / "toolchain_dependencies.json", scan_toolchain(repo))
    write_json(out_base / "inter_system_dependencies.json", scan_inter_system(repo))
    print(out_base)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
