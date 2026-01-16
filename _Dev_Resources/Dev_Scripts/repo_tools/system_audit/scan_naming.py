#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from _common import is_excluded_path, title_case_violation, write_json
try:
    from ._diagnostic_record import diag
except ImportError:  # script execution fallback
    from _diagnostic_record import diag

def scan(repo: Path) -> Dict[str, Any]:
    file_violations = []
    dir_violations = []

    for p in repo.rglob("*"):
        if is_excluded_path(p, repo):
            continue
        rel = str(p.relative_to(repo))
        name = p.name

        if p.is_dir():
            if title_case_violation(name):
                rec = diag(
                    error_type="NamingViolation",
                    line=1,
                    char_start=0,
                    char_end=len(name),
                    details="directory naming",
                    source="scan_naming",
                )
                rec.update({"path": rel, "name": name})
                dir_violations.append(rec)
        else:
            # For files, enforce base name (without extension) + also check extension-only edge cases
            stem = p.stem
            if stem and title_case_violation(stem):
                rec = diag(
                    error_type="NamingViolation",
                    line=1,
                    char_start=0,
                    char_end=len(stem),
                    details="file naming",
                    source="scan_naming",
                )
                rec.update({"path": rel, "name": name, "stem": stem, "suffix": p.suffix})
                file_violations.append(rec)

    # module_names (python packages) are files; we still provide separate channel for __init__.py-containing dirs
    module_violations = []
    for d in repo.rglob("*"):
        if not d.is_dir():
            continue
        if is_excluded_path(d, repo):
            continue
        init = d / "__init__.py"
        if init.exists():
            rel = str(d.relative_to(repo))
            if title_case_violation(d.name):
                rec = diag(
                    error_type="NamingViolation",
                    line=1,
                    char_start=0,
                    char_end=len(d.name),
                    details="module naming",
                    source="scan_naming",
                )
                rec.update({"package_dir": rel, "name": d.name})
                module_violations.append(rec)

    return {
        "file_names": sorted(file_violations, key=lambda x: x["path"]),
        "directory_names": sorted(dir_violations, key=lambda x: x["path"]),
        "module_names": sorted(module_violations, key=lambda x: x["package_dir"]),
        "rule": "Title_Case_With_Underscores",
    }

def main() -> int:
    repo = Path("/workspaces/Logos_System").resolve()
    base = Path("/workspaces/Logos_System/_Reports/SYSTEM_AUDIT/05_naming_violations")
    r = scan(repo)
    write_json(base / "file_names.json", r["file_names"])
    write_json(base / "directory_names.json", r["directory_names"])
    write_json(base / "module_names.json", r["module_names"])
    print(base)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
