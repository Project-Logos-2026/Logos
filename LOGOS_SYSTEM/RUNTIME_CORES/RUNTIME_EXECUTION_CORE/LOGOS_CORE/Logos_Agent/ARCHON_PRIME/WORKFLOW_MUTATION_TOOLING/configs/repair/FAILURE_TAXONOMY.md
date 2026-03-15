# ARCHON_PRIME — FAILURE TAXONOMY + REMEDIATION REGISTRY
**Deliverable 7** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE

This is the canonical failure classification system for the ARCHON_PRIME crawl.
Every failure the system can encounter must map to exactly one class here.
If `error_classifier.py` encounters a failure that does not match any class: severity = HALT.

---

## SEVERITY LEVELS

| Level | Meaning | Crawl Behavior |
|-------|---------|----------------|
| `BLOCKING` | This module cannot advance until resolved | Pause; attempt repair; quarantine if repair fails |
| `HALT` | Crawl cannot continue at all | Stop crawl; emit diagnostic; exit non-zero; await manual resolution |
| `WARNING` | Issue detected; module can still advance | Log; emit warning in report; advance |

---

## FAILURE CLASS 01 — `SYNTAX_FAILURE`

| Field | Value |
|-------|-------|
| **Class ID** | `SYNTAX_FAILURE` |
| **Description** | Module source cannot be parsed as valid Python (`ast.parse()` raises `SyntaxError`) |
| **Detection Mechanism** | `syntax_validator.py` (M62) — run pre-mutation AND post-mutation |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | Attempt AST-level correction for common patterns (unclosed brackets, encoding BOM, trailing commas in wrong position). If correction produces valid parse: apply. If not: escalate. |
| **Retry Policy** | 1 automated repair attempt |
| **Escalation Condition** | Repair fails to produce parseable source after 1 attempt |
| **Escalation Target** | `QUARANTINE` |
| **Crawl Behavior** | Pause on current module; attempt repair; re-validate; advance or quarantine |
| **Log Entry** | `repair_event_log.json` + `crawl_execution_log.json` |
| **Notes** | If a SYNTAX_FAILURE is detected AFTER a mutation (post-mutation check), the mutation is rolled back before quarantine decision. Pre-mutation hash from `mutation_log.json` used for rollback. |

---

## FAILURE CLASS 02 — `IMPORT_RESOLUTION_FAILURE`

| Field | Value |
|-------|-------|
| **Class ID** | `IMPORT_RESOLUTION_FAILURE` |
| **Description** | Module contains an import that cannot be resolved to any known module dotpath in `module_index.json` and is not a stdlib or known external dependency |
| **Detection Mechanism** | `import_extractor.py` (M12) output cross-checked against `module_index.json`; detected by `module_processor.py` (M61) during pipeline |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | Check `canonical_import_registry.json` for known stub or redirect. If registered: apply rewrite. If not registered and module is non-boot: flag as WARNING and continue. If boot chain: HALT. |
| **Retry Policy** | 1 attempt (registry lookup) |
| **Escalation Condition** | Unregistered import in boot-chain module |
| **Escalation Target** | `HALT` (boot chain) or `QUARANTINE` (post-boot) |
| **Crawl Behavior** | Boot chain: HALT. Post-boot: Pause; attempt rewrite or stub; quarantine if unresolvable. |
| **Log Entry** | `repair_event_log.json` |

---

## FAILURE CLASS 03 — `DEEP_IMPORT_VIOLATION`

| Field | Value |
|-------|-------|
| **Class ID** | `DEEP_IMPORT_VIOLATION` |
| **Description** | Module imports from a non-facade internal dotpath (bypasses Canonical Import Facade) |
| **Detection Mechanism** | `import_rewriter.py` (M51) identifies violations against `canonical_import_registry.json`; flagged pre-mutation by `canonical_import_rewrite_plan.json` |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | Rewrite import to facade-compliant form per `canonical_import_rewrite_plan.json`. If `confidence: INFERRED` and produces invalid result: mark `requires_manual_review: true` and quarantine. |
| **Retry Policy** | 1 rewrite attempt; then validation; then quarantine if invalid |
| **Escalation Condition** | Rewrite produces SYNTAX_FAILURE or IMPORT_RESOLUTION_FAILURE |
| **Escalation Target** | `QUARANTINE` |
| **Crawl Behavior** | Apply rewrite; revalidate syntax; advance or quarantine |
| **Log Entry** | `mutation_log.json` + `repair_event_log.json` |

---

## FAILURE CLASS 04 — `CIRCULAR_DEPENDENCY`

| Field | Value |
|-------|-------|
| **Class ID** | `CIRCULAR_DEPENDENCY` |
| **Description** | Module is part of an import cycle detected by SCC analysis |
| **Detection Mechanism** | `circular_dependency_detector.py` (M22) — pre-crawl only |
| **Blocking Severity** | `HALT` if `in_boot_chain: true`; `WARNING` if `in_boot_chain: false` |
| **Remediation Action** | **No automated repair.** Boot-chain cycles require manual architectural resolution before crawl proceeds. Post-boot cycles are logged and flagged for post-crawl attention. |
| **Retry Policy** | 0 (manual resolution required for HALT; WARNING requires no action) |
| **Escalation Condition** | N/A (detected pre-crawl; crawl does not begin if HALT) |
| **Escalation Target** | HALT (blocks pre-crawl checklist D1/D2) |
| **Crawl Behavior** | Boot chain: crawl never starts. Post-boot: WARNING in report; module processed normally; cycle documented. |
| **Log Entry** | `circular_dependency_groups.json` + pre-crawl checklist result |

---

## FAILURE CLASS 05 — `MISSING_MODULE`

| Field | Value |
|-------|-------|
| **Class ID** | `MISSING_MODULE` |
| **Description** | A module dotpath is referenced (imported or declared as dependency) but has no corresponding file in `module_index.json` |
| **Detection Mechanism** | `module_index_builder.py` (M20) cross-check; `import_extractor.py` (M12) output |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | If a governance-compliant stub can be generated (module is non-critical, post-boot): create stub, add to module index, continue. If boot-chain or governance-critical: HALT. |
| **Retry Policy** | 1 stub generation attempt |
| **Escalation Condition** | Boot-chain missing module; or stub generation fails |
| **Escalation Target** | `HALT` (boot chain) or `QUARANTINE` (any dependent that cannot be resolved) |
| **Crawl Behavior** | Boot chain: HALT. Post-boot: generate stub; update module index; advance dependent. |
| **Log Entry** | `repair_event_log.json` + `mutation_log.json` |

---

## FAILURE CLASS 06 — `GOVERNANCE_HEADER_MISSING`

| Field | Value |
|-------|-------|
| **Class ID** | `GOVERNANCE_HEADER_MISSING` |
| **Description** | Module has no canonical governance header block |
| **Detection Mechanism** | `header_schema_scanner.py` (M14) pre-crawl; `module_processor.py` (M61) during crawl |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | Auto-inject canonical header using `header_injector.py` (M50) per `header_schema.json`. Injection is deterministic. No ambiguity. |
| **Retry Policy** | 0 retries needed (injection is deterministic) |
| **Escalation Condition** | Post-injection syntax validation fails |
| **Escalation Target** | `QUARANTINE` (only if injection corrupts file) |
| **Crawl Behavior** | Inject; revalidate syntax and governance; advance (quarantine only if injection produces invalid file — treated as SYNTAX_FAILURE post-repair) |
| **Log Entry** | `mutation_log.json` (type: HEADER_INJECT) |

---

## FAILURE CLASS 07 — `GOVERNANCE_HEADER_STALE`

| Field | Value |
|-------|-------|
| **Class ID** | `GOVERNANCE_HEADER_STALE` |
| **Description** | Module has a header that is present but does not conform to the canonical schema (missing fields, wrong field values, deprecated format) |
| **Detection Mechanism** | `header_schema_scanner.py` (M14) pre-crawl; `module_processor.py` during crawl |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | Replace header with canonical form using `header_injector.py`, preserving module-specific field values where schema allows. |
| **Retry Policy** | 1 replacement attempt |
| **Escalation Condition** | Post-replacement syntax failure |
| **Escalation Target** | `QUARANTINE` |
| **Crawl Behavior** | Replace; revalidate; advance or quarantine |
| **Log Entry** | `mutation_log.json` (type: HEADER_REPLACE) |

---

## FAILURE CLASS 08 — `GOVERNANCE_CONTRACT_MISMATCH`

| Field | Value |
|-------|-------|
| **Class ID** | `GOVERNANCE_CONTRACT_MISMATCH` |
| **Description** | Module's declared governance contract conflicts with the expected contract in `governance_contract_map.json` (wrong class, wrong declared exports, wrong declared dependencies) |
| **Detection Mechanism** | `governance_validator.py` (M63) |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | If mismatch is schema-driven and correctable (field value wrong): auto-correct. If structural mismatch (wrong contract class): log and quarantine — no auto-correction of governance class. |
| **Retry Policy** | 1 correction attempt for field-level mismatches |
| **Escalation Condition** | Structural contract class mismatch; or correction produces further violation |
| **Escalation Target** | `QUARANTINE` |
| **Crawl Behavior** | Pause; attempt field correction; revalidate; advance or quarantine |
| **Log Entry** | `repair_event_log.json` + `violation_logs/` |

---

## FAILURE CLASS 09 — `RUNTIME_PHASE_VIOLATION`

| Field | Value |
|-------|-------|
| **Class ID** | `RUNTIME_PHASE_VIOLATION` |
| **Description** | Module's declared phase (in header) does not match its authoritative phase in `runtime_phase_map.json` |
| **Detection Mechanism** | `phase_validator.py` (M64) |
| **Blocking Severity** | `BLOCKING` if in boot chain (phase 0/1); `WARNING` if post-boot |
| **Remediation Action** | Update the phase field in the module header to match `runtime_phase_map.json`. Phase map is the authority — header is updated, not the map. |
| **Retry Policy** | 1 correction; then revalidation |
| **Escalation Condition** | Correction produces syntax failure; or phase is ambiguous in phase map (`conflict: true`) |
| **Escalation Target** | `QUARANTINE` (if syntax failure); `HALT` (if phase map conflict not resolved) |
| **Crawl Behavior** | Boot chain: BLOCKING → repair → quarantine if failed. Post-boot: WARNING → repair → advance |
| **Log Entry** | `mutation_log.json` + `repair_event_log.json` |

---

## FAILURE CLASS 10 — `BOOT_CHAIN_VIOLATION`

| Field | Value |
|-------|-------|
| **Class ID** | `BOOT_CHAIN_VIOLATION` |
| **Description** | A boot-chain constraint is violated: a phase-1 module imports a phase-3 module, or boot sequence is broken by a missing or misphased dependency |
| **Detection Mechanism** | `runtime_boot_sequencer.py` (M24) pre-crawl; `phase_validator.py` (M64) in-crawl |
| **Blocking Severity** | `HALT` |
| **Remediation Action** | No automated repair. Boot chain violations require architectural review. |
| **Retry Policy** | 0 |
| **Escalation Condition** | N/A — always HALT |
| **Escalation Target** | `HALT` — crawl stops entirely |
| **Crawl Behavior** | Emit diagnostic with full boot chain violation detail. Exit non-zero. Await manual resolution. |
| **Log Entry** | `crawl_execution_log.json` entry with status HALTED; diagnostic emitted to stdout |

---

## FAILURE CLASS 11 — `ARTIFACT_ROUTING_FAILURE`

| Field | Value |
|-------|-------|
| **Class ID** | `ARTIFACT_ROUTING_FAILURE` |
| **Description** | `artifact_router.py` cannot write an artifact to its canonical location (directory missing, permissions error, disk full) |
| **Detection Mechanism** | `artifact_router.py` (M90) — catches IOError/OSError and classifies |
| **Blocking Severity** | `BLOCKING` |
| **Remediation Action** | Retry up to 2 times with brief delay. On each retry: verify destination directory exists (create if missing per routing table). If still fails: HALT. |
| **Retry Policy** | 2 retries |
| **Escalation Condition** | 3rd consecutive failure |
| **Escalation Target** | `HALT` |
| **Crawl Behavior** | Pause routing; retry; halt if unresolved (artifact loss is unacceptable) |
| **Log Entry** | `repair_event_log.json` |

---

## FAILURE CLASS 12 — `UNRESOLVED_REPAIR_THRESHOLD`

| Field | Value |
|-------|-------|
| **Class ID** | `UNRESOLVED_REPAIR_THRESHOLD` |
| **Description** | A module has exhausted its repair retry budget across one or more failure classes without reaching a PASS state |
| **Detection Mechanism** | `repair_router.py` (M71) — retry counter enforcement |
| **Blocking Severity** | `BLOCKING` (but resolution is quarantine, not halt) |
| **Remediation Action** | Quarantine module: generate governance-compliant stub, write stub to module path, back up original, update quarantine registry. |
| **Retry Policy** | 0 (already at threshold) |
| **Escalation Condition** | Quarantine stub generation fails → `HALT` |
| **Escalation Target** | `QUARANTINE` → `HALT` if stub fails |
| **Crawl Behavior** | Quarantine module; stub in place; update `quarantine_registry.json`; advance to next module |
| **Log Entry** | `quarantine_registry.json` + `repair_event_log.json` |

---

## REMEDIATION ACTION REGISTRY

The following table maps failure class IDs to their repair handler functions (implemented in `repair_executor.py`):

| Failure Class | Handler Function | Auto-Repairable |
|--------------|-----------------|----------------|
| `SYNTAX_FAILURE` | `repair_syntax_error()` | Partially |
| `IMPORT_RESOLUTION_FAILURE` | `repair_unresolved_import()` | If registered |
| `DEEP_IMPORT_VIOLATION` | `repair_deep_import()` | Yes (if plan exists) |
| `CIRCULAR_DEPENDENCY` | N/A — pre-crawl HALT or WARNING | No |
| `MISSING_MODULE` | `repair_missing_module()` | Stub generation only |
| `GOVERNANCE_HEADER_MISSING` | `inject_canonical_header()` | Yes |
| `GOVERNANCE_HEADER_STALE` | `replace_stale_header()` | Yes |
| `GOVERNANCE_CONTRACT_MISMATCH` | `repair_contract_mismatch()` | Field-level only |
| `RUNTIME_PHASE_VIOLATION` | `repair_phase_field()` | Yes (header update) |
| `BOOT_CHAIN_VIOLATION` | N/A — HALT | No |
| `ARTIFACT_ROUTING_FAILURE` | `retry_artifact_routing()` | Retry only |
| `UNRESOLVED_REPAIR_THRESHOLD` | `quarantine_module()` | N/A (managed state) |

---

## FAILURE ESCALATION DECISION TREE

```
Failure detected
    │
    ├─► Is this an UNKNOWN failure class?
    │       YES → HALT (no silent failures)
    │
    ├─► Is severity == HALT?
    │       YES → Emit diagnostic → Stop crawl → Exit non-zero
    │
    ├─► Is severity == BLOCKING?
    │       YES → Is auto-repair registered?
    │               YES → Attempt repair → Revalidate
    │                       PASS → Log → Advance
    │                       FAIL → Retry within limit?
    │                               YES → Retry
    │                               NO → Quarantine → Advance
    │               NO → Quarantine immediately → Advance
    │
    └─► Is severity == WARNING?
            YES → Log → Append to report → Advance
```
