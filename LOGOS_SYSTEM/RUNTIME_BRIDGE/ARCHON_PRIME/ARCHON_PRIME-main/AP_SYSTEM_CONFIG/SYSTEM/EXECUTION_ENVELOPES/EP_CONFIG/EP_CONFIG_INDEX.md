SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: EP_Configuration
ARTIFACT_NAME: EP_CONFIG_INDEX
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / EP_CONFIG
STATUS: Active

---------------------------------------------------------------------

# EP_CONFIG — Configuration Artifact Index

## Purpose

This index provides a complete reference for all artifacts in the
EP_CONFIG layer, all rules defined across those artifacts, and a
cross-reference map between phases, rules, and EA addenda.

---------------------------------------------------------------------

## ARTIFACT REGISTRY

| Artifact                              | Purpose                                                | Rules Defined        |
|---------------------------------------|--------------------------------------------------------|----------------------|
| EP_CONFIG_PHASE_MODEL.md              | Canonical ten-phase pipeline definition               | Phase specs          |
| EP_CONFIG_EXECUTION_ORDER_RULES.md    | Phase dependencies, skip prohibitions, checkpoints    | EOR-001–031          |
| EP_CONFIG_MUTATION_GATE_RULES.md      | Mutation authorization gate conditions                | MGR-001–024          |
| EP_CONFIG_README.md                   | Layer overview, lifecycle, invariants                 | (reference)          |
| EP_CONFIG_INDEX.md                    | This file — complete index                            | (index)              |

---------------------------------------------------------------------

## SECTION 1 — CANONICAL PHASE MODEL

Defined in: `EP_CONFIG_PHASE_MODEL.md`

| Code     | Phase Name                    | Category   | Mutations | EA Authority                |
|----------|-------------------------------|------------|-----------|-----------------------------|
| PHASE-01 | Environment Initialization    | Setup      | No        | EA-001, EA-005, EA-007, EA-008 |
| PHASE-02 | Artifact Discovery            | Analysis   | No        | EA-002, EA-006              |
| PHASE-03 | Structural Analysis           | Analysis   | No        | EA-005, EA-006, EA-007      |
| PHASE-04 | Dependency Graph Construction | Analysis   | No        | EA-003, EA-005              |
| PHASE-05 | Simulation Pass               | Simulation | No        | EA-003, EA-004, EA-006      |
| PHASE-06 | Simulation Validation         | Simulation | No        | EA-004, EA-005, EA-006      |
| PHASE-07 | Mutation Planning             | Planning   | No        | EA-002, EA-003, EA-006      |
| PHASE-08 | Controlled Mutation           | Mutation   | **YES**   | EA-002, EA-003, EA-004, EA-006, EA-010 |
| PHASE-09 | Post-Mutation Validation      | Validation | No        | EA-005, EA-006, EA-007, EA-010 |
| PHASE-10 | Reporting                     | Reporting  | No        | EA-006, EA-008              |

**Key invariant:** Only PHASE-08 may perform mutations. PHASE-10 always
executes regardless of prior phase outcomes.

---------------------------------------------------------------------

## SECTION 2 — EXECUTION ORDER RULES (EOR)

Defined in: `EP_CONFIG_EXECUTION_ORDER_RULES.md`

### Rule Set 1 — Phase Dependency Rules

| Rule ID  | Rule Title                                    | Severity | EA Authority |
|----------|-----------------------------------------------|----------|--------------|
| EOR-001  | Canonical Phase Dependency Chain              | CRITICAL | EA-003       |
| EOR-002  | Single-Predecessor Constraint                 | HIGH     | EA-003       |
| EOR-003  | Phase Completion Status Must Be Persisted     | HIGH     | EA-006       |

### Rule Set 2 — Prohibited Phase Skipping

| Rule ID  | Rule Title                                            | Severity | EA Authority      |
|----------|-------------------------------------------------------|----------|-------------------|
| EOR-010  | Absolute Skip Prohibition for Simulation Phases       | CRITICAL | EA-004            |
| EOR-011  | Analysis Phase Skip Prohibition                       | CRITICAL | EA-003            |
| EOR-012  | Validation Phase Skip Prohibition (PHASE-09)          | CRITICAL | EA-005, EA-007    |
| EOR-013  | PHASE-10 Skip Prohibition                             | HIGH     | EA-006            |
| EOR-014  | STATUS Value `SKIPPED` Prohibited in EP Logs          | CRITICAL | EA-003, EA-006    |

### Rule Set 3 — Required Validation Checkpoints

| Rule ID  | Rule Title                                    | Position                    | Severity |
|----------|-----------------------------------------------|-----------------------------|----------|
| EOR-020  | Post-Initialization Verification              | Between PHASE-01 and PHASE-02 | CRITICAL |
| EOR-021  | Pre-Simulation Gate                           | Between PHASE-04 and PHASE-05 | CRITICAL |
| EOR-022  | Mutation Authorization Gate                   | Between PHASE-06 and PHASE-07 | CRITICAL |
| EOR-023  | Pre-Reporting Validation Consolidation        | Between PHASE-09 and PHASE-10 | HIGH     |

### Rule Set 4 — Phase Sequence Structural Rules

| Rule ID  | Rule Title                                    | Severity | EA Authority      |
|----------|-----------------------------------------------|----------|-------------------|
| EOR-030  | EP Artifact Must Declare Phase Sequence       | CRITICAL | EA-003            |
| EOR-031  | Phase Sequence Must Match Manifest            | HIGH     | EA-003, EA-008    |

---------------------------------------------------------------------

## SECTION 3 — MUTATION GATE RULES (MGR)

Defined in: `EP_CONFIG_MUTATION_GATE_RULES.md`

**Gate Position:** Between PHASE-06 and PHASE-07
**Verdict Values:** `AUTHORIZED` (all 13 rules pass) or `BLOCKED` (any rule fails)

### Condition Category 1 — Successful Simulation

| Rule ID  | Rule Title                                        | Severity | EA Authority |
|----------|---------------------------------------------------|----------|--------------|
| MGR-001  | Simulation Pass Recorded As Completed             | CRITICAL | EA-004       |
| MGR-002  | No Critical Simulation Failures                   | CRITICAL | EA-004       |
| MGR-003  | Simulation Coverage Threshold Met (100%)          | HIGH     | EA-004       |
| MGR-004  | Simulation Execution Log Exists and Non-Empty     | CRITICAL | EA-004, EA-006 |

### Condition Category 2 — Validation Pass

| Rule ID  | Rule Title                                        | Severity | EA Authority   |
|----------|---------------------------------------------------|----------|----------------|
| MGR-010  | Simulation Validation Recorded As Completed       | CRITICAL | EA-004, EA-005 |
| MGR-011  | Simulated Outcomes Meet DS Success Criteria       | CRITICAL | EA-005         |
| MGR-012  | Simulation Validation Report Artifact Exists      | HIGH     | EA-006         |
| MGR-013  | No Unreviewed HIGH-Severity Simulation Failures   | HIGH     | EA-005         |

### Condition Category 3 — Governance Compliance

| Rule ID  | Rule Title                                        | Severity | EA Authority |
|----------|---------------------------------------------------|----------|--------------|
| MGR-020  | EA-005 Governance Consistency Check Passed        | CRITICAL | EA-005       |
| MGR-021  | EA-001 Artifact Hash Integrity Confirmed          | CRITICAL | EA-001       |
| MGR-022  | EA-002 Artifact Router Confirmed Active           | HIGH     | EA-002       |
| MGR-023  | EA-010 Rollback Mechanism Confirmed Armed         | CRITICAL | EA-010       |
| MGR-024  | EA-003 Deterministic Order Lock Confirmed         | HIGH     | EA-003       |

**Gate evaluation sequence:** MGR-001 → MGR-004 → MGR-010 → MGR-013
→ MGR-020 → MGR-024 → issue verdict

---------------------------------------------------------------------

## SECTION 4 — RULE SEVERITY SUMMARY

### EOR Rules

| Severity | Count | Rule IDs                                           |
|----------|-------|----------------------------------------------------|
| CRITICAL | 9     | EOR-001, EOR-010, EOR-011, EOR-012, EOR-014, EOR-020, EOR-021, EOR-022, EOR-030 |
| HIGH     | 5     | EOR-002, EOR-003, EOR-013, EOR-023, EOR-031        |

### MGR Rules

| Severity | Count | Rule IDs                                           |
|----------|-------|----------------------------------------------------|
| CRITICAL | 7     | MGR-001, MGR-002, MGR-004, MGR-010, MGR-011, MGR-020, MGR-021, MGR-023 |
| HIGH     | 6     | MGR-003, MGR-012, MGR-013, MGR-022, MGR-024        |

---------------------------------------------------------------------

## SECTION 5 — EA AUTHORITY MAP

| EA ID  | EOR Rules                          | MGR Rules              |
|--------|------------------------------------|------------------------|
| EA-001 | EOR-020                            | MGR-021                |
| EA-002 | —                                  | MGR-022                |
| EA-003 | EOR-001, EOR-011, EOR-014, EOR-030, EOR-031 | MGR-024       |
| EA-004 | EOR-010, EOR-021, EOR-022          | MGR-001–004, MGR-010   |
| EA-005 | EOR-020                            | MGR-011, MGR-013, MGR-020 |
| EA-006 | EOR-003, EOR-013, EOR-014          | MGR-004, MGR-012       |
| EA-007 | EOR-012, EOR-020                   | —                      |
| EA-008 | EOR-031                            | —                      |
| EA-010 | EOR-022                            | MGR-023                |

---------------------------------------------------------------------

## SECTION 6 — PHASE SKIP-PROHIBITION SUMMARY

| Phase Group      | Skip Allowed? | Rule Prohibiting Skip | Notes                      |
|------------------|---------------|-----------------------|----------------------------|
| PHASE-01         | No            | EOR-001               | Entry phase; must complete |
| PHASE-02–04      | No            | EOR-011               | Stub permitted for PHASE-04 only with justification |
| PHASE-05–06      | **Never**     | EOR-010               | Simulation phases are absolutely non-skippable |
| PHASE-07         | No            | MGR verdict required  | Planning follows gate      |
| PHASE-08         | No            | EOR-001               | Zero-mutation runs still execute phase |
| PHASE-09         | No            | EOR-012               | Runs even if PHASE-08 had zero mutations |
| PHASE-10         | **Never**     | EOR-013               | Reporting is unconditional |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
