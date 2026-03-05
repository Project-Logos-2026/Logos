# Canonical Import Facade — Blueprint

---

## Governance Header

| Field | Value |
|---|---|
| Artifact | `Canonical_Import_Facade_Blueprint.md` |
| Canonical Path | `/workspaces/Logos/BLUEPRINTS/Canonical_Import_Facade_Blueprint.md` |
| Phase | Infrastructure / Cross-Phase |
| Layer | Import_Infrastructure |
| Artifact Type | Blueprint |
| Authority | `LOGOS_Import_Infrastructure` |
| Mutability | Manual revision only — requires diff review |
| Execution Status | Non_Executable (design specification) |
| Version | 1.1.0 |
| Governed By Schema | This document is the governing schema for all implementation artifacts it specifies |

---

## Revision History

| Version | Change |
|---|---|
| 1.0.0 | Initial blueprint |
| 1.1.0 | AST-guided line replacement in `replace_imports.py`; corrected CI enforcement phase order (Phase D precedes Phase E); added `rollback_imports.py` and `Replacement_Log.json`; corrected `check_import_boundaries.py` logic flaw; corrected `validate_canonical_map.py` to verify `internal_module` paths on disk; extended `detect_import_drift.py` to full forbidden prefix registry; scoped `runtime_import_smoke.py` to importable roots only; removed `importlib.import_module` from `validate_facade.py` |

---

## 1. Purpose and Scope

This blueprint specifies the design, deliverables, implementation sequence, and acceptance criteria for the Canonical Import Facade system.

**Purpose:** Eliminate import and call-path breakage caused by deep absolute imports against LOGOS's nested module hierarchy, by introducing a single stable import surface and enforcing a repo-wide "no deep imports" policy.

**Scope — Included:**
- All Python modules under `LOGOS_SYSTEM/`
- Import surface for `Runtime_Spine`, `RUNTIME_CORES`, `RUNTIME_OPPERATIONS_CORE`, governance, and orchestration symbols
- Automation scripts in `Tools/Import_Facade/`
- CI enforcement via GitHub Actions

**Scope — Excluded:**
- `LOGOS_EXTERNALIZATION/` — projection-only layer; no runtime cross-imports
- `DRAC/` — excluded unless deep imports cause compilation failure
- Coq / `.v` files — not Python; not in scope
- Third-party library imports
- Test-only files — excluded from enforcement; tracked separately

---

## 2. Problem Statement

The repository exhibits:

1. Module hierarchy nesting 8–10 levels deep under `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/`
2. A duplicate deep hierarchy — `Agent_Resources/` and `Logos_Core/Logos_Protocol/Logos_Agent_Resources/` — creating ambiguous canonical sources for some symbols
3. Widespread deep absolute imports that couple consumers to internal file positions
4. Import failures that surface only at runtime rather than at validation time
5. AI-assistant-generated deep import paths that bypass established boundaries

When files move during refactors, imports break widely and runtime fails late.

---

## 3. Non-Negotiable Constraints

The following constraints are binding and may not be relaxed by implementors.

1. **No runtime logic changes.** Only import statements and facade modules are modified. No refactoring of module behavior.
2. **No directory restructuring.** Directory layout is unchanged in this pass.
3. **Fail-closed on ambiguity.** If a symbol maps to multiple internal definitions, no auto-resolution occurs. An ambiguity report is emitted and manual adjudication is required before that symbol is added to the canonical map.
4. **Allowlist-driven replacement only.** Import replacement touches only symbols explicitly present in the approved `Canonical_Map.json`. No fuzzy matching.
5. **Dry-run gate is mandatory.** Apply mode requires an explicitly approved `Canonical_Map.json` with a non-empty `symbols` array. Scripts enforce this programmatically.
6. **Canonical Map is a governance artifact.** It must not be modified by automated scripts. The build script produces a candidate map for human review; only the reviewed and approved map is used for replacement.
7. **Additive-only facade construction.** Facade modules contain only imports and `__all__` declarations. No logic, no classes, no functions may be defined in any facade module.
8. **`RUNTIME_OPPERATIONS_CORE` spelling preserved.** The repository contains a directory spelled `RUNTIME_OPPERATIONS_CORE` (double-P). All scripts must reference this exact string. Do not correct the spelling.
9. **File formatting must be preserved.** Import replacement must not alter comments, docstrings, blank lines, or any non-import content. Full AST rewrite via `ast.unparse()` is prohibited for this reason.

---

## 4. Authority and Location

**Decision: Option A is adopted.** The Canonical Import Facade package is located at:

```
LOGOS_SYSTEM/Canonical_Import_Facade/
```

**Rationale:**
- Preserves the `LOGOS_SYSTEM.*` namespace convention used throughout the repository
- Keeps the facade package adjacent to the subsystems it mediates
- Internal imports (`from LOGOS_SYSTEM.RUNTIME_CORES...`) resolve without `sys.path` changes
- Option B (`logos/` at repo root) is rejected: it introduces a new top-level package namespace inconsistent with existing repo conventions and would require `setup.py` / `pyproject.toml` changes

**Tier Classification:** The `Canonical_Import_Facade/` directory is classified as **Import_Infrastructure**, not a runtime component. It does not participate in the Octafolium protocol stack, the agent hierarchy, or the tick loop. This distinction must be documented in its `METADATA.json`.

**Authority Level:** `LOGOS_Import_Infrastructure`. Subordinate to `Logos_Agent` (runtime sovereign) and parallel to subsystem-level authorities. Has no governance enforcement power. Exposes symbols and enforces import paths only.

---

## 5. Canonical Facade Design

### 5.1 Directory Structure

```
LOGOS_SYSTEM/Canonical_Import_Facade/
    __init__.py
    runtime.py
    governance.py
    orchestration.py
    memory.py
    protocols.py
    types.py
    Canonical_Map.json
    Documentation/
        GOVERNANCE_SCOPE.md
        MANIFEST.md
        METADATA.json
```

### 5.2 Canonical Header (Required on All Facade `.py` Files)

Every `.py` file in `Canonical_Import_Facade/` must carry this header block as the first non-shebang content:

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: <filename>.py
# Layer: Import_Infrastructure
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Non_Executable_Logic (re-export only)
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================
```

### 5.3 Facade Module Structure

Each facade module must conform to this pattern exactly:

```python
# [canonical header]

"""
<module_name> — Canonical import surface for [domain].

Re-exports authoritative symbols from their internal canonical sources.
No logic, classes, or functions may be defined in this module.
"""

from <internal.canonical.path> import <Symbol>

__all__ = [
    "<Symbol>",
]
```

### 5.4 Canonical Map Schema

`LOGOS_SYSTEM/Canonical_Import_Facade/Canonical_Map.json` is the single source of truth for all facade symbol mappings.

Required structure:

```json
{
  "schema_version": "1.0.0",
  "governed_by": "/workspaces/Logos/BLUEPRINTS/Canonical_Import_Facade_Blueprint.md",
  "authority": "LOGOS_Import_Infrastructure",
  "mutability": "manual_only",
  "last_reviewed": "<ISO-8601 date>",
  "symbols": [
    {
      "canonical_name": "<SymbolName>",
      "facade_module": "LOGOS_SYSTEM.Canonical_Import_Facade.<module>",
      "internal_module": "<LOGOS_SYSTEM.full.internal.path>",
      "notes": "<optional: rationale, caveats, or adjudication record>"
    }
  ]
}
```

**Constraints:**
- `canonical_name` must be unique across all entries
- `internal_module` must be verified to resolve to an existing file on disk before the entry is added
- Ambiguous symbols (multiple candidate `internal_module` values) must NOT be added until manually adjudicated; they remain in `Ambiguity_Report.json` only
- The `symbols` array must not be empty when `replace_imports.py --apply` is invoked

### 5.5 Forbidden Prefix Registry

The following internal import prefixes are forbidden outside of allowlisted directories. This list is a governance artifact. Additions require a blueprint revision (version bump).

```python
FORBIDDEN_PREFIXES = [
    "LOGOS_SYSTEM.RUNTIME_CORES",
    "LOGOS_SYSTEM.RUNTIME_OPPERATIONS_CORE",   # repo spelling — double-P preserved
    "LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT",
    "LOGOS_SYSTEM.Runtime_Spine",
    "LOGOS_SYSTEM.STARTUP",
]
```

**Allowlisted path segments** (directories permitted to use deep imports):

```python
ALLOWLISTED_PATH_SEGMENTS = {
    "Canonical_Import_Facade",
    "Import_Facade",
}
```

---

## 6. Automation Scripts

All scripts reside under `Tools/Import_Facade/`. All scripts carry the LOGOS canonical header. Default execution mode is always dry-run unless `--apply` is passed explicitly.

---

### 6.1 `build_facade.py`

**Purpose:** Inventory all Python modules. Classify imports. Produce candidate canonical map and ambiguity report. Dry-run only — does not modify any existing file.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: build_facade.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Inventory all Python modules and produce the candidate canonical map.

Outputs:
  _Reports/Canonical_Import_Facade/Import_Inventory.json
  _Reports/Canonical_Import_Facade/Canonical_Candidate_List.json
  _Reports/Canonical_Import_Facade/Ambiguity_Report.json

Does not write to LOGOS_SYSTEM/. Does not modify any existing file.
Canonical_Map.json must be populated manually from the candidate list.
"""

import ast
import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT    = Path(".")
REPORT_DIR   = Path("_Reports/Canonical_Import_Facade")
EXCLUDE_DIRS = {".venv", "site-packages", "__pycache__", ".git"}

REPORT_DIR.mkdir(parents=True, exist_ok=True)

python_files: list[str] = []
symbol_to_modules: dict[str, list[str]] = defaultdict(list)
parse_failures: list[dict] = []

for path in sorted(REPO_ROOT.rglob("*.py")):
    if any(ex in path.parts for ex in EXCLUDE_DIRS):
        continue
    python_files.append(str(path))

    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as e:
        parse_failures.append({"file": str(path), "error": str(e)})
        continue

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                symbol_to_modules[alias.name].append(node.module)

inventory = {
    "python_files": python_files,
    "parse_failures": parse_failures,
    "symbol_sources": {k: list(set(v)) for k, v in symbol_to_modules.items()},
}

(REPORT_DIR / "Import_Inventory.json").write_text(
    json.dumps(inventory, indent=2), encoding="utf-8"
)

candidates: list[dict] = []
ambiguous: list[dict] = []

for symbol, modules in symbol_to_modules.items():
    unique_modules = list(set(modules))
    if len(unique_modules) == 1 and len(modules) > 2:
        candidates.append({
            "symbol": symbol,
            "module": unique_modules[0],
            "import_count": len(modules),
        })
    elif len(unique_modules) > 1 and len(modules) > 2:
        ambiguous.append({
            "symbol": symbol,
            "candidate_modules": unique_modules,
            "import_count": len(modules),
        })

(REPORT_DIR / "Canonical_Candidate_List.json").write_text(
    json.dumps(sorted(candidates, key=lambda x: -x["import_count"]), indent=2),
    encoding="utf-8",
)

(REPORT_DIR / "Ambiguity_Report.json").write_text(
    json.dumps(ambiguous, indent=2), encoding="utf-8"
)

print("Dry-run complete.")
print(f"  Python files scanned         : {len(python_files)}")
print(f"  Parse failures               : {len(parse_failures)}")
print(f"  Canonical candidates         : {len(candidates)}")
print(f"  Ambiguous symbols (deferred) : {len(ambiguous)}")
print()
print("Next step: review Canonical_Candidate_List.json and Ambiguity_Report.json,")
print("then manually populate LOGOS_SYSTEM/Canonical_Import_Facade/Canonical_Map.json.")
print("Ambiguous symbols must not be added to the map until adjudicated.")
```

---

### 6.2 `replace_imports.py`

**Purpose:** Rewrite deep import statements to facade imports using the approved `Canonical_Map.json`.

**Replacement strategy:** AST-guided line replacement. `ast.parse()` identifies exact line numbers of matching `ImportFrom` nodes. Only those specific lines are subject to a targeted regex substitution. This eliminates false rewrites in comments, docstrings, string literals, and multiline import continuations while fully preserving file formatting. `ast.unparse()` full-tree rewriting is explicitly prohibited (it destroys comments and normalizes whitespace).

Emits `Replacement_Log.json` — the required input for `rollback_imports.py`.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: replace_imports.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
AST-guided import replacement.

Identification phase : ast.parse() locates exact line numbers of matching
                       ImportFrom nodes.
Replacement phase    : Only those specific lines are rewritten via a
                       word-boundary regex. All other content is untouched.

This approach eliminates false rewrites in:
  - comments
  - docstrings
  - string literals
  - multiline import continuations
  - alias imports

Requires Python >= 3.8.

Usage:
  python Tools/Import_Facade/replace_imports.py            # dry-run
  python Tools/Import_Facade/replace_imports.py --apply    # execute
"""

import ast
import json
import re
import sys
from pathlib import Path

MAP_FILE   = Path("LOGOS_SYSTEM/Canonical_Import_Facade/Canonical_Map.json")
REPORT_DIR = Path("_Reports/Canonical_Import_Facade")
LOG_FILE   = REPORT_DIR / "Replacement_Log.json"
APPLY_MODE = "--apply" in sys.argv

EXCLUDE_PATH_SEGMENTS = {
    ".venv", "site-packages", "__pycache__", ".git",
    "Canonical_Import_Facade", "Import_Facade",
}

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Dry-run gates ─────────────────────────────────────────────────────────────

if not MAP_FILE.exists():
    print("ERROR: Canonical_Map.json not found. "
          "Run build_facade.py and populate the map before proceeding.")
    sys.exit(1)

canonical_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))

if not canonical_map.get("symbols"):
    print("ERROR: Canonical_Map.json has no symbols. "
          "Populate and approve the map before running --apply.")
    sys.exit(1)

# Build lookup: internal_module → facade_module
module_map: dict[str, str] = {
    entry["internal_module"]: entry["facade_module"]
    for entry in canonical_map["symbols"]
    if "internal_module" in entry and "facade_module" in entry
}

# ── Per-file processing ────────────────────────────────────────────────────────

replacement_report: list[dict] = []
log_entries: list[dict] = []
skipped: list[dict] = []

for path in sorted(Path(".").rglob("*.py")):
    if any(seg in path.parts for seg in EXCLUDE_PATH_SEGMENTS):
        continue

    try:
        original_text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        skipped.append({"file": str(path), "reason": str(e)})
        continue

    # ── AST identification pass ────────────────────────────────────────────────
    try:
        tree = ast.parse(original_text, filename=str(path))
    except SyntaxError as e:
        skipped.append({"file": str(path), "reason": f"SyntaxError: {e}"})
        continue

    # Collect: lineno (1-based) → (old_module, new_module)
    line_rewrites: dict[int, tuple[str, str]] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in module_map:
            line_rewrites[node.lineno] = (node.module, module_map[node.module])

    if not line_rewrites:
        continue

    # ── Surgical line replacement pass ────────────────────────────────────────
    lines = original_text.splitlines(keepends=True)
    file_log: list[dict] = []

    for lineno, (old_module, new_module) in sorted(line_rewrites.items()):
        idx = lineno - 1
        if idx >= len(lines):
            skipped.append({
                "file": str(path),
                "reason": (
                    f"Line {lineno} out of range "
                    f"(AST reported {lineno}, file has {len(lines)} lines)"
                ),
            })
            continue

        old_line = lines[idx]

        # Word-boundary guard: match old_module only when preceded by
        # 'from ' or 'import ' and followed by whitespace, end-of-line, or '.'.
        # Prevents partial-name collisions (e.g. Foo.Bar vs Foo.Bar.Baz).
        pattern = re.compile(
            r'(?<=(from |import ))' + re.escape(old_module) + r'(?=\s|$|\.)'
        )
        new_line = pattern.sub(new_module, old_line, count=1)

        if new_line == old_line:
            skipped.append({
                "file": str(path),
                "reason": (
                    f"Line {lineno}: AST matched '{old_module}' "
                    f"but word-boundary guard did not fire — skipped"
                ),
            })
            continue

        lines[idx] = new_line
        file_log.append({
            "file": str(path),
            "line": lineno,
            "old_import": old_line.rstrip("\n"),
            "new_import": new_line.rstrip("\n"),
        })

    if file_log:
        replacement_report.append({
            "file": str(path),
            "replacements": [
                {"from": old, "to": new}
                for _, (old, new) in sorted(line_rewrites.items())
            ],
        })
        log_entries.extend(file_log)

        if APPLY_MODE:
            path.write_text("".join(lines), encoding="utf-8")

# ── Emit reports ───────────────────────────────────────────────────────────────

(REPORT_DIR / "Replacement_Report.json").write_text(
    json.dumps({"replacements": replacement_report, "skipped": skipped}, indent=2),
    encoding="utf-8",
)

LOG_FILE.write_text(
    json.dumps(log_entries, indent=2), encoding="utf-8"
)

print(f"Files with replacements : {len(replacement_report)}")
print(f"Total line rewrites     : {len(log_entries)}")
print(f"Files skipped           : {len(skipped)}")

if APPLY_MODE:
    print("Import replacement applied.")
    print("Replacement_Log.json written — required for rollback_imports.py.")
else:
    print("Dry run only. Pass --apply to write changes.")
    print("Replacement_Log.json contains the proposed diff.")
```

---

### 6.3 `rollback_imports.py`

**Purpose:** Reverse all replacements written by `replace_imports.py --apply` using `Replacement_Log.json` as the transaction record.

**Design:** Verification-first. Before writing any file, the script verifies that every targeted line on disk still matches its expected post-replacement content. If any line has drifted, the script halts without touching any file. Partial rollback is never performed.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: rollback_imports.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Rollback replacement using Replacement_Log.json.

Each log entry records the file path, line number, old import text,
and new import text written by replace_imports.py --apply.

This script reverses each entry by restoring old_import at the
recorded line number.

Verification-first: if any line does not match its expected
post-replacement content, the script halts without writing any files.
Partial rollback is never performed.

Usage:
  python Tools/Import_Facade/rollback_imports.py            # dry-run
  python Tools/Import_Facade/rollback_imports.py --apply    # execute
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

LOG_FILE   = Path("_Reports/Canonical_Import_Facade/Replacement_Log.json")
REPORT_DIR = Path("_Reports/Canonical_Import_Facade")
APPLY_MODE = "--apply" in sys.argv

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Load log ──────────────────────────────────────────────────────────────────

if not LOG_FILE.exists():
    print("ERROR: Replacement_Log.json not found. Nothing to roll back.")
    sys.exit(1)

log_entries: list[dict] = json.loads(LOG_FILE.read_text(encoding="utf-8"))

if not log_entries:
    print("Replacement_Log.json is empty. Nothing to roll back.")
    sys.exit(0)

# Group entries by file
by_file: dict[str, list[dict]] = defaultdict(list)
for entry in log_entries:
    by_file[entry["file"]].append(entry)

# ── Verification pass (read-only) ─────────────────────────────────────────────

verification_failures: list[dict] = []

for filepath, entries in by_file.items():
    path = Path(filepath)
    if not path.exists():
        verification_failures.append({
            "file": filepath,
            "reason": "File not found on disk",
        })
        continue

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)

    for entry in entries:
        lineno = entry["line"]
        expected_new = entry["new_import"]
        idx = lineno - 1

        if idx >= len(lines):
            verification_failures.append({
                "file": filepath,
                "line": lineno,
                "reason": f"Line {lineno} out of range (file has {len(lines)} lines)",
            })
            continue

        actual = lines[idx].rstrip("\n")
        if actual != expected_new:
            verification_failures.append({
                "file": filepath,
                "line": lineno,
                "expected": expected_new,
                "actual": actual,
                "reason": "Line does not match expected post-replacement content",
            })

if verification_failures:
    (REPORT_DIR / "Rollback_Verification_Failures.json").write_text(
        json.dumps(verification_failures, indent=2), encoding="utf-8"
    )
    print(f"Rollback HALTED — {len(verification_failures)} verification failure(s).")
    print("No files were modified.")
    print("See Rollback_Verification_Failures.json for details.")
    sys.exit(1)

print(
    f"Verification passed — {len(log_entries)} line(s) across "
    f"{len(by_file)} file(s) ready for rollback."
)

if not APPLY_MODE:
    print("Dry run only. Pass --apply to execute rollback.")
    sys.exit(0)

# ── Rollback pass ─────────────────────────────────────────────────────────────

rolled_back: list[dict] = []

for filepath, entries in by_file.items():
    path = Path(filepath)
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)

    for entry in entries:
        idx = entry["line"] - 1
        old_text = entry["old_import"]
        current = lines[idx]
        # Preserve original line ending
        ending = current[len(current.rstrip("\n\r")):]
        lines[idx] = old_text + ending

        rolled_back.append({
            "file": filepath,
            "line": entry["line"],
            "restored": old_text,
        })

    path.write_text("".join(lines), encoding="utf-8")

(REPORT_DIR / "Rollback_Report.json").write_text(
    json.dumps(rolled_back, indent=2), encoding="utf-8"
)

print(
    f"Rollback complete. {len(rolled_back)} line(s) restored across "
    f"{len(by_file)} file(s)."
)
print("Rollback_Report.json written.")
```

---

### 6.4 `validate_facade.py`

**Purpose:** Post-change compile validation across all Python files. Uses `py_compile` only — does not invoke `importlib.import_module` (avoids side-effect hazards and fragile path derivation). Writes a baseline on first run; detects regressions on subsequent runs.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: validate_facade.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Post-change compile validation.

Runs python -m py_compile against all .py files in the repository.
On first run, writes the result as a baseline.
On subsequent runs, compares against the baseline and flags regressions.

Does not use importlib.import_module.

Outputs:
  _Reports/Canonical_Import_Facade/Compile_Report.json
  _Reports/Canonical_Import_Facade/Compile_Report_Baseline.json  (first run only)
"""

import json
import subprocess
import sys
from pathlib import Path

REPORT_DIR = Path("_Reports/Canonical_Import_Facade")
BASELINE   = REPORT_DIR / "Compile_Report_Baseline.json"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

EXCLUDE_DIRS = {".venv", "site-packages", "__pycache__", ".git"}

compile_failures: list[dict] = []
compile_passed = 0

for path in sorted(Path(".").rglob("*.py")):
    if any(ex in path.parts for ex in EXCLUDE_DIRS):
        continue

    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        compile_failures.append({
            "file": str(path),
            "error": result.stderr.strip(),
        })
    else:
        compile_passed += 1

report = {
    "passed": compile_passed,
    "failed": len(compile_failures),
    "failures": compile_failures,
}

(REPORT_DIR / "Compile_Report.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8"
)

print(f"Compile check: {compile_passed} passed, {len(compile_failures)} failed.")

if BASELINE.exists():
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    baseline_files = {f["file"] for f in baseline.get("failures", [])}
    current_files  = {f["file"] for f in compile_failures}
    regressions    = current_files - baseline_files

    if regressions:
        print(f"\nREGRESSION DETECTED — {len(regressions)} new failure(s):")
        for r in sorted(regressions):
            print(f"  {r}")
        sys.exit(1)
    else:
        print("No regressions relative to baseline.")
else:
    print("No baseline found. Writing current report as baseline.")
    BASELINE.write_text(json.dumps(report, indent=2), encoding="utf-8")

if not compile_failures:
    print("Validation passed.")
```

---

### 6.5 `validate_canonical_map.py`

**Purpose:** Structural validation of `Canonical_Map.json`. Verifies required fields and confirms that all `internal_module` entries resolve to existing files on disk.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: validate_canonical_map.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Validate Canonical_Map.json.

Checks:
  - Required top-level fields are present
  - Each symbol entry has required fields
  - canonical_name values are unique
  - Each internal_module resolves to an existing .py file on disk

Outputs:
  Exit 0 on pass.
  Exit 1 with error list on any failure.
"""

import json
import sys
from pathlib import Path

MAP_FILE = Path("LOGOS_SYSTEM/Canonical_Import_Facade/Canonical_Map.json")

REQUIRED_TOP    = {"schema_version", "governed_by", "authority",
                   "mutability", "last_reviewed", "symbols"}
REQUIRED_SYMBOL = {"canonical_name", "facade_module", "internal_module"}

errors: list[str] = []

if not MAP_FILE.exists():
    print(f"ERROR: {MAP_FILE} not found.")
    sys.exit(1)

try:
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
except Exception as e:
    print(f"ERROR: Cannot parse Canonical_Map.json: {e}")
    sys.exit(1)

missing_top = REQUIRED_TOP - set(data.keys())
if missing_top:
    errors.append(f"Missing top-level fields: {sorted(missing_top)}")

seen_names: set[str] = set()

for i, entry in enumerate(data.get("symbols", [])):
    missing = REQUIRED_SYMBOL - set(entry.keys())
    if missing:
        errors.append(f"symbols[{i}] missing fields: {sorted(missing)}")
        continue

    name = entry["canonical_name"]
    if name in seen_names:
        errors.append(f"Duplicate canonical_name: '{name}'")
    seen_names.add(name)

    module_path = Path(entry["internal_module"].replace(".", "/") + ".py")
    if not module_path.exists():
        errors.append(
            f"symbols[{i}] '{name}': internal_module path not found on disk: {module_path}"
        )

if errors:
    print(f"Canonical map validation FAILED ({len(errors)} error(s)):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(
    f"Canonical map validation passed. "
    f"{len(data.get('symbols', []))} symbol(s) verified."
)
```

---

### 6.6 `check_import_boundaries.py`

**Purpose:** Enforce the "no deep imports" policy. Scans each import line individually. Allowlist is path-based — determined by where a file lives, not by what else it imports.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: check_import_boundaries.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Import boundary enforcement.

Scans every .py file line by line. Flags any import statement containing
a forbidden deep import prefix.

Allowlist is path-based. A file containing both a forbidden import AND
a facade import is still flagged — exemption is determined solely by
the file's location (path segments), not its content.

Outputs:
  Exit 0 if no violations.
  Exit 1 with violation list if any are found.
"""

import sys
from pathlib import Path

# Canonical forbidden prefix registry — see Blueprint Section 5.5
FORBIDDEN_PREFIXES = [
    "LOGOS_SYSTEM.RUNTIME_CORES",
    "LOGOS_SYSTEM.RUNTIME_OPPERATIONS_CORE",
    "LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT",
    "LOGOS_SYSTEM.Runtime_Spine",
    "LOGOS_SYSTEM.STARTUP",
]

ALLOWLISTED_PATH_SEGMENTS = {"Canonical_Import_Facade", "Import_Facade"}
EXCLUDE_DIRS = {".venv", "site-packages", "__pycache__", ".git"}

violations: list[dict] = []

for file in sorted(Path(".").rglob("*.py")):
    if any(ex in file.parts for ex in EXCLUDE_DIRS):
        continue
    if any(seg in file.parts for seg in ALLOWLISTED_PATH_SEGMENTS):
        continue

    try:
        lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        continue

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not (stripped.startswith("import ") or stripped.startswith("from ")):
            continue
        for prefix in FORBIDDEN_PREFIXES:
            if prefix in stripped:
                violations.append({
                    "file": str(file),
                    "line": lineno,
                    "content": stripped,
                    "forbidden_prefix": prefix,
                })

if violations:
    print(f"Import boundary violations detected: {len(violations)}")
    for v in violations:
        print(f"  {v['file']}:{v['line']} — {v['content']}")
    sys.exit(1)

print("Import boundary validation passed.")
```

---

### 6.7 `check_facade_integrity.py`

**Purpose:** Verify that facade modules contain only imports, `__all__`, and docstrings. No logic, classes, or functions may accumulate in the facade layer.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: check_facade_integrity.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Facade module integrity check.

Verifies that all .py files in Canonical_Import_Facade/ (excluding
__init__.py) contain only:
  - import statements        (ast.Import, ast.ImportFrom)
  - __all__ assignments      (ast.Assign)
  - module-level docstrings  (ast.Expr)

Any other top-level node type is a violation.

Outputs:
  Exit 0 on pass.
  Exit 1 with violation list on failure.
"""

import ast
import sys
from pathlib import Path

FACADE_DIR           = Path("LOGOS_SYSTEM/Canonical_Import_Facade")
PERMITTED_NODE_TYPES = (ast.Import, ast.ImportFrom, ast.Assign, ast.Expr)

violations: list[str] = []

for file in sorted(FACADE_DIR.glob("*.py")):
    if file.name == "__init__.py":
        continue

    try:
        tree = ast.parse(file.read_text(encoding="utf-8"))
    except SyntaxError as e:
        violations.append(f"{file}: SyntaxError — {e}")
        continue

    for node in tree.body:
        if not isinstance(node, PERMITTED_NODE_TYPES):
            violations.append(
                f"{file}:{node.lineno} — Non-permitted node type: {type(node).__name__}"
            )

if violations:
    print(f"Facade integrity violations: {len(violations)}")
    for v in violations:
        print(f"  {v}")
    sys.exit(1)

print("Facade integrity verified.")
```

---

### 6.8 `detect_import_drift.py`

**Purpose:** Snapshot deep import occurrences and detect new ones in future CI runs. Tracks all forbidden prefixes from the canonical registry.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: detect_import_drift.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Import drift detection.

First run  : records all files containing forbidden deep imports as the
             authoritative snapshot.
Subsequent : compares current state against the snapshot. Any file not
             present in the snapshot that now contains a forbidden import
             is flagged as drift.

Allowlisted path segments are exempt from tracking.

Outputs:
  _Reports/Canonical_Import_Facade/import_snapshot.json  (written/updated)
  Exit 0 on pass.
  Exit 1 if new drift is detected.
"""

import json
import sys
from pathlib import Path

# Canonical forbidden prefix registry — see Blueprint Section 5.5
FORBIDDEN_PREFIXES = [
    "LOGOS_SYSTEM.RUNTIME_CORES",
    "LOGOS_SYSTEM.RUNTIME_OPPERATIONS_CORE",
    "LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT",
    "LOGOS_SYSTEM.Runtime_Spine",
    "LOGOS_SYSTEM.STARTUP",
]

ALLOWLISTED_PATH_SEGMENTS = {"Canonical_Import_Facade", "Import_Facade"}
EXCLUDE_DIRS = {".venv", "site-packages", "__pycache__", ".git"}

SNAPSHOT_FILE = Path("_Reports/Canonical_Import_Facade/import_snapshot.json")

current: dict[str, list[str]] = {}

for file in sorted(Path(".").rglob("*.py")):
    if any(ex in file.parts for ex in EXCLUDE_DIRS):
        continue
    if any(seg in file.parts for seg in ALLOWLISTED_PATH_SEGMENTS):
        continue

    try:
        text = file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue

    hits = [p for p in FORBIDDEN_PREFIXES if p in text]
    if hits:
        current[str(file)] = hits

if SNAPSHOT_FILE.exists():
    previous: dict[str, list[str]] = json.loads(
        SNAPSHOT_FILE.read_text(encoding="utf-8")
    )
    new_violations = {f: hits for f, hits in current.items() if f not in previous}

    if new_violations:
        print(f"Import drift detected: {len(new_violations)} new file(s) with deep imports.")
        for f, hits in new_violations.items():
            print(f"  {f}: {hits}")
        sys.exit(1)

    print(
        f"No import drift detected. "
        f"Snapshot baseline: {len(previous)} file(s). "
        f"Current: {len(current)} file(s)."
    )
else:
    print(f"No snapshot found. Writing initial snapshot ({len(current)} file(s)).")

SNAPSHOT_FILE.write_text(json.dumps(current, indent=2), encoding="utf-8")
```

---

### 6.9 `runtime_import_smoke.py`

**Purpose:** Detect modules with broken imports by attempting `importlib.import_module`. Scoped to known importable package roots only. **Not in the default CI workflow** — deploy only after baseline health assessment.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: runtime_import_smoke.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Runtime import smoke test.

Attempts importlib.import_module() for all modules under known importable
package roots. Excludes test files, DRAC, and non-package scripts.

NOT in the default CI workflow. Evaluate against baseline health before
adding to CI automation.

Outputs:
  _Reports/Canonical_Import_Facade/Import_Smoke_Report.json
  Exit 0 on pass.
  Exit 1 if any import failures are detected.
"""

import importlib
import json
import sys
from pathlib import Path

REPORT_DIR = Path("_Reports/Canonical_Import_Facade")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

IMPORTABLE_ROOTS = {"LOGOS_SYSTEM"}
EXCLUDE_DIRS     = {".venv", "site-packages", "__pycache__", ".git", "tests", "DRAC"}

failures: list[dict] = []
passed = 0

for file in sorted(Path(".").rglob("*.py")):
    if any(ex in file.parts for ex in EXCLUDE_DIRS):
        continue
    if file.parts[0] not in IMPORTABLE_ROOTS:
        continue
    if file.name.startswith("test_") or file.name == "__main__.py":
        continue

    module_name = str(file.with_suffix("")).replace("/", ".").replace("\\", ".")

    try:
        importlib.import_module(module_name)
        passed += 1
    except Exception as e:
        failures.append({
            "module": module_name,
            "file": str(file),
            "error": str(e),
        })

(REPORT_DIR / "Import_Smoke_Report.json").write_text(
    json.dumps({"passed": passed, "failed": len(failures), "failures": failures}, indent=2),
    encoding="utf-8",
)

print(f"Import smoke test: {passed} passed, {len(failures)} failed.")

if failures:
    print("Import failures detected — see Import_Smoke_Report.json.")
    sys.exit(1)
```

---

### 6.10 `report.py`

**Purpose:** Consolidated summary of all report artifacts in `_Reports/Canonical_Import_Facade/`.

```python
# ============================================================
# LOGOS — Canonical Import Facade
# File: report.py
# Layer: Import_Infrastructure / Tools
# Authority: LOGOS_Import_Infrastructure
# Mutability: Manual revision only
# Execution_Status: Tooling
# Governed_By: BLUEPRINTS/Canonical_Import_Facade_Blueprint.md
# ============================================================

#!/usr/bin/env python3

"""
Consolidated report summary.

Reads all .json files in _Reports/Canonical_Import_Facade/ and
aggregates them into a single Summary_Report.json.

Outputs:
  _Reports/Canonical_Import_Facade/Summary_Report.json
"""

import json
from pathlib import Path

REPORT_DIR = Path("_Reports/Canonical_Import_Facade")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

summary: dict = {}

for report_file in sorted(REPORT_DIR.glob("*.json")):
    if report_file.name == "Summary_Report.json":
        continue
    try:
        summary[report_file.name] = json.loads(report_file.read_text(encoding="utf-8"))
    except Exception as e:
        summary[report_file.name] = {"error": str(e)}

(REPORT_DIR / "Summary_Report.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)

print(f"Summary report generated. Reports included: {len(summary)}")
```

---

## 7. GitHub Actions CI Integration

Add the following workflow to `.github/workflows/import_facade.yml`.

```yaml
name: Import Facade Enforcement

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  import-facade:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Compile Check
        run: python Tools/Import_Facade/validate_facade.py

      - name: Canonical Map Validation
        run: python Tools/Import_Facade/validate_canonical_map.py

      - name: Import Boundary Enforcement
        run: python Tools/Import_Facade/check_import_boundaries.py

      - name: Import Drift Detection
        run: python Tools/Import_Facade/detect_import_drift.py

      - name: Facade Integrity Check
        run: python Tools/Import_Facade/check_facade_integrity.py
```

`runtime_import_smoke.py` is not included in the default workflow. Add it manually or as an optional step after baseline health assessment is complete.

---

## 8. Phased Implementation Plan

### Phase A — Inventory and Classification

**Steps:**
1. Run `build_facade.py` (dry-run)
2. Review `Canonical_Candidate_List.json` — prioritize runtime entrypoints
3. Review `Ambiguity_Report.json` — manually adjudicate or exclude each ambiguous symbol

**Outputs:** `Import_Inventory.json`, `Canonical_Candidate_List.json`, `Ambiguity_Report.json`

**Fail-closed condition:** Any symbol with more than one candidate `internal_module` must not proceed until manually resolved.

---

### Phase B — Canonical Map Approval

**Steps:**
1. Manually populate `Canonical_Map.json` from Phase A candidates
2. Run `validate_canonical_map.py` — verify all `internal_module` paths resolve on disk
3. Obtain explicit operator sign-off before proceeding

**Outputs:** Approved and validated `Canonical_Map.json`

**Gate:** Map must be non-empty and pass validation. No downstream phase may proceed without this gate.

---

### Phase C — Facade Skeleton Construction

**Steps:**
1. Create `LOGOS_SYSTEM/Canonical_Import_Facade/` and `Documentation/` subdirectory
2. Create `__init__.py` (canonical header, empty body)
3. Create facade domain modules with canonical headers and empty `__all__`
4. Populate facade modules from approved `Canonical_Map.json` entries
5. Create `Documentation/METADATA.json` declaring `tier: Import_Infrastructure`
6. Run `check_facade_integrity.py` to verify no logic entered facade modules

**Outputs:** Populated facade package; `Documentation/METADATA.json`

---

### Phase D — CI Enforcement Activation *(before replacement)*

**Steps:**
1. Run `detect_import_drift.py` once against the unmodified repo to generate the initial `import_snapshot.json`
2. Commit `import_snapshot.json`
3. Add and push `.github/workflows/import_facade.yml`
4. Verify all CI steps pass against the current (pre-replacement) repo state

**Outputs:** Active CI workflow; committed drift snapshot

**Rationale:** CI enforcement must be active before replacement runs. If enabled after, the drift detection has no pre-replacement baseline and cannot distinguish migration-time changes from new violations introduced later.

---

### Phase E — Import Replacement

**Steps:**
1. Run `replace_imports.py` (dry-run) — review `Replacement_Report.json` and `Replacement_Log.json`
2. Confirm no unintended replacements in the diff
3. Run `replace_imports.py --apply`
4. Verify `Replacement_Log.json` was written — required rollback precondition

**Outputs:** Modified source files; `Replacement_Report.json`; `Replacement_Log.json`

**Rollback:** Run `rollback_imports.py` (dry-run to verify), then `rollback_imports.py --apply`. The script verifies every targeted line before writing and halts on any mismatch. Partial rollback is never performed.

---

### Phase F — Post-Change Validation

**Steps:**
1. Run `validate_facade.py` — compare compile failures against Phase B baseline; new failures are regressions
2. Run `check_import_boundaries.py` — confirm no forbidden deep imports remain outside allowlisted paths
3. Run `report.py` — generate consolidated summary
4. Refresh drift snapshot: run `detect_import_drift.py` once more to commit the post-replacement baseline

**Outputs:** `Compile_Report.json` (post-change), `Summary_Report.json`, updated `import_snapshot.json`

---

### Deliverable File Map

| Artifact | Path |
|---|---|
| This blueprint | `BLUEPRINTS/Canonical_Import_Facade_Blueprint.md` |
| Canonical map | `LOGOS_SYSTEM/Canonical_Import_Facade/Canonical_Map.json` |
| Facade package | `LOGOS_SYSTEM/Canonical_Import_Facade/` |
| Tooling scripts | `Tools/Import_Facade/` |
| CI workflow | `.github/workflows/import_facade.yml` |
| Reports | `_Reports/Canonical_Import_Facade/` |
| Symbol mapping doc | `BLUEPRINTS/Canonical_Import_Facade_Mapping.md` *(authored post-Phase B)* |

---

### Deferred to V1.1

| Item | Reason |
|---|---|
| `ast.unparse()` full-tree rewriting | Destroys comments and file formatting; AST-guided line replacement is correct and sufficient at V1 |
| Import graph visualization | Useful, not required for correctness |
| Circular dependency detection | Additive enhancement to `build_facade.py` |
| `runtime_import_smoke.py` in CI | Requires baseline health assessment first |
| `LOGOS_EXTERNALIZATION/` import coverage | Projection-only layer; no runtime import coupling expected |
| Symbol retirement protocol | Schema stable at V1; retirement workflow needed when map matures |

---

## 9. Acceptance Criteria

The Canonical Import Facade implementation is accepted when all of the following are true:

1. `validate_facade.py` passes with zero new compile failures relative to the Phase B baseline
2. `validate_canonical_map.py` passes — all symbols have required fields and all `internal_module` paths resolve to existing files on disk
3. `check_import_boundaries.py` passes — zero forbidden deep import violations outside allowlisted directories
4. `check_facade_integrity.py` passes — no logic present in any facade module
5. `detect_import_drift.py` passes — post-replacement drift snapshot committed
6. GitHub Actions workflow is active and passing on the main branch
7. Key runtime path (`RuntimeLoop` or V1 smoke equivalent) resolves through the facade without error

---

## 10. Maintenance Protocol

**Adding a symbol:** Manually edit `Canonical_Map.json`. Update `last_reviewed`. Add the export to the appropriate facade module and update `__all__`. Run `validate_canonical_map.py`.

**Renaming or moving an internal module:** Update `Canonical_Map.json` `internal_module` field. Update the facade module import. Run `validate_canonical_map.py`. Consumer imports are unaffected — this is the primary operational benefit of the facade.

**Retiring a symbol:** Remove from `Canonical_Map.json`. Remove from the facade module `__all__`. Consumers receive an `ImportError` at compile time. Resolve by migrating consumers to a replacement symbol before retiring.

**Adding a forbidden prefix:** Requires a blueprint revision (version bump). Update `FORBIDDEN_PREFIXES` in `check_import_boundaries.py` and `detect_import_drift.py` in the same commit. Update `Canonical_Map.json` `last_reviewed`.

**Periodic drift snapshot refresh:** After any batch migration or refactor, commit an updated `import_snapshot.json` as the new baseline.
