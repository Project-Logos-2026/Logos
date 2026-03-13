#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-023
# module_name:          ap_artifact_collection_p1
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ap_artifact_collection_p1.py
# responsibility:       Inspection module: ap artifact collection p1
# runtime_stage:        audit
# execution_entry:      main
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
AP_ARTIFACT_COLLECTION_P1_R1_EXECUTION
Phase 1 Control Dataset Generator for ARCHON_PRIME

Copy-only operation. No repository files are modified.
"""

import datetime
import json
import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
OUTPUT_ROOT = REPO_ROOT / "ALL_ARTIFACTS_P1"

SCAN_EXCLUSIONS = {
    "ALL_ARTIFACTS_P1",
    ".git",
    "__pycache__",
    "node_modules",
}
SCAN_EXCLUSION_SUFFIXES = (".egg-info",)

# Tree exclusions: same as scan but ALL_ARTIFACTS_P1 is included in the snapshot
TREE_EXCLUSIONS = {
    ".git",
    "__pycache__",
    "node_modules",
}

# Directory structure to create
DIR_STRUCTURE = [
    "AP_RUNTIME/py",
    "AP_RUNTIME/json",
    "AP_RUNTIME/markdown",
    "AP_RUNTIME/yaml_yml",
    "AP_RUNTIME/other",
    "ENV_CONFIG/py",
    "ENV_CONFIG/json",
    "ENV_CONFIG/markdown",
    "ENV_CONFIG/yaml_yml",
    "ENV_CONFIG/other",
]

# ENV_CONFIG path prefixes (relative)
ENV_CONFIG_PATH_PREFIXES = (
    ".github/",
    ".vscode/",
    ".devcontainer/",
)

# ENV_CONFIG exact filenames
ENV_CONFIG_FILENAMES = {
    ".gitignore",
    ".dockerignore",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "Makefile",
    "Dockerfile",
    "CODEOWNERS",
    "devcontainer.json",
    "settings.json",
    "tasks.json",
    "launch.json",
    "extensions.json",
}

# AP_RUNTIME path prefixes (relative)
AP_RUNTIME_PATH_PREFIXES = (
    "tools/",
    "crawler/",
    "simulation/",
    "orchestration/",
    "AUDIT_SYSTEM/",
    "AUDIT_LOGS/",
    "AP_SYSTEM_AUDIT/",
    "AP_SYSTEM_CONFIG/",
    "configs/",
    "logs/",
    "utils/",
    "sources/",
    "Designs_and_Guides/",
)

# Extension → type_bucket mapping
EXT_TO_BUCKET = {
    ".py": "py",
    ".json": "json",
    ".md": "markdown",
    ".markdown": "markdown",
    ".yaml": "yaml_yml",
    ".yml": "yaml_yml",
}


# ─────────────────────────────────────────────────────────────────────────────
# STEP 0 — CREATE DIRECTORY STRUCTURE
# ─────────────────────────────────────────────────────────────────────────────


def step0_create_directories():
    print("\n[STEP 0] Creating directory structure...")
    for rel in DIR_STRUCTURE:
        target = OUTPUT_ROOT / rel
        target.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {target}")
    print("[STEP 0] Directory structure ready.")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — SCAN REPOSITORY
# ─────────────────────────────────────────────────────────────────────────────


def is_excluded(path: Path) -> bool:
    """Return True if this path should be excluded from scanning."""
    # Check each part of the path against exclusions
    for part in path.parts:
        if part in SCAN_EXCLUSIONS:
            return True
        for suffix in SCAN_EXCLUSION_SUFFIXES:
            if part.endswith(suffix):
                return True
    return False


def step1_scan_repository():
    print("\n[STEP 1] Scanning repository...")
    files = []
    for abs_path in REPO_ROOT.rglob("*"):
        if not abs_path.is_file():
            continue
        rel_path = abs_path.relative_to(REPO_ROOT)
        if is_excluded(rel_path):
            continue
        files.append(
            {
                "relative_path": str(rel_path),
                "absolute_path": str(abs_path),
                "filename": abs_path.name,
                "extension": abs_path.suffix.lower(),
                "size_bytes": abs_path.stat().st_size,
            }
        )
    print(f"[STEP 1] Found {len(files)} files.")
    return files


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — CLASSIFY FILES
# ─────────────────────────────────────────────────────────────────────────────


def classify_file(file_info: dict) -> tuple:
    """Returns (role, type_bucket, unclassified)."""
    rel = file_info["relative_path"].replace("\\", "/")
    fname = file_info["filename"]
    ext = file_info["extension"]

    # Determine role
    rel_lower = rel  # already normalized

    if fname in ENV_CONFIG_FILENAMES:
        role = "ENV_CONFIG"
        unclassified = False
    elif any(rel_lower.startswith(p) for p in ENV_CONFIG_PATH_PREFIXES):
        role = "ENV_CONFIG"
        unclassified = False
    elif any(rel_lower.startswith(p) for p in AP_RUNTIME_PATH_PREFIXES):
        role = "AP_RUNTIME"
        unclassified = False
    else:
        role = "AP_RUNTIME"
        unclassified = True

    # Determine type_bucket
    type_bucket = EXT_TO_BUCKET.get(ext, "other")

    return role, type_bucket, unclassified


def step2_classify(files: list) -> list:
    print("\n[STEP 2] Classifying files...")
    for f in files:
        role, type_bucket, unclassified = classify_file(f)
        f["role"] = role
        f["type_bucket"] = type_bucket
        f["unclassified"] = unclassified
    classified = sum(1 for f in files if not f["unclassified"])
    unclassified = sum(1 for f in files if f["unclassified"])
    print(f"[STEP 2] Classified: {classified}, Unclassified: {unclassified}")
    return files


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — HANDLE FILENAME COLLISIONS
# ─────────────────────────────────────────────────────────────────────────────


def path_to_safe_name(relative_path: str) -> str:
    """Convert relative path to a flat safe filename."""
    return (
        relative_path.replace("/", "_")
        .replace("\\", "_")
        .replace(".", "_", relative_path.count(".") - 1)
    )


def step3_handle_collisions(files: list) -> list:
    print("\n[STEP 3] Checking for filename collisions...")

    # Group by (role, type_bucket, filename)
    groups: dict = defaultdict(list)
    for f in files:
        key = (f["role"], f["type_bucket"], f["filename"])
        groups[key].append(f)

    collision_count = 0
    for _, group in groups.items():
        if len(group) > 1:
            collision_count += len(group)
            # Rename ALL using path-prefix rule
            for f in group:
                safe = path_to_safe_name(f["relative_path"])
                f["destination_filename"] = safe
                f["collision_renamed"] = True
        else:
            group[0]["destination_filename"] = group[0]["filename"]
            group[0]["collision_renamed"] = False

    print(f"[STEP 3] Files involved in collisions: {collision_count}")
    return files


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — COPY FILES
# ─────────────────────────────────────────────────────────────────────────────


def step4_copy_files(files: list, step_failures: list) -> list:
    print("\n[STEP 4] Copying files...")
    copied = 0
    failed = 0

    for f in files:
        dest_dir = OUTPUT_ROOT / f["role"] / f["type_bucket"]
        dest_path = dest_dir / f["destination_filename"]

        try:
            shutil.copy2(f["absolute_path"], dest_path)
            f["copy_status"] = "SUCCESS"
            f["destination_path"] = str(dest_path)
            copied += 1
        except Exception as e:
            f["copy_status"] = "FAILED"
            f["destination_path"] = str(dest_path)
            failed += 1
            step_failures.append(
                {
                    "step": 4,
                    "file": f["relative_path"],
                    "destination": str(dest_path),
                    "error": str(e),
                }
            )
            print(f"  [WARN] Copy failed: {f['relative_path']} → {e}")

    print(f"[STEP 4] Copied: {copied}, Failed: {failed}")
    return files


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — BUILD DIRECTORY TREE
# ─────────────────────────────────────────────────────────────────────────────


def build_tree(root: Path, exclusions: set, exclusion_suffixes: tuple) -> dict:
    """Recursively build a directory tree dict."""
    node: dict[str, Any] = {
        "_path": str(root.relative_to(REPO_ROOT)),
        "_files": [],
        "_subdirs": {},
    }

    try:
        entries = sorted(root.iterdir())
    except PermissionError:
        return node

    for entry in entries:
        rel = entry.relative_to(REPO_ROOT)
        # Check exclusions at top-level parts
        skip = False
        for part in rel.parts:
            if part in exclusions:
                skip = True
                break
            for suf in exclusion_suffixes:
                if part.endswith(suf):
                    skip = True
                    break
        if skip:
            continue

        if entry.is_dir():
            node["_subdirs"][entry.name] = build_tree(
                entry, exclusions, exclusion_suffixes
            )
        elif entry.is_file():
            node["_files"].append(entry.name)

    return node


def step5_build_directory_tree():
    print("\n[STEP 5] Building directory tree...")
    tree = build_tree(REPO_ROOT, TREE_EXCLUSIONS, SCAN_EXCLUSION_SUFFIXES)

    tree_output = {
        "schema_version": "1.0",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "repo_root": str(REPO_ROOT),
        "tree": tree,
    }

    out_path = OUTPUT_ROOT / "AP_DIRECTORY_TREE_CURRENT.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(tree_output, fh, indent=2)
    print(f"[STEP 5] Directory tree written to: {out_path}")
    return tree


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5.1 — DETECT EMPTY DIRECTORIES
# ─────────────────────────────────────────────────────────────────────────────


def collect_empty_dirs(node: dict, parent_path: str = "") -> list:
    """Return list of paths that are completely empty (no files, no non-empty children)."""
    empty = []
    path = node.get("_path", parent_path)

    child_empty = True
    for subdir_name, subdir_node in node.get("_subdirs", {}).items():
        sub_empties = collect_empty_dirs(subdir_node, path + "/" + subdir_name)
        empty.extend(sub_empties)
        # If child is in empty list it has no files
        if subdir_node.get("_files") or subdir_node.get("_subdirs"):
            # has something — check if that something was itself empty
            # A dir is empty only if ALL descendants are empty
            if not all(
                e == subdir_node.get("_path")
                or any(
                    e.startswith(str(subdir_node.get("_path", ""))) for e in sub_empties
                )
                for e in (
                    [subdir_node.get("_path")] if not subdir_node.get("_files") else []
                )
            ):
                child_empty = False
        else:
            pass  # totally empty subdir — fine

    if not node.get("_files") and child_empty and not node.get("_subdirs"):
        empty.append(path)

    return empty


def find_truly_empty_dirs(
    root: Path, exclusions: set, exclusion_suffixes: tuple
) -> list:
    """Walk filesystem to find directories with zero files in their entire subtree."""
    empty_dirs = []
    for dirpath, dirnames, _ in os.walk(root):
        # Filter excluded dirs in-place so os.walk skips them
        dirnames[:] = [
            d
            for d in dirnames
            if d not in exclusions
            and not any(d.endswith(s) for s in exclusion_suffixes)
        ]
        # Count all files recursively under this dir, applying the same exclusions
        total_files = 0
        for _, walk_dirs, walk_files in os.walk(dirpath):
            walk_dirs[:] = [
                d
                for d in walk_dirs
                if d not in exclusions
                and not any(d.endswith(s) for s in exclusion_suffixes)
            ]
            total_files += len(walk_files)
        if total_files == 0:
            rel = os.path.relpath(dirpath, root)
            empty_dirs.append(rel)

    return empty_dirs


def step51_detect_empty_directories():
    print("\n[STEP 5.1] Detecting empty directories...")
    empty = find_truly_empty_dirs(REPO_ROOT, SCAN_EXCLUSIONS, SCAN_EXCLUSION_SUFFIXES)

    out_path = OUTPUT_ROOT / "AP_EMPTY_DIRECTORIES.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump({"empty_directories": empty, "count": len(empty)}, fh, indent=2)
    print(f"[STEP 5.1] Empty directories detected: {len(empty)}")
    print(f"[STEP 5.1] Written to: {out_path}")
    return empty


# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — WRITE ARTIFACT INDEX
# ─────────────────────────────────────────────────────────────────────────────


def step6_write_artifact_index(files: list):
    print("\n[STEP 6] Writing artifact index...")
    index = []
    for f in files:
        index.append(
            {
                "original_relative_path": f["relative_path"],
                "original_absolute_path": f["absolute_path"],
                "role": f["role"],
                "type_bucket": f["type_bucket"],
                "destination_filename": f.get("destination_filename", f["filename"]),
                "destination_path": f.get("destination_path", ""),
                "collision_renamed": f.get("collision_renamed", False),
                "copy_status": f.get("copy_status", "NOT_ATTEMPTED"),
                "size_bytes": f["size_bytes"],
                "unclassified": f["unclassified"],
            }
        )

    out_path = OUTPUT_ROOT / "AP_ARTIFACT_INDEX.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2)
    print(f"[STEP 6] Artifact index written: {len(index)} entries → {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — WRITE FAILURE LOG
# ─────────────────────────────────────────────────────────────────────────────


def step7_write_failure_log(step_failures: list):
    print("\n[STEP 7] Writing failure log...")
    out_path = OUTPUT_ROOT / "step_failures.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(step_failures, fh, indent=2)
    print(f"[STEP 7] Failures recorded: {len(step_failures)} → {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — TERMINAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────


def step8_terminal_summary(files: list, step_failures: list):
    total = len(files)
    copied = sum(1 for f in files if f.get("copy_status") == "SUCCESS")
    failed = sum(1 for f in files if f.get("copy_status") == "FAILED")
    renamed = sum(1 for f in files if f.get("collision_renamed"))
    unclassified = sum(1 for f in files if f.get("unclassified"))

    counts = defaultdict(int)
    for f in files:
        counts[(f["role"], f["type_bucket"])] += 1

    print("\n" + "=" * 60)
    print("  PHASE 1 CONTROL DATASET — COLLECTION SUMMARY")
    print("=" * 60)
    print(f"  Total files scanned   : {total}")
    print(f"  Total files copied    : {copied}")
    print(f"  Files failed          : {failed}")
    print(f"  Files collision-renamed: {renamed}")
    print(f"  Files unclassified    : {unclassified}")
    print()
    print("  AP_RUNTIME breakdown:")
    print(f"    py        : {counts[('AP_RUNTIME', 'py')]}")
    print(f"    json      : {counts[('AP_RUNTIME', 'json')]}")
    print(f"    markdown  : {counts[('AP_RUNTIME', 'markdown')]}")
    print(f"    yaml_yml  : {counts[('AP_RUNTIME', 'yaml_yml')]}")
    print(f"    other     : {counts[('AP_RUNTIME', 'other')]}")
    print()
    print("  ENV_CONFIG breakdown:")
    print(f"    py        : {counts[('ENV_CONFIG', 'py')]}")
    print(f"    json      : {counts[('ENV_CONFIG', 'json')]}")
    print(f"    markdown  : {counts[('ENV_CONFIG', 'markdown')]}")
    print(f"    yaml_yml  : {counts[('ENV_CONFIG', 'yaml_yml')]}")
    print(f"    other     : {counts[('ENV_CONFIG', 'other')]}")
    print("=" * 60)

    if failed == 0:
        print("  EXIT GATE: SUCCESS")
    else:
        print("  EXIT GATE: PARTIAL (see step_failures.json)")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────────────────────────────────────


def validate_outputs(files: list):
    print("\n[VALIDATION] Checking output artifacts...")
    required_dirs = [
        OUTPUT_ROOT / "AP_RUNTIME",
        OUTPUT_ROOT / "ENV_CONFIG",
    ]
    required_files = [
        OUTPUT_ROOT / "AP_DIRECTORY_TREE_CURRENT.json",
        OUTPUT_ROOT / "AP_ARTIFACT_INDEX.json",
        OUTPUT_ROOT / "AP_EMPTY_DIRECTORIES.json",
        OUTPUT_ROOT / "step_failures.json",
    ]

    all_ok = True
    for d in required_dirs:
        if d.is_dir():
            print(f"  [OK] Directory exists: {d}")
        else:
            print(f"  [FAIL] Directory missing: {d}")
            all_ok = False

    for fp in required_files:
        if fp.is_file():
            try:
                with open(fp, "r", encoding="utf-8") as fh:
                    _ = json.load(fh)
                print(f"  [OK] Valid JSON: {fp.name}")
            except json.JSONDecodeError as e:
                print(f"  [FAIL] Invalid JSON: {fp.name} → {e}")
                all_ok = False
        else:
            print(f"  [FAIL] File missing: {fp.name}")
            all_ok = False

    # Verify artifact index entry count
    index_path = OUTPUT_ROOT / "AP_ARTIFACT_INDEX.json"
    if index_path.is_file():
        with open(index_path, "r", encoding="utf-8") as fh:
            index_data = json.load(fh)
        if len(index_data) == len(files):
            print(
                f"  [OK] AP_ARTIFACT_INDEX.json has {len(index_data)} entries (matches scan count)."
            )
        else:
            print(
                f"  [WARN] Index has {len(index_data)} entries but scan found {len(files)} files."
            )

    if all_ok:
        print("[VALIDATION] PASSED — all required artifacts present and valid.")
    else:
        print("[VALIDATION] FAILED — see above for details.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────


def main():
    print("=" * 60)
    print("  AP_ARTIFACT_COLLECTION_P1_R1_EXECUTION")
    print("  Phase 1 Control Dataset Generator")
    print("=" * 60)

    step_failures = []

    # Step 0: Create directory structure
    step0_create_directories()

    # Step 1: Scan repository
    files = step1_scan_repository()

    # Step 2: Classify files
    files = step2_classify(files)

    # Step 3: Handle collisions
    files = step3_handle_collisions(files)

    # Step 4: Copy files
    files = step4_copy_files(files, step_failures)

    # Step 5: Build directory tree
    _tree = step5_build_directory_tree()

    # Step 5.1: Detect empty directories
    step51_detect_empty_directories()

    # Step 6: Write artifact index
    step6_write_artifact_index(files)

    # Step 7: Write failure log
    step7_write_failure_log(step_failures)

    # Step 8: Print terminal summary
    step8_terminal_summary(files, step_failures)

    # Validate outputs
    validate_outputs(files)


if __name__ == "__main__":
    main()
