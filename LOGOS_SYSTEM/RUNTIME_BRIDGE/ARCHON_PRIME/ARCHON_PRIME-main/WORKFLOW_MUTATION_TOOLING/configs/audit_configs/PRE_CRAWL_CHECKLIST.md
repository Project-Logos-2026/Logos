# ARCHON_PRIME — PRE-CRAWL CHECKLIST
**Deliverable 6** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE

All items must be GREEN before `controller_main.py` is permitted to begin the crawl phase.
Any RED item blocks the crawl. There are no conditional greens.

The checklist is evaluated by `controller_main.py` pre-crawl gate.
Results are written to: `ARCHON_PRIME/logs/crawler_logs/pre_crawl_checklist_result.json`

---

## SECTION A — FOUNDATION LAYER READINESS

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| A1 | `schema_registry.py` is importable without error | Import test | YES |
| A2 | `routing_table.json` is present and valid JSON | Schema load test | YES |
| A3 | `routing_table.json` has entries for all 21 artifact types | Registry completeness check | YES |
| A4 | `repair_registry.json` is present and valid JSON | Schema load test | YES |
| A5 | `repair_registry.json` has entries for all 12 failure classes | Registry completeness check | YES |
| A6 | `header_schema.json` is present, valid, and has all required fields | Schema load test | YES |
| A7 | `canonical_import_registry.json` is present and loaded | Load test | YES |
| A8 | `crawl_config.json` is present and valid | Config load test | YES |

---

## SECTION B — AUDIT ARTIFACT COMPLETENESS

All artifacts in this section must exist at their canonical locations AND pass schema validation.

| # | Artifact | Canonical Location | Blocking |
|---|----------|--------------------|---------|
| B1 | `repo_directory_tree.json` | `ARCHON_PRIME/sources/baseline_analysis/` | YES |
| B2 | `repo_python_files.json` | `ARCHON_PRIME/sources/baseline_analysis/` | YES |
| B3 | `repo_imports.json` | `ARCHON_PRIME/sources/baseline_analysis/` | YES |
| B4 | `repo_symbol_imports.json` | `AUDIT_SYSTEM/analysis/repo_maps/` | NO (WARNING) |
| B5 | `header_schema_compliance.json` | `AUDIT_SYSTEM/reports/governance_reports/` | YES |
| B6 | `modules_missing_headers.json` | `AUDIT_SYSTEM/reports/governance_reports/` | YES |
| B7 | `governance_contract_map.json` | `ARCHON_PRIME/sources/governance_artifacts/` | YES |
| B8 | `missing_governance_modules.json` | `ARCHON_PRIME/sources/governance_artifacts/` | YES |

**Audit Age Check:** All B-section artifacts must have `generated_at` timestamps within the current crawl session (same calendar day unless explicitly overridden by config). Stale audits from a prior session must be regenerated.

---

## SECTION C — ANALYSIS ARTIFACT COMPLETENESS

| # | Artifact | Canonical Location | Blocking |
|---|----------|--------------------|---------|
| C1 | `module_index.json` | `ARCHON_PRIME/sources/baseline_analysis/` | YES |
| C2 | `dependency_graph.json` | `ARCHON_PRIME/sources/baseline_analysis/` | YES |
| C3 | `circular_dependency_groups.json` | `AUDIT_SYSTEM/analysis/dependency_graphs/` | YES |
| C4 | `runtime_phase_map.json` | `ARCHON_PRIME/sources/baseline_analysis/` | YES |
| C5 | `runtime_boot_sequence.json` | `ARCHON_PRIME/sources/baseline_analysis/` | YES |
| C6 | `canonical_import_rewrite_plan.json` | `AUDIT_SYSTEM/analysis/dependency_graphs/` | YES |

---

## SECTION D — CYCLE ANALYSIS CLEARANCE

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| D1 | `circular_dependency_groups.json` → `crawl_blocked` is `false` | Direct field check | YES |
| D2 | `circular_dependency_groups.json` → `boot_chain_cycles` count is 0 | Direct field check | YES |
| D3 | All cycles present are severity `WARNING` (post-boot only) | Field check on all entries | YES |

If D1 or D2 fail: crawl is HALTED. Boot-chain circular dependencies require manual resolution before the checklist can be re-evaluated.

---

## SECTION E — RUNTIME BOOT CHAIN CLEARANCE

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| E1 | `runtime_boot_sequence.json` → `unresolvable_boot_modules` is empty | Direct field check | YES |
| E2 | All phase 0 and phase 1 modules appear in boot sequence | Cross-check module_index vs boot_sequence | YES |
| E3 | Boot sequence topological sort is acyclic | Verified by `runtime_boot_sequencer.py` exit code | YES |

---

## SECTION F — GOVERNANCE MAP CLEARANCE

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| F1 | `governance_contract_map.json` produced with at least 1 compliant module | Count check | YES |
| F2 | `missing_governance_modules.json` reviewed — all MISSING entries are known and documented | Manual sign-off OR automated policy: missing OK if in non-governance package | NO (WARNING) |
| F3 | No governance contract conflicts (module declares contract that contradicts declared dependencies) | Validator check | YES |

---

## SECTION G — HEADER SCHEMA LOCK

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| G1 | `header_schema.json` is at version ≥ 1.0 | Version field check | YES |
| G2 | `header_injector.py` successfully produces a header from `header_schema.json` for a test module | Unit test | YES |
| G3 | All fields in `header_schema.json` have defined types and default values | Schema completeness check | YES |

---

## SECTION H — CANONICAL IMPORT REGISTRY LOCK

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| H1 | `canonical_import_registry.json` is present and loaded | Load test | YES |
| H2 | `canonical_import_rewrite_plan.json` has 0 entries with `confidence: UNCERTAIN` (unknown confidence level) | Field check | YES |
| H3 | All `requires_manual_review: true` items have been reviewed and accepted or resolved | Manual sign-off OR check that count matches accepted list in config | NO (WARNING — must be logged) |
| H4 | `import_rewriter.py` successfully rewrites a test deep import to facade form | Unit test | YES |

---

## SECTION I — SIMULATION PASS

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| I1 | `simulation_report.json` is present | File existence check | YES |
| I2 | `simulation_report.json` → `overall_result: "PASS"` | Direct field check | YES |
| I3 | `simulation_report.json` → `crawl_permitted: true` | Direct field check | YES |
| I4 | `simulation_report.json` → `repo_simulation.structural_violations` is empty | Array length check | YES |
| I5 | `simulation_report.json` → `runtime_simulation.boot_chain_violations` is empty | Array length check | YES |
| I6 | `simulation_report.json` → `import_simulation.broken_after_rewrite` is empty | Array length check | YES |
| I7 | `simulation_report.json` `generated_at` is within current crawl session | Timestamp check | YES |

---

## SECTION J — CRAWL PLAN READINESS

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| J1 | `crawl_plan.json` is present and schema-valid | Schema validation | YES |
| J2 | `execution_graph.json` is present and schema-valid | Schema validation | YES |
| J3 | Crawl plan total module count matches `module_index.json` total (no missing modules) | Count comparison | YES |
| J4 | Boot-chain modules appear first in crawl plan | Order check: all phase 0+1 before phase 2+ | YES |
| J5 | No module appears twice in crawl plan | Uniqueness check | YES |

---

## SECTION K — REPAIR REGISTRY LOADED

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| K1 | `repair_registry_loader.py` loads registry without error | Load test | YES |
| K2 | All 12 failure classes have a registered remediation action | Coverage check | YES |
| K3 | All registered repair actions reference callable handlers | Handler existence check | YES |

---

## SECTION L — ROUTING PATH VERIFICATION

| # | Check | Verification Method | Blocking |
|---|-------|-------------------|---------|
| L1 | All canonical destination directories exist on disk | `os.path.isdir()` check for each routing table path | YES |
| L2 | All destination directories are writable | Write permission check | YES |
| L3 | Log file destinations (`crawler_logs/`, `repair_logs/`, `execution_logs/`) are empty OR explicitly cleared for new crawl | State check | YES |
| L4 | `quarantine_registry.json` is initialized (empty entries array) for new crawl | File check | YES |

---

## CHECKLIST RESULT FORMAT

`pre_crawl_checklist_result.json` (produced by controller_main.py):

```json
{
  "schema_version": "1.0",
  "evaluated_at": "<ISO8601>",
  "crawl_id": "<uuid>",
  "overall_result": "GREEN | RED",
  "crawl_permitted": "<bool>",
  "sections": {
    "A": {"result": "GREEN | RED", "failed_items": ["A3"], "warnings": []},
    "B": {"result": "GREEN | RED", "failed_items": [], "warnings": ["B4"]},
    "...": "..."
  },
  "blocking_failures": ["<check_id: description>"],
  "warnings": ["<check_id: description>"],
  "halt_reason": "<str | null>"
}
```

`crawl_permitted: false` → `controller_main.py` exits non-zero. Crawl does NOT begin.
