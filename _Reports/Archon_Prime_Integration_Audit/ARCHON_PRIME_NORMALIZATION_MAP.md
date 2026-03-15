# ARCHON PRIME — NORMALIZATION MAP
**Generated:** 2026-03-13  
**Scope:** Analysis-only normalization plan — no repository mutations authorized  
**Purpose:** Document what normalization would be required for each AP component category to reach LOGOS canonical standards  

---

## 1. Normalization Scope

"Normalization" in LOGOS context means aligning an external artifact to the LOGOS canonical conventions for:
1. Module header schema (LOGOS governance header format)
2. Import conventions (absolute `LOGOS_SYSTEM.*` paths or installed package)
3. Governance gate (LOGOS `GOVERNANCE_ENFORCEMENT/` authority)
4. Output schema (LOGOS report envelope format)
5. CLI interface (LOGOS `--root`, `--target`, `--output` conventions)
6. Naming conventions (LOGOS module naming / directory naming rules)
7. Path independence (no CWD assumptions)

---

## 2. Component Normalization Map

### 2A. Pure Duplicate Tools (19 tools — DEPRECATE)

These tools are near-identical copies of LOGOS canonical modules. No normalization needed — they should be deprecated.

| AP Module | LOGOS Canonical | Action |
|-----------|----------------|--------|
| `audit_tools/execution_core_isolation_audit.py` | `Architecture_Validation/execution_core_isolation_audit.py` | Verify equivalence → Deprecate AP copy |
| `audit_tools/nexus_structural_audit.py` | `Architecture_Validation/nexus_structural_audit.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/import_prefix_verifier.py` | `Architecture_Validation/import_prefix_verifier.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/import_root_grouping_analyzer.py` | `Architecture_Validation/import_root_grouping_analyzer.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/import_violation_classifier.py` | `Architecture_Validation/import_violation_classifier.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/violation_prefix_grouper.py` | `Architecture_Validation/violation_prefix_grouper.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/module_root_existence_checker.py` | `Architecture_Validation/module_root_existence_checker.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/namespace_discovery_scan.py` | `Architecture_Validation/namespace_discovery_scan.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/generate_deep_import_violations.py` | `Dependency_Analysis/generate_deep_import_violations.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/Import_Linter.py` | `Repo_Audit/Import_Linter.py` | Verify equivalence → Deprecate AP copy |
| `import_analysis/generate_symbol_import_index.py` | `Static_Analysis/generate_symbol_import_index.py` | Verify equivalence → Deprecate AP copy |
| `runtime_analysis/runtime_analysis.py` | `Static_Analysis/runtime_analysis.py` | Verify equivalence → Deprecate AP copy |
| `runtime_analysis/runtime_callgraph_extractor.py` | `Runtime_Diagnostics/runtime_callgraph_extractor.py` | Verify equivalence → Deprecate AP copy |
| `runtime_analysis/runtime_debug_artifact_scanner.py` | `Runtime_Diagnostics/runtime_debug_artifact_scanner.py` | Verify equivalence → Deprecate AP copy |
| `runtime_analysis/runtime_execution_tracer.py` | `Runtime_Diagnostics/runtime_execution_tracer.py` | Verify equivalence → Deprecate AP copy |
| `runtime_analysis/runtime_module_tree_auditor.py` | `Runtime_Diagnostics/runtime_module_tree_auditor.py` | Verify equivalence → Deprecate AP copy |
| `semantic_extraction/ast_parser.py` | `Static_Analysis/ast_parser.py` | Verify equivalence → Deprecate AP copy |
| `semantic_extraction/classifier.py` | `Static_Analysis/classifier.py` | Verify equivalence → Deprecate AP copy |
| `semantic_extraction/semantic_extractor.py` | `Static_Analysis/semantic_extractor.py` | Verify equivalence → Deprecate AP copy |

---

### 2B. Unique AP Governance Tools (HIGH VALUE — Target: `Runtime_Tools/Governance_Audit/`)

These tools have no LOGOS equivalent and address critical coverage gaps. Full normalization required.

#### `audit_tools/governance_contract_audit.py`

| Normalization Step | Current State | Required Change |
|-------------------|---------------|-----------------|
| Module header | AP comment-block header | Replace with LOGOS RUNTIME_TOOL_METADATA docstring |
| Import convention | Bare relative imports | Convert to absolute package imports via pyproject.toml install |
| Governance gate | `enforce_runtime_gate()` | Replace with LOGOS `GOVERNANCE_ENFORCEMENT` gate mechanism |
| Output schema | AP-internal JSON | Convert to LOGOS report envelope format |
| CLI interface | Hardcoded paths | Add `--root`, `--output`, `--target` CLI args |
| Target path | AP-specific WORKFLOW_NEXUS paths | Parameterize to accept any LOGOS governance path |
| Naming | `governance_contract_audit.py` | Compliant — no change needed |

#### `audit_tools/governance_coverage_map.py`
*(Same normalization table as above — identical requirements)*

#### `audit_tools/governance_module_audit.py`
*(Same normalization table — additionally: module-role field in output must map to LOGOS module roles)*

#### `audit_tools/governance_scanner.py`
*(Same normalization table — additionally: scan patterns must be updated from AP governance gate to LOGOS governance gate string)*

---

### 2C. Unique AP Analysis Tools (MEDIUM VALUE — Target: `Runtime_Tools/Extended_Analysis/`)

| AP Module | Additional Normalization Notes |
|-----------|-------------------------------|
| `audit_tools/duplicate_module_audit.py` | Parameterize scan root; normalize output |
| `audit_tools/module_path_ambiguity_audit.py` | Parameterize; normalize output |
| `audit_tools/namespace_shadow_audit.py` | Parameterize; normalize output |
| `audit_tools/orphan_module_audit.py` | Parameterize; normalize output |
| `audit_tools/symbol_collision_audit.py` | Parameterize; normalize output |
| `audit_tools/unused_import_audit.py` | Parameterize; normalize output |
| `audit_tools/runtime_entry_audit.py` | Parameterize; normalize output |
| `audit_tools/facade_bypass_audit.py` | Parameterize; verify LOGOS facade surfaces are covered |
| `audit_tools/import_surface_audit.py` | Parameterize; normalize output |
| `audit_tools/circular_dependency_audit.py` | Compare vs cluster_analysis.py; merge if superior |
| `audit_tools/cross_package_dependency_audit.py` | Compare vs generate_deep_import_violations.py; merge if superior |

---

### 2D. Header Schema Auditor (Requires Schema Translation)

#### `audit_tools/header_schema_audit.py`

| Normalization Step | Current State | Required Change |
|-------------------|---------------|-----------------|
| Validation target | `AP_MODULE_HEADER_SCHEMA.json` | Re-target to LOGOS header schema |
| Header schema format | AP comment-block (17 fields) | Map to LOGOS RUNTIME_TOOL_METADATA docstring format |
| Schema location | `AP_SYSTEM_CONFIG/` | Move schema to LOGOS governance schema directory |
| Governance gate | AP internal | LOGOS governance |
| Output | AP-internal JSON | LOGOS report format |

---

### 2E. Normalization Engine (CRITICAL — Requires Governance)

#### `normalization_tools/normalization_engine.py`

| Normalization Step | Current State | Required Change |
|-------------------|---------------|-----------------|
| Mutation capability | YES — can rewrite files | MUST be governed before any LOGOS integration |
| Governance gate | AP internal | LOGOS governance artifact REQUIRED before integration |
| Target scope | AP module headers | Must be re-scoped to LOGOS targets under governance |
| CLI interface | Hardcoded AP paths | Must accept `--root`, `--target`, `--dry-run` flags |
| Output | AP mutation record schema | Align to LOGOS mutation record format |
| Safety classification | MUTATING — like `facade_rewrite_pass.py` | Must be classified READ_ONLY in dry-run, MUTATING otherwise |

**Status:** CANNOT be integrated without a LOGOS governance artifact authorizing its execution scope.

---

### 2F. Broken Pre-Migration Tools (DEPRECATE or Repair)

| AP Module | Broken Import | Repair Path | Disposition |
|-----------|--------------|-------------|-------------|
| `semantic_extraction/extract.py` | `from Tools.Scripts.*` (4 imports) | Map to LOGOS package equivalents OR deprecate if LOGOS version exists | DEPRECATE (LOGOS has `Code_Extraction/extract.py`) |
| `semantic_extraction/legacy_extract.py` | `from drac_af_extractor.ast_parser import parse_file` | Legacy; `drac_af_extractor` no longer exists | DEPRECATE |

---

### 2G. AP-Internal Tools (REMAIN AP-LOCAL — No Normalization to LOGOS)

| AP Module | Reason for No Normalization |
|-----------|----------------------------|
| `WORKFLOW_NEXUS/Governance/workflow_gate.py` | AP-internal governance; no LOGOS surface equivalent |
| `controllers/pipeline_controller.py` | AP orchestration core; not a LOGOS protocol |
| `controllers/config_loader.py` | AP config format; not applicable to LOGOS |
| `crawler/core/crawl_engine.py` | AP-specific crawl logic |
| `crawler/core/crawl_monitor.py` | AP-specific monitoring |
| `mutation/repair/operators/*` | Mutating operators; must remain AP-governed |
| `processors/fbc_registry.py` | AP-internal registry |
| Schema files under `AP_SYSTEM_CONFIG/` | AP-specific schemas; may inform LOGOS schema design |

---

## 3. Normalization Priority Matrix

| Priority | Category | Tools | Rationale |
|----------|----------|-------|-----------|
| P0 — Prerequisite | Fix SyntaxError in bridge neighbor | 1 file | Blocks any bridge integration |
| P0 — Prerequisite | Resolve AP pyproject.toml install | 1 action | Unblocks all AP imports |
| P1 — High | Deprecate pure duplicates | 19 tools | Immediate maintenance debt reduction |
| P1 — High | Surface governance tools | 4 tools | Fills critical LOGOS gap |
| P2 — Medium | Surface extended analysis tools | 11 tools | Adds meaningful LOGOS coverage |
| P2 — Medium | Normalize header schema auditor | 1 tool | Schema update required |
| P3 — Governed | Normalize normalization engine | 1 tool | Requires governance artifact first |
| P3 — Governed | All mutating repair operators | 8+ tools | Require governance artifacts |
| P4 — Deferred | Schema/envelope LOGOS alignment | N/A | Design task, not normalization |

---

## 4. Normalization Pattern Template

For any AP tool being normalized to LOGOS canonical standard, the following template applies:

```python
# ------------------------------------------------------------------
# RUNTIME_TOOL_METADATA
# tool_id:              RT-NEW-NNN
# tool_name:            <tool_name>
# category:             Governance_Audit | Extended_Analysis | ...
# mutation_capability:  NONE
# safety_classification: READ_ONLY
# target_scope:         repository | module | file
# output_format:        JSON
# output_path:          _Dev_Resources/Reports/Tool_Outputs/Runtime/
# logos_version:        1.0
# source:               ARCHON_PRIME (normalized)
# ------------------------------------------------------------------
"""<tool description>"""

import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", default="_Dev_Resources/Reports/Tool_Outputs/Runtime/")
    args = parser.parse_args()
    # ... implementation
```

---

*Report produced by: LOGOS Archon Prime Integration Audit — 2026-03-13*
