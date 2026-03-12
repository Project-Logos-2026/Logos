# ARCHON PRIME — Legacy Application Function Salvage Report
**Generated:** 2026-03-10  
**Mode:** Static Analysis — Read-Only  
**Target:** `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`  

---

## Summary

| Metric | Value |
|--------|-------|
| Total Python files in target | 418 |
| Modules analyzed | 361 |
| Modules ignored (exclusion rules) | 57 |
| Total functions + methods detected | 8225 |
| Salvageable function blocks | 1141 |
| Parse errors (partial extraction) | 0 |

---

## Staging Groups

| Group | Files Analyzed |
|-------|---------------|
| `APPLICATION_FUNCTIONS` | 1 |
| `Agents` | 119 |
| `Memory` | 7 |
| `Reasoning` | 54 |
| `Tooling` | 11 |
| `Utilities` | 169 |

---

## Excluded Files by Rule

| Rule | Files Excluded |
|------|---------------|
| `test` in filename | 36 |
| `nexus` in filename | 17 |
| `boot` in filename | 3 |
| `audit` in filename | 1 |

---

## Runtime Role Distribution

| Runtime Role | Module Count |
|-------------|-------------|
| utility library | 113 |
| safety guard | 74 |
| reasoning engine | 53 |
| analysis engine | 48 |
| runtime orchestration | 19 |
| semantic inference | 17 |
| state manager | 14 |
| prediction engine | 12 |
| translation engine | 6 |
| identity/agent core | 5 |

---

## Semantic Signal Frequency

| Signal Keyword | Total Occurrences |
|---------------|------------------|
| `check` | 817 |
| `validate` | 537 |
| `build` | 438 |
| `generate` | 313 |
| `process` | 266 |
| `analyze` | 214 |
| `evaluate` | 207 |
| `map` | 199 |
| `apply` | 176 |
| `extract` | 164 |
| `detect` | 151 |
| `predict` | 137 |
| `compute` | 108 |
| `merge` | 106 |
| `infer` | 99 |
| `transform` | 96 |
| `score` | 94 |
| `parse` | 71 |
| `execute` | 67 |
| `determine` | 59 |

---

## Salvageable Function Cluster Distribution

| Candidate Cluster | Function Count |
|------------------|---------------|
| `safety_validation` | 304 |
| `general` | 170 |
| `pxl_privation` | 156 |
| `arp_reasoning` | 77 |
| `agent_identity` | 75 |
| `csp_memory` | 70 |
| `bdn_mvs` | 63 |
| `mtp_translation` | 63 |
| `iel_epistemic` | 50 |
| `prediction_temporal` | 46 |
| `tooling` | 24 |
| `utility` | 22 |
| `rge_genesis` | 16 |
| `orchestration` | 5 |

---

## Top 10 Modules by Salvageable Function Density

| Module | Salvageable Functions |
|--------|-----------------------|
| `Utilities/privation_mathematics.py` | 64 |
| `Reasoning/safety_formalisms.py` | 33 |
| `Reasoning/three_pillars_alt.py` | 32 |
| `Reasoning/three_pillars_framework.py` | 32 |
| `Reasoning/pxl_schema.py` | 31 |
| `Agents/iel_schema.py` | 29 |
| `Utilities/validation_schemas_system.py` | 28 |
| `Utilities/entry.py` | 27 |
| `Reasoning/bayesian_inference.py` | 24 |
| `Reasoning/temporal_predictor.py` | 21 |

---

## Core Compatibility Hints

| Runtime Core | Compatible Modules |
|-------------|-------------------|
| `DRAC` | 131 |
| `UTILITY` | 118 |
| `RUNTIME_EXECUTION_CORE` | 105 |
| `IEL` | 83 |
| `UNRESOLVED` | 75 |
| `TOOLING` | 59 |
| `AGENT_SYSTEM` | 48 |
| `RGE` | 31 |
| `RUNTIME_OPPERATIONS_CORE` | 25 |

---

## Parse Errors (Partial Extraction)

The following modules had syntax errors. Partial data was captured where possible.

| Module | Error |
|--------|-------|

---

## Recommended Deletions

The following categories of files are safe candidates for deletion
after confirming their content is captured in the output artifacts:

1. **Excluded files** (test/audit/nexus/boot) — these are non-functional stubs or test harnesses.
2. **`__init__.py` files** with no content — pure package markers, no logic.
3. **Duplicate reasoning engines** — pairs like `abductive_engine.py` + `abductive_reasoning_engine.py` should be reviewed; the shorter name is likely the legacy version.

> **Governance Note:** No deletions are performed by this pass. All recommendations require human review.

---

## Output Artifacts

| File | Description |
|------|-------------|
| `module_semantic_profiles.json` | Full per-module profile: purpose, role, imports, signals, exports |
| `salvageable_function_blocks.json` | Candidate DRAC application functions extracted from all modules |
| `core_compatibility_hints.json` | Mapping of modules to compatible runtime cores |
| `module_salvage_report.md` | This report |