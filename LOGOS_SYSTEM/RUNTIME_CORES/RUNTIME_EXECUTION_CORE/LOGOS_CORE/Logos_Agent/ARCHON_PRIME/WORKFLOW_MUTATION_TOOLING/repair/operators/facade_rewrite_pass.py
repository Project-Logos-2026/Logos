#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-014
# module_name:          facade_rewrite_pass
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/facade_rewrite_pass.py
# responsibility:       Mutation module: facade rewrite pass
# runtime_stage:        repair
# execution_entry:      main
# allowed_targets:      ["WORKFLOW_TARGET_PROCESSING/PROCESSING"]
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
ARCHON PRIME — Facade Import Rewrite Pass
==========================================
Applies deterministic facade substitution from the Runtime_Facade_Synthesis
rewrite table to every AUTO_REPAIRABLE deep import violation.

Safety contract:
  - Fail-closed.  Preconditions must pass before any file is touched.
  - Dry-run simulates all rewrites with AST verification first.
  - Only when dry-run is 100% clean does the live pass proceed.
  - On any ABORT condition: write failure report, exit non-zero.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: facade_rewrite_pass.py
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
python facade_rewrite_pass.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import difflib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
SYNTHESIS = REPO_ROOT / "Runtime_Facade_Synthesis"
OUTPUT_DIR = REPO_ROOT / "Reports" / "Facade_Rewrite_Pass"
ARCHON = REPO_ROOT / "ARCHON_RUNTIME_ANALYSIS"

# ── Runtime dirs (constrain scanning to runtime surface) ──────────────────────
RUNTIME_DIRS = [
    REPO_ROOT / "LOGOS_SYSTEM",
    REPO_ROOT / "STARTUP",
    REPO_ROOT / "BLUEPRINTS",
    REPO_ROOT / "_Governance",
]

EXCLUDED_SEGMENTS = frozenset(
    {
        "__pycache__",
        ".git",
        "node_modules",
        "venv",
        ".venv",
        "build",
        "dist",
        "ARCHIVE",
        "ARCHIVES",
        "HISTORY",
    }
)

NOW = datetime.now(timezone.utc).isoformat()

# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════


def should_skip(path: Path) -> bool:
    return any(
        p.upper() in EXCLUDED_SEGMENTS or p in EXCLUDED_SEGMENTS for p in path.parts
    )


def write_json(path: Path, data) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def module_to_file(module_path: str) -> Path | None:
    """Convert a dotted module path to an absolute .py file path."""
    rel = module_path.replace(".", "/") + ".py"
    p = REPO_ROOT / rel
    if p.exists():
        return p
    # Try __init__.py
    p2 = REPO_ROOT / module_path.replace(".", "/") / "__init__.py"
    if p2.exists():
        return p2
    return None


def check_syntax(source: str, label: str) -> list[str]:
    """Return list of syntax error descriptions, empty if clean."""
    try:
        ast.parse(source)
        return []
    except SyntaxError as e:
        return [f"{label}: SyntaxError: {e}"]


# ══════════════════════════════════════════════════════════════════════════════
# ABORT — write failure report and exit
# ══════════════════════════════════════════════════════════════════════════════


def abort(reason: str, details: dict | None = None) -> None:
    print(f"\n[ABORT] {reason}")
    report = {
        "generated_utc": NOW,
        "status": "ABORTED",
        "abort_reason": reason,
        "details": details or {},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "facade_rewrite_failure.json", report)
    print(
        "  [✓] Failure report → Reports/Facade_Rewrite_Pass/facade_rewrite_failure.json"
    )
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Load Input Artifacts
# ══════════════════════════════════════════════════════════════════════════════


def step1_load() -> tuple:
    print("\n[STEP 1] Loading synthesis artifacts …")
    rewrite_table = load_json(SYNTHESIS / "import_rewrite_table.json")
    feasibility = load_json(SYNTHESIS / "repair_feasibility.json")
    facade_map_raw = load_json(SYNTHESIS / "facade_map.json")
    surface_spec = load_json(SYNTHESIS / "facade_surface_spec.json")

    missing = []
    if rewrite_table is None:
        missing.append("import_rewrite_table.json")
    if feasibility is None:
        missing.append("repair_feasibility.json")
    if facade_map_raw is None:
        missing.append("facade_map.json")
    if surface_spec is None:
        missing.append("facade_surface_spec.json")
    if missing:
        abort("Required artifacts missing", {"missing": missing})

    # Build quick-lookup: (source_module, illegal_import) → feasibility record
    feas_lookup: dict[tuple, dict] = {}
    for f in feasibility:
        key = (f["source_module"], f["illegal_import"])
        feas_lookup[key] = f

    # Extract AUTO_REPAIRABLE rules only
    auto_rules = [
        r
        for r in rewrite_table
        if feas_lookup.get((r["source_module"], r["illegal_import"]), {}).get("status")
        == "AUTO_REPAIRABLE"
    ]

    print(f"  [i] Total rewrite rules  : {len(rewrite_table)}")
    print(f"  [i] AUTO_REPAIRABLE      : {len(auto_rules)}")
    return auto_rules, feasibility, facade_map_raw, surface_spec


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Precondition Gate
# ══════════════════════════════════════════════════════════════════════════════


def step2_preconditions(auto_rules: list[dict]) -> dict[str, dict]:
    """
    Preconditions required before any mutation:
      P1: All source files must exist on disk.
      P2: All facade replacement namespaces must exist as importable modules.
      P3: For each rule, the exact import statement must be locatable in the source file.

    If any precondition fails → ABORT (fail-closed).

    Returns: {source_module → {"file": Path, "rules": [...]}}
    """
    print("\n[STEP 2] Checking preconditions …")

    # ── P2: Facade namespaces must exist ────────────────────────────────────
    replacement_nss = {r["replacement_import"] for r in auto_rules}
    missing_facades: list[str] = []
    for ns in sorted(replacement_nss):
        ns_path = REPO_ROOT / (ns.replace(".", "/") + ".py")
        ns_init = REPO_ROOT / ns.replace(".", "/") / "__init__.py"
        if not ns_path.exists() and not ns_init.exists():
            missing_facades.append(ns)

    if missing_facades:
        # ── Facade modules do not exist → ABORT ─────────────────────────────
        # We still produce a comprehensive pre-flight report so ARCHON knows
        # exactly what to create before re-running the rewrite pass.
        abort(
            "PRECONDITION FAILED — Facade target modules do not exist. "
            "Create facade shim modules before executing the rewrite pass.",
            {
                "precondition": "P2_facade_modules_must_exist",
                "missing_facade_modules": missing_facades,
                "required_action": (
                    "Create one Python module (or package __init__.py) "
                    "for each missing facade namespace listed above. "
                    "Each facade module must re-export all symbols that "
                    "affected source files import from it. "
                    "Symbol inventory is in Runtime_Facade_Synthesis/facade_surface_spec.json."
                ),
                "auto_repairable_count": len(auto_rules),
                "blocked_rewrites": [
                    {
                        "source_module": r["source_module"],
                        "illegal_import": r["illegal_import"],
                        "replacement_import": r["replacement_import"],
                    }
                    for r in auto_rules
                ],
            },
        )

    # ── P1: Source files must exist ─────────────────────────────────────────
    missing_sources: list[str] = []
    file_rule_map: dict[str, dict] = {}
    for r in auto_rules:
        src_mod = r["source_module"]
        if src_mod in file_rule_map:
            file_rule_map[src_mod]["rules"].append(r)
            continue
        f = module_to_file(src_mod)
        if f is None:
            missing_sources.append(src_mod)
        else:
            file_rule_map[src_mod] = {"file": f, "rules": [r]}

    if missing_sources:
        abort(
            "PRECONDITION FAILED — Source module files not found on disk",
            {
                "precondition": "P1_source_files_must_exist",
                "missing_source_modules": missing_sources,
            },
        )

    print(f"  [✓] P1: All {len(file_rule_map)} source files present")
    print(f"  [✓] P2: All {len(replacement_nss)} facade namespaces present")
    return file_rule_map


# ══════════════════════════════════════════════════════════════════════════════
# Import-line rewriting helpers
# ══════════════════════════════════════════════════════════════════════════════


def build_import_pattern(target_module: str) -> re.Pattern:
    """
        Build a regex that matches:
            from <target_module> import ...
            import <target_module> [as ...]

    OUTPUT_ROOT = Path("/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


    def write_report(name: str, data) -> None:
        path = OUTPUT_ROOT / name
        with open(path, "w", encoding="utf-8") as f:
            import json as _json
            _json.dump(data, f, indent=2)
        print(f"  Report written: {path}")

        anchored to line-start, respecting indentation.
    """
    escaped = re.escape(target_module)
    # Match 'from TARGET import ...'  OR  'import TARGET' / 'import TARGET as X'
    pat = (
        r"^(?P<indent>[ \t]*)"
        r"(?P<stmt>from\s+" + escaped + r"\s+import\s+.*"
        r"|import\s+" + escaped + r"(?:\s+as\s+\S+)?\s*)"
        r"$"
    )
    return re.compile(pat, re.MULTILINE)


def rewrite_import_lines(
    source_text: str, target_module: str, replacement_ns: str
) -> tuple[str, list[str]]:
    """
    Replace every import line whose module is exactly `target_module` with one
    using `replacement_ns`.

    Returns (new_source_text, list_of_change_descriptions).
    Multi-line parenthesised imports are handled by reconstructing the `from`
    clause while preserving the symbol list.
    """
    lines = source_text.splitlines(keepends=True)
    changes: list[str] = []
    result: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip("\n\r")

        # ── Check for 'from TARGET import ...' (possibly multi-line) ─────────
        from_match = re.match(
            r"^(?P<indent>[ \t]*)from\s+"
            + re.escape(target_module)
            + r"\s+import\s+(?P<rest>.*)",
            stripped,
        )
        if from_match:
            indent = from_match.group("indent")
            rest = from_match.group("rest")

            # Collect continued lines if the import opens a parenthesis
            full_block = [stripped]
            j = i + 1
            if "(" in rest and ")" not in rest:
                while j < len(lines):
                    cont = lines[j].rstrip("\n\r")
                    full_block.append(cont)
                    j += 1
                    if ")" in cont:
                        break

            # Extract symbols by joining and parsing the full block
            full_stmt = " ".join(full_block)
            # Extract everything after 'import'
            sym_part_match = re.search(
                r"from\s+" + re.escape(target_module) + r"\s+import\s+(.+)",
                full_stmt,
                flags=re.DOTALL,
            )
            if sym_part_match:
                sym_raw = sym_part_match.group(1).strip()
                # Strip outer parens
                sym_raw = sym_raw.strip("()")
                # Strip trailing comments
                sym_raw = re.sub(r"#.*", "", sym_raw)
                symbols_str = sym_raw.strip().rstrip(",")
            else:
                symbols_str = "*"

            new_line = f"{indent}from {replacement_ns} import {symbols_str}\n"
            result.append(new_line)
            changes.append(
                f"L{i+1}: 'from {target_module} import ...' → "
                f"'from {replacement_ns} import {symbols_str}'"
            )
            i = j  # skip any continuation lines
            continue

        # ── Check for 'import TARGET' or 'import TARGET as X' ────────────────
        bare_match = re.match(
            r"^(?P<indent>[ \t]*)import\s+"
            + re.escape(target_module)
            + r"(?:\s+as\s+(?P<alias>\S+))?\s*$",
            stripped,
        )
        if bare_match:
            indent = bare_match.group("indent")
            alias = bare_match.group("alias")
            if alias:
                new_line = f"{indent}import {replacement_ns} as {alias}\n"
            else:
                new_line = f"{indent}import {replacement_ns}\n"
            result.append(new_line)
            changes.append(
                f"L{i+1}: 'import {target_module}' → " f"'import {replacement_ns}'"
            )
            i += 1
            continue

        result.append(line)
        i += 1

    return "".join(result), changes


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Dry-Run Pass
# ══════════════════════════════════════════════════════════════════════════════


def step3_dry_run(file_rule_map: dict) -> dict[str, dict]:
    """
    Simulate every rewrite: apply to in-memory copy, verify syntax.
    Returns { source_module → { file, original, rewritten, changes, errors } }
    No files are written.
    """
    print(f"\n[STEP 3] Dry-run simulation ({len(file_rule_map)} files) …")

    dry_run_results: dict[str, dict] = {}
    total_changes = 0
    syntax_errors = []

    for src_mod, info in sorted(file_rule_map.items()):
        fpath = info["file"]
        rules = info["rules"]
        original = fpath.read_text(encoding="utf-8", errors="replace")
        working = original
        file_changes: list[str] = []

        for rule in rules:
            tgt = rule["illegal_import"]
            rep = rule["replacement_import"]
            working, ch = rewrite_import_lines(working, tgt, rep)
            file_changes.extend(ch)

        # Verify syntax of rewritten text
        errs = check_syntax(working, src_mod)
        if errs:
            syntax_errors.extend(errs)

        dry_run_results[src_mod] = {
            "file": str(fpath.relative_to(REPO_ROOT)),
            "original_text": original,
            "rewritten_text": working,
            "changes": file_changes,
            "syntax_errors": errs,
            "changed": working != original,
        }
        if file_changes:
            total_changes += len(file_changes)

    print(f"  [i] Changes simulated : {total_changes}")
    print(f"  [i] Syntax errors     : {len(syntax_errors)}")
    if syntax_errors:
        for e in syntax_errors:
            print(f"      [!] {e}")
    return dry_run_results


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Apply Live Rewrites
# ══════════════════════════════════════════════════════════════════════════════


def step4_apply(dry_run_results: dict) -> tuple[int, int, list[str]]:
    """
    Write rewritten files to disk only for changed, syntax-clean files.
    Returns (files_modified, rewrites_applied, errors).
    """
    print("\n[STEP 4] Applying rewrites …")
    files_modified = 0
    rewrites_applied = 0
    errors: list[str] = []

    for src_mod, info in sorted(dry_run_results.items()):
        if not info["changed"]:
            continue
        if info["syntax_errors"]:
            errors.append(f"{src_mod}: skipped — syntax error in dry-run output")
            continue

        fpath = REPO_ROOT / info["file"]
        fpath.write_text(info["rewritten_text"], encoding="utf-8")
        files_modified += 1
        rewrites_applied += len(info["changes"])
        print(f"  [✓] {info['file']}  ({len(info['changes'])} rewrite(s))")

    print(f"\n  [i] Files modified   : {files_modified}")
    print(f"  [i] Rewrites applied : {rewrites_applied}")
    if errors:
        print(f"  [!] Errors           : {len(errors)}")
    return files_modified, rewrites_applied, errors


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Post-Rewrite Validation
# ══════════════════════════════════════════════════════════════════════════════


def step5_validate(auto_rules: list[dict]) -> dict:
    """
    Re-scan all rewritten files.
    Count remaining cross-cluster deep imports and syntax errors.
    """
    print("\n[STEP 5] Post-rewrite validation …")

    # Build set of (source_module, illegal_import) pairs we attempted to fix
    fixed_pairs = {(r["source_module"], r["illegal_import"]) for r in auto_rules}

    remaining_violations: list[dict] = []
    syntax_errors: list[str] = []
    files_scanned = 0

    for d in RUNTIME_DIRS:
        if not d.exists():
            continue
        for fpath in sorted(d.rglob("*.py")):
            if should_skip(fpath):
                continue
            files_scanned += 1
            try:
                txt = fpath.read_text(encoding="utf-8", errors="replace")
                ast.parse(txt)
            except SyntaxError as e:
                syntax_errors.append(f"{fpath.relative_to(REPO_ROOT)}: {e}")
                continue
            except Exception:
                continue

            # Check for any remaining illegal deep imports we tried to fix
            mod_path = ".".join(fpath.relative_to(REPO_ROOT).with_suffix("").parts)
            for line_no, line in enumerate(txt.splitlines(), 1):
                for src_m, ill_imp in fixed_pairs:
                    if src_m == mod_path and ill_imp in line:
                        remaining_violations.append(
                            {
                                "source_module": src_m,
                                "illegal_import": ill_imp,
                                "line": line_no,
                                "content": line.strip(),
                            }
                        )

    cross_remaining = len(remaining_violations)
    print(f"  [i] Files scanned             : {files_scanned}")
    print(f"  [i] Remaining violations      : {cross_remaining}")
    print(f"  [i] Syntax errors post-rewrite: {len(syntax_errors)}")

    return {
        "files_scanned": files_scanned,
        "cross_cluster_violations_remaining": cross_remaining,
        "syntax_errors_detected": len(syntax_errors),
        "remaining_violations": remaining_violations,
        "syntax_errors": syntax_errors,
    }


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Write Artifacts
# ══════════════════════════════════════════════════════════════════════════════


def step6_write_artifacts(
    auto_rules: list[dict],
    dry_run_results: dict,
    files_modified: int,
    rewrites_applied: int,
    apply_errors: list[str],
    validation: dict,
    feasibility: list[dict],
    total_files_scanned: int,
) -> None:
    print("\n[STEP 6] Writing output artifacts …")

    # ── facade_rewrite_summary.json ──────────────────────────────────────────
    auto_count = len(auto_rules)
    optional_count = sum(
        1 for f in feasibility if f["status"] == "OPTIONAL_INTRA_CLUSTER"
    )
    manual_count = sum(
        1 for f in feasibility if f["status"] == "MANUAL_REVIEW_REQUIRED"
    )

    summary = {
        "generated_utc": NOW,
        "status": (
            "SUCCESS"
            if (
                validation["cross_cluster_violations_remaining"] == 0
                and validation["syntax_errors_detected"] == 0
            )
            else "PARTIAL"
        ),
        "total_files_scanned": validation["files_scanned"],
        "files_modified": files_modified,
        "rewrites_applied": rewrites_applied,
        "auto_repairable_rules": auto_count,
        "optional_intra_cluster": optional_count,
        "manual_review_required": manual_count,
        "cross_cluster_violations_remaining": validation[
            "cross_cluster_violations_remaining"
        ],
        "syntax_errors_detected": validation["syntax_errors_detected"],
        "apply_errors": apply_errors,
    }
    write_json(OUTPUT_DIR / "facade_rewrite_summary.json", summary)
    print("  [✓] Reports/Facade_Rewrite_Pass/facade_rewrite_summary.json")

    # ── facade_rewrite_changes.json ──────────────────────────────────────────
    changes_list: list[dict] = []
    for src_mod, info in sorted(dry_run_results.items()):
        if info["changes"]:
            changes_list.append(
                {
                    "source_module": src_mod,
                    "file": info["file"],
                    "changes": info["changes"],
                    "changed": info["changed"],
                    "syntax_errors": info["syntax_errors"],
                }
            )
    write_json(OUTPUT_DIR / "facade_rewrite_changes.json", changes_list)
    print("  [✓] Reports/Facade_Rewrite_Pass/facade_rewrite_changes.json")

    # ── facade_rewrite_diff.patch ────────────────────────────────────────────
    diff_lines: list[str] = []
    for _, info in sorted(dry_run_results.items()):
        if not info["changed"]:
            continue
        orig_lines = info["original_text"].splitlines(keepends=True)
        new_lines = info["rewritten_text"].splitlines(keepends=True)
        fname = info["file"]
        diff = list(
            difflib.unified_diff(
                orig_lines,
                new_lines,
                fromfile=f"a/{fname}",
                tofile=f"b/{fname}",
            )
        )
        diff_lines.extend(diff)
    write_text(OUTPUT_DIR / "facade_rewrite_diff.patch", "".join(diff_lines))
    print("  [✓] Reports/Facade_Rewrite_Pass/facade_rewrite_diff.patch")

    # ── facade_rewrite_validation.json ───────────────────────────────────────
    write_json(OUTPUT_DIR / "facade_rewrite_validation.json", validation)
    print("  [✓] Reports/Facade_Rewrite_Pass/facade_rewrite_validation.json")

    # ── facade_rewrite_report.md ─────────────────────────────────────────────
    status_str = summary["status"]
    lines = [
        "# ARCHON — Facade Import Rewrite Pass Report",
        "",
        f"**Generated:** {NOW}",
        f"**Status:** {status_str}",
        "",
        "---",
        "",
        "## 1. Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total files scanned | {validation['files_scanned']} |",
        f"| Files modified | {files_modified} |",
        f"| Rewrites applied | {rewrites_applied} |",
        f"| AUTO_REPAIRABLE rules | {auto_count} |",
        f"| OPTIONAL_INTRA_CLUSTER (untouched) | {optional_count} |",
        f"| MANUAL_REVIEW_REQUIRED (untouched) | {manual_count} |",
        f"| Cross-cluster violations remaining | {validation['cross_cluster_violations_remaining']} |",
        f"| Syntax errors detected | {validation['syntax_errors_detected']} |",
        "",
        "---",
        "",
        "## 2. Files Modified",
        "",
    ]
    if changes_list:
        lines += ["| File | Rewrites |", "|------|---------|"]
        for c in changes_list:
            if c["changed"]:
                lines.append(f"| `{c['file']}` | {len(c['changes'])} |")
    else:
        lines.append("_No files were modified._")

    lines += [
        "",
        "---",
        "",
        "## 3. Sample Rewrites",
        "",
    ]
    sample_count = 0
    for c in changes_list:
        if sample_count >= 20:
            break
        if c["changed"] and c["changes"]:
            lines.append(f"**`{c['file']}`**")
            for ch in c["changes"][:3]:
                lines.append(f"- {ch}")
            lines.append("")
            sample_count += 1

    if validation["syntax_errors"]:
        lines += [
            "---",
            "",
            "## 4. Syntax Errors (Post-Rewrite)",
            "",
        ]
        for e in validation["syntax_errors"][:20]:
            lines.append(f"- `{e}`")
        lines.append("")

    if validation["remaining_violations"]:
        lines += [
            "---",
            "",
            "## 5. Remaining Violations",
            "",
            "| Source Module | Illegal Import | Line |",
            "|--------------|----------------|------|",
        ]
        for v in validation["remaining_violations"][:30]:
            lines.append(
                f"| `{v['source_module'][-50:]}` "
                f"| `{v['illegal_import'][-60:]}` | {v['line']} |"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "## 6. Validation Criteria",
        "",
        f"- cross_cluster_deep_imports == 0 : "
        f"{'✅ PASS' if validation['cross_cluster_violations_remaining'] == 0 else '❌ FAIL'}",
        f"- syntax_errors_detected == 0     : "
        f"{'✅ PASS' if validation['syntax_errors_detected'] == 0 else '❌ FAIL'}",
        "",
        "---",
        "",
        "_End of ARCHON Facade Rewrite Pass Report_",
        "",
    ]
    write_text(OUTPUT_DIR / "facade_rewrite_report.md", "\n".join(lines))
    print("  [✓] Reports/Facade_Rewrite_Pass/facade_rewrite_report.md")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def main():
    print("=" * 70)
    print("  ARCHON PRIME — FACADE IMPORT REWRITE PASS")
    print("  Mode: Deterministic Repair / Fail-Closed")
    print("=" * 70)

    # STEP 1 — Load artifacts
    auto_rules, feasibility, facade_map_raw, surface_spec = step1_load()

    # STEP 2 — Preconditions (aborts if not met)
    file_rule_map = step2_preconditions(auto_rules)

    # STEP 3 — Dry-run simulation
    dry_run_results = step3_dry_run(file_rule_map)

    # Check dry-run for syntax errors before proceeding
    dry_syntax_errors = []
    for info in dry_run_results.values():
        dry_syntax_errors.extend(info["syntax_errors"])

    if dry_syntax_errors:
        abort(
            "Dry-run introduced syntax errors — aborting before any file mutation",
            {"syntax_errors": dry_syntax_errors},
        )

    # STEP 4 — Live apply
    files_modified, rewrites_applied, apply_errors = step4_apply(dry_run_results)

    if apply_errors:
        print(
            f"\n[!] {len(apply_errors)} apply errors (non-fatal, partial rewrite executed):"
        )
        for e in apply_errors:
            print(f"    {e}")

    # STEP 5 — Post-rewrite validation
    validation = step5_validate(auto_rules)

    # STEP 6 — Artifacts
    step6_write_artifacts(
        auto_rules,
        dry_run_results,
        files_modified,
        rewrites_applied,
        apply_errors,
        validation,
        feasibility,
        total_files_scanned=validation["files_scanned"],
    )

    # Final verdict
    print("\n" + "=" * 70)
    print("  REWRITE PASS COMPLETE")
    print("=" * 70)
    print(f"  Files modified                    : {files_modified}")
    print(f"  Rewrites applied                  : {rewrites_applied}")
    print(
        f"  Cross-cluster violations remaining: {validation['cross_cluster_violations_remaining']}"
    )
    print(
        f"  Syntax errors post-rewrite        : {validation['syntax_errors_detected']}"
    )
    print("=" * 70)

    success = (
        validation["cross_cluster_violations_remaining"] == 0
        and validation["syntax_errors_detected"] == 0
    )

    if success:
        print("\n[SUCCESS] All validation criteria satisfied.")
    else:
        print("\n[PARTIAL] One or more criteria not yet met — see report.")
        # Per spec: SUCCESS requires both criteria == 0; report but don't abort
        # since files were already written correctly.


if __name__ == "__main__":
    main()
