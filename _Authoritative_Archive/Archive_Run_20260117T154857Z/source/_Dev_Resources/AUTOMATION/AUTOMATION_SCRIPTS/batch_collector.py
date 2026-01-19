#!/usr/bin/env python3
"""
Batch Collector

Scans /Logos_System/
Includes only .py files
Excludes:
- Runtime_Compiler
- iel_domains
- math_categories
- Any file with Coq-related extensions
Moves selected files into LEGACY_SCRIPTS_TO_EXAMINE
Emits manifest and stops
"""

import os
from pathlib import Path
import shutil
from datetime import datetime, timezone
import json
import hashlib

CONTRACT_FILE = Path("/workspaces/Logos_System/_Dev_Resources/AUTOMATION_ORCHESTRATOR/AUTOMATION_WORKFLOW_CONTRACT.md")


def _contract_text() -> str:
    return CONTRACT_FILE.read_text(encoding="utf-8")


def _contract_hash() -> str:
    b = _contract_text().encode("utf-8")
    return "sha256:" + hashlib.sha256(b).hexdigest()


def _print_contract_banner() -> None:
    text = _contract_text()
    h = _contract_hash()
    print("=" * 78)
    print("AUTOMATION WORKFLOW CONTRACT (RE-LOADED)")
    print(f"CONTRACT_HASH: {h}")
    print("-" * 78)
    lines = text.splitlines()
    head = lines[:120]
    for ln in head:
        print(ln)
    if len(lines) > 120:
        print("... (contract truncated in output; file is authoritative on disk) ...")
    print("=" * 78)

REPO = Path("/workspaces/Logos_System").resolve()
SRC_ROOT = REPO / "Logos_System"
TARGET = REPO / "_Dev_Resources/LEGACY_SCRIPTS_TO_EXAMINE"
MANIFEST_DIR = REPO / "_Reports/Batch_Manifests"
BATCH_SIZE = 10

DENY_DIRS = {
    SRC_ROOT / "System_Entry_Point" / "Runtime_Compiler",
    SRC_ROOT / "System_Stack" / "Advanced_Reasoning_Protocol" / "iel_domains",
    SRC_ROOT / "System_Stack" / "Advanced_Reasoning_Protocol" / "mathematical_foundations" / "math_categories",
}

BLOCKED_EXTS = {
    ".v", ".vh", ".vo", ".glob", ".aux", ".cmx", ".cmxa", ".cmo", ".cmi",
    ".ml", ".mli", ".mlpack", ".mld", ".native", ".byte"
}

def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

def is_excluded(path: Path) -> bool:
    if any(path.is_relative_to(deny) for deny in DENY_DIRS):
        return True
    if path.suffix in BLOCKED_EXTS:
        return True
    return False

def find_eligible_py_files(root: Path) -> list[Path]:
    all_py = []
    for path in root.rglob("*.py"):
        if not path.is_file():
            continue
        if is_excluded(path):
            continue
        all_py.append(path)
    return all_py

def already_collected(path: Path) -> bool:
    return (TARGET / path.name).exists()

def generate_manifest(batch: list[Path], dests: list[Path]) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    manifest = {
        "batch_id": f"BATCH_{ts}",
        "timestamp": ts,
        "contract_hash": _contract_hash(),
        "count": len(batch),
        "files": [
            {
                "original": str(src),
                "destination": str(dst),
                "hash": hash_file(dst)
            } for src, dst in zip(batch, dests)
        ]
    }
    out_path = MANIFEST_DIR / f"batch_manifest_{ts}.json"
    out_path.write_text(json.dumps(manifest, indent=2))
    return out_path

def main():
    _print_contract_banner()
    eligible = find_eligible_py_files(SRC_ROOT)
    batch = []
    for path in eligible:
        if already_collected(path):
            continue
        batch.append(path)
        if len(batch) >= BATCH_SIZE:
            break
    if not batch:
        print("No eligible files found.")
        return

    moved_paths = []
    for path in batch:
        dst = TARGET / path.name
        shutil.copy2(path, dst)
        moved_paths.append(dst)

    manifest_path = generate_manifest(batch, moved_paths)
    print(f"Collected {len(batch)} files.")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
