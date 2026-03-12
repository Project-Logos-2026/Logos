# `_Dev_Resources` — Developer Resource Root

**Governance Authority:** `Repo_Governance/Developer/`  
**Scope:** `/workspaces/Logos/_Dev_Resources`  
**Status:** ACTIVE  
**Last Updated:** 2026-03-12

---

## Overview

`_Dev_Resources` is the canonical root for all developer-facing infrastructure in the Logos repository. It contains:

- **Active tooling** for repository auditing, static analysis, architecture validation, and code extraction (`Dev_Tools/`)
- **Governance policy documents** and header schemas that define rules for all tool and module generation (`Repo_Governance/`)
- **Repository inventory** — deterministic index and manifest artifacts capturing the runtime import and dependency graph (`Repo_Inventory/`)
- **Tool registry** and operational guides (`Tool_Index/`)
- **Processing pipeline** for normalizing, refactoring, and onboarding runtime content from external or legacy sources (`Processing_Center/`)
- **Developer notes** for supplementary policies outside the canonical governance layer (`Developer_Notes/`)

`_Dev_Resources` is **NOT** the runtime stack. Nothing here is imported by LOGOS_SYSTEM at runtime. All content here is either tooling, governance documentation, or pipeline staging material.

---

## Directory Structure

```
_Dev_Resources/
├── Dev_Tools/                       # All developer tooling scripts
│   ├── Archive/                     # Tier 1 HARD FROZEN — read-only historical scripts
│   │   ├── P1-5/                    # Archived P1–P5 migration and normalization scripts
│   │   └── RGE/                     # Archived RGE audit scripts
│   ├── Repo_Governance_Tools/       # Governance enforcement validators (8 scripts)
│   └── Runtime_Tools/               # Active runtime tooling — Tier 3 CONTROLLED MUTABLE
│       ├── Architecture_Validation/ # Import boundary and structural audits
│       ├── Code_Extraction/         # AST and source code extraction
│       ├── Dependency_Analysis/     # Import graph and dependency edge analysis
│       ├── Dev_Utilities/           # General dev workflow helpers and test utilities
│       ├── Migration/               # Module reorganization and migration
│       ├── Repo_Audit/              # Repository structure and import auditing
│       ├── Report_Generation/       # Report assembly and formatting
│       ├── Runtime_Diagnostics/     # Live and static runtime diagnostics
│       └── Static_Analysis/         # Syntax, lint, and structural static analysis
│
├── Developer_Notes/                 # Supplementary policy notes (non-canonical governance)
│
├── Processing_Center/               # Pipeline for normalizing / refactoring runtime content
│   ├── BLUEPRINTS/                  # Processing consumption artifacts (variable contents)
│   └── STAGING/                     # Modules and artifacts actively being processed
│       ├── In_Process/              # Items currently under active transformation
│       │   ├── EXTRACT_LOGIC/       # Logic fragments being extracted for reuse
│       │   ├── KEEP_VERIFY/         # Candidates for retention pending verification
│       │   └── NORMALIZE_INTGRATE/  # Items being normalized and integrated
│       ├── Inspection_Targets/      # Items queued for manual or automated inspection
│       ├── Post_Processing/         # Items that have completed pipeline processing
│       └── Pre-Processing/          # Items being categorized prior to pipeline entry
│           ├── agent/               # Agent-layer modules under pre-processing
│           ├── math/                # Math-layer modules under pre-processing
│           ├── reasoning/           # Reasoning modules under pre-processing
│           ├── safety/              # Safety modules under pre-processing
│           ├── semantic/            # Semantic modules under pre-processing
│           ├── utility/             # Utility modules under pre-processing
│           └── utils/               # Utility helpers under pre-processing
│
├── Repo_Governance/                 # Governance policy artifacts — authority layer
│   ├── Developer/                   # Developer environment governance documents
│   ├── Header_Schemas/              # Tier 1 HARD FROZEN — canonical header JSON schemas
│   └── Runtime/                     # Runtime module governance documents
│
├── Repo_Inventory/                  # Deterministic repository indexing — APPEND-ONLY
│   ├── Master_Indexes/
│   │   ├── Environment/             # Environment dependency indexes (JSONL)
│   │   └── Runtime/                 # Runtime wiring and import indexes (JSONL)
│   └── Master_Manifests/            # Full repository manifests
│
├── Tool_Index/                      # Tool registry, capability index, operational guides
│
└── Reports/                         # [RUNTIME OUTPUT ONLY — not README content]
```

> **Note:** `Reports/` is the output sink for all tooling runs. Its contents are generated artifacts, not canonical structure. It is excluded from this README.

---

## Component Reference

### `Dev_Tools/`

All developer scripting lives here. There are three sub-roots:

#### `Dev_Tools/Archive/` — Tier 1 Hard Frozen

Historical scripts from Phases 1–5 and the RGE audit campaign. These are immutable audit records. No modification, rename, or deletion is permitted. They exist as read-only reference material.

| Directory | Contents |
|---|---|
| `Archive/P1-5/` | 18 migration and normalization scripts from Phases 1–5 |
| `Archive/RGE/` | 7 RGE stage smoke test and audit runner scripts |

#### `Dev_Tools/Repo_Governance_Tools/` — Tier 3 Controlled Mutable

Eight governance enforcement validators. All are read-only auditors — they inspect the repository and emit JSON reports; they do not mutate any files.

| Script | Purpose |
|---|---|
| `devscript_header_validator.py` | Audits all Dev_Tools scripts for `RUNTIME_TOOL_METADATA` / `REPO_GOVERNANCE_TOOL_METADATA` header schema compliance |
| `tool_registry_validator.py` | Validates Tool_Index registry consistency — path existence, capability alignment, destructive classification |
| `directory_structure_validator.py` | Validates the canonical `_Dev_Resources` directory contract (35 required directories) |
| `governance_contract_validator.py` | Audits naming conventions, header marker presence, and abbreviation token usage against the registry |
| `repo_policy_enforcer.py` | Aggregates all seven validators via subprocess; produces a consolidated compliance report |
| `dev_resources_freeze_validator.py` | Audits Tier 1 / Tier 2 / Coq exclusion zone freeze compliance |
| `abbreviation_registry_validator.py` | Scans source files for ALL-CAPS tokens not registered in `Abbreviations.json` |
| `runtime_wiring_log_validator.py` | Validates JSONL append-only integrity and required fields in `Repo_Inventory/Master_Indexes/Runtime/` |

**Running the full suite:**
```bash
python3 _Dev_Resources/Dev_Tools/Repo_Governance_Tools/repo_policy_enforcer.py
```

All reports are written to `_Dev_Resources/Reports/_Dev_Governance/`.

#### `Dev_Tools/Runtime_Tools/` — Tier 3 Controlled Mutable

Active analysis tooling organized into nine subcategories. All tools:
- Are read-only by default (mutation and destructive capabilities declared false unless explicitly required)
- Include a `RUNTIME_TOOL_METADATA` docstring header compliant with `Header_Schemas/runtime_tool_header_schema.json`
- Route output to `_Dev_Resources/Reports/Execution_Reports/Tool_Outputs/Runtime/`
- Support a `--output` CLI argument for report filename control

| Subcategory | Modules | Summary |
|---|---|---|
| `Architecture_Validation/` | `execution_core_isolation_audit.py`, `import_prefix_verifier.py`, `import_root_grouping_analyzer.py`, `import_violation_classifier.py`, `module_root_existence_checker.py`, `namespace_discovery_scan.py`, `nexus_structural_audit.py`, `violation_prefix_grouper.py` | Static architectural boundary analysis — import violations, prefix grouping, namespace mapping |
| `Code_Extraction/` | `extract.py`, `fbc_registry.py`, `legacy_extract.py` | AST-level function block extraction and registry generation |
| `Dependency_Analysis/` | `cluster_analysis.py`, `facade_rewrite_pass.py`, `facade_synthesis.py`, `generate_deep_import_violations.py` | Import graph clustering, facade candidate synthesis, deep violation detection |
| `Dev_Utilities/` | `python_file_list.py`, `test_import_base_reasoning_registry.py` | General developer workflow helpers and test support |
| `Migration/` | `reorganize.py` | Module reorganization and canonical relocation |
| `Repo_Audit/` | `Import_Linter.py`, `repo_structure_export.py`, `scanner.py`, `triage.py` | Repository structure scanning, import linting, and triage classification |
| `Report_Generation/` | `pipeline.py`, `registry_writer.py` | Report assembly pipeline and tool registry writer |
| `Runtime_Diagnostics/` | `runtime_callgraph_extractor.py`, `runtime_debug_artifact_scanner.py`, `runtime_execution_tracer.py`, `runtime_module_tree_auditor.py` | Runtime call graph extraction, artifact scanning, execution tracing, module tree auditing |
| `Static_Analysis/` | `ast_parser.py`, `classifier.py`, `drac_indexer.py`, `generate_symbol_import_index.py`, `packet_discovery.py`, `runtime_analysis.py`, `semantic_extractor.py`, `static_ast_analysis.py` | AST parsing, symbol indexing, semantic classification, packet discovery |

---

### `Processing_Center/`

`Processing_Center` is the pipeline for receiving, categorizing, normalizing, and refactoring runtime content — typically legacy modules, salvaged logic, or external code being considered for integration into the LOGOS runtime stack.

**The directory skeleton is Tier 2 SKELETON FROZEN.** The `Processing_Center/`, `BLUEPRINTS/`, `STAGING/`, and all `STAGING/` first-level subdirectories are immutable directory entries. Their contents are workflow-variable.

#### `Processing_Center/BLUEPRINTS/`

Blueprint artifacts consumed during processing workflows. The `BLUEPRINTS/` directory itself is canonical; its contents are entirely determined by the current workflow and are non-canonical. Subdirectories and files within `BLUEPRINTS/` appear and disappear as workflows progress. Do not treat any specific item inside `BLUEPRINTS/` as a permanent artifact.

#### `Processing_Center/STAGING/`

Pipeline staging area. The first-level subdirectory structure is canonical; the modules and artifacts within each subdirectory are workflow objects (non-canonical, variable).

| Canonical Stage Directory | Role |
|---|---|
| `STAGING/In_Process/` | Items currently under active transformation. Contains three workflow buckets: `EXTRACT_LOGIC/` (logic being extracted), `KEEP_VERIFY/` (candidates for retention), `NORMALIZE_INTGRATE/` (items being normalized). |
| `STAGING/Inspection_Targets/` | Items queued for manual or automated structural inspection before pipeline entry. |
| `STAGING/Post_Processing/` | Items that have completed pipeline stages and are awaiting final disposition (integration, archive, or discard). |
| `STAGING/Pre-Processing/` | Items in the categorization phase before full pipeline entry. Organized by domain layer: `agent/`, `math/`, `reasoning/`, `safety/`, `semantic/`, `utility/`, `utils/`. |

---

### `Repo_Governance/`

The authority layer for all developer and runtime tooling rules. All governance documents here are binding on automated agents, tooling scripts, and human contributors.

#### `Repo_Governance/Developer/`

| Document | Purpose |
|---|---|
| `Dev_Environment_Rules.md` | Rules for the local dev environment: venv usage, tool invocation, prohibited global mutations |
| `Dev_Resources_Directory_Contract.md` | Binding canonical directory map and subdomain mutation classes |
| `Dev_Resources_Freeze_Protocol.md` | Tier 1 / Tier 2 / Tier 3 freeze classification, violation response protocol, exception process |
| `Dev_Tool_Generation_Policy.md` | Naming, header compliance, output routing, CLI, determinism, and registry rules for all new tools |
| `Directory_Creation_Authorization_Rules.md` | Authorization requirements for creating new directories under governed roots; authorization log |
| `Development_Rules.json` | Machine-readable governance rules including Coq stack guardrails, repo inventory governance, and runtime governance cross-references |

#### `Repo_Governance/Header_Schemas/` — Tier 1 Hard Frozen

Three canonical JSON header schema files. These define the required metadata fields for every script and module in the repository. **Never modify these files.** Schema changes require a formal governance exception.

| Schema File | Applies To |
|---|---|
| `runtime_tool_header_schema.json` | All `Dev_Tools/Runtime_Tools/` scripts — requires `RUNTIME_TOOL_METADATA` docstring |
| `repo_governance_tool_header_schema.json` | All `Dev_Tools/Repo_Governance_Tools/` scripts — requires `REPO_GOVERNANCE_TOOL_METADATA` docstring |
| `runtime_module_header_schema.json` | All `LOGOS_SYSTEM/` runtime modules — requires `RUNTIME_MODULE_METADATA` docstring |

#### `Repo_Governance/Runtime/`

| Document | Purpose |
|---|---|
| `Abbreviation_Usage_Policy.md` | Rules for abbreviation registration, approved contexts, and validation against `Abbreviations.json` |
| `Abbreviations.json` | Canonical abbreviation registry — all ALL-CAPS tokens used across the repo must appear here |
| `Dependency_Wiring_Log_Contract.md` | JSONL format and required fields for append-only dependency logs in `Repo_Inventory/` |
| `Naming_Convention_Enforcement.md` | File, directory, class, function, and constant naming rules; prohibited patterns |
| `Runtime_Artifact_Formatting_Spec.md` | Canonical output paths, JSON format spec (`indent=2`), append-only JSONL rules |
| `Runtime_Execution_Environment_Rules.md` | I/O rules, process isolation, security requirements, exclusion zones, logging requirements |
| `Runtime_Module_Generation_Spec.md` | Layer assignment, failure mode declaration, header requirements, protocol binding for new runtime modules |

---

### `Repo_Inventory/`

Deterministic, append-only indexing of the repository's runtime structure. Write operations to this directory are strictly append-only — no record may be modified or deleted after writing. Managed by `Repo_Governance_Tools/runtime_wiring_log_validator.py`.

| Path | Purpose |
|---|---|
| `Master_Indexes/Runtime/` | JSONL index files: `import_graph_index.jsonl`, `call_path_index.jsonl`, `external_interaction_index.jsonl`, `runtime_wiring_index.jsonl` |
| `Master_Indexes/Environment/` | Environment dependency indexes |
| `Master_Manifests/` | Full repository manifests (module lists, surface exports) |

---

### `Tool_Index/`

The tool registry and developer operational documentation.

| File | Purpose |
|---|---|
| `dev_tool_registry.json` | Master registry of all `Dev_Tools/` scripts with paths, categories, capability flags, and safety classifications |
| `Dev_Tooling_Operations_Guide.md` | Step-by-step usage guide for all Runtime_Tools, including CLI examples and output locations |
| `Dev_Tooling_Policies.md` | Operational policy summary for dev tooling |

Tool registry updates are required whenever a new script is added or an existing script is renamed. Use `registry_writer.py` in `Runtime_Tools/Report_Generation/` for automated registry updates.

---

### `Developer_Notes/`

Supplementary policy documents that do not fit within the formal governance layer. These are informational and advisory.

| File | Purpose |
|---|---|
| `External_Wrapper_Testing_Policy.md` | Policy for testing external library wrappers and third-party integrations |

---

## Governance Rules Summary

### Freeze Tiers

| Tier | Description | Paths |
|---|---|---|
| **Tier 1 — Hard Frozen** | No modification, addition, rename, or deletion permitted. Requires architect exception to change. | `Repo_Governance/Header_Schemas/`, `Dev_Tools/Archive/P1-5/`, `Dev_Tools/Archive/RGE/` |
| **Tier 2 — Skeleton Frozen** | Directory skeletons immutable; file contents within permitted areas may change during pipeline operations. | `Processing_Center/` (and all first-level subdirs) |
| **Tier 3 — Controlled Mutable** | May be modified under authorized conditions with appropriate logging. | `Dev_Tools/Runtime_Tools/`, `Dev_Tools/Repo_Governance_Tools/`, `Repo_Governance/Developer/`, `Repo_Governance/Runtime/`, `Repo_Inventory/`, `Tool_Index/` |
| **Extended — Coq Stack Frozen** | Governed by additional Coq stack freeze rules in `Development_Rules.json`. | `STARTUP/PXL_Gate/`, `STARTUP/Runtime_Compiler/` (repo root level) |

### Directory Creation Authorization

New directories under `_Dev_Resources` require **explicit architect authorization**. No automated agent may create a directory not pre-authorized in `Directory_Creation_Authorization_Rules.md`. The following additions are prohibited without authorization:

- New top-level directories under `_Dev_Resources/`
- New subdirectories under `Processing_Center/` at any level
- New subcategory directories under `Dev_Tools/Runtime_Tools/` (the nine existing subcategories are the canonical set)
- Any directory inside `Repo_Governance/Header_Schemas/`

### Naming Conventions

| Artifact Type | Required Pattern |
|---|---|
| Tool scripts (`Dev_Tools/`) | `Title_Case_With_Underscores.py` |
| Runtime modules (`LOGOS_SYSTEM/`) | `Title_Case_With_Underscores.py` |
| Governance documents | `Title_Case_With_Underscores.md` |
| Report output files | `lower_snake_case.json` or `lower_snake_case.md` |
| Directory names | `Title_Case_With_Underscores/` or `ALL_CAPS/` (for pipeline stages) |
| Constants | `UPPER_SNAKE_CASE` |
| Functions / methods | `lower_snake_case` |
| Classes | `TitleCase` |

Abbreviations in filenames must be ALL-CAPS (e.g., `AST_Walker.py`, `Import_Linter.py`). All abbreviations must be registered in `Repo_Governance/Runtime/Abbreviations.json`.

### Tool Header Requirements

Every script in `Dev_Tools/` must include a metadata docstring at file top:

- `Runtime_Tools/` scripts → `RUNTIME_TOOL_METADATA` block, validated against `runtime_tool_header_schema.json`
- `Repo_Governance_Tools/` scripts → `REPO_GOVERNANCE_TOOL_METADATA` block, validated against `repo_governance_tool_header_schema.json`

Run `devscript_header_validator.py` to audit header compliance across all Dev_Tools scripts.

### Output Routing

All tooling output must be written to designated subdirectories under `_Dev_Resources/Reports/`:

| Tool Class | Output Root |
|---|---|
| `Runtime_Tools/` output | `_Dev_Resources/Reports/Execution_Reports/Tool_Outputs/Runtime/` |
| `Repo_Governance_Tools/` output | `_Dev_Resources/Reports/_Dev_Governance/` |

No output artifacts may be written to locations outside `_Dev_Resources/Reports/`. Tools must define `OUTPUT_ROOT` pointing to the canonical path and call `OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)` before writing.

---

## Security and Safety Posture

- **Default posture: DENY / FAIL-CLOSED.** All tooling defaults to read-only. Mutation capability is explicitly declared in each tool's header (field: `mutation_capability: false`).
- **No runtime authority.** No script in `_Dev_Resources` may directly modify `LOGOS_SYSTEM/`, `STARTUP/`, or `_Governance/` without explicit governance authorization artifacts.
- **Freeze enforcement.** `dev_resources_freeze_validator.py` enforces freeze tiers automatically. Violations halt execution and require architect review before resuming.
- **Append-only inventory.** Wiring log indexes in `Repo_Inventory/` are append-only. The `runtime_wiring_log_validator.py` checks timestamp monotonicity to detect accidental overwrites.

---

## Cross-Reference Index

| Document | Location | Scope |
|---|---|---|
| `Dev_Resources_Directory_Contract.md` | `Repo_Governance/Developer/` | Canonical directory map and mutation classes |
| `Dev_Resources_Freeze_Protocol.md` | `Repo_Governance/Developer/` | Tier 1/2/3 freeze rules and exception process |
| `Dev_Tool_Generation_Policy.md` | `Repo_Governance/Developer/` | Tool generation naming, header, output routing rules |
| `Directory_Creation_Authorization_Rules.md` | `Repo_Governance/Developer/` | Directory creation authorization log |
| `Dev_Environment_Rules.md` | `Repo_Governance/Developer/` | Local dev environment operating rules |
| `Development_Rules.json` | `Repo_Governance/Developer/` | Machine-readable governance rule set |
| `Naming_Convention_Enforcement.md` | `Repo_Governance/Runtime/` | Naming rules for all artifact types |
| `Abbreviation_Usage_Policy.md` | `Repo_Governance/Runtime/` | Abbreviation registration and usage rules |
| `Abbreviations.json` | `Repo_Governance/Runtime/` | Canonical abbreviation registry |
| `Runtime_Artifact_Formatting_Spec.md` | `Repo_Governance/Runtime/` | Output format, path, and JSON spec |
| `Runtime_Execution_Environment_Rules.md` | `Repo_Governance/Runtime/` | I/O, isolation, and security rules |
| `Runtime_Module_Generation_Spec.md` | `Repo_Governance/Runtime/` | Rules for generating LOGOS_SYSTEM modules |
| `Dependency_Wiring_Log_Contract.md` | `Repo_Governance/Runtime/` | Append-only JSONL index format contract |
| `runtime_tool_header_schema.json` | `Repo_Governance/Header_Schemas/` | Runtime tool header schema (frozen) |
| `repo_governance_tool_header_schema.json` | `Repo_Governance/Header_Schemas/` | Governance tool header schema (frozen) |
| `runtime_module_header_schema.json` | `Repo_Governance/Header_Schemas/` | Runtime module header schema (frozen) |
| `dev_tool_registry.json` | `Tool_Index/` | Master tool registry |
| `Dev_Tooling_Operations_Guide.md` | `Tool_Index/` | Tool usage guide and CLI reference |
