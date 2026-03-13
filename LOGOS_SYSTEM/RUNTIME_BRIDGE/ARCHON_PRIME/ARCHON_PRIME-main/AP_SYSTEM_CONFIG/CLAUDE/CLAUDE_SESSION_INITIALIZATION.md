# CLAUDE_SESSION_INITIALIZATION.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-002 |
| System | ARCHON_PRIME |
| Platform | Claude |
| Artifact Type | Session Initialization Protocol |
| Version | v2 |
| Status | Draft |
| Authority Source | Architect |
| Supersedes | CLAUDE_SESSION_INITIALIZATION.md v1 |

---

## V2 Change Summary

- Added V2 artifact availability verification (Section 2) — confirms all 27 expected project files are loaded before accepting any task
- Added active phase and deferment state declaration (Section 3) — Claude must confirm current constraints before first output
- Added session readiness gate with structured readiness report (Section 4)
- Added critical constraint echo (Section 5) — surfaces the 5 most operationally consequential constraints at session start
- Session start invocation phrase added (Section 7)

All v1 content preserved in Section 6 (Context Ingestion).

---

## Purpose

This protocol governs Claude's initialization sequence at the start of every ARCHON_PRIME session. It ensures Claude begins work with the correct governance stack loaded, the correct phase constraints active, and the correct operational posture confirmed.

A session that begins without initialization confirmation risks: operating under stale phase assumptions, producing artifacts against v1 schema when v2 is required, missing critical constraints, or failing to notice that required governance artifacts are absent from the project knowledge environment.

---

## Section 1 — Initialization Trigger

Run this full initialization sequence when:
- A new conversation begins in the ARCHON_PRIME Claude project
- The Architect uses the invocation phrase `INITIALIZE ARCHON PRIME CLAUDE SESSION`
- The session context has been compacted or reset and Claude cannot confirm which artifacts were active

Do not skip initialization on the assumption that the environment is correct. The cost of a 60-second initialization is lower than the cost of an hour of work against the wrong schema.

---

## Section 2 — Artifact Availability Verification

Before accepting any task, Claude must confirm that all required project knowledge artifacts are available. This is the V2 protocol stack. 27 files.

**Step 2.1 — Governance and Operational Protocols (10 files)**

Confirm each of the following is accessible in project knowledge:

| # | Artifact | Artifact ID | Critical |
|---|---|---|---|
| 1 | `CLAUDE_GOVERNANCE_PROTOCOL.md` | GOV-001 | Yes |
| 2 | `CLAUDE_OPERATIONAL_CONSTRAINTS.md` | GOV-003 | Yes |
| 3 | `AI_FAILURE_PROTOCOL.md` | GOV-004 | Yes |
| 4 | `CLAUDE_DRIFT_TRIAGE_PROTOCOL.md` | OPS-010 | Yes |
| 5 | `ARTIFACT_LIFECYCLE_RULES.md` | GOV-005 | Yes |
| 6 | `CLAUDE_PHASE_PARTICIPATION.md` | (unlabeled) | Yes |
| 7 | `CLAUDE_SYSTEM_PROMPT.md` | OPS-001 v2 | Yes |
| 8 | `CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md` | OPS-006 | Yes |
| 9 | `CLAUDE_SPEC_TO_GPT_HANDOFF_FORMAT.md` | OPS-007 | Yes |
| 10 | `PROJECT_INSTRUCTIONS.md` | (style) | No |

**Step 2.2 — Mode Protocols (3 files)**

| # | Artifact | Critical |
|---|---|---|
| 11 | `CLAUDE_FORMALIZATION_PROTOCOL.md` v2 | Yes |
| 12 | `CLAUDE_CONCEPT_AUDIT_PROTOCOL.md` | Yes |
| 13 | `CLAUDE_RESEARCH_PROTOCOL.md` | Yes |

**Step 2.3 — Operational Tooling Protocols (3 files)**

| # | Artifact | Artifact ID | Critical |
|---|---|---|---|
| 14 | `CLAUDE_MODULE_HEADER_PROTOCOL.md` | OPS-008 | Yes |
| 15 | `CLAUDE_VALIDATION_REPORT_PROTOCOL.md` | OPS-009 | Yes |
| 16 | `CLAUDE_DRIFT_TRIAGE_PROTOCOL.md` | OPS-010 | Yes (already in row 4) |

**Step 2.4 — Workflow and Handoff Artifacts (4 files)**

| # | Artifact | Critical |
|---|---|---|
| 17 | `CLAUDE_SESSION_INITIALIZATION.md` v2 | Yes — this document |
| 18 | `CLAUDE_CONCEPT_HANDOFF_FORMAT.md` | Yes |
| 19 | `CLAUDE_CONCEPT_REFINEMENT_WORKFLOW.md` | No |
| 20 | `CLAUDE_FEEDBACK_REPORT_FORMAT.md` | No |

**Step 2.5 — Templates (4 files)**

| # | Artifact | Critical | Schema Reference |
|---|---|---|---|
| 21 | `DESIGN_SPEC_TEMPLATE.md` v2 | Yes | AP_MASTER_SPEC_V2_SCHEMA.json |
| 22 | `IMPLEMENTATION_GUIDE_TEMPLATE.md` v2 | Yes | AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json |
| 23 | `FORMAL_MODEL_TEMPLATE.md` | Yes | None |
| 24 | `ALGORITHM_MODEL_TEMPLATE.md` | Yes | None |

**Step 2.6 — Schemas (5 files)**

| # | Artifact | Critical | Notes |
|---|---|---|---|
| 25 | `AP_MASTER_SPEC_V2_SCHEMA.json` | Yes | Design Specification validator |
| 26 | `AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json` | Yes | Implementation Guide validator |
| 27 | `ARTIFACT_SCHEMA.json` | Yes | Shared meta-schema (renamed from DESIGN_SPEC_SCHEMA.json) |
| 28 | `CONCEPT_ARTIFACT_SCHEMA.json` | Yes | Concept artifact validator |
| 29 | `TOOL_ENFORCEMENT_SCHEMA.json` | Yes | Tool invocation validator (renamed from IMPLEMENTATION_GUIDE_SCHEMA.json) |

**Note:** Items 16 and the count of 27 unique files — the list above enumerates 29 rows but `CLAUDE_DRIFT_TRIAGE_PROTOCOL.md` appears in both row 4 and row 16. Unique count is 27 files.

**If a Critical artifact is missing:**
1. State which artifact is missing
2. State which capabilities are impaired without it
3. Do not proceed with tasks that require the missing artifact
4. Notify the Architect before accepting work

**If a Non-Critical artifact is missing:** Note it; proceed with reduced capability in the relevant area.

---

## Section 3 — Active Phase and Deferment State Declaration

After confirming artifact availability, declare the active phase constraints from `CLAUDE_PHASE_PARTICIPATION.md`.

State the following at session start:

```
ACTIVE PHASE STATE
Current phases: Phase 1 (Conceptualization) + Phase 2 (Specification Production)
Active campaign: Specification production — Design Specs and Implementation Guides authorized
Deferred: DRAC implementation (deferred until canonical runtime exists)
Deferred: All Phase 3+ activities (prompt engineering is GPT domain)
Deferred: Any subsystem explicitly marked as deferred in active specs

WHAT THIS MEANS FOR THIS SESSION:
✓ Concept auditing authorized
✓ Analog discovery authorized
✓ Formal model production authorized
✓ Design Specification production authorized (V2 schema required)
✓ Implementation Guide production authorized (V2 schema required)
✗ VS Code prompt engineering — not Claude's domain
✗ DRAC implementation — deferred
✗ Implementation of any deferred subsystem
```

If the Architect has provided a session overlay that updates active phases or deferments, apply the overlay and state the updated phase state explicitly.

---

## Section 4 — Session Readiness Gate

After Steps 2 and 3, Claude produces a structured readiness report before accepting any task:

```
ARCHON_PRIME CLAUDE SESSION — READINESS REPORT
Session Start: [timestamp if available, otherwise "session start"]
Protocol Version: V2

ARTIFACT AVAILABILITY
Critical artifacts loaded:    [N]/[N] — [COMPLETE / INCOMPLETE]
Missing critical artifacts:   [list, or "None"]
Non-critical gaps:             [list, or "None"]

V2 SCHEMA STATUS
AP_MASTER_SPEC_V2_SCHEMA.json:           [Present / Missing]
AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json:  [Present / Missing]
DESIGN_SPEC_TEMPLATE.md v2:              [Present / Missing]
IMPLEMENTATION_GUIDE_TEMPLATE.md v2:     [Present / Missing]
CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md:    [Present / Missing]

ACTIVE PHASE CONSTRAINTS
Current phases:    Phase 1 + Phase 2
Deferred systems:  DRAC, [any others from spec deferments]
Spec campaign:     Active

OPERATIONAL MODES AVAILABLE
Research_Specialist:    [Ready / Impaired — reason]
Formalization_Expert:   [Ready / Impaired — reason]
Concept_Auditor:        [Ready / Impaired — reason]

Status: READY / NOT READY
Blocking Issues: [list, or "None"]
```

**Status: NOT READY** blocks task acceptance for affected modes. If all critical artifacts are present, Status is READY. If any critical artifact is absent, Status is NOT READY for modes that depend on it.

Do not begin task execution until the readiness report shows Status: READY for the mode required by the task.

---

## Section 5 — Critical Constraint Echo

After the readiness report, echo the 5 most operationally consequential constraints. This is not a lecture — it is a session anchor. It runs once at initialization and is not repeated mid-session.

```
CRITICAL CONSTRAINTS ACTIVE THIS SESSION

1. GOVERNANCE-FIRST: Governance enforcement must be in place before or during
   capability activation. Never schedule governance after functionality.

2. FOUR-LAYER SEPARATION: Conceptual completeness, specification completeness,
   integration readiness, and implementation priority are independent dimensions.
   Merging them is a Category F drift violation.

3. V2 SCHEMA REQUIRED: All Design Specifications must conform to
   AP_MASTER_SPEC_V2_SCHEMA.json. All Implementation Guides must conform to
   AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json. Output preflight is mandatory before
   every delivery.

4. DEFERMENTS ARE BINDING: DRAC and all deferred subsystems must not be
   re-prioritized into active analysis without explicit Architect authorization.

5. HALT ON DRIFT: All 6 failure categories (A–F) trigger immediate halt.
   Apply CLAUDE_DRIFT_TRIAGE_PROTOCOL.md for the appropriate response.
   Never proceed past detected drift.
```

---

## Section 6 — Context Ingestion

*(Content from v1 preserved in full)*

After completing Sections 2–5, ingest any provided context:

### 6.1 Project Context Overlay

If the Architect provides a session overlay (updated phase state, new deferments, active concept or spec to work on), ingest it and update the readiness report accordingly. State any changes to active phase, deferments, or priority.

### 6.2 Concept or Task Artifact

If the Architect provides a concept artifact, spec artifact, or task description at session start:

1. Identify which operational mode the task requires
2. Confirm that mode is available (per readiness report)
3. Identify any required artifacts for the task (source concept, prior spec, analog candidates)
4. If required artifacts are missing: request them before beginning
5. State the mode you are operating in and the task scope before producing output

### 6.3 Handoff Packet from GPT

If the Architect provides a handoff packet from GPT (per `CLAUDE_CONCEPT_HANDOFF_FORMAT.md`):

1. Validate that the handoff packet includes the required fields
2. Extract the concept artifact and maturity assessment
3. Confirm the concept has been through at minimum one GPT brainstorming pass
4. Identify whether an audit pass or direct formalization is requested
5. State the identified mode and begin

### 6.4 Continuation from Prior Session

If continuing from a prior session:

1. Identify the last produced artifact (ID, type, status)
2. State where the prior session ended
3. If continuing formalization: confirm the source concept is still the active authoritative concept
4. If prior output is referenced: revalidate it against the current authority hierarchy before using it

---

## Section 7 — Invocation Phrase

```
INITIALIZE ARCHON PRIME CLAUDE SESSION
```

When this phrase is received, execute Sections 2 through 6 in order. Produce the readiness report before accepting any task.

When the Architect provides this phrase mid-session (e.g., after a context reset), re-run the full initialization sequence.

---

## Section 8 — Abbreviated Initialization

For sessions where the Architect confirms the environment is already set up and requests abbreviated initialization:

1. Confirm the V2 schema files are present (Step 2.6 only)
2. State active phase and deferments (Section 3, abbreviated to 3 lines)
3. State the mode requested
4. Begin work

Abbreviated initialization is appropriate only when the Architect explicitly authorizes it. Do not abbreviate by default.

---

## End of Protocol
