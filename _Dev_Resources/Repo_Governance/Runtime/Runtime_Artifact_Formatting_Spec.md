# Runtime_Artifact_Formatting_Spec

**Governance Domain:** Runtime  
**Scope:** All output artifacts produced by Runtime_Tools and runtime modules  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Runtime  

---

## 1. Purpose

This specification defines the canonical formatting rules for all artifacts produced by Runtime_Tools and runtime modules. Artifacts include JSON reports, index files, manifests, and log files.

---

## 2. Canonical Output Paths

| Artifact Type | Canonical Output Path |
|---|---|
| Runtime_Tool reports | `_Dev_Resources/Reports/Tool_Outputs/Runtime/` |
| Governance reports | `_Dev_Resources/Reports/_Dev_Governance/` |
| Dependency wiring logs | `_Dev_Resources/Repo_Inventory/Master_Indexes/Runtime/` |
| Environment indexes | `_Dev_Resources/Repo_Inventory/Master_Indexes/Environment/` |
| Immutable manifests | `_Dev_Resources/Repo_Inventory/Master_Manifests/` |
| Test artifacts | `_Reports/Test_Artifacts/` |
| Audit outputs | `_Reports/Audit_Outputs/<subdomain>/` |

No artifact may be written to a path outside these canonical routes.

---

## 3. JSON Artifact Format

All JSON artifacts MUST comply with the following format rules:

### 3.1 Structure

```json
{
  "artifact_type": "<descriptor>",
  "generated_utc": "<ISO-8601 timestamp>",
  "tool_name": "<generating tool name>",
  "schema_version": "1.0",
  "metadata": { ... },
  "results": { ... }
}
```

### 3.2 Formatting Rules

- `indent=2` — two-space indentation, no tabs.
- Keys MUST be sorted alphabetically within each object where the key set is dynamic.
- Keys with fixed semantic meaning (e.g., `artifact_type`, `generated_utc`) maintain their defined order.
- UTF-8 encoding is mandatory. No BOM.
- Trailing commas are forbidden (strict JSON).
- No comments within JSON files.

### 3.3 Timestamp Format

All timestamps in artifacts must be UTC ISO-8601:

```
YYYY-MM-DDTHH:MM:SSZ
```

Example: `2026-03-12T14:30:00Z`

No local time, no epoch integers, no informal date strings.

---

## 4. Report Naming Convention

Report files must be named using `snake_case` derived from the tool name plus the operation:

```
<tool_name>_report.json
<tool_name>_<operation>_report.json
```

Examples:
- `import_linter_report.json`
- `runtime_callgraph_extractor_report.json`
- `governance_artifact_generation_report.json`

Abbreviations in report filenames must remain lowercase (snake_case convention; this is the only context where ALL-CAPS abbreviations are relaxed).

---

## 5. Append-Only Artifacts

Artifacts written to `Repo_Inventory/Master_Indexes/` and `Repo_Inventory/Master_Manifests/` are **append-only**:

- New entries are appended to existing files.
- Existing entries MUST NOT be modified.
- Deletions from these files require explicit governance authorization.
- Append operations must include a UTC timestamp and generating tool name in each appended record.

### 5.1 Append-Only JSON Format

Append-only log files use JSON Lines format (one JSON object per line):

```jsonl
{"timestamp": "2026-03-12T14:30:00Z", "tool": "...", "event": "...", "data": {...}}
```

Each line is a self-contained JSON object. Do not write arrays or nested structures at the top level of a `.jsonl` file.

---

## 6. Report Contents — Minimum Required Fields

Every Runtime_Tool report must contain:

| Field | Type | Description |
|---|---|---|
| `artifact_type` | string | Semantic descriptor of artifact (e.g., `"import_analysis"`) |
| `generated_utc` | string | ISO-8601 UTC timestamp |
| `tool_name` | string | Name of the generating tool |
| `schema_version` | string | Schema version (default `"1.0"`) |
| `status` | string | `"PASS"`, `"FAIL"`, `"PARTIAL"`, or `"SKIPPED"` |
| `results` | object | Tool-specific results |

---

## 7. Governance Report Format

Governance operation reports (written to `_Dev_Governance/`) must include:

| Field | Type | Description |
|---|---|---|
| `operation` | string | Name of the governance operation |
| `generated_utc` | string | ISO-8601 UTC timestamp |
| `created_artifacts` | array | List of files created |
| `created_directories` | array | List of directories created |
| `constraint_violations` | array | Any governance constraint violations detected |
| `environment_mutations` | array | Any environment-level mutations performed |
| `validation_results` | object | Per-check validation outcomes |

---

## 8. Formatting Enforcement

Automated tools that write artifacts must validate their output before writing:

1. Parse the JSON after serialization; if unparseable, abort and report error.
2. Verify required fields are present.
3. Verify timestamp is valid UTC ISO-8601.
4. Write the file only after validation passes.

---

## 9. Cross-References

| Document | Location |
|---|---|
| Dependency_Wiring_Log_Contract.md | `Repo_Governance/Runtime/` |
| Runtime_Execution_Environment_Rules.md | `Repo_Governance/Runtime/` |
| Dev_Resources_Directory_Contract.md | `Repo_Governance/Developer/` |
