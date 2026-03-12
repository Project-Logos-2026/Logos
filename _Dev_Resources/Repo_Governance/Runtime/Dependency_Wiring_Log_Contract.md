# Dependency_Wiring_Log_Contract

**Governance Domain:** Runtime  
**Scope:** All runtime modules and Runtime_Tools that declare dependency edges  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Runtime  

---

## 1. Purpose

This contract defines the mandatory logging requirements for dependency wiring — the tracking of import edges, call paths, external module interactions, and boot-time dependency resolution — within all runtime modules.

---

## 2. Scope

This contract applies to:

- All modules in `LOGOS_SYSTEM/` at any layer.
- All Runtime_Tools in `Dev_Tools/Runtime_Tools/` that perform dependency analysis.
- Any module that explicitly imports another LOGOS module.

It does NOT apply to:
- Coq proof files (exclusion zone).
- Files in `Dev_Tools/Archive/` (frozen artifacts).

---

## 3. Log Destinations

| Log Type | Destination |
|---|---|
| Runtime module dependency edges | `_Dev_Resources/Repo_Inventory/Master_Indexes/Runtime/` |
| Environment-level import graph | `_Dev_Resources/Repo_Inventory/Master_Indexes/Environment/` |
| Immutable wiring manifests | `_Dev_Resources/Repo_Inventory/Master_Manifests/` |

All destinations are **append-only**. Existing entries must not be modified.

---

## 4. Required Log Dimensions

Every dependency wiring log entry must capture:

### 4.1 Import Edges

For each `import` or `from ... import ...` statement:

| Field | Description |
|---|---|
| `source_module` | Module containing the import statement |
| `imported_module` | Fully qualified module being imported |
| `import_type` | `"IMPORT"` or `"FROM_IMPORT"` |
| `imported_names` | List of names imported (for FROM_IMPORT); `["*"]` is a violation |
| `is_third_party` | Boolean — whether the import is from outside the repo |
| `is_stdlib` | Boolean — whether the import is from Python stdlib |
| `line_number` | Line number of the import in source |

### 4.2 Call Paths

For each significant function-to-function or module-to-module call:

| Field | Description |
|---|---|
| `caller_module` | Module containing the calling code |
| `caller_function` | Function making the call |
| `callee_module` | Module containing the called code |
| `callee_function` | Function being called |
| `call_type` | `"DIRECT"`, `"DELEGATED"`, `"CONDITIONAL"`, or `"ASYNC"` |

### 4.3 External Module Interactions

| Field | Description |
|---|---|
| `module` | The runtime module |
| `external_service` | Name of external service or system (e.g., `"RabbitMQ"`, `"Redis"`) |
| `interaction_type` | `"CONNECT"`, `"PUBLISH"`, `"SUBSCRIBE"`, `"READ"`, `"WRITE"` |
| `authorized` | Boolean — whether the interaction is governance-authorized |

---

## 5. Log File Format

### 5.1 Index Files (Append-Only JSON Lines)

Files in `Master_Indexes/` use JSON Lines format (`.jsonl`):

```jsonl
{"timestamp": "2026-03-12T14:30:00Z", "log_type": "import_edge", "tool": "runtime_module_tree_auditor", "data": {"source_module": "...", "imported_module": "...", ...}}
{"timestamp": "2026-03-12T14:30:01Z", "log_type": "call_path", "tool": "runtime_callgraph_extractor", "data": {"caller_module": "...", ...}}
```

Each line:
- Is a self-contained JSON object.
- Includes `timestamp` (UTC ISO-8601), `log_type`, `tool` (generating tool name), and `data`.
- Must be parseable independently of other lines.

### 5.2 Manifest Files (Immutable JSON)

Files in `Master_Manifests/` use standard JSON format and are written once:

```json
{
  "manifest_type": "dependency_wiring_manifest",
  "generated_utc": "2026-03-12T14:30:00Z",
  "generating_tool": "<tool_name>",
  "schema_version": "1.0",
  "entries": [...]
}
```

Once written, a manifest file MUST NOT be overwritten. Subsequent captures produce new manifest files with incremented version or date suffix.

---

## 6. Required Index Files

The following index files must exist (or be created when first populated) in `Master_Indexes/Runtime/`:

| Filename | Content |
|---|---|
| `import_graph_index.jsonl` | All import edge log entries |
| `call_path_index.jsonl` | All call path log entries |
| `external_interaction_index.jsonl` | All external service interaction log entries |
| `runtime_wiring_index.jsonl` | Combined runtime wiring events (union of above) |

The following index files must exist in `Master_Indexes/Environment/`:

| Filename | Content |
|---|---|
| `file_type_index.jsonl` | Repository file type classification entries |
| `dependency_index.jsonl` | Cross-module dependency index |

---

## 7. Wiring Log Entry Lifecycle

```
Module loaded → emit import_edge entries
Function called → (optional, for tracing tools) emit call_path entries
External service contacted → emit external_interaction entry
Tool completes → flush all pending log entries to Master_Indexes/
```

---

## 8. Violations

The following are dependency wiring violations that must be reported:

| Violation | Severity |
|---|---|
| Wildcard import (`from x import *`) | ERROR |
| Import of `_Dev_Resources/Dev_Tools/` from a runtime module | ERROR |
| External interaction with `authorized=false` | ERROR |
| Missing `source_module` in a log entry | WARNING |
| Log written to non-canonical path | ERROR |

Violations must be logged in the `constraint_violations` field of the generating tool's report.

---

## 9. Tooling

The following Runtime_Tools implement this contract:

| Tool | Function |
|---|---|
| `runtime_module_tree_auditor.py` | Emits import_edge entries via AST analysis |
| `runtime_callgraph_extractor.py` | Emits call_path entries via AST walk |
| `runtime_execution_tracer.py` | Emits call_path entries via live sys.settrace |

---

## 10. Cross-References

| Document | Location |
|---|---|
| Runtime_Artifact_Formatting_Spec.md | `Repo_Governance/Runtime/` |
| Runtime_Module_Generation_Spec.md | `Repo_Governance/Runtime/` |
| Repo_Inventory directories | `_Dev_Resources/Repo_Inventory/` |
