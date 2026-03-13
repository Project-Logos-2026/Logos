# ARCHON_PRIME — JSON / ARTIFACT SCHEMA SET
**Deliverable 4** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE

All schemas defined here are the canonical data contracts for every artifact the system produces.
No module may write or consume a defined artifact type without conforming to this schema.
Schema versions are frozen before crawl begins and may not be changed mid-crawl.

---

## SCHEMA 01 — `repo_directory_tree.json`

**Purpose:** Complete directory tree of the LOGOS repo at the time of audit. Baseline for all subsequent analysis.

**Writer:** `AUDIT_SYSTEM/scripts/repo_scanners/repo_directory_scanner.py` (M10)
**Consumer:** `python_file_collector.py` (M11), `module_index_builder.py` (M20)
**Canonical Location:** `ARCHON_PRIME/sources/baseline_analysis/repo_directory_tree.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "repo_root": "<absolute_path>",
  "total_directories": "<int>",
  "total_files": "<int>",
  "tree": [
    {
      "path": "<relative_path_from_repo_root>",
      "type": "directory | file",
      "name": "<basename>",
      "size_bytes": "<int | null>",
      "extension": "<str | null>",
      "children": ["<relative_path>", "..."]
    }
  ]
}
```

**Required fields:** `schema_version`, `generated_at`, `repo_root`, `tree`
**tree[].path** — relative from repo root, normalized with forward slashes
**tree[].children** — present only if type == "directory"

---

## SCHEMA 02 — `repo_python_files.json`

**Purpose:** Enumeration of all `.py` files in the LOGOS repo with module dotpath mappings.

**Writer:** `python_file_collector.py` (M11)
**Consumer:** All audit scanners (M12–M17), `module_index_builder.py` (M20)
**Canonical Location:** `ARCHON_PRIME/sources/baseline_analysis/repo_python_files.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "repo_root": "<absolute_path>",
  "total_count": "<int>",
  "files": [
    {
      "path": "<relative_path>",
      "absolute_path": "<absolute_path>",
      "dotpath": "<module.dotpath>",
      "size_bytes": "<int>",
      "last_modified": "<ISO8601>",
      "is_init": "<bool>",
      "package": "<parent_package_dotpath | null>"
    }
  ]
}
```

**Required fields:** `schema_version`, `generated_at`, `repo_root`, `total_count`, `files`
**files[].dotpath** — derived from repo_root-relative path with `.py` stripped; `__init__` → parent package dotpath

---

## SCHEMA 03 — `repo_imports.json`

**Purpose:** All raw import statements extracted from every `.py` file via AST parse.

**Writer:** `import_extractor.py` (M12)
**Consumer:** `symbol_import_extractor.py` (M13), `dependency_graph_builder.py` (M21), `canonical_import_registry_builder.py` (M25)
**Canonical Location:** `ARCHON_PRIME/sources/baseline_analysis/repo_imports.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_modules_scanned": "<int>",
  "total_import_statements": "<int>",
  "modules": [
    {
      "dotpath": "<module.dotpath>",
      "path": "<relative_path>",
      "imports": [
        {
          "type": "import | from_import",
          "module": "<imported_module_dotpath>",
          "names": ["<symbol_or_star>"],
          "alias": "<alias | null>",
          "line_number": "<int>",
          "is_relative": "<bool>"
        }
      ],
      "parse_error": "<error_message | null>"
    }
  ]
}
```

**Required fields:** `schema_version`, `generated_at`, `modules`
Modules with `parse_error` != null are flagged as SYNTAX_FAILURE candidates.

---

## SCHEMA 04 — `repo_symbol_imports.json`

**Purpose:** Symbol-level import resolution: which symbols each module imports from which modules.

**Writer:** `symbol_import_extractor.py` (M13)
**Consumer:** Governance validator (M63), concept/spec gap detector (M17)
**Canonical Location:** `AUDIT_SYSTEM/analysis/repo_maps/repo_symbol_imports.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "modules": [
    {
      "dotpath": "<module.dotpath>",
      "imported_symbols": [
        {
          "from_module": "<source_module_dotpath>",
          "symbol": "<symbol_name>",
          "alias": "<alias | null>",
          "is_facade_import": "<bool>",
          "is_deep_import": "<bool>"
        }
      ]
    }
  ]
}
```

---

## SCHEMA 05 — `module_index.json`

**Purpose:** Master module registry — single source of truth for all module metadata during crawl.

**Writer:** `module_index_builder.py` (M20)
**Consumer:** All crawl planner, executor, simulation, and reporting modules
**Canonical Location:** `ARCHON_PRIME/sources/baseline_analysis/module_index.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_modules": "<int>",
  "modules": {
    "<module.dotpath>": {
      "dotpath": "<module.dotpath>",
      "path": "<relative_path>",
      "absolute_path": "<absolute_path>",
      "package": "<parent_package | null>",
      "is_init": "<bool>",
      "runtime_phase": "<int | null>",
      "governance_class": "<str | null>",
      "governance_contract_present": "<bool>",
      "header_present": "<bool>",
      "header_compliant": "<bool>",
      "imports": ["<imported_dotpath>"],
      "imported_by": ["<importing_dotpath>"],
      "has_deep_imports": "<bool>",
      "deep_import_count": "<int>",
      "size_bytes": "<int>",
      "parse_error": "<str | null>"
    }
  }
}
```

**Required fields:** All fields required. `null` is permitted for fields that are genuinely unknown.

---

## SCHEMA 06 — `dependency_graph.json`

**Purpose:** Directed graph of module dependencies. Nodes = modules, edges = import relationships.

**Writer:** `dependency_graph_builder.py` (M21)
**Consumer:** `circular_dependency_detector.py` (M22), `runtime_boot_sequencer.py` (M24), `crawl_planner.py` (M38), all simulators
**Canonical Location:** `ARCHON_PRIME/sources/baseline_analysis/dependency_graph.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_nodes": "<int>",
  "total_edges": "<int>",
  "nodes": ["<module.dotpath>"],
  "edges": [
    {
      "from": "<module.dotpath>",
      "to": "<imported_module.dotpath>",
      "import_type": "import | from_import",
      "is_deep_import": "<bool>",
      "line_number": "<int>"
    }
  ],
  "adjacency": {
    "<module.dotpath>": {
      "depends_on": ["<module.dotpath>"],
      "depended_on_by": ["<module.dotpath>"]
    }
  }
}
```

---

## SCHEMA 07 — `circular_dependency_groups.json`

**Purpose:** All detected import cycles, classified by severity.

**Writer:** `circular_dependency_detector.py` (M22)
**Consumer:** `crawl_planner.py` (M38), pre-crawl checklist gate
**Canonical Location:** `AUDIT_SYSTEM/analysis/dependency_graphs/circular_dependency_groups.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_cycles": "<int>",
  "boot_chain_cycles": "<int>",
  "post_boot_cycles": "<int>",
  "cycles": [
    {
      "cycle_id": "<uuid>",
      "members": ["<module.dotpath>"],
      "severity": "HALT | WARNING",
      "in_boot_chain": "<bool>",
      "phases_involved": ["<int>"],
      "detection_method": "tarjan_scc"
    }
  ],
  "crawl_blocked": "<bool>"
}
```

`crawl_blocked: true` if any `severity == "HALT"` cycle exists. Pre-crawl checklist gate checks this field.

---

## SCHEMA 08 — `runtime_phase_map.json`

**Purpose:** Authoritative phase assignment for every module in the repo.

**Writer:** `runtime_phase_mapper.py` (M23)
**Consumer:** `runtime_boot_sequencer.py` (M24), `crawl_planner.py` (M38), `phase_validator.py` (M64)
**Canonical Location:** `ARCHON_PRIME/sources/baseline_analysis/runtime_phase_map.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "phase_definitions": {
    "0": "kernel / pre-boot primitives",
    "1": "bootstrap / session control",
    "2": "governance + protocol layer",
    "3": "runtime services",
    "4": "application modules",
    "99": "unphased / utility"
  },
  "modules": {
    "<module.dotpath>": {
      "phase": "<int>",
      "phase_source": "declared | inferred | default",
      "conflict": "<bool>",
      "conflict_detail": "<str | null>"
    }
  }
}
```

---

## SCHEMA 09 — `runtime_boot_sequence.json`

**Purpose:** Topologically-sorted boot order for phase 0 and phase 1 modules.

**Writer:** `runtime_boot_sequencer.py` (M24)
**Consumer:** `runtime_simulator.py` (M31), `crawl_planner.py` (M38)
**Canonical Location:** `ARCHON_PRIME/sources/baseline_analysis/runtime_boot_sequence.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "boot_phases_covered": [0, 1],
  "sequence": [
    {
      "order": "<int>",
      "dotpath": "<module.dotpath>",
      "phase": "<int>",
      "depends_on": ["<module.dotpath>"],
      "is_boot_critical": "<bool>"
    }
  ],
  "unresolvable_boot_modules": ["<module.dotpath>"]
}
```

`unresolvable_boot_modules` must be empty for pre-crawl checklist to pass.

---

## SCHEMA 10 — `governance_contract_map.json`

**Purpose:** Map of every module's governance contract declarations and compliance status.

**Writer:** `governance_contract_scanner.py` (M15)
**Consumer:** `governance_validator.py` (M63), `crawl_planner.py` (M38)
**Canonical Location:** `ARCHON_PRIME/sources/governance_artifacts/governance_contract_map.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_modules": "<int>",
  "compliant_count": "<int>",
  "non_compliant_count": "<int>",
  "missing_contract_count": "<int>",
  "contracts": {
    "<module.dotpath>": {
      "contract_present": "<bool>",
      "contract_class": "<str | null>",
      "declared_dependencies": ["<module.dotpath>"],
      "declared_exports": ["<symbol_name>"],
      "compliance_status": "COMPLIANT | NON_COMPLIANT | MISSING",
      "violations": ["<violation_description>"]
    }
  }
}
```

---

## SCHEMA 11 — `missing_governance_modules.json`

**Purpose:** List of modules with absent or non-compliant governance contracts. Pre-crawl diagnostic.

**Writer:** `governance_contract_scanner.py` (M15)
**Consumer:** Pre-crawl checklist, `crawl_planner.py` (M38)
**Canonical Location:** `ARCHON_PRIME/sources/governance_artifacts/missing_governance_modules.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_missing": "<int>",
  "total_non_compliant": "<int>",
  "modules": [
    {
      "dotpath": "<module.dotpath>",
      "path": "<relative_path>",
      "issue": "MISSING_CONTRACT | NON_COMPLIANT",
      "detail": "<str>"
    }
  ]
}
```

---

## SCHEMA 12 — `header_schema_compliance.json`

**Purpose:** Per-module compliance status against the canonical header schema.

**Writer:** `header_schema_scanner.py` (M14)
**Consumer:** `crawl_planner.py` (M38), `header_injector.py` (M50)
**Canonical Location:** `AUDIT_SYSTEM/reports/governance_reports/header_schema_compliance.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "header_schema_version": "<str>",
  "total_scanned": "<int>",
  "compliant_count": "<int>",
  "non_compliant_count": "<int>",
  "missing_count": "<int>",
  "modules": {
    "<module.dotpath>": {
      "header_present": "<bool>",
      "header_compliant": "<bool>",
      "missing_fields": ["<field_name>"],
      "stale_fields": ["<field_name>"],
      "action_required": "NONE | INJECT | REPLACE"
    }
  }
}
```

---

## SCHEMA 13 — `modules_missing_headers.json`

**Purpose:** Flat list of modules requiring header injection or replacement. Consumed by header_injector.

**Writer:** `header_schema_scanner.py` (M14)
**Consumer:** `header_injector.py` (M50), pre-crawl checklist
**Canonical Location:** `AUDIT_SYSTEM/reports/governance_reports/modules_missing_headers.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_requiring_action": "<int>",
  "modules": [
    {
      "dotpath": "<module.dotpath>",
      "path": "<relative_path>",
      "action": "INJECT | REPLACE",
      "missing_fields": ["<field_name>"]
    }
  ]
}
```

---

## SCHEMA 14 — `canonical_import_rewrite_plan.json`

**Purpose:** Complete plan of all import rewrites to be executed by `import_rewriter.py`.

**Writer:** `canonical_import_registry_builder.py` (M25)
**Consumer:** `import_rewriter.py` (M51), `import_simulator.py` (M32)
**Canonical Location:** `AUDIT_SYSTEM/analysis/dependency_graphs/canonical_import_rewrite_plan.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "total_violations": "<int>",
  "total_rewrites_planned": "<int>",
  "rewrites": [
    {
      "module_dotpath": "<module.dotpath>",
      "line_number": "<int>",
      "original_import": "<raw_import_statement>",
      "rewritten_import": "<canonical_import_statement>",
      "violation_type": "DEEP_IMPORT | WRONG_FACADE | MISSING_FACADE",
      "confidence": "CERTAIN | INFERRED",
      "requires_manual_review": "<bool>"
    }
  ],
  "unresolvable_violations": [
    {
      "module_dotpath": "<module.dotpath>",
      "import_statement": "<raw>",
      "reason": "<str>"
    }
  ]
}
```

`requires_manual_review: true` items trigger WARNING (not BLOCKING) unless in boot chain.

---

## SCHEMA 15 — `crawl_execution_log.json`

**Purpose:** Append-only log of every module processed during the crawl, with result.

**Writer:** `crawl_executor.py` (M60)
**Consumer:** `report_generator.py` (M91), `commit_finalizer.py` (M92)
**Canonical Location:** `ARCHON_PRIME/logs/crawler_logs/crawl_execution_log.json`

```json
{
  "schema_version": "1.0",
  "crawl_id": "<uuid>",
  "started_at": "<ISO8601>",
  "entries": [
    {
      "sequence_number": "<int>",
      "timestamp": "<ISO8601>",
      "module_dotpath": "<module.dotpath>",
      "status": "PASS | FAIL | REPAIRED | QUARANTINED | SKIPPED | HALTED",
      "mutations_applied": ["<mutation_type>"],
      "validation_results": {
        "syntax": "PASS | FAIL",
        "governance": "PASS | FAIL | SKIP",
        "phase": "PASS | FAIL | SKIP"
      },
      "repair_attempts": "<int>",
      "duration_ms": "<int>",
      "error": "<str | null>"
    }
  ]
}
```

---

## SCHEMA 16 — `crawl_status.json`

**Purpose:** Live crawl progress indicator. Updated in-place after every module. Used for monitoring and crash recovery.

**Writer:** `crawl_executor.py` (M60)
**Consumer:** `crawl_monitor.py` (M65), crash recovery logic in `controller_main.py` (M96)
**Canonical Location:** `ARCHON_PRIME/logs/crawler_logs/crawl_status.json`

```json
{
  "schema_version": "1.0",
  "crawl_id": "<uuid>",
  "started_at": "<ISO8601>",
  "last_updated": "<ISO8601>",
  "status": "RUNNING | HALTED | COMPLETE | FAILED",
  "total_modules": "<int>",
  "processed_count": "<int>",
  "pass_count": "<int>",
  "fail_count": "<int>",
  "repaired_count": "<int>",
  "quarantined_count": "<int>",
  "current_module": "<module.dotpath | null>",
  "last_completed_module": "<module.dotpath | null>",
  "halt_reason": "<str | null>",
  "resume_from": "<module.dotpath | null>"
}
```

---

## SCHEMA 17 — `repair_event_log.json`

**Purpose:** Append-only log of every repair attempt (successful or failed).

**Writer:** `repair_executor.py` (M72)
**Consumer:** `report_generator.py` (M91)
**Canonical Location:** `ARCHON_PRIME/logs/repair_logs/repair_event_log.json`

```json
{
  "schema_version": "1.0",
  "crawl_id": "<uuid>",
  "entries": [
    {
      "timestamp": "<ISO8601>",
      "module_dotpath": "<module.dotpath>",
      "failure_class": "<failure_class_id>",
      "severity": "BLOCKING | HALT | WARNING",
      "repair_action": "<action_type>",
      "attempt_number": "<int>",
      "outcome": "REPAIRED | FAILED | ESCALATED_TO_QUARANTINE",
      "detail": "<str>"
    }
  ]
}
```

---

## SCHEMA 18 — `quarantine_registry.json`

**Purpose:** Registry of all quarantined modules: permanent record for post-crawl manual resolution.

**Writer:** `quarantine_manager.py` (M80)
**Consumer:** `report_generator.py` (M91), `commit_finalizer.py` (M92)
**Canonical Location:** `ARCHON_PRIME/logs/repair_logs/quarantine_registry.json`

```json
{
  "schema_version": "1.0",
  "crawl_id": "<uuid>",
  "total_quarantined": "<int>",
  "entries": [
    {
      "quarantine_id": "<uuid>",
      "timestamp": "<ISO8601>",
      "module_dotpath": "<module.dotpath>",
      "original_path": "<relative_path>",
      "backup_path": "<relative_path_to_backup>",
      "stub_path": "<relative_path_to_stub>",
      "failure_class": "<failure_class_id>",
      "repair_attempts": "<int>",
      "final_failure_detail": "<str>",
      "manual_resolution_required": true
    }
  ]
}
```

---

## SCHEMA 19 — `mutation_log.json`

**Purpose:** Record of every mutation applied to every module during the crawl.

**Writer:** `module_processor.py` (M61), via `crawl_executor.py` (M60)
**Consumer:** `report_generator.py` (M91)
**Canonical Location:** `ARCHON_PRIME/logs/execution_logs/mutation_log.json`

```json
{
  "schema_version": "1.0",
  "crawl_id": "<uuid>",
  "entries": [
    {
      "timestamp": "<ISO8601>",
      "module_dotpath": "<module.dotpath>",
      "mutation_type": "HEADER_INJECT | HEADER_REPLACE | IMPORT_REWRITE | STUB_INSERT | NONE",
      "detail": "<str>",
      "lines_changed": "<int>",
      "pre_mutation_hash": "<sha256>",
      "post_mutation_hash": "<sha256>"
    }
  ]
}
```

`sha256` hashes of module source enable diff verification and rollback identification.

---

## SCHEMA 20 — `validation_report.json`

**Purpose:** Aggregate validation results across all modules after crawl completion.

**Writer:** `report_generator.py` (M91)
**Consumer:** `commit_finalizer.py` (M92)
**Canonical Location:** `ARCHON_PRIME/logs/execution_logs/validation_report.json`

```json
{
  "schema_version": "1.0",
  "crawl_id": "<uuid>",
  "generated_at": "<ISO8601>",
  "summary": {
    "total_modules": "<int>",
    "syntax_pass": "<int>",
    "syntax_fail": "<int>",
    "governance_pass": "<int>",
    "governance_fail": "<int>",
    "phase_pass": "<int>",
    "phase_fail": "<int>",
    "import_violations_resolved": "<int>",
    "import_violations_unresolved": "<int>",
    "headers_injected": "<int>",
    "headers_replaced": "<int>",
    "quarantined": "<int>"
  },
  "per_module": {
    "<module.dotpath>": {
      "syntax": "PASS | FAIL",
      "governance": "PASS | FAIL | SKIP",
      "phase": "PASS | FAIL | SKIP",
      "import_clean": "<bool>",
      "header_canonical": "<bool>",
      "final_status": "CLEAN | REPAIRED | QUARANTINED"
    }
  }
}
```

---

## SCHEMA 21 — `simulation_report.json`

**Purpose:** Aggregated results from all three simulation modules pre-crawl.

**Writer:** `repo_simulator.py` (M30), `runtime_simulator.py` (M31), `import_simulator.py` (M32) — merged
**Consumer:** Pre-crawl gate, `crawl_planner.py` (M38), `controller_main.py` (M96)
**Canonical Location:** `ARCHON_PRIME/logs/simulation_logs/simulation_report.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO8601>",
  "overall_result": "PASS | FAIL",
  "repo_simulation": {
    "result": "PASS | FAIL",
    "modules_simulated": "<int>",
    "structural_violations": ["<str>"],
    "detail": "<str>"
  },
  "runtime_simulation": {
    "result": "PASS | FAIL",
    "boot_sequence_valid": "<bool>",
    "boot_chain_violations": ["<str>"],
    "detail": "<str>"
  },
  "import_simulation": {
    "result": "PASS | FAIL",
    "resolved_imports": "<int>",
    "unresolved_imports": "<int>",
    "broken_after_rewrite": ["<module.dotpath>"],
    "detail": "<str>"
  },
  "blocking_issues": ["<str>"],
  "crawl_permitted": "<bool>"
}
```

`crawl_permitted: false` → `controller_main.py` exits with error before crawl begins.
