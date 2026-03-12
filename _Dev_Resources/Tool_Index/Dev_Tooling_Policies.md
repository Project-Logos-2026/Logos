# Dev Tooling Policies
**Version:** 2.0  
**Generated:** 2026-03-11  
**Authority:** Canonical Dev Tooling Migration — ARCH_PRIME / Import_Facade consolidation

---

## 1. Tool Placement Rules

### 1.1 Canonical Root
All dev tooling scripts must reside under:

```
/workspaces/Logos/_Dev_Resources/_Dev_Scripts/Repo_Tools/
```

No scripts may live directly in `_Dev_Scripts/` or in ad-hoc subdirectories
outside of `Repo_Tools/`.

### 1.2 Classification-Based Placement
Every script must be placed according to its **functional classification**,
not its file name or origin directory. Permitted classifications and their
canonical locations:

| Classification         | Directory                              | Purpose |
|------------------------|----------------------------------------|---------|
| `Repo_Audit`           | `Repo_Tools/Repo_Audit/`               | Repository scanning, import linting, structure export |
| `Static_Analysis`      | `Repo_Tools/Static_Analysis/`          | AST parsing, symbol extraction, layer classification |
| `Dependency_Analysis`  | `Repo_Tools/Dependency_Analysis/`      | Import graph clustering, facade synthesis, violation scanning |
| `Migration`            | `Repo_Tools/Migration/`                | File relocation and categorical reorganization passes |
| `Code_Extraction`      | `Repo_Tools/Code_Extraction/`          | Function and registry extraction from source |
| `Architecture_Validation` | `Repo_Tools/Architecture_Validation/` | Structural and governance conformance checks |
| `Runtime_Diagnostics`  | `Repo_Tools/Runtime_Diagnostics/`      | Live runtime analysis and health probing |
| `Report_Generation`    | `Repo_Tools/Report_Generation/`        | Pipeline orchestration and artifact report writing |
| `Dev_Utilities`        | `Repo_Tools/Dev_Utilities/`            | Shared utilities, conftest, smoke tests, package init |

### 1.3 Protected Directories
The following directories must **never** be modified by tooling operations
or migration passes:

- `_Dev_Scripts/P1-5/` — Phase 1–5 scripts, lifecycle-frozen
- `_Dev_Scripts/RGE/` — Reasoning Governance Engine scripts, governance-controlled

### 1.4 Directory Naming Convention
All directory names must follow `Title_Case_With_Underscores`. No lowercase,
no abbreviations, no spaces.

---

## 2. Tool Registry Maintenance Rules

### 2.1 Registry Files
Three canonical artifacts must always be kept synchronized:

| Artifact | Location | Purpose |
|----------|----------|---------|
| `dev_scripts_manifest.json` | `Tool_Index/` | Per-tool metadata: path, classification, capabilities, dependencies, artifacts |
| `dev_tool_registry.json`    | `Tool_Index/` | Full functional registry with invocation patterns, entrypoints, function lists |
| `dev_tool_capability_index.json` | `Tool_Index/` | Inverted capability-to-tool index and category summary |

### 2.2 When Registry Must Be Updated
The Tool Index must be regenerated whenever:

- A new script is added to `Repo_Tools/`
- An existing script is moved between subdirectories
- An existing script's functionality changes materially
- A script is deprecated or removed

### 2.3 Registry Ownership
No script may be added to `Repo_Tools/` without a corresponding entry in
all three Tool Index artifacts. Unregistered scripts are treated as
non-canonical and must not be invoked by any automation system.

---

## 3. Mutation / Destructive Tool Confirmation Protocol

### 3.1 Destructive Tool Definition
A tool is classified as destructive if it is capable of any of:
- Moving, renaming, or deleting files
- Rewriting source file content
- Modifying import statements
- Executing automatic refactoring

Current destructive tools: `triage`, `facade_rewrite_pass`, `reorganize`

### 3.2 Pre-Execution Protocol

Before executing any destructive tool:

1. **Confirm the target scope** — identify which files or directories will
   be affected and verify no protected paths are included.
2. **Run dry-run mode** — where available, always execute with `--dry-run`
   first and review the diff output.
3. **Capture a snapshot** — verify the current state via `git status` or
   equivalent before any live pass.
4. **Explicit approval** — destructive passes must be explicitly approved
   before execution. Autonomous triggering of destructive tools is forbidden.
5. **Post-pass verification** — after any live pass, verify output artifacts
   and confirm no unintended files were affected.

### 3.3 Fail-Closed Requirement
Destructive tools must implement fail-closed behavior: if any precondition
fails, the tool must write a failure report and exit non-zero without making
changes.

---

## 4. Index Regeneration Requirements

### 4.1 Triggering Events
The Tool Index must be regenerated after any of:
- Script migration between subdirectories
- Addition of new scripts
- Removal or deprecation of scripts
- Changes to classification of an existing script

### 4.2 Regeneration Order
Regenerate in this order to preserve consistency:

1. `dev_scripts_manifest.json` (source of truth for capabilities)
2. `dev_tool_registry.json` (derived from manifest + script inspection)
3. `dev_tool_capability_index.json` (derived from manifest)

### 4.3 Validation After Regeneration
After regeneration, verify:
- All scripts in `Repo_Tools/` appear in the manifest
- All manifest entries have a corresponding `Repo_Tools/` file
- The capability index contains no orphaned capability references

---

## 5. Session Enforcement Rules

### 5.1 No Ad-Hoc Script Placement
Scripts must not be placed in temporary or ad-hoc directories during a work
session. All scripts must go into the appropriate `Repo_Tools/` subdirectory
immediately.

### 5.2 No Silent Mutations
Any session that executes a destructive tool must log the operation to
`Systm_Audit_Logs/` before and after execution.

### 5.3 Index Coherence Check
Any automated session that operates on `Repo_Tools/` scripts must verify
Tool Index coherence at session start and regenerate if stale.

### 5.4 Governance Boundary
Dev tooling scripts must not cross the governance boundary:
- No dev tool may import from `LOGOS_SYSTEM.Governance` or `_Governance`
  at runtime
- No dev tool may write to `LOGOS_SYSTEM/` directories
- No dev tool may execute runtime modules

---

*Policy version 2.0 — established as part of canonical Dev Tooling Migration, 2026-03-11*
