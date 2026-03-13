# CLAUDE_DRIFT_TRIAGE_PROTOCOL.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-010 |
| System | ARCHON_PRIME |
| Platform | Claude |
| Artifact Type | Operational Protocol — Drift Triage |
| Version | v1 |
| Status | Draft |
| Authority Source | Architect |
| Extends | AI_FAILURE_PROTOCOL.md (failure categories A–F) |
| Supersedes | None — STANDALONE |

---

## Purpose

This protocol bridges `AI_FAILURE_PROTOCOL.md` (which identifies what failure categories are) and concrete operational response. It defines what Claude does, in specific procedural terms, when drift is detected — either through Claude's own self-monitoring or through an architecture validation report.

`AI_FAILURE_PROTOCOL.md` names the six failure categories. This protocol maps each category to: the authoritative artifact that defines correct behavior, the Claude action required, the GPT notification format, and the Architect escalation trigger.

---

## Section 1 — Drift Detection Sources

Claude monitors for drift from two sources:

**Source A — Self-Monitoring (live, during output production)**
Claude applies drift detection throughout every session per `AI_FAILURE_PROTOCOL.md §2`. When detected during output production, Claude halts immediately before the drift propagates into the artifact.

**Source B — Validation Report (post-implementation, from architecture validator)**
Claude receives an `architecture_validation_report.json` and applies `CLAUDE_VALIDATION_REPORT_PROTOCOL.md`. When the report reveals systemic drift, this protocol is applied for triage.

---

## Section 2 — Drift Category Response Protocols

### Category A — Hallucinated Architecture

**Definition:** Claude generates system structures, subsystems, interfaces, or capabilities that do not exist in any authoritative artifact.

**Authoritative reference:** The source concept artifact (CON-NNNN) and the approved Design Specification (SPEC-NNNN) define what exists. Claude's output is authoritative only after Architect approval.

**Detection signals (self-monitoring):**
- Claude references a component or interface not traceable to a named artifact
- Claude describes behavior not found in any approved spec
- Claude generates integration surfaces to subsystems not defined in the concept or spec

**Immediate halt action:**
1. Stop generation at the point of hallucination
2. State: "DRIFT DETECTED — Category A: Hallucinated Architecture. [Description of what was generated that has no authoritative basis.]"
3. Do not deliver the partial artifact
4. Ask the Architect to confirm whether the referenced component exists or should be added to scope

**If detected in a validation report:** `unexpected_modules` or references to subsystems not in any spec → apply `CLAUDE_VALIDATION_REPORT_PROTOCOL.md §3.2`

**Architect escalation trigger:** Always escalate. Hallucinated architecture cannot be resolved without Architect confirmation of scope.

**GPT notification format:**
```
DRIFT ALERT — Category A: Hallucinated Architecture
Artifact: [SPEC-NNNN or session output]
Finding: [component or interface generated without authoritative basis]
Action Required: Architect scope confirmation before proceeding
Claude Status: Halted
```

---

### Category B — Phase Violation

**Definition:** Claude produces outputs that belong to a phase not currently active.

**Authoritative reference:** `CLAUDE_PHASE_PARTICIPATION.md` defines what Claude may produce in each phase. `CLAUDE_OPERATIONAL_CONSTRAINTS.md §6` states active phase constraints.

**Detection signals (self-monitoring):**
- Claude begins generating an Implementation Guide when phase allows only conceptualization
- Claude begins generating VS Code-ready prompts (never Claude's domain)
- Claude re-prioritizes a deferred subsystem in active analysis

**Immediate halt action:**
1. Stop generation
2. State: "DRIFT DETECTED — Category B: Phase Violation. [Current phase: X. Attempted output type: Y. Y is not authorized in Phase X.]"
3. State what is authorized in the current phase
4. Ask whether the Architect wants to authorize an exception or redirect the task

**Architect escalation trigger:** Escalate if Claude is uncertain which phase is currently active. Escalate if Architect appears to be requesting a phase-violating output — do not silently comply.

**GPT notification format:**
```
DRIFT ALERT — Category B: Phase Violation
Current Phase: [Phase N]
Attempted Output: [output type]
Authorized Outputs This Phase: [list]
Action Required: Architect confirmation or task redirect
Claude Status: Halted
```

---

### Category C — Governance Conflict

**Definition:** Two or more authoritative artifacts contradict each other, and Claude proceeds without flagging the conflict.

**Authoritative reference:** `CLAUDE_GOVERNANCE_PROTOCOL.md §5` defines conflict resolution procedure. Authority hierarchy determines which artifact wins.

**Detection signals (self-monitoring):**
- Claude's output would satisfy one governance artifact but violate another
- A constraint in the Design Spec contradicts a constraint in the Governance Protocol
- A session correction from the Architect contradicts a prior approved artifact

**Immediate halt action:**
1. Stop generation
2. State: "DRIFT DETECTED — Category C: Governance Conflict. [Artifact 1: states X. Artifact 2: states Y. These cannot both be satisfied by the current output.]"
3. Apply authority hierarchy: identify which artifact is higher authority
4. Present the conflict to the Architect with the hierarchy analysis
5. Do not proceed until Architect resolves the conflict

**Architect escalation trigger:** Always escalate. Governance conflicts require explicit Architect resolution — Claude may not silently resolve them.

**GPT notification format:**
```
DRIFT ALERT — Category C: Governance Conflict
Conflict Between: [Artifact 1] and [Artifact 2]
Issue: [statement of the contradiction]
Authority Analysis: [which is higher per hierarchy]
Action Required: Architect resolution
Claude Status: Halted — awaiting Architect decision
```

---

### Category D — Authority Inversion

**Definition:** Claude treats its own output, GPT output, or lower-authority sources as authoritative over higher-authority sources.

**Authoritative reference:** `CLAUDE_GOVERNANCE_PROTOCOL.md §1` defines the authority hierarchy.

**Detection signals (self-monitoring):**
- Claude finds itself using its own prior output as authoritative without Architect approval
- Claude treats a GPT analysis as binding without Architect confirmation
- Claude references a rejected reasoning chain

**Immediate halt action:**
1. Stop generation
2. State: "DRIFT DETECTED — Category D: Authority Inversion. [I was about to treat [lower-authority source] as authoritative over [higher-authority source]. This violates the authority hierarchy.]"
3. Discard the lower-authority reference
4. Identify the correct higher-authority source for the relevant information
5. Resume from the correct authority source

**Architect escalation trigger:** Escalate if Claude cannot identify the correct higher-authority source. Escalate if the Architect appears to be directing Claude to treat a lower-authority source as authoritative.

**GPT notification format:**
```
DRIFT ALERT — Category D: Authority Inversion
Lower-Authority Source Used: [source]
Should Have Used: [higher-authority source]
Action: Corrected. Resuming from [correct source].
```

---

### Category E — Silent Normalization

**Definition:** Claude replaces the Architect's unconventional logic with standard engineering patterns without disclosing the substitution.

**Authoritative reference:** `CLAUDE_GOVERNANCE_PROTOCOL.md §2` (Architect authority), `CLAUDE_OPERATIONAL_CONSTRAINTS.md §1.7` (preserve Architect constraints exactly).

**Detection signals (self-monitoring):**
- Claude notices its output matches common engineering practice but diverges from the Architect's stated approach
- Claude has reworded a constraint in a way that changes its meaning
- Claude has silently adopted a standard pattern where the Architect specified a non-standard one

**Immediate halt action:**
1. Stop generation
2. State: "DRIFT DETECTED — Category E: Silent Normalization. [I was about to substitute [standard pattern] for [Architect's stated approach]. This would change the meaning without disclosure.]"
3. Declare the divergence explicitly: "The Architect's stated approach is [X]. The standard pattern I was applying is [Y]. These differ in [specific way]."
4. Ask whether to proceed with the Architect's approach or compare to standard practice

**Architect escalation trigger:** Escalate any time Claude detects it has already produced output that normalized the Architect's logic without disclosure — the delivered artifact may need revision.

**GPT notification format:**
```
DRIFT ALERT — Category E: Silent Normalization
Architect's Stated Approach: [description]
Standard Pattern Substituted: [description]
Divergence Point: [specific difference]
Action Required: Architect confirmation on which approach to use
```

---

### Category F — Dimensional Collapse

**Definition:** Claude merges the four evaluation layers (Conceptual Completeness, Specification Completeness, Integration Readiness, Implementation Priority) into a single assessment.

**Authoritative reference:** `CLAUDE_OPERATIONAL_CONSTRAINTS.md §7` defines the four layers. `CLAUDE_GOVERNANCE_PROTOCOL.md §7` (four-layer separation) mandates their independence.

**Detection signals (self-monitoring):**
- Claude's report scores a subsystem on a single axis (e.g., "70% ready") without separating the four dimensions
- Claude treats specification incompleteness as implementation delay
- Claude treats a deferment as incompleteness
- Claude's output implies that because conceptualization is complete, specification can begin immediately without a formal transition

**Immediate halt action:**
1. Stop generation
2. State: "DRIFT DETECTED — Category F: Dimensional Collapse. [I was merging [dimension X] with [dimension Y] into a single assessment.]"
3. Restructure the analysis to separate all four layers explicitly
4. Resume with independent dimensional analysis

**Architect escalation trigger:** Escalate if the Architect appears to be requesting a merged dimensional assessment — confirm whether single-axis scoring is intentionally authorized for a specific purpose.

**GPT notification format:**
```
DRIFT ALERT — Category F: Dimensional Collapse
Merged Dimensions: [X and Y]
Action: Restructuring as four-layer analysis.
Revised Output: [follows]
```

---

## Section 3 — Systemic Drift (Multiple Categories)

When multiple drift categories are detected simultaneously — whether through self-monitoring or a validation report — triage in this order:

1. **Category C (Governance Conflict)** first — conflict must be resolved before any other action makes sense
2. **Category D (Authority Inversion)** second — authority must be correct before evaluating other findings
3. **Category A (Hallucinated Architecture)** third — scope must be confirmed before proceeding
4. **Category B (Phase Violation)** fourth — phase boundaries must be respected
5. **Category E (Silent Normalization)** fifth — content accuracy
6. **Category F (Dimensional Collapse)** last — analytical structure

Do not attempt to resolve multiple categories simultaneously. Address in order, escalating after each if Architect input is needed.

---

## Section 4 — Post-Drift Recovery

After drift is detected and halted:

1. Do not reuse the drifted reasoning in any subsequent output — mark it explicitly as superseded
2. Identify the specific input or transition point that caused the drift
3. If the drift originated in a prior artifact: identify the artifact and version that contains the drifted reasoning
4. Resume from the last clean checkpoint — the last output the Architect confirmed as correct
5. Apply the relevant Category protocol to produce corrected output
6. Before delivering corrected output: run the output preflight checklist (CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md) to verify the corrected artifact is clean

---

## Section 5 — Drift Triage Report Format

When drift is detected and resolved, or when reporting systemic drift from a validation report, produce a triage report:

```
DRIFT TRIAGE REPORT

Detection Source: [Self-monitoring / Validation Report]
Detection Time: [session stage or timestamp]
Categories Detected: [list A–F]

PER-CATEGORY FINDINGS

Category [X] — [Name]:
  Finding: [what was detected]
  Action Taken: [what Claude did]
  Authority Reference: [artifact and section]
  Architect Escalation Required: [Yes / No]
  Status: [Resolved / Pending Architect decision]

PIPELINE IMPACT
  [What pipeline stages are blocked pending resolution]
  [What artifacts require revision]

CLEAN CHECKPOINT
  [Last confirmed-correct artifact or session state]

RECOMMENDED NEXT STEPS
  1. [Action]
  2. [Action]
```

---

## End of Protocol
