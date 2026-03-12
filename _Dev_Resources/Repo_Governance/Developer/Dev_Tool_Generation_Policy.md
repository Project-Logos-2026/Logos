# Dev_Tool_Generation_Policy

**Governance Domain:** Developer  
**Scope:** `Dev_Tools/Runtime_Tools/`, `Dev_Tools/Repo_Governance_Tools/`  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Developer  

---

## 1. Purpose

This document governs the generation, naming, placement, and compliance requirements for all new dev tooling scripts created inside `_Dev_Resources/Dev_Tools/`. It applies to Runtime_Tools and Repo_Governance_Tools alike.

---

## 2. Canonical Tool Categories

| Category | Path | Schema Reference |
|---|---|---|
| Runtime_Tools | `Dev_Tools/Runtime_Tools/<subcategory>/` | `Header_Schemas/runtime_tool_header_schema.json` |
| Repo_Governance_Tools | `Dev_Tools/Repo_Governance_Tools/` | `Header_Schemas/repo_governance_tool_header_schema.json` |

### 2.1 Runtime_Tools Subcategories

| Subcategory | Purpose |
|---|---|
| `Architecture_Validation/` | Static architectural boundary and import validation |
| `Code_Extraction/` | AST and source code extraction |
| `Dependency_Analysis/` | Import graph and dependency edge analysis |
| `Dev_Utilities/` | General dev workflow helpers |
| `Migration/` | Module reorganization and migration |
| `Repo_Audit/` | Repository structure and import auditing |
| `Report_Generation/` | Report assembly and formatting |
| `Runtime_Diagnostics/` | Live and static runtime diagnostics |
| `Static_Analysis/` | Syntax, lint, and structural static analysis |

---

## 3. Naming Rules

- All new tool filenames MUST use `Title_Case_With_Underscores`.
- Abbreviations in filenames MUST be ALL-CAPS (e.g., `AST_Walker.py`, `Import_Linter.py`).
- The filename MUST exactly match the `tool_name` field in the file's header.
- No renaming after creation without:
  1. Header `tool_name` update.
  2. Tool_Index registry update.
  3. Logged rename event.

---

## 4. Header Compliance

Every generated tool MUST include a `RUNTIME_TOOL_METADATA` docstring at the top of the file containing all fields required by the applicable header schema.

### 4.1 Runtime_Tool Required Fields (from `runtime_tool_header_schema.json`)

```
tool_name           — Must match filename (no extension)
tool_category       — Top-level category (e.g., "Runtime_Tools")
tool_subcategory    — Subcategory dir name (e.g., "Architecture_Validation")
purpose             — One-sentence description
authoritative_scope — Which repo areas this tool analyzes
mutation_capability — true/false
destructive_capability — true/false
requires_repo_context  — true/false
cli_entrypoint      — argparse entry function
output_artifacts    — list of output filenames
dependencies        — list of Python stdlib or local imports
safety_classification — "READ_ONLY" | "WRITE_SAFE" | "DESTRUCTIVE"
```

### 4.2 Repo_Governance_Tool Required Fields (from `repo_governance_tool_header_schema.json`)

```
tool_name
governance_scope
policy_dependencies
purpose
mutation_capability
destructive_capability
requires_repo_context
cli_entrypoint
output_artifacts
```

---

## 5. Output Routing

All Runtime_Tool and Repo_Governance_Tool output artifacts MUST route to:

```
/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime/
```

Each tool must include:

```python
OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(data, f, indent=2)
```

No tool may write output to an arbitrary path, `TOOLS_DIR`, `REPO_ROOT`, or any relative path.

---

## 6. CLI Entrypoint Rules

- Every tool MUST expose a CLI via `argparse`.
- No interactive prompts permitted.
- Default values MUST be safe (no destructive defaults).
- `if __name__ == "__main__": main()` pattern is mandatory.

---

## 7. Import Rules

- No wildcard imports (`from module import *`).
- All imports must be explicit.
- Standard library imports only, unless a dependency is declared in `requirements.txt`.
- Import ordering: stdlib → third-party → local.

---

## 8. Determinism Requirements

- Tool output must be deterministic for identical inputs.
- No randomness, no environment-dependent formatting (e.g., no unsorted dicts in output).
- JSON output must use `indent=2` and consistent key ordering.
- Where keys are dynamic, sort them before writing.

---

## 9. Tool Index Registration

Every new tool MUST be registered in:

```
_Dev_Resources/Tool_Index/dev_tool_registry.json
_Dev_Resources/Tool_Index/dev_tool_capability_index.json
```

Registration must occur at the same time as tool creation, not after.

---

## 10. Safety Classification

Every tool must carry an explicit safety classification:

| Class | Meaning |
|---|---|
| `READ_ONLY` | No filesystem writes except to canonical output path |
| `WRITE_SAFE` | Writes to canonical output path only |
| `DESTRUCTIVE` | Modifies, deletes, or moves source files |

Destructive tools MUST also appear in `_Dev_Resources/Tool_Index/destructive_tools_index.json`.

---

## 11. Cross-References

| Document | Location |
|---|---|
| runtime_tool_header_schema.json | `Repo_Governance/Header_Schemas/` (FROZEN) |
| repo_governance_tool_header_schema.json | `Repo_Governance/Header_Schemas/` (FROZEN) |
| Naming_Convention_Enforcement.md | `Repo_Governance/Runtime/` |
| Dev_Resources_Directory_Contract.md | `Repo_Governance/Developer/` |
| dev_tool_registry.json | `Tool_Index/` |
