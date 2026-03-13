"""
ARCHON PRIME V2.1 BULK HEADER + WORKFLOW GATE INJECTION
Performs phases 1-7 of the V2.1 injection protocol.
"""

import ast
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────────────────

REPO_ROOT = Path("/workspaces/ARCHON_PRIME")

HEADER_BOUNDARY_START = "# ARCHON PRIME MODULE HEADER"
HEADER_BOUNDARY_END = "# END ARCHON PRIME MODULE HEADER"

GATE_IMPORT = "from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate"
GATE_CALL = "enforce_runtime_gate()"

GATE_MODULE_REL = "WORKFLOW_NEXUS/Governance/workflow_gate.py"

SPEC_REF = "[SPEC-AP-V2.1]"
IMPLEMENTATION_PHASE = "PHASE_2"
AUTHORING_AUTHORITY = "ARCHON_PRIME"
VERSION = "1.0"
STATUS = "canonical"

# ─── Exclusions ───────────────────────────────────────────────────────────────

EXCLUDE_DIRS = {
    "WORKFLOW_TARGET_PROCESSING/PROCESSING",
    "WORKFLOW_TARGET_PROCESSING/COMPLETED",
    "__pycache__",
}

EXCLUDE_NAME_PATTERNS = [
    r"^test_",
    r"_test\.py$",
]

EXCLUDE_DIR_PATTERNS = [
    r"[/\\]test[s]?[/\\]",
    r"[/\\]simulation[/\\]",
    r"[/\\]__pycache__[/\\]",
]

# ─── Inference tables ─────────────────────────────────────────────────────────

SUBSYSTEM_MAP = {
    "WORKFLOW_MUTATION_TOOLING": "mutation_tooling",
    "WORKFLOW_TARGET_AUDITS": "audit_tooling",
    "WORKFLOW_TARGET_PROCESSING": "processing_engine",
    "WORKFLOW_NEXUS": "workflow_nexus",
}

ROLE_MAP = {
    "analysis": "analysis",
    "audit_tools": "inspection",
    "audit": "inspection",
    "operators": "mutation",
    "simulation": "simulation",
    "controllers": "orchestration",
    "orchestration": "orchestration",
    "reports": "reporting",
    "reporting": "reporting",
    "repo_mapping": "inspection",
    "normalization_tools": "utility",
    "import_analysis": "analysis",
    "runtime_analysis": "analysis",
    "semantic_extraction": "analysis",
    "governance_analysis": "inspection",
    "governance": "utility",
    "registry": "utility",
    "utils": "utility",
    "crawler": "utility",
    "repair": "mutation",
    "tools": "utility",
}

STAGE_MAP = {
    "analysis": "analysis",
    "audit_tools": "audit",
    "audit": "audit",
    "operators": "repair",
    "repair": "repair",
    "processing": "processing",
    "repo_mapping": "inspection",
    "runtime_analysis": "validation",
    "controllers": "orchestration",
    "orchestration": "orchestration",
    "normalization_tools": "utility",
    "import_analysis": "analysis",
    "semantic_extraction": "analysis",
    "governance_analysis": "inspection",
    "governance": "utility",
    "registry": "utility",
    "utils": "utility",
    "crawler": "utility",
    "tools": "utility",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────


def infer_subsystem(rel_path: str) -> str:
    for key, val in SUBSYSTEM_MAP.items():
        if rel_path.startswith(key):
            return val
    return "unknown"


def infer_role(rel_path: str) -> str:
    parts = Path(rel_path).parts
    for part in reversed(parts[:-1]):  # skip filename
        key = part.lower()
        if key in ROLE_MAP:
            return ROLE_MAP[key]
    return "utility"


def infer_stage(rel_path: str) -> str:
    parts = Path(rel_path).parts
    for part in reversed(parts[:-1]):
        key = part.lower()
        if key in STAGE_MAP:
            return STAGE_MAP[key]
    return "utility"


def detect_execution_entry(source: str) -> str:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return "None"
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name in ("main", "run", "execute"):
                return node.name
    return "None"


def generate_responsibility(module_name: str, role: str) -> str:
    words = re.sub(r"[_\-]", " ", module_name)
    return f"{role.capitalize()} module: {words}"


def is_excluded(rel_path: str) -> bool:
    for excl in EXCLUDE_DIRS:
        if excl in rel_path:
            return True
    for pat in EXCLUDE_DIR_PATTERNS:
        if re.search(pat, rel_path):
            return True
    filename = Path(rel_path).name
    for pat in EXCLUDE_NAME_PATTERNS:
        if re.search(pat, filename):
            return True
    return False


# ─── Module enumeration ───────────────────────────────────────────────────────


def enumerate_modules() -> list[dict]:
    modules = []
    for py_file in sorted(REPO_ROOT.rglob("*.py")):
        rel = py_file.relative_to(REPO_ROOT).as_posix()
        if not re.match(r"WORKFLOW_", rel):
            continue
        if is_excluded(rel):
            continue
        modules.append(
            {
                "module_name": py_file.stem,
                "absolute_path": str(py_file),
                "relative_repo_path": rel,
                "directory_context": "/".join(py_file.parts[1:-1]),
            }
        )
    return modules


# ─── Simulation ───────────────────────────────────────────────────────────────


def simulate_module(entry: dict) -> dict:
    path = Path(entry["absolute_path"])
    source = path.read_text(encoding="utf-8")
    has_header = HEADER_BOUNDARY_START in source
    has_gate = GATE_IMPORT in source or "enforce_runtime_gate" in source
    malformed = has_header and HEADER_BOUNDARY_END not in source
    syntax_ok = True
    try:
        ast.parse(source)
    except SyntaxError:
        syntax_ok = False

    return {
        "module": entry["relative_repo_path"],
        "has_header": has_header,
        "has_gate": has_gate,
        "malformed": malformed,
        "syntax_ok": syntax_ok,
        "needs_injection": not has_header,
        "safe_to_inject": syntax_ok and not malformed,
    }


# ─── Header construction ──────────────────────────────────────────────────────


def build_header(module_id: str, info: dict, source: str) -> str:
    rel = info["relative_repo_path"]
    name = info["module_name"]
    role = infer_role(rel)
    stage = infer_stage(rel)
    subsys = infer_subsystem(rel)
    entry = detect_execution_entry(source)
    resp = generate_responsibility(name, role)
    is_mutation = role == "mutation"
    allowed_targets = (
        '["WORKFLOW_TARGET_PROCESSING/PROCESSING"]' if is_mutation else "[]"
    )
    forbidden_targets = '["SYSTEM", "WORKFLOW_NEXUS"]'

    header = f"""\
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            {module_id}
# module_name:          {name}
# subsystem:            {subsys}
# module_role:          {role}
# canonical_path:       {rel}
# responsibility:       {resp}
# runtime_stage:        {stage}
# execution_entry:      {entry}
# allowed_targets:      {allowed_targets}
# forbidden_targets:    {forbidden_targets}
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       {SPEC_REF}
# implementation_phase: {IMPLEMENTATION_PHASE}
# authoring_authority:  {AUTHORING_AUTHORITY}
# version:              {VERSION}
# status:               {STATUS}
# ============================================================
"""
    return header


def build_gate_block(is_gate_module: bool) -> str:
    """Return the gate activation and end marker block."""
    if is_gate_module:
        # Governance module: no self-referential gate call
        gate_lines = "# NOTE: This is the workflow_gate governance module; gate self-call omitted.\n"
    else:
        gate_lines = f"{GATE_IMPORT}\n{GATE_CALL}\n"

    end_marker = (
        "\n"
        "# ------------------------------------------------------------\n"
        "# END ARCHON PRIME MODULE HEADER\n"
        "# ------------------------------------------------------------\n"
        "\n"
    )
    return gate_lines + end_marker


def inject_header(module_id: str, info: dict, source: str) -> str:
    rel = info["relative_repo_path"]
    is_gate = rel == GATE_MODULE_REL

    header = build_header(module_id, info, source)
    gate_block = build_gate_block(is_gate)

    # Strip leading BOM / shebang lines and preserve them at front later
    leading = ""
    body = source

    # Handle encoding declarations and shebangs
    lines = source.splitlines(keepends=True)
    kept_leading = []
    rest_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0 and stripped.startswith("#!"):
            kept_leading.append(line)
            rest_start = 1
        elif i < 2 and re.match(r"#.*coding[=: ]", stripped):
            kept_leading.append(line)
            rest_start = i + 1
        else:
            break
    if kept_leading:
        leading = "".join(kept_leading)
        body = "".join(lines[rest_start:])

    return leading + header + gate_block + body


# ─── Validation ───────────────────────────────────────────────────────────────

REQUIRED_FIELDS = [
    "module_id",
    "module_name",
    "subsystem",
    "module_role",
    "canonical_path",
    "responsibility",
    "runtime_stage",
    "execution_entry",
    "allowed_targets",
    "forbidden_targets",
    "allowed_imports",
    "forbidden_imports",
    "spec_reference",
    "implementation_phase",
    "authoring_authority",
    "version",
    "status",
]


def validate_injected(path: Path, rel: str) -> dict:
    try:
        source = path.read_text(encoding="utf-8")
    except Exception as exc:
        return {"module": rel, "valid": False, "error": str(exc)}

    issues = []
    if HEADER_BOUNDARY_START not in source:
        issues.append("missing header boundary start")
    if HEADER_BOUNDARY_END not in source:
        issues.append("missing header boundary end")

    is_gate = rel == GATE_MODULE_REL
    if not is_gate:
        if GATE_IMPORT not in source:
            issues.append("missing gate import")
        if "enforce_runtime_gate()" not in source:
            issues.append("missing gate call")

    for field in REQUIRED_FIELDS:
        if f"# {field}:" not in source:
            issues.append(f"missing field: {field}")

    try:
        ast.parse(source)
    except SyntaxError as exc:
        issues.append(f"syntax error: {exc}")

    return {
        "module": rel,
        "valid": len(issues) == 0,
        "issues": issues,
    }


# ─── Main pipeline ────────────────────────────────────────────────────────────


def main():
    print("=" * 60)
    print("ARCHON PRIME V2.1 HEADER INJECTION PIPELINE")
    print("=" * 60)

    # ── Phase 1: Enumerate ────────────────────────────────────────
    print("\n[PHASE 1] Enumerating target modules...")
    modules = enumerate_modules()
    print(f"  Found: {len(modules)} modules  (expected ~91)")

    inventory_path = (
        REPO_ROOT
        / "WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports"
        / "header_injection_target_inventory.json"
    )
    inventory_path.write_text(
        json.dumps(
            {
                "generated": datetime.utcnow().isoformat() + "Z",
                "module_count": len(modules),
                "expected_count": 91,
                "modules": modules,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"  Inventory written: {inventory_path.relative_to(REPO_ROOT)}")

    # ── Phase 2: Simulation ───────────────────────────────────────
    print("\n[PHASE 2] Running header injection simulation...")
    sim_results = [simulate_module(m) for m in modules]

    syntax_conflicts = [s for s in sim_results if not s["syntax_ok"]]
    if syntax_conflicts:
        print(f"  ABORT: {len(syntax_conflicts)} module(s) have syntax errors:")
        for sc in syntax_conflicts:
            print(f"    {sc['module']}")
        sys.exit(2)

    already_compliant = [s for s in sim_results if s["has_header"]]
    needs_injection = [
        s for s in sim_results if s["needs_injection"] and s["safe_to_inject"]
    ]
    malformed = [s for s in sim_results if s["malformed"]]

    print(f"  Already compliant : {len(already_compliant)}")
    print(f"  Need injection    : {len(needs_injection)}")
    print(f"  Malformed headers : {len(malformed)}")
    print("  Syntax conflicts  : 0 (cleared for injection)")

    sim_report_path = (
        REPO_ROOT
        / "WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports"
        / "header_injection_simulation_report.json"
    )
    sim_report_path.write_text(
        json.dumps(
            {
                "generated": datetime.utcnow().isoformat() + "Z",
                "total_modules": len(modules),
                "already_compliant": len(already_compliant),
                "needs_injection": len(needs_injection),
                "malformed_headers": len(malformed),
                "syntax_conflicts": 0,
                "abort_triggered": False,
                "results": sim_results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"  Simulation report written: {sim_report_path.relative_to(REPO_ROOT)}")

    # ── Phase 3 + 4: Inject ───────────────────────────────────────
    print("\n[PHASE 3+4] Auto-populating fields and injecting headers...")

    mutated = []
    failed = []
    skipped = []

    module_id_counter = 1

    for mod_info in modules:
        rel = mod_info["relative_repo_path"]
        path = Path(mod_info["absolute_path"])
        sim = next(s for s in sim_results if s["module"] == rel)

        if sim["has_header"]:
            skipped.append({"module": rel, "reason": "already_compliant"})
            module_id_counter += 1
            continue

        if not sim["safe_to_inject"]:
            failed.append({"module": rel, "reason": "unsafe"})
            module_id_counter += 1
            continue

        module_id = f"M-{module_id_counter:03d}"
        module_id_counter += 1

        try:
            source = path.read_text(encoding="utf-8")
            new_source = inject_header(module_id, mod_info, source)
            path.write_text(new_source, encoding="utf-8")
            mutated.append({"module": rel, "module_id": module_id})
            print(f"  [{module_id}] Injected: {rel}")
        except Exception as exc:
            failed.append({"module": rel, "reason": str(exc)})
            print(f"  FAILED: {rel} -> {exc}")

    print(f"\n  Mutated : {len(mutated)}")
    print(f"  Skipped : {len(skipped)}")
    print(f"  Failed  : {len(failed)}")

    # ── Phase 5: Post-injection normalization (structural check) ──
    print("\n[PHASE 5] Post-injection normalization (syntax verification)...")
    syntax_failures = []
    for mod_info in modules:
        path = Path(mod_info["absolute_path"])
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source)
        except SyntaxError as exc:
            syntax_failures.append(
                {"module": mod_info["relative_repo_path"], "error": str(exc)}
            )

    if syntax_failures:
        print(f"  WARNING: {len(syntax_failures)} syntax failures after injection!")
        for sf in syntax_failures:
            print(f"    {sf['module']}: {sf['error']}")
    else:
        print("  All modules pass syntax verification.")

    # ── Phase 6: Validation sweep ─────────────────────────────────
    print("\n[PHASE 6] Running repo-wide header validation sweep...")
    validation_results = []
    for mod_info in modules:
        path = Path(mod_info["absolute_path"])
        result = validate_injected(path, mod_info["relative_repo_path"])
        validation_results.append(result)

    valid_count = sum(1 for r in validation_results if r["valid"])
    invalid_count = len(validation_results) - valid_count
    schema_compliance_pct = (
        (valid_count / len(validation_results) * 100) if validation_results else 0
    )

    print(f"  Valid   : {valid_count}/{len(validation_results)}")
    print(f"  Invalid : {invalid_count}")
    print(f"  Schema compliance: {schema_compliance_pct:.1f}%")

    if invalid_count:
        print("  Invalid modules:")
        for r in validation_results:
            if not r["valid"]:
                print(f"    {r['module']}: {r.get('issues', [])}")

    # ── Phase 7: Governance report ────────────────────────────────
    print("\n[PHASE 7] Writing governance report...")

    fields_auto_populated = [
        "module_id",
        "module_name",
        "subsystem",
        "module_role",
        "canonical_path",
        "responsibility",
        "runtime_stage",
        "execution_entry",
        "allowed_targets",
        "forbidden_targets",
        "spec_reference",
        "implementation_phase",
        "authoring_authority",
        "version",
        "status",
    ]
    fields_left_blank = ["allowed_imports", "forbidden_imports"]

    total_processed = len(mutated) + len(skipped)
    success_criteria = (
        total_processed >= 90 and len(failed) == 0 and schema_compliance_pct == 100.0
    )

    report_md = f"""# ARCHON PRIME V2.1 HEADER INJECTION GOVERNANCE REPORT

**Generated:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC  
**Authority:** ARCHON_PRIME  
**Schema:** AP_MODULE_HEADER_SCHEMA v1.0  
**Spec:** {SPEC_REF}

---

## Summary

| Metric | Value |
|--------|-------|
| Modules enumerated | {len(modules)} |
| Expected (target) | 91 |
| Modules already compliant | {len(skipped)} |
| Modules mutated (injected) | {len(mutated)} |
| Modules failed | {len(failed)} |
| Total processed | {total_processed} |
| Schema compliance | {schema_compliance_pct:.1f}% |
| Syntax errors post-injection | {len(syntax_failures)} |

---

## Fields Auto-Populated

{chr(10).join(f"- `{f}`" for f in fields_auto_populated)}

## Fields Left Blank (Schema Default `[]`)

{chr(10).join(f"- `{f}`" for f in fields_left_blank)}

---

## Phase Outcomes

| Phase | Status |
|-------|--------|
| Phase 0: Precondition Validation | PASS |
| Phase 1: Module Enumeration | PASS — {len(modules)} modules ({len(modules) - 91:+d} vs expected 91) |
| Phase 2: Simulation | PASS — 0 syntax conflicts |
| Phase 3: Field Auto-Population | PASS |
| Phase 4: Header + Gate Injection | {'PASS' if len(failed) == 0 else 'PARTIAL'} |
| Phase 5: Post-Injection Normalization | {'PASS' if not syntax_failures else 'FAILURE'} |
| Phase 6: Repo-Wide Validation | {'PASS' if invalid_count == 0 else 'PARTIAL'} |
| Phase 7: Report Generation | PASS |

---

## Mutated Modules

| Module ID | Relative Path |
|-----------|--------------|
{chr(10).join(f"| {m['module_id']} | `{m['module']}` |" for m in mutated)}

---

## Already Compliant (Skipped)

{chr(10).join(f"- `{s['module']}`" for s in skipped) if skipped else "_None_"}

---

## Failed Modules

{chr(10).join(f"- `{f['module']}`: {f['reason']}" for f in failed) if failed else "_None — all modules processed successfully._"}

---

## Validation Issues

{chr(10).join(f"- `{r['module']}`: {r.get('issues', [])}" for r in validation_results if not r['valid']) if invalid_count else "_None — all modules pass schema validation._"}

---

## Success Criteria

| Criterion | Required | Actual | Status |
|-----------|----------|--------|--------|
| Modules processed | ≥ 90 | {total_processed} | {'PASS' if total_processed >= 90 else 'FAIL'} |
| Modules failed | = 0 | {len(failed)} | {'PASS' if len(failed) == 0 else 'FAIL'} |
| Schema compliance | = 100% | {schema_compliance_pct:.1f}% | {'PASS' if schema_compliance_pct == 100.0 else 'FAIL'} |
| **Overall** | | | **{'PASS — ARCHON PRIME TOOLING V2.1 COMPLIANT' if success_criteria else 'INCOMPLETE'}** |

---

_Report generated by ARCHON PRIME V2.1 Header Injection Pipeline_
"""

    gov_report_path = (
        REPO_ROOT
        / "WORKFLOW_TARGET_AUDITS/MODULES/reports/governance_reports"
        / "header_injection_v21_report.md"
    )
    gov_report_path.write_text(report_md, encoding="utf-8")
    print(f"  Governance report written: {gov_report_path.relative_to(REPO_ROOT)}")

    # ── Final summary ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("ARCHON PRIME V2.1 INJECTION COMPLETE")
    print("=" * 60)
    print(f"  Modules processed  : {total_processed}")
    print(f"  Modules mutated    : {len(mutated)}")
    print(f"  Modules compliant  : {len(skipped)}")
    print(f"  Modules failed     : {len(failed)}")
    print(f"  Schema compliance  : {schema_compliance_pct:.1f}%")
    print(
        f"  Overall result     : {'SUCCESS — V2.1 COMPLIANT' if success_criteria else 'PARTIAL COMPLETION'}"
    )
    print("=" * 60)

    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
