# Naming_Convention_Enforcement

**Governance Domain:** Runtime  
**Scope:** All files, directories, identifiers, and artifacts within the LOGOS repository  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Runtime  
**Note:** Developer-level naming rules are defined in `Repo_Governance/Developer/Development_Rules.json` (§naming). This document extends those rules with runtime-specific enforcement detail. Do not duplicate content from Development_Rules.json.

---

## 1. Purpose

This document defines the canonical naming conventions for all runtime modules, dev tool scripts, governance artifacts, directory names, Python identifiers, and output artifacts in the LOGOS repository. It extends and enforces the naming rules defined in `Development_Rules.json`.

---

## 2. File and Directory Naming

### 2.1 General Rule

> All new files and directories under governed roots MUST use `Title_Case_With_Underscores`.

| Element | Rule | Example |
|---|---|---|
| Runtime module files | `Title_Case_With_Underscores.py` | `Runtime_Module_Tree_Auditor.py` |
| Dev tool scripts | `Title_Case_With_Underscores.py` | `Import_Violation_Classifier.py` |
| Governance documents | `Title_Case_With_Underscores.md` | `Naming_Convention_Enforcement.md` |
| JSON artifacts | `snake_case_report.json` | `import_linter_report.json` |
| JSON Lines indexes | `snake_case_index.jsonl` | `import_graph_index.jsonl` |
| Directories | `Title_Case_With_Underscores` | `Runtime_Diagnostics/` |

**Exception:** JSON and JSONL output files use `snake_case` (lowercase with underscores) because they are machine-generated report artifacts, not source code.

### 2.2 Abbreviations in Filenames

Abbreviations appearing in file or directory names MUST be ALL-CAPS:

| Correct | Incorrect |
|---|---|
| `AST_Walker.py` | `Ast_Walker.py` |
| `Import_Linter.py` | `Import_linter.py` |
| `RGE_Auditor.py` | `Rge_Auditor.py` |
| `LOGOS_SYSTEM/` | `Logos_System/` (if it appears as an abbreviation context) |

Abbreviation expansions must be verified against:
```
_Dev_Resources/Repo_Governance/Runtime/Abbreviations.json
```

### 2.3 Header Name Field Must Match Filename

For all Python tool scripts and runtime modules:

- The `tool_name` (Runtime_Tools header) or `module_name` (runtime module header) MUST exactly match the filename without extension.
- Renames require a synchronized header update.

---

## 3. Python Identifier Naming

### 3.1 Classes

- `PascalCase` — e.g., `RuntimeModuleAuditor`, `ImportEdgeScanner`
- Abbreviations within class names: ALL-CAPS — e.g., `ASTWalker`, `RGEAgent`

### 3.2 Functions and Methods

- `snake_case` — e.g., `extract_import_edges()`, `write_report()`
- Abbreviations within function names follow the same pattern as module-level: stay ALL-CAPS within snake context — e.g., `build_ast_graph()`, `parse_rge_packet()`

### 3.3 Constants

- `ALL_CAPS_WITH_UNDERSCORES` — e.g., `OUTPUT_ROOT`, `SCHEMA_VERSION`, `FAIL_CLOSED`

### 3.4 Variables

- `snake_case` — e.g., `import_edges`, `call_path_index`, `output_root`

### 3.5 Module-Level Names

- Module filename (without `.py`) is the canonical module name; it must be `Title_Case_With_Underscores`.

---

## 4. Governance Artifact Naming

| Artifact Type | Convention | Example |
|---|---|---|
| Governance `.md` documents | `Title_Case_With_Underscores.md` | `Dev_Resources_Freeze_Protocol.md` |
| JSON governance configs | `Title_Case_With_Underscores.json` | `Development_Rules.json` |
| JSON schema files | `snake_case_schema.json` | `runtime_tool_header_schema.json` |
| Report files | `snake_case_report.json` | `governance_artifact_generation_report.json` |

---

## 5. Benchmark — Existing Repository Patterns

The following patterns from existing files establish the naming benchmark:

| Existing File | Pattern |
|---|---|
| `LOGOS_SYSTEM/__init__.py` | ALL-CAPS abbreviation in directory name |
| `Dev_Tools/Runtime_Tools/Repo_Audit/Import_Linter.py` | `Title_Case_With_Underscores.py` |
| `Repo_Governance/Header_Schemas/runtime_tool_header_schema.json` | `snake_case_schema.json` |
| `_Dev_Resources/Repo_Governance/Developer/Development_Rules.json` | `Title_Case_With_Underscores.json` |
| `_Dev_Resources/Reports/Tool_Outputs/Runtime/` | `Title_Case_With_Underscores/` |

All new files and directories must conform to the pattern established by these existing examples.

---

## 6. Prohibited Naming Patterns

The following naming patterns are prohibited:

| Pattern | Reason |
|---|---|
| `camelCase` for files or directories | Not canonical for LOGOS |
| `lowercase_only` for source modules | Violates Title_Case rule |
| `ALLCAPS_FILENAME.py` for source files (non-abbreviation) | Reserved for constants and Coq artifacts only |
| Mixed conventions in a single name (`Import_linter.py`) | Violates consistency |
| Spaces in filenames | Prohibited universally |
| Special characters (`!`, `@`, `#`, etc.) in names | Prohibited universally |

---

## 7. Enforcement Process

During automated normalization (Phase 5 Rewrite Contract):

1. Every identifier, filename, and directory name is checked against these rules.
2. Violations trigger the rewrite escalation path in `Development_Rules.json → automated_normalization_appendix → rewrite_threshold`.
3. Mixed or conflicting naming in a single file is escalated to FULL REWRITE.
4. Corrections must be deterministic: same input → same corrected output.

---

## 8. Cross-References

| Document | Location |
|---|---|
| Development_Rules.json (§naming) | `Repo_Governance/Developer/Development_Rules.json` |
| Abbreviation_Usage_Policy.md | `Repo_Governance/Runtime/` |
| Abbreviations.json | `Repo_Governance/Runtime/Abbreviations.json` |
