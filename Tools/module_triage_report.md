# ARCHON PRIME — Module Triage Report
**Generated:** 2026-03-10  
**Source:** `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`  
**Destinations:** `Blueprints/reasoning`, `Blueprints/utils`  

---

## Summary

| Metric | Value |
|--------|-------|
| Total Python files scanned | 0 |
| Excluded by rule (test/audit/nexus/boot) | 0 |
| Candidates analyzed | 0 |
| **Reasoning modules extracted** | **0** |
| **Utility modules extracted** | **0** |
| Stub modules deleted | 0 |
| Empty `__init__.py` deleted | 0 |
| Duplicates removed | 0 |
| Total files deleted | 0 |
| `__pycache__` directories removed | 0 |
| `*.pyc` files removed | 0 |
| Unclassified (remaining in source) | 0 |

---

## Reasoning Modules Extracted
**Destination:** `Blueprints/reasoning/`  **Total:** 0

| Module | Lines | Source |
|--------|-------|--------|

---

## Utility Modules Extracted
**Destination:** `Blueprints/utils/`  **Total:** 0

| Module | Lines | Source |
|--------|-------|--------|

---

## Duplicates Removed
**Total:** 0

| Victim Module | Kept As | Fn Similarity | Line Similarity |
|--------------|---------|--------------|----------------|

---

## Stub Deletions
**Total:** 0

| Module | Reason |
|--------|--------|

---

## Output Artifacts

| File | Description |
|------|-------------|
| `Tools/module_extraction_summary.json` | Aggregate metrics |
| `Tools/reasoning_modules_moved.json` | All reasoning modules with source/dest paths |
| `Tools/utility_modules_moved.json` | All utility modules with source/dest paths |
| `Tools/modules_deleted.json` | All deleted files with deletion reason |
| `Tools/module_triage_report.md` | This report |

---

## Governance Note

No changes were made to the live runtime stack (`LOGOS_SYSTEM/`, `STARTUP/`).  
All operations were scoped to `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`.  
Extracted modules in `Blueprints/reasoning/` and `Blueprints/utils/` are candidates;
integration into live subsystems requires a separate governance-approved pass.