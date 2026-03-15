# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-021
# module_name:          ap_phase2_audit
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/ap_phase2_audit.py
# responsibility:       Utility module: ap phase2 audit
# runtime_stage:        utility
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

# ARCHON_PRIME MODULE
# Created by remediation stage AP-REM-002
# Purpose: Phase-2 pre-crawl audit snapshot generator

"""
ap_phase2_audit.py — Phase-2 Pre-Crawl Audit Regeneration

Read-only scan of the repository surface.  Produces
AP_SYSTEM_AUDIT/phase2_audit_snapshot.json.

Governance: NON-DELETION enforced. No file mutations permitted.
"""

import ast
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# ─── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
PLAN_PATH = (
    REPO_ROOT / "Designs_and_Guides/AP_REMEDIATION_SOURCES/phase1_remediation_plan.json"
)
OUTPUT_PATH = REPO_ROOT / "AP_SYSTEM_AUDIT/phase2_audit_snapshot.json"

EXCLUDE_DIRS: Set[str] = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".env",
    ".venv",
}

# ─── Subsystem → expected modules (from Phase-1 plan, by module_id prefix) ───
SUBSYSTEM_MAP = {
    "C1_REPO_MAPPING": ["M10", "M11", "M20"],
    "C2_IMPORT_ANALYSIS": ["M12", "M13", "M21", "M22", "M25"],
    "C3_GOVERNANCE": ["M14", "M15", "M63"],
    "C4_DEPENDENCY": ["M21", "M22"],
    "C5_RUNTIME": ["M16", "M23", "M24"],
    "C6_REPAIR": ["M70", "M71", "M72"],
    "C7_SIMULATION": ["M30", "M31", "M32"],
    "C8_PIPELINE": [
        "M38",
        "M39",
        "M50",
        "M51",
        "M60",
        "M61",
        "M62",
        "M64",
        "M65",
        "M80",
        "M90",
        "M91",
        "M92",
    ],
    "C9_AUDIT": [
        "M00",
        "M01",
        "M02",
        "M10",
        "M11",
        "M12",
        "M13",
        "M14",
        "M15",
        "M16",
        "M17",
    ],
    "C10_CONTROLLER": ["M95", "M96"],
    "C11_UTILITIES": [],  # non-spec / enhancement modules
}

# ─── Heuristic name → spec module mapping for non-spec classification ─────────
ANALOG_HINTS: Dict[str, str] = {
    "repo_mapper": "M10",
    "repo_scanner": "M10",
    "import_scanner": "M12",
    "header_validator": "M14",
    "governance_scanner": "M15",
    "governance_contract_audit": "M15",
    "governance_module_audit": "M15",
    "circular_dependency_audit": "M22",
    "dependency_graph": "M21",
    "dependency_normalizer": "M21",
    "header_injection_operator": "M50",
    "import_rewrite_operator": "M51",
    "crawl_engine": "M60",
    "pipeline_controller": "M96",
    "config_loader": "M01",
    "audit_controller": "M95",
    "analysis_controller": "M95",
    "crawler_controller": "M60",
    "repair_controller": "M71",
    "import_surface_audit": "M25",
    "facade_bypass_audit": "M25",
    "header_schema_audit": "M14",
    "runtime_entry_audit": "M23",
    "unused_import_audit": "M12",
}

LEGACY_HINTS = {"crawl_monitor"}  # duplicates of existing spec modules


def load_plan() -> Dict[str, Any]:
    with open(PLAN_PATH) as fh:
        return json.load(fh)


def collect_py_files(root: Path) -> List[Path]:
    """Walk repo, yield all .py files, respecting exclusions."""
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".py"):
                result.append(Path(dirpath) / fname)
    return result


def extract_imports(source: str, file_path: Path) -> List[Dict[str, str]]:
    """Parse a Python file and extract import statements."""
    imports = []
    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "type": "import",
                        "module": alias.name,
                        "name": alias.asname or alias.name,
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                imports.append(
                    {"type": "from_import", "module": mod, "name": alias.name}
                )
    return imports


def classify_non_spec(stem: str, rel_path: str, imports: List[Dict]) -> str:
    """Heuristic classification for non-spec modules."""
    if stem in LEGACY_HINTS:
        return "LEGACY_MODULE"
    if stem in ANALOG_HINTS:
        return "ANALOG_IMPLEMENTATION"
    # Path-based hints
    if any(k in stem for k in ANALOG_HINTS):
        return "ANALOG_IMPLEMENTATION"
    if "test" in stem or "placeholder" in stem:
        return "UNKNOWN_MODULE"
    if "_run_audit" in stem or stem.startswith("_"):
        return "UNKNOWN_MODULE"
    if "audit" in stem or "scanner" in stem or "inspector" in stem:
        return "ENHANCEMENT_MODULE"
    if "logger" in stem or "utils" in stem or "util" in stem:
        return "ENHANCEMENT_MODULE"
    if "operator" in stem or "simulator" in stem or "generator" in stem:
        return "ENHANCEMENT_MODULE"
    if "controller" in stem:
        return "ANALOG_IMPLEMENTATION"
    return "ENHANCEMENT_MODULE"


def guess_subsystem(rel_path: str) -> str:
    p = rel_path.lower()
    if "simulation" in p:
        return "C7_SIMULATION"
    if "repair" in p:
        return "C6_REPAIR"
    if "controller" in p:
        return "C10_CONTROLLER"
    if "import_analysis" in p:
        return "C2_IMPORT_ANALYSIS"
    if "runtime_analysis" in p:
        return "C5_RUNTIME"
    if "repo_mapping" in p:
        return "C1_REPO_MAPPING"
    if "normalization" in p:
        return "C9_AUDIT"
    if "audit_tools" in p:
        return "C9_AUDIT"
    if "crawler" in p:
        return "C8_PIPELINE"
    if "orchestration" in p:
        return "C10_CONTROLLER"
    if "governance" in p:
        return "C3_GOVERNANCE"
    if "AUDIT_SYSTEM" in rel_path:
        return "C9_AUDIT"
    if "utils" in p:
        return "C11_UTILITIES"
    return "C11_UTILITIES"


def build_surface_map(py_files: List[Path]) -> List[Dict[str, Any]]:
    surface = []
    for fpath in py_files:
        rel = fpath.relative_to(REPO_ROOT)
        try:
            source = fpath.read_text(encoding="utf-8", errors="replace")
            lines = source.count("\n") + 1
            size = fpath.stat().st_size
            imports = extract_imports(source, fpath)
        except Exception:
            lines, size, imports = 0, 0, []

        surface.append(
            {
                "module_name": fpath.name,
                "stem": fpath.stem,
                "absolute_path": str(fpath),
                "relative_path": str(rel),
                "directory": str(rel.parent),
                "imports": imports,
                "file_size": size,
                "line_count": lines,
                "subsystem_guess": guess_subsystem(str(rel)),
            }
        )
    return surface


def compare_targets(
    surface: List[Dict], targets: List[Dict]
) -> Tuple[List, List, List]:
    """Return (present, missing, misplaced) target classifications."""
    # Build lookup: filename → list of surface entries
    by_name: Dict[str, List[Dict]] = defaultdict(list)
    by_rel: Dict[str, Dict] = {}
    for entry in surface:
        by_name[entry["module_name"]].append(entry)
        by_rel[entry["relative_path"]] = entry

    present, missing, misplaced = [], [], []

    for t in targets:
        expected_rel = t["expected_path"]
        module_name = t["module_name"]

        if expected_rel in by_rel:
            present.append(
                {
                    "module_id": t["module_id"],
                    "module_name": module_name,
                    "expected_path": expected_rel,
                    "actual_path": expected_rel,
                    "subsystem": t["subsystem"],
                    "status": "SPEC_PRESENT",
                }
            )
        elif module_name in by_name:
            actual = by_name[module_name][0]
            misplaced.append(
                {
                    "module_id": t["module_id"],
                    "module_name": module_name,
                    "expected_path": expected_rel,
                    "actual_path": actual["relative_path"],
                    "subsystem": t["subsystem"],
                    "status": "MISPLACED_MODULE",
                }
            )
        else:
            missing.append(
                {
                    "module_id": t["module_id"],
                    "module_name": module_name,
                    "expected_path": expected_rel,
                    "subsystem": t["subsystem"],
                    "blocking": t.get("blocking", False),
                    "status": "SPEC_MISSING",
                }
            )

    return present, missing, misplaced


def discover_non_spec(surface: List[Dict], targets: List[Dict]) -> List[Dict]:
    """Return surface entries that are not target spec modules."""
    spec_names = {t["module_name"] for t in targets}
    spec_paths = {t["expected_path"] for t in targets}
    results = []
    for entry in surface:
        if entry["module_name"] in spec_names and entry["relative_path"] in spec_paths:
            continue  # exact spec module
        classification = classify_non_spec(
            entry["stem"], entry["relative_path"], entry["imports"]
        )
        analog_hint = ANALOG_HINTS.get(entry["stem"], None)
        results.append(
            {
                "module_name": entry["module_name"],
                "path": entry["relative_path"],
                "classification": classification,
                "possible_spec_mapping": analog_hint or "None",
                "subsystem_guess": entry["subsystem_guess"],
                "line_count": entry["line_count"],
                "file_size": entry["file_size"],
            }
        )
    return results


def build_dependency_graph(surface: List[Dict]) -> Dict[str, Any]:
    """Build a dependency edge list from import data."""
    # Map relative_path stem sets for resolution
    stem_to_rel: Dict[str, str] = {e["stem"]: e["relative_path"] for e in surface}
    edges = []
    for entry in surface:
        src = entry["relative_path"]
        for imp in entry["imports"]:
            # Try to resolve the target module from stem
            parts = imp["module"].split(".")
            for part in reversed(parts):
                if part in stem_to_rel:
                    tgt = stem_to_rel[part]
                    if tgt != src:
                        edges.append(
                            {
                                "source_module": src,
                                "target_module": tgt,
                                "edge_type": imp["type"],
                            }
                        )
                    break
    # Deduplicate
    seen = set()
    deduped = []
    for e in edges:
        key = (e["source_module"], e["target_module"], e["edge_type"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    return {
        "nodes": len(surface),
        "edges": len(deduped),
        "edge_list": deduped,
    }


def compute_subsystem_completion(
    present: List[Dict], missing: List[Dict], misplaced: List[Dict], targets: List[Dict]
) -> Dict[str, Any]:
    # Build set of present module_ids
    present_ids = {m["module_id"] for m in present}
    misplaced_ids = {m["module_id"] for m in misplaced}

    completion = {}
    for sys_id, module_ids in SUBSYSTEM_MAP.items():
        if not module_ids:
            completion[sys_id] = {
                "expected_modules": 0,
                "present_modules": 0,
                "misplaced_modules": 0,
                "missing_modules": 0,
                "completion_pct": 100.0,
                "note": "non-spec / utility subsystem",
            }
            continue

        # Deduplicate module IDs listed in multiple subsystems
        unique = list(dict.fromkeys(module_ids))
        exp = len(unique)
        pres = sum(1 for m in unique if m in present_ids)
        mispl = sum(1 for m in unique if m in misplaced_ids)
        miss = exp - pres - mispl
        completion[sys_id] = {
            "expected_modules": exp,
            "present_modules": pres,
            "misplaced_modules": mispl,
            "missing_modules": miss,
            "completion_pct": round(pres / exp * 100, 1) if exp else 100.0,
        }
    return completion


def main() -> None:
    # ── Step 1: Validate Phase-1 plan ─────────────────────────────────────────
    plan = load_plan()
    assert plan["phase"] == "PHASE_1_REMEDIATION", "HALT: phase mismatch"
    assert (
        plan["exit_condition"]["phase1_status"] == "COMPLETE"
    ), "HALT: phase1 not COMPLETE"
    targets: List[Dict] = plan["remediation_targets"]
    assert len(targets) == 35, f"HALT: expected 35 targets, got {len(targets)}"
    print(f"[STEP 1] Phase-1 plan validated. Targets: {len(targets)}")

    # ── Steps 3-4: Repository crawl & surface map ─────────────────────────────
    py_files = collect_py_files(REPO_ROOT)
    print(f"[STEP 3] Python files found: {len(py_files)}")
    surface = build_surface_map(py_files)
    print(f"[STEP 4] Surface map built: {len(surface)} entries")

    # ── Step 5: Target comparison ─────────────────────────────────────────────
    present, missing, misplaced = compare_targets(surface, targets)
    print(
        f"[STEP 5] Present: {len(present)}, "
        f"Missing: {len(missing)}, Misplaced: {len(misplaced)}"
    )

    # ── Step 6: Non-spec discovery ────────────────────────────────────────────
    non_spec = discover_non_spec(surface, targets)
    print(f"[STEP 6] Non-spec modules: {len(non_spec)}")

    # ── Step 7: Dependency graph ──────────────────────────────────────────────
    dep_graph = build_dependency_graph(surface)
    nodes = dep_graph["nodes"]
    edges = dep_graph["edges"]
    print(f"[STEP 7] Dependency graph: nodes={nodes}, edges={edges}")

    # ── Step 8: Subsystem completion ──────────────────────────────────────────
    sub_completion = compute_subsystem_completion(present, missing, misplaced, targets)
    print(
        f"[STEP 8] Subsystem completion computed for {len(sub_completion)} subsystems"
    )

    # ── Step 9: Write artifact ────────────────────────────────────────────────
    artifact = {
        "phase": "PHASE_2_AUDIT",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repo_root": str(REPO_ROOT),
        "source_plan": str(PLAN_PATH.relative_to(REPO_ROOT)),
        "scan_stats": {
            "total_python_files_scanned": len(py_files),
            "excluded_dirs": sorted(EXCLUDE_DIRS),
        },
        "targets_summary": {
            "total_targets": len(targets),
            "present": len(present),
            "missing": len(missing),
            "misplaced": len(misplaced),
        },
        "present_modules": present,
        "missing_modules": missing,
        "misplaced_modules": misplaced,
        "non_spec_modules": non_spec,
        "dependency_graph": {
            "nodes": dep_graph["nodes"],
            "edges": dep_graph["edges"],
            "edge_list": dep_graph["edge_list"],
        },
        "subsystem_completion": sub_completion,
        "governance": {
            "non_deletion_policy": True,
            "auto_removal_allowed": False,
            "mutation_policy": "NON-DELETION_ENFORCED",
            "scan_mode": "READ_ONLY",
        },
        "exit_condition": {
            "audit_complete": True,
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(artifact, fh, indent=2)
    print(f"[STEP 9] Artifact written: {OUTPUT_PATH}")

    # ── Step 10: Validate ─────────────────────────────────────────────────────
    with open(OUTPUT_PATH) as fh:
        verify = json.load(fh)
    assert verify["exit_condition"]["audit_complete"] is True
    assert verify["targets_summary"]["total_targets"] == 35
    print("[STEP 10] Post-write validation: PASS")
    print("== PHASE-2 AUDIT COMPLETE ==")


if __name__ == "__main__":
    main()
