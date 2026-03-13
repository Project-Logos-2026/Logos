SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: EP_Configuration
ARTIFACT_NAME: EP_CONFIG_PHASE_MODEL
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / EP_CONFIG
STATUS: Active

---------------------------------------------------------------------

# EP_CONFIG — Canonical Execution Phase Model

## Purpose

This document defines the canonical ten-phase execution pipeline
that every ARCHON_PRIME Execution Plan (EP) artifact must conform
to. Each phase has a defined position, purpose, required inputs,
required outputs, and gate conditions.

This model governs all EP artifacts across all Execution Envelopes.
No EP may define phases outside of this model without explicit
Architect-level authority.

---------------------------------------------------------------------

## SECTION 1 — PHASE INVENTORY

The canonical pipeline consists of ten phases, numbered and named
as follows. Phase numbering is fixed. Phase names must appear
verbatim in EP artifacts.

| Phase | Canonical Name              | Code     | Category    |
|-------|-----------------------------|----------|-------------|
| 1     | Environment Initialization  | PHASE-01 | Setup       |
| 2     | Artifact Discovery          | PHASE-02 | Analysis    |
| 3     | Structural Analysis         | PHASE-03 | Analysis    |
| 4     | Dependency Graph Construction | PHASE-04 | Analysis  |
| 5     | Simulation Pass             | PHASE-05 | Simulation  |
| 6     | Simulation Validation       | PHASE-06 | Simulation  |
| 7     | Mutation Planning           | PHASE-07 | Planning    |
| 8     | Controlled Mutation         | PHASE-08 | Mutation    |
| 9     | Post-Mutation Validation    | PHASE-09 | Validation  |
| 10    | Reporting                   | PHASE-10 | Reporting   |

---------------------------------------------------------------------

## SECTION 2 — PHASE DEFINITIONS

---

### PHASE-01 — Environment Initialization

**Category:** Setup
**Position:** First — no prior phases required
**EA Governance:** EA-001, EA-005, EA-007

**Purpose:**
Verifies that the execution environment satisfies all preconditions
required for safe envelope execution. This phase must complete
successfully before any artifact or data operations proceed.

**Required Inputs:**
- `ENVELOPE_MANIFEST.json` — present and schema-valid
- All DS, EP, and IG artifact files declared in the manifest
- All EA addenda files declared in the manifest
- Execution context configuration (artifact router, rollback config)

**Required Outputs:**
- Environment verification report
- Artifact hash check results (all DS/EP/IG hashes validated against
  manifest records per EA-001)
- Schema validation results for all bundle artifacts (per EA-007)
- Governance consistency check result (per EA-005)

**Gate Condition:**
All artifact hashes match manifest. All schema validations pass.
No governance conflicts detected. Phase fails and execution halts
if any check fails.

**Prohibited Actions:**
- No file mutations
- No data writes outside of reporting targets
- No phase advancement if any check fails

---

### PHASE-02 — Artifact Discovery

**Category:** Analysis
**Position:** Follows PHASE-01
**EA Governance:** EA-002, EA-006

**Purpose:**
Inventories all target artifacts within the envelope's defined scope.
Produces a complete, ordered artifact list for use in subsequent
analysis phases.

**Required Inputs:**
- Target scope declaration from DS Section 3
- System boundary declaration from DS Section 4
- Artifact router configuration (EA-002)

**Required Outputs:**
- Artifact inventory list (all in-scope files and modules)
- Artifact discovery log entry (per EA-006)
- Out-of-scope exclusion record
- Artifact count summary

**Gate Condition:**
Discovery must cover all targets declared in the DS scope. Any
target declared in-scope that cannot be located must be flagged
as a discovery failure. Execution does not halt on discovery
failures but failures must be recorded.

**Prohibited Actions:**
- No mutations to discovered artifacts
- Artifacts outside declared scope must not be inventoried

---

### PHASE-03 — Structural Analysis

**Category:** Analysis
**Position:** Follows PHASE-02
**EA Governance:** EA-005, EA-006, EA-007

**Purpose:**
Analyzes the structural properties of all discovered artifacts.
This includes header validation, section structure, metadata
completeness, and schema conformance for each artifact.

**Required Inputs:**
- Artifact inventory from PHASE-02
- Applicable schemas from `EE_SCHEMAS/`
- Metadata validation rules (EA-007)

**Required Outputs:**
- Structural analysis report per artifact
- List of structural violations (if any)
- Header metadata validation results
- Schema conformance results per artifact

**Gate Condition:**
Structural analysis must complete across all discovered artifacts
before proceeding. Critical structural violations are recorded but
do not halt the pipeline at this phase — they are consumed by
PHASE-05 (Simulation Pass) and PHASE-07 (Mutation Planning).

**Prohibited Actions:**
- No mutations
- No schema updates based on analysis findings

---

### PHASE-04 — Dependency Graph Construction

**Category:** Analysis
**Position:** Follows PHASE-03
**EA Governance:** EA-003, EA-005

**Purpose:**
Constructs the dependency graph for all in-scope modules and
artifacts. Identifies dependency ordering, circular dependencies,
and any dependency conditions relevant to the execution sequence.

**Required Inputs:**
- Structural analysis results from PHASE-03
- Import and dependency declarations from in-scope modules
- Canonical Import Registry (if applicable to envelope scope)

**Required Outputs:**
- Dependency graph artifact (ordered adjacency model)
- Circular dependency report (if any circulars detected)
- Module execution order derived from dependency graph
- Dependency validation log

**Gate Condition:**
Dependency graph must be constructed and validated. Unresolvable
circular dependencies that would block execution must be flagged.
The derived module execution order must be recorded before
PHASE-05 can be authorized to begin.

**Prohibited Actions:**
- No mutations
- Dependency graph must not be modified after construction
  (treat as read-only input to subsequent phases)

---

### PHASE-05 — Simulation Pass

**Category:** Simulation
**Position:** Follows PHASE-04
**EA Governance:** EA-004 (authoritative), EA-003, EA-006

**Purpose:**
Executes a full dry-run simulation of all planned mutations against
the in-scope artifact set. No file system mutations are committed
during this phase. Simulation must produce the same logical outcome
as live execution would produce, without side effects.

**Required Inputs:**
- Dependency-ordered module list from PHASE-04
- Structural violation list from PHASE-03
- Simulation layer configuration
- All target artifacts (read-only)

**Required Outputs:**
- Simulation execution log (per EA-006)
- Simulation outcome per artifact (PASS / FAIL / WARNING)
- List of simulated mutations with predicted outcomes
- Simulation summary report

**Gate Condition:**
This is a mandatory phase. Per EA-004, no mutation phase may begin
without a completed simulation pass. If the simulation layer itself
fails to execute (not if individual artifact simulations fail), the
pipeline halts.

**Prohibited Actions:**
- Absolutely no writes to target artifact files
- No commits, no staging, no git operations against live content
- Simulation results must not be treated as final states

---

### PHASE-06 — Simulation Validation

**Category:** Simulation
**Position:** Follows PHASE-05 — this is the mutation gate
**EA Governance:** EA-004, EA-005, EA-006

**Purpose:**
Validates the results of the Simulation Pass. Determines whether
the simulation outcomes meet the quality and safety thresholds
required to authorize progression to mutation phases.

**Required Inputs:**
- Simulation execution log from PHASE-05
- Simulation outcome records from PHASE-05
- Governance compliance thresholds (EA-005)
- Success criteria from DS Section 10

**Required Outputs:**
- Simulation validation report
- Mutation authorization verdict: AUTHORIZED or BLOCKED
- Per-artifact mutation authorization list
- Validation log entry (per EA-006)

**Gate Condition:**
This phase produces the **Mutation Authorization Verdict**. The
verdict must be AUTHORIZED before PHASE-07 or PHASE-08 may begin.
If the verdict is BLOCKED, the pipeline halts and a failure report
is generated. There is no bypass mechanism for a BLOCKED verdict.

**Pass Threshold:**
Mutation authorization requires all of the following:
- No CRITICAL-severity simulation failures
- Simulated outcomes consistent with DS success criteria
- Governance consistency check passes (EA-005)

**Prohibited Actions:**
- PHASE-07 and PHASE-08 must not begin if verdict is BLOCKED
- Verdict must not be manually overridden without Architect approval

---

### PHASE-07 — Mutation Planning

**Category:** Planning
**Position:** Follows PHASE-06 (requires AUTHORIZED verdict)
**EA Governance:** EA-002, EA-003, EA-006

**Purpose:**
Constructs the ordered, deterministic mutation plan to be executed
by PHASE-08. The mutation plan is the precise, executable specification
of every write operation the pipeline will perform, in exact order.

**Required Inputs:**
- Simulation outcome records from PHASE-05
- Mutation authorization list from PHASE-06
- Dependency-ordered module list from PHASE-04
- Artifact router configuration (EA-002)

**Required Outputs:**
- Mutation plan artifact (ordered list of mutation operations)
- Per-target mutation specification (file path, operation type,
  anticipated diff, target output location)
- Mutation plan log entry (per EA-006)

**Gate Condition:**
Every mutation operation in the plan must reference a PHASE-06
authorized target. Unauthorized targets must not appear in the
mutation plan. Plan must be validated against the artifact router
(EA-002) before PHASE-08 may begin.

**Prohibited Actions:**
- No actual file mutations during planning
- No deviation from PHASE-06 authorized target list

---

### PHASE-08 — Controlled Mutation

**Category:** Mutation
**Position:** Follows PHASE-07
**EA Governance:** EA-002, EA-003, EA-004, EA-006, EA-010

**Purpose:**
Executes the mutation plan produced by PHASE-07. Applies all
authorized mutations to in-scope artifact targets in the exact
deterministic order specified by the plan. Each mutation is
individually logged and immediately eligible for rollback.

**Required Inputs:**
- Mutation plan from PHASE-07
- Rollback configuration (EA-010)
- Pre-mutation artifact state snapshots (for rollback)
- Artifact router (EA-002)

**Required Outputs:**
- Mutation execution log (per EA-006) — one entry per operation
- Post-mutation artifact state for each mutated artifact
- Rollback state registry (pre/post states)

**Gate Condition:**
Each individual mutation operation must succeed before the next
begins. If any mutation operation fails:
1. Execution halts immediately (no further mutations proceed)
2. Rollback protocol is triggered (EA-010)
3. Failure report is generated

**Prohibited Actions:**
- No mutations outside the PHASE-07 mutation plan
- No skipping of failed operations to continue execution
- Rollback mechanism must remain armed throughout this phase

---

### PHASE-09 — Post-Mutation Validation

**Category:** Validation
**Position:** Follows PHASE-08
**EA Governance:** EA-005, EA-006, EA-007, EA-010

**Purpose:**
Validates the state of all mutated artifacts to confirm that
mutations were applied correctly and that the post-mutation
system state meets all schema, governance, and correctness
requirements.

**Required Inputs:**
- Mutation execution log from PHASE-08
- All mutated artifact files (post-mutation state)
- Applicable schemas from `EE_SCHEMAS/`
- DS Section 10 success criteria

**Required Outputs:**
- Post-mutation validation report (per artifact)
- Success criteria evaluation results
- Overall validation verdict: PASSED or FAILED
- If FAILED: rollback trigger signal to PHASE-08 rollback protocol

**Gate Condition:**
If the overall validation verdict is FAILED, rollback is triggered
per EA-010 and PHASE-10 must produce a failure report rather than
a success report.

**Prohibited Actions:**
- No further mutations during this phase
- Validation results must not be suppressed or filtered

---

### PHASE-10 — Reporting

**Category:** Reporting
**Position:** Final — follows PHASE-09
**EA Governance:** EA-006, EA-008

**Purpose:**
Produces the canonical execution report artifact for the envelope.
The report must capture the full execution record across all phases,
including outcomes, metrics, artifacts produced, and final verdict.

**Required Inputs:**
- Phase logs from PHASE-01 through PHASE-09
- Post-mutation validation report from PHASE-09
- Envelope manifest (per EA-008)

**Required Outputs:**
- Execution summary report (canonical artifact, routed per EA-002)
- Final execution verdict: SUCCESS or FAILURE
- Artifact inventory of all produced outputs
- Execution metrics (phase durations, mutation counts, error counts)

**Gate Condition:**
None — Reporting always executes, regardless of whether prior phases
produced success or failure outcomes. The report captures the honest
execution record.

**Prohibited Actions:**
- Reporting phase must not trigger any mutations
- Report must not omit failed phases or suppressed errors

---------------------------------------------------------------------

## SECTION 3 — PHASE CATEGORY SUMMARY

| Category   | Phases          | Mutations Permitted | Gate Authority       |
|------------|-----------------|---------------------|----------------------|
| Setup      | PHASE-01        | No                  | Environment checks   |
| Analysis   | PHASE-02–04     | No                  | Internal             |
| Simulation | PHASE-05–06     | No                  | EA-004               |
| Planning   | PHASE-07        | No                  | EA-002, EA-006       |
| Mutation   | PHASE-08        | Yes (authorized)    | PHASE-06 verdict     |
| Validation | PHASE-09        | No                  | EA-005, EA-007       |
| Reporting  | PHASE-10        | No                  | None (always runs)   |

---------------------------------------------------------------------

## SECTION 4 — PHASE-TO-EA GOVERNANCE MAP

| Phase     | EA-001 | EA-002 | EA-003 | EA-004 | EA-005 | EA-006 | EA-007 | EA-008 | EA-009 | EA-010 |
|-----------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| PHASE-01  | ●      |        |        |        | ●      |        | ●      | ●      |        |        |
| PHASE-02  |        | ●      |        |        |        | ●      |        |        |        |        |
| PHASE-03  |        |        |        |        | ●      | ●      | ●      |        |        |        |
| PHASE-04  |        |        | ●      |        | ●      |        |        |        |        |        |
| PHASE-05  |        |        | ●      | ●      |        | ●      |        |        |        |        |
| PHASE-06  |        |        |        | ●      | ●      | ●      |        |        |        |        |
| PHASE-07  |        | ●      | ●      |        |        | ●      |        |        |        |        |
| PHASE-08  |        | ●      | ●      | ●      |        | ●      |        |        |        | ●      |
| PHASE-09  |        |        |        |        | ●      | ●      | ●      |        |        | ●      |
| PHASE-10  |        |        |        |        |        | ●      |        | ●      |        |        |

---------------------------------------------------------------------

## SECTION 5 — VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
