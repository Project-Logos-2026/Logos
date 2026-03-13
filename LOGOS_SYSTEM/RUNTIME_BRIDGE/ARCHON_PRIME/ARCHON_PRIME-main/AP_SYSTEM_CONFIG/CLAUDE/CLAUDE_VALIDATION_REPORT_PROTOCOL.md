# CLAUDE_VALIDATION_REPORT_PROTOCOL.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-009 |
| System | ARCHON_PRIME |
| Platform | Claude |
| Artifact Type | Operational Protocol — Architecture Validation Report Interpretation |
| Version | v1 |
| Status | Draft |
| Authority Source | Architect |
| Schema Reference | AP_MASTER_SPEC_V2_SCHEMA.json §14 |
| Supersedes | None — STANDALONE |

---

## Purpose

This protocol defines how Claude interprets an `architecture_validation_report.json` produced by the ARCHON_PRIME architecture validator. It maps each report field to a specific action protocol and connects findings to the appropriate Claude operational mode.

Without this protocol, the feedback loop from the validator back into Claude's workflow is undefined. Claude would receive a validation report with no structured procedure for converting findings into remediation actions.

---

## Section 1 — Report Structure Reference

The architecture validation report has the following top-level structure. Claude must be able to parse all fields.

```json
{
  "validation_timestamp": "ISO_TIMESTAMP",
  "summary": {
    "modules_scanned": int,
    "registry_modules": int,
    "missing_spec_modules": int,
    "unexpected_modules": int,
    "misplaced_modules": int,
    "header_schema_violations": int,
    "import_rule_violations": int
  },
  "missing_spec_modules": [],
  "unexpected_modules": [],
  "misplaced_modules": [],
  "header_schema_violations": [],
  "import_rule_violations": [],
  "subsystem_boundary_violations": [],
  "artifact_surface_violations": [],
  "architecture_valid": true | false
}
```

---

## Section 2 — Interpretation Entry Point

When Claude receives a validation report, execute this procedure:

**Step 1:** Read `architecture_valid`.
- If `true` and all finding arrays are empty: state "Architecture validation passed. No findings." No further action required.
- If `true` but finding arrays are non-empty: non-blocking findings exist. Proceed to Step 3 for each finding type.
- If `false`: blocking findings exist. Proceed to Step 2.

**Step 2:** Read the `summary` block. Identify which finding counts are non-zero. These are the active finding categories requiring action. Proceed to Section 3 for each active category.

**Step 3:** For each finding category with non-zero count, read the corresponding array and apply the action protocol from Section 3.

**Step 4:** Produce a triage report (Section 5 format) summarizing findings, severities, recommended actions, and which findings require Architect decision.

---

## Section 3 — Finding Category Action Protocols

### 3.1 `missing_spec_modules`

**What it means:** A module defined in the canonical registry does not exist at its canonical path. The spec requires it; the repository does not have it.

**Claude mode:** Formalization_Expert (if spec update needed) or advisory (if this is an implementation gap)

**Action protocol:**

1. For each missing module: identify which implementation phase it belongs to (from registry `implementation_phase` field)
2. Determine whether the phase is active or future
3. If phase is active: flag as implementation gap. Recommend that GPT generate an implementation prompt for this module. No spec update needed.
4. If phase is future: this is expected. Note it as deferred, not a violation.
5. If the module appears to have been deleted: escalate to Architect per non-deletion policy.

**Severity:** Blocking if phase is active; Non-blocking if phase is future.

**GPT notification format:**
```
MISSING MODULE — [module_name]
Registry Path: [canonical_path]
Phase: [implementation_phase]
Status: [Active gap — requires implementation prompt / Future phase — deferred]
```

---

### 3.2 `unexpected_modules`

**What it means:** A module exists in the runtime surface but is not in the canonical registry. It has no canonical identity.

**Claude mode:** Concept_Auditor (assess whether the module represents a valid enhancement or analog) → Formalization_Expert (if adoption or spec update is warranted)

**Action protocol:**

1. For each unexpected module: attempt to identify it
   - Does it correspond to a spec module with a different name or path? → candidate for `ANALOG_IMPLEMENTATION`
   - Does it implement functionality not in the spec? → candidate for `ENHANCEMENT_MODULE`
   - Is it from a prior implementation cycle with no clear role? → candidate for `LEGACY_MODULE`
   - Cannot be identified: → `UNKNOWN_MODULE`

2. Apply the analog reconciliation process (IMPLEMENTATION_GUIDE_TEMPLATE.md §7) for all ANALOG_IMPLEMENTATION candidates

3. For ENHANCEMENT_MODULE: do not adopt without Architect authorization and spec update (enhancement lifecycle)

4. For LEGACY_MODULE: flag for Architect decision on retain/archive/remove

5. For UNKNOWN_MODULE: escalate immediately. Do not integrate or retain without Architect decision.

**Severity:** Blocking for UNKNOWN_MODULE and ENHANCEMENT_MODULE (until resolved); Major for ANALOG_IMPLEMENTATION (until reconciled); Minor for LEGACY_MODULE.

---

### 3.3 `misplaced_modules`

**What it means:** A module exists but is not at its canonical path. Its canonical identity cannot be verified by the validator.

**Claude mode:** Formalization_Expert (spec review) or advisory

**Action protocol:**

1. For each misplaced module: compare actual path to registry `canonical_path`
2. Determine which type of misplacement:
   - Wrong directory, correct filename: path error in placement or registry — determine which is authoritative
   - Wrong filename, correct directory: naming error — determine correct name
   - Wrong directory and filename: candidate for ANALOG_IMPLEMENTATION — apply reconciliation
3. If the registry is correct: recommend path correction via GPT/VS Code
4. If the registry may be wrong: escalate to Architect — do not update registry without authorization

**Severity:** Blocking until resolved.

---

### 3.4 `header_schema_violations`

**What it means:** One or more runtime modules have headers that are missing, incomplete, or contain values that do not match the canonical registry.

**Claude mode:** Advisory (validation) using CLAUDE_MODULE_HEADER_PROTOCOL.md

**Action protocol:**

1. For each violation: apply CLAUDE_MODULE_HEADER_PROTOCOL.md §2 (Validation Procedure) to determine the specific failure type
2. Classify the failure:
   - Missing header entirely → generate correct header using CLAUDE_MODULE_HEADER_PROTOCOL.md §1
   - Missing fields → identify which fields and generate the complete correct header
   - Registry mismatch → identify the discrepancy; if registry is authoritative, generate corrected header; if mismatch reveals a registry error, escalate to Architect
3. Produce a corrected header block for each violated module
4. Flag for GPT/VS Code to inject the corrected header

**Severity:** Blocking for all header violations.

---

### 3.5 `import_rule_violations`

**What it means:** A module imports from a subsystem or module it is not permitted to import from, or fails to import from a required source.

**Claude mode:** Formalization_Expert (spec review) or Concept_Auditor (if the violation reveals a systemic boundary design issue)

**Action protocol:**

1. For each violation: identify the importing module and the illegal import target
2. Check the subsystem contract for the importing module's subsystem
3. Determine the cause:
   - Import violates `forbidden_cross_imports`: hard boundary violation — escalate; cannot proceed without Architect decision on whether to change the architecture or remove the import
   - Import not in `allowed_imports` but not explicitly forbidden: soft boundary gap — check whether the spec should permit this import; if yes, propose spec update; if no, flag for removal
4. Do not recommend removing an import without understanding why it exists. An unexpected import may reveal a missing dependency declaration in the spec.

**Severity:** Blocking for hard boundary violations; Major for soft boundary gaps.

---

### 3.6 `subsystem_boundary_violations`

**What it means:** A module's header declares a subsystem that does not match the registry, or cross-subsystem import rules at the subsystem level are violated.

**Claude mode:** Concept_Auditor

**Action protocol:**

1. Determine whether this is a header error (wrong subsystem declared) or an actual architectural violation (module placed in wrong subsystem)
2. If header error: correct the header (see 3.4 protocol)
3. If architectural violation: this may indicate a spec design issue — modules may have been split across the wrong subsystem boundaries. Escalate to Architect with a description of what was expected vs. what was found.

**Severity:** Blocking.

---

### 3.7 `artifact_surface_violations`

**What it means:** Runtime code exists in a non-runtime surface directory, or non-runtime artifacts exist in the runtime surface.

**Claude mode:** Advisory

**Action protocol:**

1. For each violation: identify the file and its current location vs. the correct surface
2. Determine whether the file is runtime code or an artifact (report, design doc, schema)
3. Recommend the correct surface and directory for the file
4. Flag for GPT/VS Code to move the file
5. If moving runtime code out of a runtime directory will break imports: flag this dependency before recommending the move — do not recommend moves that break the build without a remediation plan

**Severity:** Blocking for runtime code in non-runtime surfaces; Major for non-runtime artifacts in runtime surfaces.

---

## Section 4 — Escalation Triggers

The following conditions require immediate Architect escalation before Claude takes any further action:

| Condition | Escalation Reason |
|-----------|------------------|
| `architecture_valid == false` AND unknown root cause | Cannot safely recommend remediation without understanding systemic cause |
| UNKNOWN_MODULE present | No classification can be assigned without Architect context |
| Hard subsystem boundary violation (forbidden import) | Architectural decision required — cannot resolve at implementation level |
| Module appears to have been deleted from registry | Non-deletion policy may have been violated |
| Registry-vs-header mismatch where registry may be incorrect | Registry is authoritative — only Architect can authorize registry change |
| Validation report contradicts Design Specification | Spec may need revision — cannot proceed without Architect review |

---

## Section 5 — Triage Report Format

After interpreting a validation report, Claude produces a triage report in this format:

```
ARCHITECTURE VALIDATION TRIAGE REPORT

Report Timestamp: [ISO timestamp from report]
Architecture Valid: [Yes / No]
Total Findings: [count by category]

FINDING SUMMARY
  missing_spec_modules:         [count] — [Blocking / Non-blocking]
  unexpected_modules:           [count] — [Blocking / Non-blocking]
  misplaced_modules:            [count] — [Blocking]
  header_schema_violations:     [count] — [Blocking]
  import_rule_violations:       [count] — [Blocking / Major]
  subsystem_boundary_violations:[count] — [Blocking]
  artifact_surface_violations:  [count] — [Blocking / Major]

FINDINGS REQUIRING ARCHITECT DECISION
  [Finding ID]: [description and reason escalation is required]

FINDINGS CLAUDE CAN RESOLVE
  [Finding ID]: [description and recommended action]
  [Corrected header blocks or registry proposals as applicable]

PIPELINE STATUS
  [All gates blocked / Specific gates blocked / No gates blocked]
  [Which pipeline stages cannot proceed until findings are resolved]

RECOMMENDED NEXT STEPS
  1. [Action]
  2. [Action]
  3. [Action]
```

---

## Section 6 — Scope Boundaries

Claude interprets validation reports and produces triage reports and corrected headers. Claude does not:
- Directly modify the repository
- Execute the architecture validator
- Modify the canonical registry without Architect authorization
- Resolve hard boundary violations without Architect decision

All physical remediation actions (file moves, header injections, module deletions) belong to GPT/VS Code.

---

## End of Protocol
