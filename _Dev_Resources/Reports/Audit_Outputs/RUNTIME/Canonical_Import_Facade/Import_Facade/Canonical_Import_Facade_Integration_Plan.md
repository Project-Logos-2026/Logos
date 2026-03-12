# Canonical Import Facade — Integration Plan

---

## Governance Header

| Field | Value |
|---|---|
| Artifact | `Canonical_Import_Facade_Integration_Plan.md` |
| Canonical Path | `/workspaces/Logos/BLUEPRINTS/Canonical_Import_Facade_Integration_Plan.md` |
| Authority Source | `Canonical_Import_Facade_Blueprint.md` v1.1.1 |
| Mutability | Manual revision only — must stay in sync with blueprint version |
| Version | 1.0.0 |
| Audience | GPT (prompt engineering); VS Code / Codespaces (execution) |

---

## Purpose and Usage

This plan translates the blueprint into a sequenced, prompt-ready execution workflow. It is the operational layer on top of the blueprint — not an authority unto itself.

**GPT role:** Use this plan to engineer implementation prompts. Each prompt you produce must cite:
- The specific integration plan phase being addressed
- The corresponding blueprint section(s) by number
- Exact artifact names and output paths as specified in the blueprint

**VS Code / executor role:** Execute prompts against the live repo. Treat the blueprint as the authoritative specification. Treat this plan as the sequencing and batching guide. If a prompt and the blueprint disagree, the blueprint wins and GPT must be corrected.

**Five JSON artifacts provided alongside this plan:**
- `repo_directory_tree.json` — canonical spelling authority for all paths and directory names
- `repo_imports.json` — line-level import inventory (source for preflight and violation detection)
- `repo_python_files.json` — complete Python file list
- `repo_symbol_imports.json` — symbol-to-module mapping (cross-check target for Phase 3)
- `Deep_Import_Violations.json` — pre-computed deep import violation set (primary dataset for Phase 7 replacement targeting)

Use exact file paths and line numbers from these artifacts in prompts wherever they add precision.

---

## Hard Gate — Phase 0 (Prerequisite, Non-Skippable)

**Objective:** Confirm authority set is canonical and internally consistent before any implementation begins.

**Steps:**

1. Confirm the blueprint file exists at its canonical path:
   `/workspaces/Logos/BLUEPRINTS/Canonical_Import_Facade_Blueprint.md`
   This is a flat file in `BLUEPRINTS/` — not a subdirectory.

2. Confirm the governance header version in the blueprint file reads `1.1.1`.
   Blueprint ref: **Governance Header table, line 17**.
   If the file shows any other version, stop. The blueprint copy is stale. Replace it with the v1.1.1 artifact.

3. Confirm the forbidden prefix registry in the blueprint (Section 5.5) contains `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` — NOT the invalid standalone `LOGOS_SYSTEM.RUNTIME_OPPERATIONS_CORE`.
   Verify against `repo_directory_tree.json`: the double-P directory appears at path `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/`, confirming the dotted import root is `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE`.

4. Once confirmed, treat the blueprint as immutable for this implementation run. Any future change requires an explicit version bump with diff review per **Blueprint Section 3, Constraint 6**.

**Gate condition:** Do not proceed to Phase 1 until all three confirmations pass.

---

## Phase 1 — Tooling Script Implementation

**Blueprint ref:** Section 6 (all subsections 6.1–6.10); Section 3 (constraints apply to all scripts)

**Objective:** Create the complete `Tools/Import_Facade/` script suite exactly as specified in the blueprint. No drift from script specifications.

**Target directory:**
```
Tools/Import_Facade/
    build_facade.py         # Blueprint Section 6.1
    replace_imports.py      # Blueprint Section 6.2
    rollback_imports.py     # Blueprint Section 6.3
    validate_facade.py      # Blueprint Section 6.4
    validate_canonical_map.py  # Blueprint Section 6.5
    check_import_boundaries.py # Blueprint Section 6.6
    check_facade_integrity.py  # Blueprint Section 6.7
    detect_import_drift.py  # Blueprint Section 6.8
    runtime_import_smoke.py # Blueprint Section 6.9
    report.py               # Blueprint Section 6.10
```

**Critical enforcement constraints (Blueprint Section 3):**
- All scripts must carry the canonical header exactly as specified in **Blueprint Section 5.2**
- Forbidden prefix registry in `check_import_boundaries.py` and `detect_import_drift.py` must match **Blueprint Section 5.5** exactly — including the corrected `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` entry
- `replace_imports.py` dry-run gate (Blueprint Section 6.2): must exit with error if `Canonical_Map.json` is absent or `symbols` array is empty — do not soften this check
- `rollback_imports.py` verification-first design (Blueprint Section 6.3): verification pass must complete before any file write; partial rollback is prohibited

**Prompt engineering note for GPT:** When prompting for each script, paste the blueprint section verbatim as the spec. Instruct VS Code to implement exactly what is in the spec with no additions, removals, or logic changes. Each script is a separate atomic prompt.

---

## Phase 2 — Inventory and Classification (Blueprint Phase A)

**Blueprint ref:** Section 8, Phase A

**Objective:** Generate the three Phase A output artifacts.

**Execution:**
```
cd /workspaces/Logos
python Tools/Import_Facade/build_facade.py
```

**Expected outputs in `_Reports/Canonical_Import_Facade/`:**
- `Import_Inventory.json` — all Python files + parse failures + symbol sources
- `Canonical_Candidate_List.json` — symbols imported from a single source >2 times, sorted by frequency
- `Ambiguity_Report.json` — symbols with multiple candidate source modules

**Cross-check step (halt condition):** Compare `Import_Inventory.json → symbol_sources` against `repo_symbol_imports.json`. If the tooling's symbol count differs from `repo_symbol_imports.json` by more than 10%, treat as a scanner misconfiguration. Do not proceed until the discrepancy is explained. This is an explicit halt condition per this plan.

**Fail-closed condition (Blueprint Section 8, Phase A):** Symbols in `Ambiguity_Report.json` must not appear in `Canonical_Map.json`. They are deferred until manually adjudicated.

---

## Phase 3 — Deep Import Violation Dataset (Pre-Map)

**Objective:** Establish `Deep_Import_Violations.json` as the authoritative target list for replacement. This artifact is not produced by `build_facade.py` — it is either provided pre-computed (as one of the five JSON artifacts) or generated as follows.

**If pre-computed:** Confirm `Deep_Import_Violations.json` was generated against the same forbidden prefix registry as **Blueprint Section 5.5** (must include `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE`; must not contain the invalid `LOGOS_SYSTEM.RUNTIME_OPPERATIONS_CORE`). If the registry used to generate it differs, regenerate.

**If generating fresh:** Cross-reference `repo_imports.json` against the blueprint's forbidden prefix list. For each import line in `repo_imports.json` that matches a forbidden prefix and is not in an allowlisted path segment (`Canonical_Import_Facade`, `Import_Facade`), emit an entry:
```json
{
  "file": "<path>",
  "line": <line_number>,
  "import_statement": "<raw import>",
  "matched_prefix": "<which forbidden prefix matched>"
}
```

**Output path:** `_Reports/Canonical_Import_Facade/Deep_Import_Violations.json`

**Purpose:** This dataset becomes the primary targeting list for Phase 7 replacement. GPT prompts for Phase 7 must reference specific entries from this file.

---

## Phase 4 — Canonical Map Authoring and Approval (Blueprint Phase B)

**Blueprint ref:** Section 8, Phase B; Section 5.4 (schema); Section 9 (acceptance criterion 2)

**Objective:** Manually populate `Canonical_Map.json` as a governance artifact.

**Rules (non-negotiable):**
- Populate only from `Canonical_Candidate_List.json` (unambiguous symbols only)
- Prioritize runtime entrypoints — `RuntimeLoop`, `NexusFactory`, agent wrappers, orchestration entry points
- Do not add any symbol from `Ambiguity_Report.json` until it has been manually adjudicated
- Schema must conform exactly to **Blueprint Section 5.4** — all six required top-level fields must be present
- `internal_module` for each entry must resolve to an existing `.py` file; run `validate_canonical_map.py` to verify

**Validation gate:**
```
python Tools/Import_Facade/validate_canonical_map.py
```
Must exit 0 before proceeding. This is an explicit acceptance criterion per **Blueprint Section 9, criterion 2**.

**Map location:** `LOGOS_SYSTEM/Canonical_Import_Facade/Canonical_Map.json`
**This file must not be written or modified by any automated script** — Blueprint Section 3, Constraint 6.

---

## Phase 5 — Facade Package Construction (Blueprint Phase C)

**Blueprint ref:** Section 8, Phase C; Sections 5.1–5.3 (directory structure, header, module pattern)

**Objective:** Create the `Canonical_Import_Facade/` package with correct structure and canonical headers.

**Target directory structure (Blueprint Section 5.1):**
```
LOGOS_SYSTEM/Canonical_Import_Facade/
    __init__.py
    runtime.py
    governance.py
    orchestration.py
    memory.py
    protocols.py
    types.py
    Canonical_Map.json           # already authored in Phase 4
    Documentation/
        GOVERNANCE_SCOPE.md
        MANIFEST.md
        METADATA.json            # must declare: tier: Import_Infrastructure
```

**Each `.py` file must:**
1. Begin with the canonical header from **Blueprint Section 5.2** (exact text, filename field filled in)
2. Contain only imports and `__all__` per the module pattern at **Blueprint Section 5.3**
3. Export only symbols present in the approved `Canonical_Map.json`

**Integrity verification:**
```
python Tools/Import_Facade/check_facade_integrity.py
```
Must exit 0 before proceeding.

**Prompt engineering note for GPT:** Each facade module is a separate prompt. Provide the `Canonical_Map.json` entries for the relevant domain as the symbol source. Provide the header spec from Blueprint Section 5.2 and the module pattern from Blueprint Section 5.3 as the structural spec.

---

## Phase 6 — CI Enforcement Activation (Blueprint Phase D)

**Blueprint ref:** Section 8, Phase D; Section 7 (workflow YAML)

**Objective:** Activate CI guardrails before any import replacement runs, so the pre-replacement state becomes the drift baseline.

**Ordering rationale (Blueprint Section 8, Phase D):** CI must be live before Phase 7 (replacement). If activated after replacement, `detect_import_drift.py` has no pre-replacement baseline and cannot distinguish migration changes from new violations.

**Steps:**

1. Generate initial drift snapshot:
   ```
   python Tools/Import_Facade/detect_import_drift.py
   ```
   This writes `_Reports/Canonical_Import_Facade/import_snapshot.json`. Commit this file.

2. Add workflow file at `.github/workflows/import_facade.yml` using exact YAML from **Blueprint Section 7**.

3. Push. Verify all five CI steps pass against the current (pre-replacement) repo state:
   - Compile Check (`validate_facade.py`)
   - Canonical Map Validation (`validate_canonical_map.py`)
   - Import Boundary Enforcement (`check_import_boundaries.py`)
   - Import Drift Detection (`detect_import_drift.py`)
   - Facade Integrity Check (`check_facade_integrity.py`)

4. Record compile baseline:
   ```
   python Tools/Import_Facade/validate_facade.py
   ```
   On first run this writes `Compile_Report_Baseline.json`. Commit it.

**Gate:** All five CI checks must pass before Phase 7 begins. If any fail, triage and resolve — they represent pre-existing violations that must be understood before replacement adds noise.

---

## Phase 7 — Controlled Import Replacement (Blueprint Phase E)

**Blueprint ref:** Section 8, Phase E; Section 6.2 (`replace_imports.py`); Section 6.3 (`rollback_imports.py`)

**Objective:** Replace deep imports with facade imports in small, auditable batches using `Deep_Import_Violations.json` as the targeting list and the approved `Canonical_Map.json` as the allowlist.

**Batching rule:** Do not replace more than 25 files per apply step. This keeps each diff reviewable and each `Replacement_Log.json` tractable for rollback. Batch boundaries should follow subsystem lines where possible (e.g., all CSP files in one batch, all EMP files in one batch).

**Per-batch execution sequence:**

Step 1 — Dry-run:
```
python Tools/Import_Facade/replace_imports.py
```
Review `Replacement_Report.json`. Verify:
- Only files present in `Deep_Import_Violations.json` for this batch appear in the report
- All `from` → `to` pairs match entries in `Canonical_Map.json`
- No unexpected files are listed

Step 2 — Apply:
```
python Tools/Import_Facade/replace_imports.py --apply
```
Verify `Replacement_Log.json` was written immediately after. This is the rollback precondition.

Step 3 — Immediate validation:
```
python Tools/Import_Facade/validate_facade.py
```
If new compile failures appear that were not in `Compile_Report_Baseline.json`, treat as regression. Roll back immediately.

Step 4 — Rollback (only if regression detected):
```
python Tools/Import_Facade/rollback_imports.py          # dry-run first
python Tools/Import_Facade/rollback_imports.py --apply
```
Per **Blueprint Section 6.3**: verification pass runs before any write; halts on line mismatch; partial rollback never occurs.

**GPT prompt engineering note:** For each batch prompt, reference the specific file list from `Deep_Import_Violations.json` (by file path and line number). Reference the exact `Canonical_Map.json` entries that cover the symbols being replaced. The prompt must not ask VS Code to infer or extend the map — only to execute against what the map already specifies.

---

## Phase 8 — Post-Change Validation and Acceptance Closure (Blueprint Phase F)

**Blueprint ref:** Section 8, Phase F; Section 9 (full acceptance criteria checklist)

**Objective:** Verify all acceptance criteria are met. Close the implementation.

**Acceptance criteria checklist (Blueprint Section 9, all seven criteria):**

| # | Criterion | Verification command |
|---|---|---|
| 1 | Zero new compile failures relative to baseline | `python Tools/Import_Facade/validate_facade.py` — no regressions |
| 2 | `validate_canonical_map.py` passes | `python Tools/Import_Facade/validate_canonical_map.py` |
| 3 | Zero boundary violations | `python Tools/Import_Facade/check_import_boundaries.py` |
| 4 | Zero facade integrity violations | `python Tools/Import_Facade/check_facade_integrity.py` |
| 5 | Drift snapshot committed post-replacement | `python Tools/Import_Facade/detect_import_drift.py` — then commit `import_snapshot.json` |
| 6 | GitHub Actions workflow passing on main branch | Check CI status after merge |
| 7 | Key runtime path resolves through facade | Manual smoke: `from LOGOS_SYSTEM.Canonical_Import_Facade.runtime import RuntimeLoop` (or V1 equivalent) |

**Final steps:**
1. Run `python Tools/Import_Facade/report.py` to generate `Summary_Report.json`
2. Commit `Summary_Report.json` and updated `import_snapshot.json`
3. Update `Canonical_Map.json → last_reviewed` field to today's date

All seven criteria must pass before the implementation is considered closed.

---

## Prompt Engineering Reference Card (for GPT)

| Phase | Blueprint Sections | Key JSON artifacts | Prompt focus |
|---|---|---|---|
| Phase 0 | Governance Header, §3 | `repo_directory_tree.json` | Authority confirmation; prefix registry verification |
| Phase 1 | §5.2, §6.1–6.10 | None | One script per prompt; paste blueprint spec verbatim |
| Phase 2 | §8 Phase A | `repo_symbol_imports.json`, `repo_python_files.json` | Run `build_facade.py`; cross-check output counts |
| Phase 3 | §5.5 | `repo_imports.json`, `repo_directory_tree.json` | Generate or validate `Deep_Import_Violations.json` |
| Phase 4 | §5.4, §8 Phase B, §9 criterion 2 | `Canonical_Candidate_List.json`, `Ambiguity_Report.json` | Manual map authoring; run `validate_canonical_map.py` |
| Phase 5 | §5.1–5.3, §8 Phase C | `Canonical_Map.json` | One facade module per prompt; run `check_facade_integrity.py` |
| Phase 6 | §7, §8 Phase D | None | Workflow YAML; drift snapshot; compile baseline |
| Phase 7 | §6.2, §6.3, §8 Phase E | `Deep_Import_Violations.json`, `Canonical_Map.json` | Batch ≤25 files; dry-run review; apply; immediate validate |
| Phase 8 | §9, §8 Phase F | All report JSONs | All 7 acceptance criteria; `Summary_Report.json` |

---

## Failure Modes and Halt Conditions

| Condition | Phase | Action |
|---|---|---|
| Blueprint version ≠ 1.1.1 | Phase 0 | Stop. Replace blueprint file. Do not proceed. |
| Forbidden prefix registry does not contain `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | Phase 0 | Stop. Blueprint copy is stale or corrupted. |
| `validate_canonical_map.py` exits non-zero | Phase 4 | Fix map errors before proceeding. |
| CI steps fail on clean repo (pre-replacement) | Phase 6 | Triage pre-existing violations. Do not begin replacement until clean. |
| New compile failures after batch apply | Phase 7 | Roll back immediately. Do not proceed to next batch. |
| `Replacement_Log.json` absent after `--apply` | Phase 7 | Do not proceed. Log write failure means rollback is unavailable. Investigate before continuing. |
| `rollback_imports.py` verification failures | Phase 7 rollback | Manual intervention required. Do not force rollback. Inspect `Rollback_Verification_Failures.json`. |
| Acceptance criterion 7 (runtime smoke) fails | Phase 8 | Implementation is not closed. Diagnose facade wiring before signing off. |
