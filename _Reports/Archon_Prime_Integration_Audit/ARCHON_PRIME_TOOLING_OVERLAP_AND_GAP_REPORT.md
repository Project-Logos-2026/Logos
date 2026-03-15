# ARCHON PRIME TOOLING — OVERLAP AND GAP REPORT
**Generated:** 2026-03-13  
**Scope:** Side-by-side comparison of AP internal tooling vs. LOGOS Dev Resources Runtime_Tools surface  
**Purpose:** Identify duplication waste, capability gaps, and integration opportunities  

---

## 1. Methodology

All tools under `_Dev_Resources/Dev_Tools/Runtime_Tools/` (LOGOS canonical) and all AP tooling under `ARCHON_PRIME-main/WORKFLOW_MUTATION_TOOLING/tools/` were enumerated and compared by:  
- Tool name and functional category  
- Input/output interface  
- Coverage (what they inspect)  
- Runtime assumptions  

---

## 2. Full Overlap Matrix

### 2A. LOGOS Canonical ↔ AP Internal — Direct Matches (DUPLICATE)

| LOGOS Runtime_Tools Module | AP Internal Module | Match Type | Recommendation |
|----------------------------|--------------------|------------|----------------|
| `Architecture_Validation/execution_core_isolation_audit.py` | `audit_tools/execution_core_isolation_audit.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Architecture_Validation/nexus_structural_audit.py` | `audit_tools/nexus_structural_audit.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Architecture_Validation/import_prefix_verifier.py` | `import_analysis/import_prefix_verifier.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Architecture_Validation/import_root_grouping_analyzer.py` | `import_analysis/import_root_grouping_analyzer.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Architecture_Validation/import_violation_classifier.py` | `import_analysis/import_violation_classifier.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Architecture_Validation/violation_prefix_grouper.py` | `import_analysis/violation_prefix_grouper.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Architecture_Validation/module_root_existence_checker.py` | `import_analysis/module_root_existence_checker.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Architecture_Validation/namespace_discovery_scan.py` | `import_analysis/namespace_discovery_scan.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Dependency_Analysis/generate_deep_import_violations.py` | `import_analysis/generate_deep_import_violations.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Repo_Audit/Import_Linter.py` | `import_analysis/Import_Linter.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Static_Analysis/generate_symbol_import_index.py` | `import_analysis/generate_symbol_import_index.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Static_Analysis/runtime_analysis.py` | `runtime_analysis/runtime_analysis.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Runtime_Diagnostics/runtime_callgraph_extractor.py` | `runtime_analysis/runtime_callgraph_extractor.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Runtime_Diagnostics/runtime_debug_artifact_scanner.py` | `runtime_analysis/runtime_debug_artifact_scanner.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Runtime_Diagnostics/runtime_execution_tracer.py` | `runtime_analysis/runtime_execution_tracer.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Runtime_Diagnostics/runtime_module_tree_auditor.py` | `runtime_analysis/runtime_module_tree_auditor.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Static_Analysis/ast_parser.py` | `semantic_extraction/ast_parser.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Static_Analysis/classifier.py` | `semantic_extraction/classifier.py` | NEAR-IDENTICAL | Deprecate AP copy |
| `Static_Analysis/semantic_extractor.py` | `semantic_extraction/semantic_extractor.py` | NEAR-IDENTICAL | Deprecate AP copy |

**Count:** 19 duplicate pairs  
**LOC waste estimate:** ~8,000–12,000 LOC of duplicated content inside AP

---

### 2B. LOGOS Canonical ↔ AP Internal — Partial Overlap (COMPLEMENTARY)

| LOGOS Runtime_Tools Module | AP Internal Module | Coverage Difference | Recommendation |
|----------------------------|--------------------|---------------------|----------------|
| `Dependency_Analysis/cluster_analysis.py` | `audit_tools/circular_dependency_audit.py` | LOGOS: cluster-level; AP: module-pair level | Retain both — different granularity |
| `Dependency_Analysis/cluster_analysis.py` | `audit_tools/cross_package_dependency_audit.py` | LOGOS: cluster boundary; AP: package boundary | Retain both |
| `Dependency_Analysis/cluster_analysis.py` | `runtime_analysis/dependency_graph.py` | LOGOS: full graph; AP: edges only | LOGOS supersedes |
| `Repo_Audit/Import_Linter.py` | `audit_tools/import_surface_audit.py` | LOGOS: rule-based; AP: surface enumeration | Complementary |
| `Dependency_Analysis/facade_synthesis.py` | `audit_tools/facade_bypass_audit.py` | LOGOS: facade discovery; AP: bypass detection | Complementary — different focus |

---

### 2C. AP Unique Tools (No LOGOS Equivalent — GAPS in LOGOS coverage)

| AP Internal Module | Functional Area | LOGOS Gap | Candidate for LOGOS Surface |
|--------------------|-----------------|-----------|-----------------------------|
| `audit_tools/governance_contract_audit.py` | Governance | LOGOS has no governance contract auditor | YES — HIGH PRIORITY |
| `audit_tools/governance_coverage_map.py` | Governance | LOGOS has no governance coverage mapper | YES — HIGH PRIORITY |
| `audit_tools/governance_module_audit.py` | Governance | LOGOS has no per-module governance auditor | YES — HIGH PRIORITY |
| `audit_tools/governance_scanner.py` | Governance | LOGOS has no governance scanner | YES — HIGH PRIORITY |
| `audit_tools/header_schema_audit.py` | Header validation | LOGOS has no header schema auditor | YES (schema update needed) |
| `audit_tools/duplicate_module_audit.py` | Module analysis | LOGOS has no name-duplicate detector | YES — MEDIUM |
| `audit_tools/module_path_ambiguity_audit.py` | Module analysis | LOGOS has no path ambiguity detector | YES — MEDIUM |
| `audit_tools/namespace_shadow_audit.py` | Import analysis | LOGOS has no namespace shadow detector | YES — MEDIUM |
| `audit_tools/orphan_module_audit.py` | Module graph | LOGOS has no orphan module detector | YES — MEDIUM |
| `audit_tools/symbol_collision_audit.py` | Module analysis | LOGOS has no symbol collision detector | YES — MEDIUM |
| `audit_tools/unused_import_audit.py` | Import analysis | LOGOS has no unused import auditor | YES — MEDIUM |
| `audit_tools/runtime_entry_audit.py` | Runtime | LOGOS has no entry-point auditor | YES — MEDIUM |
| `normalization_tools/normalization_engine.py` | Normalization | LOGOS has no normalization engine | YES — HIGH (unique asset) |
| `normalization_tools/header_validator.py` | Header | LOGOS has no header validator | YES |
| `normalization_tools/schema_registry.py` | Schema | LOGOS has no schema registry | YES |
| `audit_tools/_run_audit.py` (governance suite) | Audit orchestration | LOGOS has no governance audit driver | YES — HIGH |

---

### 2D. LOGOS-Unique Tools (Not in AP — Gaps in AP Coverage)

| LOGOS Runtime_Tools Module | Category | Description | Notes |
|----------------------------|----------|-------------|-------|
| `Dependency_Analysis/cluster_analysis.py` | Clustering | Full cluster-boundary analysis | AP has no equivalent |
| `Report_Generation/report_generator.py` | Report | Structured report generator | AP uses ad-hoc stdout patterns |
| `Repo_Audit/repo_mapper.py` | Repo mapping | Full repository topology mapper | AP tools map only WORKFLOW_MUTATION_TOOLING |
| `Static_Analysis/drac_indexer.py` | Protocol index | DRAC-specific indexer | AP semantic extraction tools are pre-migration |
| `Static_Analysis/packet_discovery.py` | Operational | Module packet graph generator | No AP equivalent |
| `Runtime_Diagnostics/runtime_debug_artifact_scanner.py` | Diagnostics | Debug artifact scanner (with 658 hits in AP) | AP has but may differ |

---

## 3. Capability Gap Summary

### Critical Gaps in LOGOS (that AP fills):
1. **Governance audit surface** — LOGOS has no governance contract, coverage, or module auditor; AP's 4 governance tools are ready candidates
2. **Header validation** — LOGOS has no header schema auditor; AP has one (needs schema translation)
3. **Normalization engine** — LOGOS has no normalization pipeline; AP's normalization_engine.py is a unique asset
4. **Symbol/namespace collision detection** — AP has 3 tools with no LOGOS equivalent

### Redundancy in AP (already covered by LOGOS):
1. **Runtime analysis surface** — 5 tools in `tools/runtime_analysis/` fully covered by LOGOS Runtime_Diagnostics
2. **Architecture validation surface** — 7 tools in `tools/import_analysis/` fully covered by LOGOS Architecture_Validation
3. **Static analysis duplicates** — semantic extraction tools all have LOGOS canonical versions

---

## 4. Consolidation Recommendations

### Phase 1 — Retire Pure Duplicates (19 tools):
Deprecate all AP tools flagged NEAR-IDENTICAL in Section 2A once LOGOS canonical versions are verified equivalent. Target: reduce AP internal tool count by ~20 modules.

### Phase 2 — Surface Unique AP Tools (16 tools):
The 16 AP-unique tools (Section 2C) should be evaluated for migration into LOGOS `Runtime_Tools/Governance_Audit/` (new subcategory) with:
- LOGOS-style RUNTIME_TOOL_METADATA header added
- AP-specific hard-coded paths removed (use `--root` / `--target` CLI args)
- Output format normalized to LOGOS JSON report standards
- `sys.path` injection replaced with proper package install or pyproject.toml configuration

### Phase 3 — Resolve Partial Overlaps (5 pairs):
Evaluate whether LOGOS or AP version provides superior coverage for each partial-overlap pair. Consolidate on the superior implementation; discard redundant copy.

---

## 5. Risk Factors

| Risk | Severity | Notes |
|------|----------|-------|
| AP tools use relative `sys.path` injection | HIGH | Tools won't work from LOGOS Python environment without CWD fix |
| AP governance tools validate against AP schemas, not LOGOS schemas | HIGH | Must be re-targeted before surfacing in LOGOS |
| AP normalization_engine.py has mutation capability | CRITICAL | Must be governed before integration |
| AP audit is orchestrated by `_run_audit.py` hard-wiring AP paths | HIGH | Cannot be invoked from LOGOS without interface contract |
| 19 duplicate tools create maintenance surface confusion | MEDIUM | LOGOS and AP may diverge independently |

---

*Report produced by: LOGOS Archon Prime Integration Audit — 2026-03-13*
