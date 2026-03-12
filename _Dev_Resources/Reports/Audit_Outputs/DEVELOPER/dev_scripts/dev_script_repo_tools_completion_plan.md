# Dev Script Repo_Tools Completion Plan
**Version:** 1.0  
**Generated:** 2026-03-11  
**Scope:** Architecture analysis and migration plan to populate empty Repo_Tools categories  
**Authority:** Analysis only — no files moved, modified, or deleted

---

## 1. Missing Tool Categories

### Confirmed Empty Directories

| Directory | Status |
|-----------|--------|
| `Repo_Tools/Runtime_Diagnostics/` | EMPTY — no tools assigned |
| `Repo_Tools/Architecture_Validation/` | EMPTY — no tools assigned |

### Expected Tool Types for Each Category

#### `Runtime_Diagnostics/` — Expected Tool Types

| Tool Type | Description |
|-----------|-------------|
| Call graph extractor | Static AST traversal from entry points to map reachable modules |
| Live execution tracer | `sys.settrace()`-based call tracing across LOGOS_SYSTEM surface |
| Execution core isolation auditor | Verifies RUNTIME_EXECUTION_CORE boundary containment |
| Runtime debug artifact scanner | Scans runtime dirs for `print()`, bare `assert`, `TODO` statements |
| Module tree auditor | AST inventory of any runtime subsystem: classes, functions, LOC, layer deps |

#### `Architecture_Validation/` — Expected Tool Types

| Tool Type | Description |
|-----------|-------------|
| Import violation classifier | Loads linter artifacts; classifies violations by rule and prefix |
| Import root grouping analyzer | Groups violations by root module prefix and occurrence frequency |
| Namespace discovery scanner | Discovers physical locations of named namespaces in the repo tree |
| Import prefix verifier | Extracts and counts literal import prefixes from violation records |
| Module root existence checker | Verifies declared import roots actually exist on disk |
| Violation prefix grouper | Groups violations by N-segment prefix; produces distribution reports |
| Nexus structural auditor | Validates NEXUS classification (EXECUTION_NEXUS/BINDING_NEXUS/NON_NEXUS) |
| Execution core isolation auditor | Verifies reachable-module scope from STARTUP entry points |

---

## 2. Candidate Migration Scripts

### 2.1 P1-5 Scripts — Full Classification

| Script | Functions / Key Logic | Mutation Risk | Phase-Specific | Classification |
|--------|-----------------------|---------------|----------------|----------------|
| `Phase_2A_AST_Canonical_Root_Normalization.py` | `ImportRootNormalizer` (AST NodeTransformer), `should_exclude()` — rewrites `Logos_System.*` → `LOGOS_SYSTEM.*` in source | HIGH — rewrites `.py` files in-place | YES — Phase 2A migration campaign | `PHASE_PIPELINE_TOOL` |
| `Phase_2A_Corrected_Case_Normalization.py` | Inline regex pass — `Logos_System` → `LOGOS_SYSTEM` case normalization | HIGH — rewrites `.py` files in-place | YES — Phase 2A one-time fix | `PHASE_PIPELINE_TOOL` |
| `Phase_2A_Rule2_Classification.py` | Loads `Import_Linter_Report.json`; extracts Rule_2 violations; classifies by prefix distribution | LOW — read-only analysis, writes JSON | Partially — depends on linter artifact, not on phase sequence | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `Phase_2B_A_Rule2_Root_Grouping.py` | Groups Rule_2 violations from linter report by root module prefix and module frequency | NONE — read-only | Partially — depends on linter artifact | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `Phase_2B_Pre_Discovery_Structure_Scan.py` | READ-ONLY — discovers actual on-disk namespace locations of target directory names; writes JSON | NONE — explicitly marked READ-ONLY | YES — Phase 2B, but TARGET_DIRS is parameterizable | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `Phase_2F_Prefix_String_Verification.py` | Reads Rule_2 violations; extracts and counts literal import prefixes up to 4 segments | NONE — read-only | Partially — depends on linter artifact | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `Phase_3A_Rule3_Canonical_Expansion.py` | AST-based import rewrite: expands bare protocol roots to full LOGOS_SYSTEM paths per hardcoded canonical map | HIGH — rewrites `.py` files | YES — specific CANONICAL_PREFIX_MAP | `PHASE_PIPELINE_TOOL` |
| `Phase_3B_Agent_Canonical_Expansion.py` | AST-based import rewrite: expands I1_Agent, I2_Agent, I3_Agent to full LOGOS_SYSTEM agent paths | HIGH — rewrites `.py` files | YES — specific agent canonical map | `PHASE_PIPELINE_TOOL` |
| `Run_Nexus_Structural_Audit.py` | Invokes `NexusASTValidator("LOGOS_SYSTEM")`; classifies all LOGOS_SYSTEM files into EXECUTION_NEXUS/BINDING_NEXUS/NON_NEXUS; detects violations; writes JSON | LOW — read-only analysis, writes report | NO — fully generic; no phase number in logic | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `m5_validation_scan.py` | Scans `STARTUP/`, `LOGOS_SYSTEM/` for `print()` statements; compares against stored `runtime_print_inventory.json`; reports delta | NONE — read-only scan | Partially — references M5 milestone and depends on `_Governance/Audit_Artifacts/runtime_print_inventory.json` | **`RUNTIME_DIAGNOSTIC_CANDIDATE`** |
| `phase6_runtime_callgraph_extractor.py` | AST traversal from `STARTUP/START_LOGOS.py` and `STARTUP/LOGOS_SYSTEM.py`; maps reachable modules; records dynamic imports, `sys.path` mutations, `eval`/`exec` sites; writes JSON | LOW — read-only, writes to `_Reports/` | YES — Phase 6, entry points hardcoded | **`RUNTIME_DIAGNOSTIC_CANDIDATE`** |
| `phase6b_runtime_execution_tracer.py` | Live `sys.settrace()` tracing; captures LOGOS_SYSTEM call edges, DRAC touchpoints, RUNTIME_BRIDGE touchpoints, agent boot sequences | NONE — passive tracing | YES — Phase 6b, requires live execution | **`RUNTIME_DIAGNOSTIC_CANDIDATE`** |
| `phase6c_execution_core_isolation_audit.py` | AST-based reachable-module analysis constrained to `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE`; maps module scope from STARTUP entry points; flags boundary violations | NONE — read-only | YES — Phase 6c, but INCLUDE_ROOT is parameterizable | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `phase_2b_ast_mutator.py` | AST-based prefix expansion pass: protocol root canonical expansion for Phase 2B (same functional purpose as Phase_3A but different PREFIX_MAP) | HIGH — rewrites `.py` files | YES — duplication with Phase_3A at different phase | `PHASE_PIPELINE_TOOL` |
| `phase_2c_root_existence_map.py` | READ-ONLY — verifies each unique Rule_2 root prefix against disk; maps physical locations; writes JSON | NONE — read-only | Partially — depends on Phase_2A artifact | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `phase_2d_canonical_root_expansion.py` | AST-based import rewrite: Rule_2 legacy roots → fully canonical LOGOS_SYSTEM paths | HIGH — rewrites `.py` files | YES — Phase 2D | `PHASE_PIPELINE_TOOL` |
| `phase_2e_rule2_prefix_grouping.py` | Groups Rule_2 violations by 3-segment prefix; counts occurrences and unique files | NONE — read-only | Partially — depends on Phase_2C artifact | **`ARCHITECTURE_VALIDATION_CANDIDATE`** |
| `phase_2f_structural_namespace_relocation.py` | AST + `astor` rewrite pass for structural namespace relocation; CRITICAL mutation risk | CRITICAL — rewrites source files, requires external `astor` | YES — Phase 2F | `PHASE_PIPELINE_TOOL` |

### 2.2 RGE Scripts — Full Classification

| Script | Functionality | Stage-Specific | Generalizable | Classification |
|--------|---------------|----------------|---------------|----------------|
| `rge_audit_runner.py` | Multi-step AST audit of RGE module tree: builds module inventory, dependency graph, cross-layer dependency map, architecture compliance report (PASS/FAIL), workflow metrics | NO — analyzes the whole RGE subtree for any state | YES — parameterizing `RGE_ROOT` makes it a generic module tree auditor for any subsystem | **`RUNTIME_DIAGNOSTIC_CANDIDATE`** |
| `rge_stage10_12_smoke.py` | Functional smoke test: RGE Field Topology stages 10–12 — node creation, topology container, bridge assignment | YES — tightly coupled to stages 10–12 classes | NO — tests specific RGE component contracts | `RGE_STAGE_SPECIFIC` |
| `rge_stage13_16_smoke.py` | Functional smoke test: RGE Field Graph stages 13–16 — edge creation, graph storage, builder connection, traversal neighbors | YES — tightly coupled to stages 13–16 classes | NO — tests specific RGE component contracts | `RGE_STAGE_SPECIFIC` |
| `rge_stage17_20_smoke.py` | Functional smoke test: Packet Propagation stages 17–20 — location tracking, node accessor, propagation movement, engine propagation hook | YES — tightly coupled to stages 17–20 classes | NO — tests specific RGE component contracts | `RGE_STAGE_SPECIFIC` |
| `rge_stage21_24_smoke.py` | Functional smoke test: Cognition Signal Broadcasting stages 21–24 — signal object, subscriber registration, broadcaster emission, engine signal emission | YES — tightly coupled to stages 21–24 classes | NO — tests specific RGE component contracts | `RGE_STAGE_SPECIFIC` |
| `rge_stage25_28_smoke.py` | Functional smoke test: Runtime Bridge Integration stages 25–28 — dispatcher registration, multi-runtime dispatch, channel-triggered dispatch, registry access, engine-to-runtime dispatch | YES — tightly coupled to stages 25–28 classes | NO — tests specific RGE component contracts | `RGE_STAGE_SPECIFIC` |
| `rge_stage29_31_smoke.py` | Functional smoke test: RGE Bootstrap and Runtime Activation stages 29–31 — bridge nexus, runtime bootstrap, activation manager | YES — tightly coupled to stages 29–31 classes | NO — tests specific RGE component contracts | `RGE_STAGE_SPECIFIC` |

---

## 3. Normalization Requirements

### 3.1 Architecture_Validation Candidates — Normalization Plan

| Source Script | Normalized Tool Name | Phase Prefix | Stage Numbers | Subsystem Assumptions | Parameterize Targets | CLI Invocation |
|---------------|---------------------|:------------:|:-------------:|:---------------------:|:--------------------:|:--------------:|
| `Phase_2A_Rule2_Classification.py` | `import_violation_classifier.py` | Remove | N/A | Remove linter-artifact hardcoding; accept `--input` | `--input <linter_report.json>` | Add `if __name__ == "__main__"` with argparse |
| `Phase_2B_A_Rule2_Root_Grouping.py` | `import_root_grouping_analyzer.py` | Remove | N/A | Hardcoded `_Reports/Import_Linter_Report.json` → `--input` | `--input <report.json>` | Add `if __name__ == "__main__"` with argparse |
| `Phase_2B_Pre_Discovery_Structure_Scan.py` | `namespace_discovery_scan.py` | Remove | N/A | Hardcoded `TARGET_DIRS` list → accept `--targets` or config JSON | `--root`, `--targets` | Already script-body style; wrap in `main()` |
| `Phase_2F_Prefix_String_Verification.py` | `import_prefix_verifier.py` | Remove | N/A | Hardcoded `_Reports/Import_Linter_Report.json` → `--input` | `--input <report.json>`, `--max-segments` | Add `main()` and argparse |
| `Run_Nexus_Structural_Audit.py` | `nexus_structural_audit.py` | None (already clean) | N/A | Hardcoded `"LOGOS_SYSTEM"` scan root → `--root` | `--root <directory>`, `--output <path>` | Already has `if __name__ == "__main__"` |
| `phase_2c_root_existence_map.py` | `module_root_existence_checker.py` | Remove | N/A | Hardcoded `INPUT_PATH` and `RUNTIME_DIRS` → `--input`, `--scan-dirs` | `--input <classification.json>`, `--scan-dirs` | Add argparse |
| `phase_2e_rule2_prefix_grouping.py` | `violation_prefix_grouper.py` | Remove | N/A | Hardcoded `INPUT_PATH`/`OUTPUT_PATH` → `--input`, `--output` | `--input`, `--output`, `--prefix-depth` | Add argparse |
| `phase6c_execution_core_isolation_audit.py` | `execution_core_isolation_audit.py` | Remove (phase6c) | Remove | Hardcoded `INCLUDE_ROOT` and `EXCLUDE_PATTERNS` → `--include-root`, `--exclude` | `--roots <entry_points>`, `--include-root`, `--exclude` | Partial; add argparse |

### 3.2 Runtime_Diagnostics Candidates — Normalization Plan

| Source Script | Normalized Tool Name | Phase Prefix | Stage Numbers | Subsystem Assumptions | Parameterize Targets | CLI Invocation |
|---------------|---------------------|:------------:|:-------------:|:---------------------:|:--------------------:|:--------------:|
| `m5_validation_scan.py` | `runtime_debug_artifact_scanner.py` | Remove (m5_) | N/A | Hardcoded M5 milestone text, hardcoded inventory path → `--inventory` | `--scan-dirs`, `--inventory <json>`, `--pattern` | Add `main()` and argparse |
| `phase6_runtime_callgraph_extractor.py` | `runtime_callgraph_extractor.py` | Remove (phase6_) | Remove | Hardcoded `ROOTS` (STARTUP entry points) and `EXCLUDE_PATTERNS` | `--roots <entry_points>`, `--exclude`, `--output` | Add argparse |
| `phase6b_runtime_execution_tracer.py` | `runtime_execution_tracer.py` | Remove | Remove | Hardcoded `is_logos_system_file()` predicate (targets `LOGOS_SYSTEM/`) → `--target-prefix` | `--target-prefix`, `--entry-script`, `--output` | Add `main()` and argparse |
| `rge_audit_runner.py` | `runtime_module_tree_auditor.py` | None — rename for generic use | N/A | Hardcoded `RGE_ROOT` and `REPORTS_DIR` → `--module-root`, `--output` | `--module-root <path>`, `--output <dir>` | Already body script; add `main()` |

### 3.3 Scripts Requiring No Normalization

`Run_Nexus_Structural_Audit.py` is the closest to a canonical, ready-to-migrate tool. It uses the `logos.imports.governance.NexusASTValidator` API correctly and already has `if __name__ == "__main__"` with a well-scoped report. Only the input path needs to be exposed as a CLI argument.

---

## 4. RGE Structural Assessment

### Current State

The `RGE/` directory contains:
- **1 audit runner** (`rge_audit_runner.py`) — a broad-scope AST audit of the RGE module tree
- **5 stage-coupled smoke tests** (`rge_stage{10-12,13-16,17-20,21-24,25-28,29-31}_smoke.py`) — each tests a specific band of RGE stages with tight class-level coupling to `LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.*`

### Assessment

The 5 stage smoke tests are **correctly placed in `RGE/`** and should remain there. They are:
- RGE-subsystem-specific (test RGE classes in isolation)
- Not generalizable to repo-wide diagnostics
- Already semantically named for their scope
- Appropriate candidates for pytest discovery if converted to test functions

`rge_audit_runner.py` is a **dual-concern tool**:
- As-is, it is an RGE-specific audit runner with hardcoded paths
- Normalized, it becomes `runtime_module_tree_auditor.py` and belongs in `Runtime_Diagnostics/`

### Recommendation

**Keep `RGE/` as a standalone directory.** Do not consolidate into `Repo_Tools/Runtime_Diagnostics/`. Rationale:

1. The stage smoke tests are RGE-operational tooling, not repo-wide diagnostic tools
2. Merging would violate the classification-based placement principle
3. The stage smoke tests are best kept adjacent to the subsystem they test

**Action:** Create a normalized copy of `rge_audit_runner.py` as `runtime_module_tree_auditor.py` in `Runtime_Diagnostics/`. The original may be archived after normalization is validated.

**Long-term:** Convert `rge_stage*_smoke.py` files to pytest-compatible test functions and move them to the RGE test suite under `LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Tests/` or register them in the canonical pytest configuration.

---

## 5. Deletion Candidates

After thorough analysis, **no scripts are recommended for immediate deletion**. Reasons:

### Phase Pipeline Tools — Archive, Not Delete

The following scripts (`PHASE_PIPELINE_TOOL`) completed one-time migration operations but represent historical record of how the import repair campaign was executed. They should be **archived** rather than deleted, as they may be needed if:
- A regression reintroduces legacy import roots
- A new subsystem is onboarded via the same pipeline
- An audit requires proof of which transforms were applied

| Script | Reason for Archive (not delete) | Dependency Impact |
|--------|--------------------------------|-------------------|
| `Phase_2A_AST_Canonical_Root_Normalization.py` | Completed one-time AST migration of `Logos_System` → `LOGOS_SYSTEM`. May be re-run if regression. | No downstream scripts depend on it |
| `Phase_2A_Corrected_Case_Normalization.py` | Functionally redundant with AST version but preserves regex approach as fallback. | No downstream scripts depend on it |
| `Phase_3A_Rule3_Canonical_Expansion.py` | Protocol root expansion campaign — completed. Specific PREFIX_MAP represents architectural intent. | None |
| `Phase_3B_Agent_Canonical_Expansion.py` | Agent canonical expansion — completed. | None |
| `phase_2b_ast_mutator.py` | Phase 2B AST mutator for protocol roots — partially overlaps with Phase_3A. | None |
| `phase_2d_canonical_root_expansion.py` | Phase 2D canonical expansion — completed. | None |
| `phase_2f_structural_namespace_relocation.py` | Phase 2F relocation pass — requires external `astor` dependency; highest mutation risk. | Requires `astor` to run |

### Potential Redundancy — Phase 2A Pair

`Phase_2A_AST_Canonical_Root_Normalization.py` and `Phase_2A_Corrected_Case_Normalization.py` both target `Logos_System` → `LOGOS_SYSTEM` root normalization, making them **functionally overlapping** within Phase 2A. The AST version is more precise and safer. The regex version is a quick fallback. Neither should be deleted until the campaign is formally declared complete and all regressions are confirmed absent.

---

## 6. Final Repo_Tools Completion Strategy

### 6.1 Runtime_Diagnostics — Recommended Population

| Priority | Normalized Tool Name | Source Script | Key Normalization Steps |
|----------|----------------------|---------------|-------------------------|
| HIGH | `runtime_callgraph_extractor.py` | `P1-5/phase6_runtime_callgraph_extractor.py` | Remove `phase6_` prefix; expose `--roots`, `--exclude`, `--output` as CLI args; refactor `ROOTS`/`EXCLUDE_PATTERNS`/`REPORT_DIR` constants into argparse defaults |
| HIGH | `runtime_execution_tracer.py` | `P1-5/phase6b_runtime_execution_tracer.py` | Remove `phase6b_` prefix; parameterize target module prefix filter; add `main()` + argparse; expose `--target-prefix`, `--entry-script`, `--output` |
| HIGH | `runtime_module_tree_auditor.py` | `RGE/rge_audit_runner.py` | Parameterize `RGE_ROOT` → `--module-root`; parameterize `REPORTS_DIR` → `--output`; add argparse; generalize `LAYER_MAP` to accept external config |
| MEDIUM | `runtime_debug_artifact_scanner.py` | `P1-5/m5_validation_scan.py` | Remove M5 references; parameterize RUNTIME_DIRS → `--scan-dirs`; parameterize inventory path → `--inventory`; allow `--pattern` for scanning beyond `print()`; add argparse |

### 6.2 Architecture_Validation — Recommended Population

| Priority | Normalized Tool Name | Source Script | Key Normalization Steps |
|----------|----------------------|---------------|-------------------------|
| HIGH | `nexus_structural_audit.py` | `P1-5/Run_Nexus_Structural_Audit.py` | Minimal changes: add `--root`, `--output` CLI args; rename for convention compliance (already functional) |
| HIGH | `execution_core_isolation_audit.py` | `P1-5/phase6c_execution_core_isolation_audit.py` | Remove `phase6c_` prefix; expose `--include-root`, `--roots`, `--exclude`, `--output` as CLI args |
| HIGH | `import_violation_classifier.py` | `P1-5/Phase_2A_Rule2_Classification.py` | Remove phase prefix; replace hardcoded `CANDIDATES` list with `--input` arg; add `main()` + argparse |
| MEDIUM | `namespace_discovery_scan.py` | `P1-5/Phase_2B_Pre_Discovery_Structure_Scan.py` | Remove phase prefix; externalize `TARGET_DIRS` as `--targets` JSON or comma-separated; add argparse |
| MEDIUM | `import_root_grouping_analyzer.py` | `P1-5/Phase_2B_A_Rule2_Root_Grouping.py` | Remove phase prefix; externalize `REPORT_PATH` as `--input`; add argparse |
| MEDIUM | `import_prefix_verifier.py` | `P1-5/Phase_2F_Prefix_String_Verification.py` | Remove phase prefix; externalize input path; add `--max-segments` arg |
| LOW | `module_root_existence_checker.py` | `P1-5/phase_2c_root_existence_map.py` | Remove phase prefix; externalize `INPUT_PATH` and `RUNTIME_DIRS` as CLI args |
| LOW | `violation_prefix_grouper.py` | `P1-5/phase_2e_rule2_prefix_grouping.py` | Remove phase prefix; externalize `INPUT_PATH`/`OUTPUT_PATH`; add `--prefix-depth` |

### 6.3 P1-5 Scripts — Post-Migration Disposition

| Script | Disposition | Rationale |
|--------|-------------|-----------|
| `Phase_2A_AST_Canonical_Root_Normalization.py` | Keep in P1-5; archive candidate | Phase-specific migration tool; completed |
| `Phase_2A_Corrected_Case_Normalization.py` | Keep in P1-5; archive candidate | Regex fallback for Phase 2A normalization; completed |
| `Phase_2A_Rule2_Classification.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Analysis logic warrants both |
| `Phase_2B_A_Rule2_Root_Grouping.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Analysis logic warrants both |
| `Phase_2B_Pre_Discovery_Structure_Scan.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Logic is reusable |
| `Phase_2F_Prefix_String_Verification.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Analysis logic warrants both |
| `Phase_3A_Rule3_Canonical_Expansion.py` | Keep in P1-5; archive candidate | Completed pipeline stage |
| `Phase_3B_Agent_Canonical_Expansion.py` | Keep in P1-5; archive candidate | Completed pipeline stage |
| `Run_Nexus_Structural_Audit.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Closest to ready-to-migrate tool |
| `m5_validation_scan.py` | Keep in P1-5; CREATE normalized copy in Runtime_Diagnostics | Runtime diagnostic logic is reusable |
| `phase6_runtime_callgraph_extractor.py` | Keep in P1-5; CREATE normalized copy in Runtime_Diagnostics | Core diagnostic logic is generic |
| `phase6b_runtime_execution_tracer.py` | Keep in P1-5; CREATE normalized copy in Runtime_Diagnostics | Unique live-trace capability |
| `phase6c_execution_core_isolation_audit.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Generalizable isolation audit |
| `phase_2b_ast_mutator.py` | Keep in P1-5; archive candidate | Completed Phase 2B; functionally similar to Phase_3A |
| `phase_2c_root_existence_map.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Root existence verification is reusable |
| `phase_2d_canonical_root_expansion.py` | Keep in P1-5; archive candidate | Completed pipeline stage |
| `phase_2e_rule2_prefix_grouping.py` | Keep in P1-5; CREATE normalized copy in Arch_Validation | Violation grouping is reusable |
| `phase_2f_structural_namespace_relocation.py` | Keep in P1-5; archive candidate | Completed pipeline stage; requires `astor` |

### 6.4 RGE Scripts — Post-Migration Disposition

| Script | Disposition | Rationale |
|--------|-------------|-----------|
| `rge_audit_runner.py` | Keep in RGE; CREATE normalized copy in Runtime_Diagnostics | Dual-concern: RGE-specific origin, generic audit pattern |
| `rge_stage10_12_smoke.py` | Keep in RGE | Stage-specific; correctly placed |
| `rge_stage13_16_smoke.py` | Keep in RGE | Stage-specific; correctly placed |
| `rge_stage17_20_smoke.py` | Keep in RGE | Stage-specific; correctly placed |
| `rge_stage21_24_smoke.py` | Keep in RGE | Stage-specific; correctly placed |
| `rge_stage25_28_smoke.py` | Keep in RGE | Stage-specific; correctly placed |
| `rge_stage29_31_smoke.py` | Keep in RGE | Stage-specific; correctly placed |

---

## 7. Repo Governance Tooling Proposal

### Proposed Directory

```
/workspaces/Logos/_Dev_Resources/_Dev_Scripts/Repo_Governance/
```

This directory should contain tools that operate on the dev tooling infrastructure itself — enforcing placement rules, validating the tool registry, and auditing governance compliance of dev scripts.

### Proposed Tools

#### `repo_policy_enforcer.py`
**Role:** Scans `Repo_Tools/` and validates that every `.py` file has a corresponding entry in `dev_tool_registry.json`. Flags unregistered scripts ('orphans') and registered scripts missing from disk ('phantoms'). Enforces placement: every script must live in one of the 9 canonical classification directories.

**Inputs:** `Repo_Tools/` filesystem tree, `dev_tool_registry.json`  
**Outputs:** `_Reports/_Dev_Scripts_Output/policy_enforcement_report.json`  
**Capabilities:** orphan_detection, phantom_detection, placement_validation, registry_coherence_check

---

#### `directory_structure_validator.py`
**Role:** Validates that `_Dev_Scripts/` directory structure matches the canonical schema defined in the tool policies. Checks for: correct Title_Case_With_Underscores naming, presence of all 9 required Repo_Tools subdirectories, absence of disallowed ad-hoc directories, protection of `P1-5/` and `RGE/`.

**Inputs:** `_Dev_Scripts/` filesystem tree, canonical schema (inline or from config)  
**Outputs:** `_Reports/_Dev_Scripts_Output/directory_structure_validation.json`  
**Capabilities:** naming_convention_check, required_directory_verification, ad_hoc_directory_detection, protected_directory_guard

---

#### `tool_registry_validator.py`
**Role:** Validates the three Tool Index artifacts (`dev_scripts_manifest.json`, `dev_tool_registry.json`, `dev_tool_capability_index.json`) for internal consistency. Checks: all manifest entries have a matching registry entry, all capability index entries reference valid tools, no capability or dependency references are orphaned, entry counts agree across all three files.

**Inputs:** `Tool_Index/dev_scripts_manifest.json`, `Tool_Index/dev_tool_registry.json`, `Tool_Index/dev_tool_capability_index.json`  
**Outputs:** `_Reports/_Dev_Scripts_Output/tool_registry_validation.json`  
**Capabilities:** cross_artifact_consistency_check, entry_count_validation, orphaned_reference_detection, capability_integrity_check

---

#### `devscript_header_validator.py`
**Role:** Reads every `.py` file in `Repo_Tools/` and validates that each file has: a module-level docstring describing purpose, a defined invocation pattern or note about module-only use, and no hardcoded absolute paths outside of config constants. Flags files that are missing docstrings or contain unparameterized hardcoded workspace paths.

**Inputs:** `Repo_Tools/` filesystem tree  
**Outputs:** `_Reports/_Dev_Scripts_Output/devscript_header_validation.json`  
**Capabilities:** docstring_presence_check, invocation_pattern_check, hardcoded_path_detection

---

#### `governance_audit.py`
**Role:** Comprehensive governance sweep. Calls all four validators in sequence and produces a unified audit report with PASS/FAIL status for each check. Records timestamp, total issues found, and recommended actions. This is the single-command audit entry point for the dev tooling infrastructure.

**Inputs:** All `Repo_Tools/` and `Tool_Index/` artifacts  
**Outputs:** `_Reports/_Dev_Scripts_Output/dev_governance_audit.json`, `_Reports/_Dev_Scripts_Output/dev_governance_audit_summary.md`  
**Capabilities:** full_governance_sweep, multi_validator_orchestration, audit_report_generation

---

### Repo_Governance Directory Structure

```
Repo_Governance/
├── repo_policy_enforcer.py
├── directory_structure_validator.py
├── tool_registry_validator.py
├── devscript_header_validator.py
└── governance_audit.py
```

All tools in `Repo_Governance/` must be:
- Read-only (no source mutations)
- Fully parameterized (no hardcoded workspace paths)
- Registered in `dev_tool_registry.json` after creation
- Non-destructive (all destructive_capability_flag: false)

---

## Appendix A — Total Scripts Analyzed

| Source | Scripts Analyzed |
|--------|-----------------|
| `P1-5/` | 18 |
| `RGE/` | 7 |
| **Total** | **25** |

## Appendix B — Summary Table

| Category | Count | Scripts |
|----------|-------|---------|
| `ARCHITECTURE_VALIDATION_CANDIDATE` | 8 | Phase_2A_Rule2_Classification, Phase_2B_A_Rule2_Root_Grouping, Phase_2B_Pre_Discovery_Structure_Scan, Phase_2F_Prefix_String_Verification, Run_Nexus_Structural_Audit, phase_2c_root_existence_map, phase_2e_rule2_prefix_grouping, phase6c_execution_core_isolation_audit |
| `RUNTIME_DIAGNOSTIC_CANDIDATE` | 5 | m5_validation_scan, phase6_runtime_callgraph_extractor, phase6b_runtime_execution_tracer, rge_audit_runner (RGE) |
| `PHASE_PIPELINE_TOOL` | 7 | Phase_2A_AST_Canonical_Root_Normalization, Phase_2A_Corrected_Case_Normalization, Phase_3A_Rule3_Canonical_Expansion, Phase_3B_Agent_Canonical_Expansion, phase_2b_ast_mutator, phase_2d_canonical_root_expansion, phase_2f_structural_namespace_relocation |
| `RGE_STAGE_SPECIFIC` | 5 | rge_stage10_12_smoke, rge_stage13_16_smoke, rge_stage17_20_smoke, rge_stage21_24_smoke, rge_stage25_28_smoke, rge_stage29_31_smoke |
| Deletion candidates | 0 | None — all scripts retained |
| Archive candidates | 7 | All `PHASE_PIPELINE_TOOL` scripts |
| Normalization candidates | 13 | All `ARCHITECTURE_VALIDATION_CANDIDATE` + `RUNTIME_DIAGNOSTIC_CANDIDATE` scripts |
| Tools that require copy (not move) into Repo_Tools | 12 | HIGH + MEDIUM priority Arch_Validation and Runtime_Diagnostics nominees |

*End of report — 2026-03-11*
