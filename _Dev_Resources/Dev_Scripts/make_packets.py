#!/usr/bin/env python3
"""
End-to-End packet bootstrapper (sweep mode).

Creates a new subdirectory under END_TO_END_PACKET for every eligible source file
in Logos_System, matching the batch collector ignore rules. Skips files already
materialized. No packet JSON is written; only directories are created.

Eligibility:
- Must be a file under /Logos_System (the monorepo root directory).
- Must not reside in deny-list directories used by batch_collector.py:
  * System_Entry_Point/Runtime_Compiler
  * System_Stack/Advanced_Reasoning_Protocol/iel_domains
  * System_Stack/Advanced_Reasoning_Protocol/mathematical_foundations/math_categories
- Must not have blocked extensions (Coq/OCaml/build artifacts from batch collector).
- Skips README-like files (case-insensitive) and non-.py files.

Outputs:
- Creates END_TO_END_PACKET/<sanitized-name>/ if it does not already exist.
- Writes a manifest summarizing creations.

Run from repo root:
    python3 _Dev_Resources/Dev_Scripts/make_packets.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

REPO = Path("/workspaces/Logos_System").resolve()
SRC_ROOT = REPO / "Logos_System"
PACKET_ROOT = REPO / "_Dev_Resources/AUTOMATION_ORCHESTRATOR/END_TO_END_PACKET"
MANIFEST_PATH = REPO / "_Reports/Batch_Manifests/packet_bootstrap_manifest.json"

DENY_DIRS = {
    SRC_ROOT / "System_Entry_Point" / "Runtime_Compiler",
    SRC_ROOT / "System_Stack" / "Advanced_Reasoning_Protocol" / "iel_domains",
    SRC_ROOT / "System_Stack" / "Advanced_Reasoning_Protocol" / "mathematical_foundations" / "math_categories",
}

BLOCKED_EXTS = {
    ".v", ".vh", ".vo", ".glob", ".aux", ".cmx", ".cmxa", ".cmo", ".cmi",
    ".ml", ".mli", ".mlpack", ".mld", ".native", ".byte",
}

README_NAMES = {"readme", "readme.md", "readme.rst", "readme.txt"}


def is_excluded(path: Path) -> bool:
    if any(path.is_relative_to(deny) for deny in DENY_DIRS):
        return True
    if path.suffix in BLOCKED_EXTS:
        return True
    name_lower = path.name.lower()
    if name_lower in README_NAMES:
        return True
    return False


def iter_python_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.py"):
        if not p.is_file():
            continue
        if is_excluded(p):
            continue
        yield p


def sanitize_relpath(rel: Path) -> str:
    # Replace path separators with double underscores to keep uniqueness and avoid nesting.
    return "__".join(rel.parts)


def ensure_unique_dir(base: Path, name: str) -> Path:
    candidate = base / name
    if not candidate.exists():
        return candidate
    # If collision, append hash suffix.
    h = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
    candidate = base / f"{name}__{h}"
    return candidate


def main() -> int:
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    created = []
    skipped_existing = []

    for path in iter_python_files(SRC_ROOT):
        rel = path.relative_to(SRC_ROOT)
        packet_dir_name = sanitize_relpath(rel)
        target_dir = ensure_unique_dir(PACKET_ROOT, packet_dir_name)
        if target_dir.exists():
            skipped_existing.append(str(target_dir))
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        created.append({"source": str(path), "packet_dir": str(target_dir)})

    manifest = {
        "created_count": len(created),
        "skipped_existing_count": len(skipped_existing),
        "created": created,
        "skipped_existing": skipped_existing,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"created": len(created), "skipped_existing": len(skipped_existing)}, indent=2))
    print(f"Manifest: {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
