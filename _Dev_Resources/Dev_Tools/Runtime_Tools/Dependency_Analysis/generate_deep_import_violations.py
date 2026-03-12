"""
generate_deep_import_violations.py
===================================
Canonical Import Facade — Phase 3: Deep Import Violation Dataset

Authority:
  - Canonical_Import_Facade_Integration_Plan.md (Phase 3)
  - Canonical_Import_Facade_Blueprint.md §5.5 (Forbidden Prefix Registry)

Output:
  /workspaces/Logos/BLUEPRINTS/Canonical_Import_Facade/Deep_Import_Violations.json

Exit codes:
  0  — scan completed and JSON written (even when violations exist)
  1  — fatal: cannot complete scan or cannot write JSON
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: generate_deep_import_violations.py
tool_category: Dependency_Analysis
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python generate_deep_import_violations.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import json
import os
import sys
from datetime import timezone, datetime
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


# ---------------------------------------------------------------------------
# Configuration (matches Blueprint §5.5 exactly)
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FORBIDDEN_PREFIXES = [
    "LOGOS_SYSTEM.RUNTIME_CORES",
    "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE",
    "LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT",
    "LOGOS_SYSTEM.Runtime_Spine",
    "LOGOS_SYSTEM.STARTUP",
]

ALLOWLISTED_PATH_SEGMENTS = ["Canonical_Import_Facade", "Import_Facade"]

EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "site-packages"}

OUTPUT_PATH = os.path.join(
    REPO_ROOT,
    "BLUEPRINTS",
    "Canonical_Import_Facade",
    "Deep_Import_Violations.json",
)

# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def is_import_line(stripped: str) -> bool:
    return stripped.startswith("import ") or stripped.startswith("from ")


def path_is_allowlisted(rel_path: str) -> bool:
    parts = rel_path.replace("\\", "/").split("/")
    return any(seg in ALLOWLISTED_PATH_SEGMENTS for seg in parts)


def scan() -> tuple[int, list[dict]]:
    """Walk REPO_ROOT, scan every .py file, return (files_scanned, violations)."""
    files_scanned = 0
    violations: list[dict] = []

    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        # Prune excluded directories in-place so os.walk won't descend into them
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        for fname in filenames:
            if not fname.endswith(".py"):
                continue

            abs_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(abs_path, REPO_ROOT)

            if path_is_allowlisted(rel_path):
                continue

            files_scanned += 1

            try:
                with open(abs_path, encoding="utf-8", errors="replace") as fh:
                    for lineno, raw_line in enumerate(fh, start=1):
                        stripped = raw_line.strip()
                        if not is_import_line(stripped):
                            continue
                        for prefix in FORBIDDEN_PREFIXES:
                            if prefix in stripped:
                                violations.append(
                                    {
                                        "file": rel_path.replace("\\", "/"),
                                        "line": lineno,
                                        "content": stripped,
                                        "forbidden_prefix": prefix,
                                    }
                                )
            except OSError as exc:
                print(f"WARNING: could not read {rel_path}: {exc}", file=sys.stderr)

    # Stable sort: file ↑, line ↑, forbidden_prefix ↑
    violations.sort(key=lambda v: (v["file"], v["line"], v["forbidden_prefix"]))
    return files_scanned, violations


def main() -> None:
    generated_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        files_scanned, violations = scan()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: scan failed — {exc}", file=sys.stderr)
        sys.exit(1)

    report = {
        "generated_utc": generated_utc,
        "forbidden_prefixes": FORBIDDEN_PREFIXES,
        "allowlisted_path_segments": ALLOWLISTED_PATH_SEGMENTS,
        "excluded_dirs": sorted(EXCLUDED_DIRS),
        "total_python_files_scanned": files_scanned,
        "total_violations": len(violations),
        "violations": violations,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        print(f"FATAL: could not write output — {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"total_python_files_scanned : {files_scanned}")
    print(f"total_violations           : {len(violations)}")
    print(f"output_path                : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
