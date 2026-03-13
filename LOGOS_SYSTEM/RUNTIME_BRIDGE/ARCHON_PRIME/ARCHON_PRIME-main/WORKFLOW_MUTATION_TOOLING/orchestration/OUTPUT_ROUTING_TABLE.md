# ARCHON_PRIME — OUTPUT ROUTING TABLE
**Deliverable 8** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE

This table eliminates all ambiguity about where every artifact produced by the system lands.
`artifact_router.py` (M90) and `routing_table_loader.py` (M01) both derive from this document.
The machine-readable form is `ARCHON_PRIME/configs/crawl_configs/routing_table.json`.

**Rule:** Every artifact produced by any module MUST appear in this table.
If an artifact has no entry here, it must not be written to disk.

---

## SECTION 1 — PRE-CRAWL AUDIT ARTIFACTS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `repo_directory_tree.json` | M10 | `ARCHON_PRIME/sources/baseline_analysis/repo_directory_tree.json` | JSON | NO (frozen post-audit) |
| `repo_directory_tree.json` (copy) | M10 | `AUDIT_SYSTEM/reports/structural_reports/repo_directory_tree.json` | JSON | NO |
| `repo_python_files.json` | M11 | `ARCHON_PRIME/sources/baseline_analysis/repo_python_files.json` | JSON | NO |
| `repo_python_files.json` (copy) | M11 | `AUDIT_SYSTEM/analysis/repo_maps/repo_python_files.json` | JSON | NO |
| `repo_imports.json` | M12 | `ARCHON_PRIME/sources/baseline_analysis/repo_imports.json` | JSON | NO |
| `repo_imports.json` (copy) | M12 | `AUDIT_SYSTEM/reports/import_reports/repo_imports.json` | JSON | NO |
| `repo_symbol_imports.json` | M13 | `AUDIT_SYSTEM/analysis/repo_maps/repo_symbol_imports.json` | JSON | NO |
| `header_schema_compliance.json` | M14 | `AUDIT_SYSTEM/reports/governance_reports/header_schema_compliance.json` | JSON | NO |
| `modules_missing_headers.json` | M14 | `AUDIT_SYSTEM/reports/governance_reports/modules_missing_headers.json` | JSON | NO |
| `governance_contract_map.json` | M15 | `ARCHON_PRIME/sources/governance_artifacts/governance_contract_map.json` | JSON | NO |
| `governance_contract_map.json` (copy) | M15 | `AUDIT_SYSTEM/reports/governance_reports/governance_contract_map.json` | JSON | NO |
| `missing_governance_modules.json` | M15 | `ARCHON_PRIME/sources/governance_artifacts/missing_governance_modules.json` | JSON | NO |
| `missing_governance_modules.json` (copy) | M15 | `AUDIT_SYSTEM/reports/governance_reports/missing_governance_modules.json` | JSON | NO |
| `raw_phase_assignments.json` | M16 | `AUDIT_SYSTEM/analysis/runtime_maps/raw_phase_assignments.json` | JSON | NO |
| `concept_spec_gap_report.json` | M17 | `AUDIT_SYSTEM/reports/concept_reports/concept_spec_gap_report.json` | JSON | NO |

---

## SECTION 2 — ANALYSIS ARTIFACTS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `module_index.json` | M20 | `ARCHON_PRIME/sources/baseline_analysis/module_index.json` | JSON | NO (frozen post-analysis) |
| `module_index.json` (copy) | M20 | `AUDIT_SYSTEM/reports/structural_reports/module_index.json` | JSON | NO |
| `dependency_graph.json` | M21 | `ARCHON_PRIME/sources/baseline_analysis/dependency_graph.json` | JSON | NO |
| `dependency_graph.json` (copy) | M21 | `AUDIT_SYSTEM/analysis/dependency_graphs/dependency_graph.json` | JSON | NO |
| `dependency_graph.json` (copy) | M21 | `AUDIT_SYSTEM/reports/import_reports/dependency_graph.json` | JSON | NO |
| `circular_dependency_groups.json` | M22 | `AUDIT_SYSTEM/analysis/dependency_graphs/circular_dependency_groups.json` | JSON | NO |
| `circular_dependency_groups.json` (copy) | M22 | `AUDIT_SYSTEM/reports/import_reports/circular_dependency_groups.json` | JSON | NO |
| `runtime_phase_map.json` | M23 | `ARCHON_PRIME/sources/baseline_analysis/runtime_phase_map.json` | JSON | NO |
| `runtime_phase_map.json` (copy) | M23 | `AUDIT_SYSTEM/analysis/runtime_maps/runtime_phase_map.json` | JSON | NO |
| `runtime_phase_map.json` (copy) | M23 | `AUDIT_SYSTEM/reports/runtime_reports/runtime_phase_map.json` | JSON | NO |
| `runtime_boot_sequence.json` | M24 | `ARCHON_PRIME/sources/baseline_analysis/runtime_boot_sequence.json` | JSON | NO |
| `runtime_boot_sequence.json` (copy) | M24 | `AUDIT_SYSTEM/reports/runtime_reports/runtime_boot_sequence.json` | JSON | NO |
| `canonical_import_registry.json` | M25 | `ARCHON_PRIME/tools/normalization_tools/canonical_import_registry.json` | JSON | NO |
| `canonical_import_rewrite_plan.json` | M25 | `AUDIT_SYSTEM/analysis/dependency_graphs/canonical_import_rewrite_plan.json` | JSON | NO |

---

## SECTION 3 — SIMULATION ARTIFACTS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `simulation_report.json` | M30+M31+M32 | `ARCHON_PRIME/logs/simulation_logs/simulation_report.json` | JSON | NO (frozen pre-crawl) |

---

## SECTION 4 — CRAWL PLANNING ARTIFACTS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `crawl_plan.json` | M38 | `ARCHON_PRIME/orchestration/execution_graphs/crawl_plan.json` | JSON | NO (frozen pre-crawl) |
| `execution_graph.json` | M39 | `ARCHON_PRIME/orchestration/execution_graphs/execution_graph.json` | JSON | NO (frozen pre-crawl) |

---

## SECTION 5 — PRE-CRAWL GOVERNANCE ARTIFACTS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `pre_crawl_snapshot.json` | M96 (controller) | `ARCHON_PRIME/sources/repo_snapshots/pre_crawl_snapshot.json` | JSON | NO |
| `pre_crawl_checklist_result.json` | M96 (controller) | `ARCHON_PRIME/logs/crawler_logs/pre_crawl_checklist_result.json` | JSON | NO |

---

## SECTION 6 — IN-CRAWL LIVE LOGS (APPEND-ONLY)

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `crawl_execution_log.json` | M60 | `ARCHON_PRIME/logs/crawler_logs/crawl_execution_log.json` | JSON (append) | YES (append-only) |
| `crawl_status.json` | M60 | `ARCHON_PRIME/logs/crawler_logs/crawl_status.json` | JSON (in-place) | YES (in-place update) |
| `mutation_log.json` | M61 | `ARCHON_PRIME/logs/execution_logs/mutation_log.json` | JSON (append) | YES (append-only) |
| `repair_event_log.json` | M72 | `ARCHON_PRIME/logs/repair_logs/repair_event_log.json` | JSON (append) | YES (append-only) |
| `quarantine_registry.json` | M80 | `ARCHON_PRIME/logs/repair_logs/quarantine_registry.json` | JSON (append) | YES (append-only) |
| `violation_log.json` | M63 | `AUDIT_SYSTEM/diagnostics/violation_logs/violation_log.json` | JSON (append) | YES (append-only) |

---

## SECTION 7 — IN-CRAWL MONITOR MIRRORS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `crawl_status_mirror.json` | M65 | `AUDIT_SYSTEM/runtime_monitor/live_status/crawl_status_mirror.json` | JSON (in-place) | YES |
| `progress_tracker.json` | M65 | `AUDIT_SYSTEM/runtime_monitor/progress_tracking/progress_tracker.json` | JSON (in-place) | YES |

---

## SECTION 8 — QUARANTINE BACKUPS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `<module_dotpath>.quarantine_backup.py` | M80 | `ARCHON_PRIME/sources/repo_snapshots/quarantine_backups/<flat_dotpath>.quarantine_backup.py` | Python | NO |

Note: `flat_dotpath` = module dotpath with `.` replaced by `__` (e.g., `logos.core.session` → `logos__core__session`).

---

## SECTION 9 — POST-CRAWL REPORTING ARTIFACTS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| `validation_report.json` | M91 | `ARCHON_PRIME/logs/execution_logs/validation_report.json` | JSON | NO |
| `post_crawl_summary_report.json` | M91 | `ARCHON_PRIME/logs/execution_logs/post_crawl_summary_report.json` | JSON | NO |
| `post_crawl_summary_report.md` | M91 | `ARCHON_PRIME/logs/execution_logs/post_crawl_summary_report.md` | Markdown | NO |
| `validation_report.json` (copy) | M91 | `AUDIT_SYSTEM/reports/structural_reports/validation_report.json` | JSON | NO |
| `post_normalization_snapshot.json` | M92 | `AUDIT_SYSTEM/baselines/post_normalization_snapshot/post_normalization_snapshot.json` | JSON | NO |
| `repair_recommendations.json` | M91 | `AUDIT_SYSTEM/diagnostics/repair_recommendations/repair_recommendations.json` | JSON | NO |

---

## SECTION 10 — DISTRIBUTION ARTIFACTS

| Artifact | Writer Module | Canonical Path | Format | Mutable |
|----------|--------------|----------------|--------|---------|
| Incoming bundles | External / M96 intake | `ARCHON_PRIME/distribution/incoming_bundle/` | Mixed | YES (intake only) |
| Sorted processed artifacts | M90 | `ARCHON_PRIME/distribution/sorted_artifacts/` | Mixed | YES (routing) |

---

## ROUTING TABLE — QUICK REFERENCE BY SYSTEM

### `ARCHON_PRIME/sources/baseline_analysis/` — FROZEN PRE-CRAWL ANALYSIS
```
repo_directory_tree.json
repo_python_files.json
repo_imports.json
module_index.json
dependency_graph.json
runtime_phase_map.json
runtime_boot_sequence.json
```

### `ARCHON_PRIME/sources/governance_artifacts/` — FROZEN GOVERNANCE
```
governance_contract_map.json
missing_governance_modules.json
```

### `ARCHON_PRIME/sources/repo_snapshots/` — REPO STATE SNAPSHOTS
```
pre_crawl_snapshot.json
quarantine_backups/<flat_dotpath>.quarantine_backup.py
```

### `ARCHON_PRIME/orchestration/execution_graphs/` — FROZEN CRAWL PLAN
```
crawl_plan.json
execution_graph.json
```

### `ARCHON_PRIME/tools/normalization_tools/` — LOCKED REGISTRIES
```
canonical_import_registry.json
header_schema.json
```

### `ARCHON_PRIME/logs/crawler_logs/` — LIVE CRAWL STATE
```
crawl_execution_log.json   (append-only)
crawl_status.json          (in-place)
pre_crawl_checklist_result.json
```

### `ARCHON_PRIME/logs/execution_logs/` — MUTATION + VALIDATION RECORDS
```
mutation_log.json          (append-only)
validation_report.json
post_crawl_summary_report.json
post_crawl_summary_report.md
```

### `ARCHON_PRIME/logs/repair_logs/` — REPAIR + QUARANTINE RECORDS
```
repair_event_log.json      (append-only)
quarantine_registry.json   (append-only)
```

### `ARCHON_PRIME/logs/simulation_logs/` — SIMULATION EVIDENCE
```
simulation_report.json
```

### `AUDIT_SYSTEM/reports/` — REPORT COPIES FOR AUDIT VISIBILITY
```
structural_reports/repo_directory_tree.json
structural_reports/module_index.json
structural_reports/validation_report.json
import_reports/repo_imports.json
import_reports/dependency_graph.json
import_reports/circular_dependency_groups.json
runtime_reports/runtime_phase_map.json
runtime_reports/runtime_boot_sequence.json
governance_reports/header_schema_compliance.json
governance_reports/modules_missing_headers.json
governance_reports/governance_contract_map.json
governance_reports/missing_governance_modules.json
concept_reports/concept_spec_gap_report.json
```

### `AUDIT_SYSTEM/analysis/` — ANALYSIS ARTIFACTS
```
repo_maps/repo_python_files.json
repo_maps/repo_symbol_imports.json
dependency_graphs/dependency_graph.json
dependency_graphs/circular_dependency_groups.json
dependency_graphs/canonical_import_rewrite_plan.json
runtime_maps/raw_phase_assignments.json
runtime_maps/runtime_phase_map.json
```

### `AUDIT_SYSTEM/diagnostics/` — DIAGNOSTICS
```
violation_logs/violation_log.json
repair_recommendations/repair_recommendations.json
```

### `AUDIT_SYSTEM/baselines/` — BASELINE SNAPSHOTS
```
initial_repo_snapshot/initial_snapshot.json
post_normalization_snapshot/post_normalization_snapshot.json
```

### `AUDIT_SYSTEM/runtime_monitor/` — LIVE MONITORING
```
live_status/crawl_status_mirror.json
progress_tracking/progress_tracker.json
```

---

## ROUTING TABLE JSON — MACHINE-READABLE FORMAT

The content below is the normative format for `ARCHON_PRIME/configs/crawl_configs/routing_table.json`.
Every key is an artifact type identifier. Every value is the canonical write path (primary location).
Secondary copies are defined separately in the `copies` array.

```json
{
  "schema_version": "1.0",
  "repo_directory_tree": {
    "primary": "ARCHON_PRIME/sources/baseline_analysis/repo_directory_tree.json",
    "copies": ["AUDIT_SYSTEM/reports/structural_reports/repo_directory_tree.json"]
  },
  "repo_python_files": {
    "primary": "ARCHON_PRIME/sources/baseline_analysis/repo_python_files.json",
    "copies": ["AUDIT_SYSTEM/analysis/repo_maps/repo_python_files.json"]
  },
  "repo_imports": {
    "primary": "ARCHON_PRIME/sources/baseline_analysis/repo_imports.json",
    "copies": ["AUDIT_SYSTEM/reports/import_reports/repo_imports.json"]
  },
  "repo_symbol_imports": {
    "primary": "AUDIT_SYSTEM/analysis/repo_maps/repo_symbol_imports.json",
    "copies": []
  },
  "module_index": {
    "primary": "ARCHON_PRIME/sources/baseline_analysis/module_index.json",
    "copies": ["AUDIT_SYSTEM/reports/structural_reports/module_index.json"]
  },
  "dependency_graph": {
    "primary": "ARCHON_PRIME/sources/baseline_analysis/dependency_graph.json",
    "copies": [
      "AUDIT_SYSTEM/analysis/dependency_graphs/dependency_graph.json",
      "AUDIT_SYSTEM/reports/import_reports/dependency_graph.json"
    ]
  },
  "circular_dependency_groups": {
    "primary": "AUDIT_SYSTEM/analysis/dependency_graphs/circular_dependency_groups.json",
    "copies": ["AUDIT_SYSTEM/reports/import_reports/circular_dependency_groups.json"]
  },
  "runtime_phase_map": {
    "primary": "ARCHON_PRIME/sources/baseline_analysis/runtime_phase_map.json",
    "copies": [
      "AUDIT_SYSTEM/analysis/runtime_maps/runtime_phase_map.json",
      "AUDIT_SYSTEM/reports/runtime_reports/runtime_phase_map.json"
    ]
  },
  "runtime_boot_sequence": {
    "primary": "ARCHON_PRIME/sources/baseline_analysis/runtime_boot_sequence.json",
    "copies": ["AUDIT_SYSTEM/reports/runtime_reports/runtime_boot_sequence.json"]
  },
  "governance_contract_map": {
    "primary": "ARCHON_PRIME/sources/governance_artifacts/governance_contract_map.json",
    "copies": ["AUDIT_SYSTEM/reports/governance_reports/governance_contract_map.json"]
  },
  "missing_governance_modules": {
    "primary": "ARCHON_PRIME/sources/governance_artifacts/missing_governance_modules.json",
    "copies": ["AUDIT_SYSTEM/reports/governance_reports/missing_governance_modules.json"]
  },
  "header_schema_compliance": {
    "primary": "AUDIT_SYSTEM/reports/governance_reports/header_schema_compliance.json",
    "copies": []
  },
  "modules_missing_headers": {
    "primary": "AUDIT_SYSTEM/reports/governance_reports/modules_missing_headers.json",
    "copies": []
  },
  "canonical_import_rewrite_plan": {
    "primary": "AUDIT_SYSTEM/analysis/dependency_graphs/canonical_import_rewrite_plan.json",
    "copies": []
  },
  "simulation_report": {
    "primary": "ARCHON_PRIME/logs/simulation_logs/simulation_report.json",
    "copies": []
  },
  "crawl_plan": {
    "primary": "ARCHON_PRIME/orchestration/execution_graphs/crawl_plan.json",
    "copies": []
  },
  "execution_graph": {
    "primary": "ARCHON_PRIME/orchestration/execution_graphs/execution_graph.json",
    "copies": []
  },
  "crawl_execution_log": {
    "primary": "ARCHON_PRIME/logs/crawler_logs/crawl_execution_log.json",
    "copies": [],
    "mode": "append"
  },
  "crawl_status": {
    "primary": "ARCHON_PRIME/logs/crawler_logs/crawl_status.json",
    "copies": [],
    "mode": "in_place"
  },
  "mutation_log": {
    "primary": "ARCHON_PRIME/logs/execution_logs/mutation_log.json",
    "copies": [],
    "mode": "append"
  },
  "repair_event_log": {
    "primary": "ARCHON_PRIME/logs/repair_logs/repair_event_log.json",
    "copies": [],
    "mode": "append"
  },
  "quarantine_registry": {
    "primary": "ARCHON_PRIME/logs/repair_logs/quarantine_registry.json",
    "copies": [],
    "mode": "append"
  },
  "validation_report": {
    "primary": "ARCHON_PRIME/logs/execution_logs/validation_report.json",
    "copies": ["AUDIT_SYSTEM/reports/structural_reports/validation_report.json"]
  },
  "post_crawl_summary_report": {
    "primary": "ARCHON_PRIME/logs/execution_logs/post_crawl_summary_report.json",
    "copies": []
  },
  "violation_log": {
    "primary": "AUDIT_SYSTEM/diagnostics/violation_logs/violation_log.json",
    "copies": [],
    "mode": "append"
  },
  "repair_recommendations": {
    "primary": "AUDIT_SYSTEM/diagnostics/repair_recommendations/repair_recommendations.json",
    "copies": []
  },
  "pre_crawl_checklist_result": {
    "primary": "ARCHON_PRIME/logs/crawler_logs/pre_crawl_checklist_result.json",
    "copies": []
  },
  "post_normalization_snapshot": {
    "primary": "AUDIT_SYSTEM/baselines/post_normalization_snapshot/post_normalization_snapshot.json",
    "copies": []
  }
}
```
