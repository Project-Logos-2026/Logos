# CLAUDE_SPEC_TO_GPT_HANDOFF_FORMAT.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-007 |
| System | ARCHON_PRIME |
| Platform | Claude → GPT |
| Artifact Type | Handoff Format Specification |
| Version | v1 |
| Status | Draft |
| Authority Source | Architect |
| Schema References | AP_MASTER_SPEC_V2_SCHEMA.json, AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json |
| Supersedes | None — STANDALONE |
| Symmetric Counterpart | CLAUDE_CONCEPT_HANDOFF_FORMAT.md (governs GPT→Claude intake) |

---

## Purpose

This artifact defines the format and completeness requirements that a Design Specification or Implementation Guide must satisfy before GPT's Prompt_Engineer may begin prompt derivation from it. It is the symmetric counterpart to `CLAUDE_CONCEPT_HANDOFF_FORMAT.md`, which governs what Claude accepts from GPT.

Without this format, GPT receives Claude-produced artifacts without a shared protocol for interpreting them. This creates interpretation gaps that become prompt engineering errors and ultimately execution errors in VS Code. This artifact closes that boundary.

This document governs two things:
1. What Claude must include in a handoff packet when delivering to GPT
2. What GPT must do when it receives each section type (directly prompt-derivable vs. requires Architect review)

---

## Section 1 — Handoff Packet Structure

When Claude delivers a Design Specification or Implementation Guide to GPT for prompt engineering, it must package the artifact in a handoff packet. The handoff packet consists of:

1. The artifact itself (Design Spec `.md` or Implementation Guide `.md`)
2. A Handoff Cover Block (defined in Section 2)
3. A Section Derivability Map (defined in Section 3)
4. An Ambiguity Flag List (defined in Section 4)

The Handoff Cover Block and Section Derivability Map may be prepended to the artifact as a header, or delivered as a separate message immediately before the artifact. They must not be omitted.

---

## Section 2 — Handoff Cover Block Format

The Handoff Cover Block is a structured header Claude prepends to every GPT delivery.

```
ARCHON_PRIME — CLAUDE→GPT HANDOFF PACKET

Artifact ID:        [SPEC-NNNN or IMPL-NNNN]
Artifact Type:      [Design Specification / Implementation Guide]
Subsystem:          [subsystem name]
Version:            [vN]
Status:             [lifecycle state]
Schema:             [AP_MASTER_SPEC_V2_SCHEMA.json or AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json]
Source Concept:     [CON-NNNN] (Design Spec only)
Source Spec:        [SPEC-NNNN] (Implementation Guide only)
Preflight Status:   [PASSED / PASSED WITH FLAGS]
Preflight Flags:    [list of non-blocking flags, or "None"]

Sections requiring Architect review before prompt derivation:
  [list section numbers, or "None"]

Sections directly prompt-derivable:
  [list section numbers]

Open blocking ambiguities (must resolve before prompt generation):
  [list ambiguity IDs and questions, or "None"]

Delivery authorized by: Claude / Formalization_Expert
Date: [YYYY-MM-DD]
```

---

## Section 3 — Section Derivability Map

This map defines which sections of a Claude-produced artifact GPT may derive prompts from directly, and which require Architect review first. This is not a suggestion — it is a handoff protocol constraint.

### 3.1 Design Specification Derivability

| Section | Title | GPT Action |
|---------|-------|-----------|
| Specification Identity | Full identity block | Direct derivation permitted — use for artifact headers |
| Lineage | Provenance chain | Reference only — do not derive implementation steps |
| Purpose | Scope statement | Direct derivation permitted — use for context framing |
| Functional Requirements | FR-NNN table | Direct derivation permitted — each FR maps to implementation obligation |
| Constraints | C-NNN table | Direct derivation permitted — each constraint maps to a validation check |
| Formal Model | Primitives, operations, axioms | **Architect review required** before deriving implementation from axioms — formal model may contain decisions with non-obvious implementation consequences |
| Mathematical Representation | Formal notation | **Architect review required** — do not translate formal notation to code without review |
| Algorithmic Representation | Data structures, algorithms | Direct derivation permitted — this section is written for implementation consumption |
| Canonical Architecture Definition | Directory tree, placement rules | Direct derivation permitted — derive directory creation steps directly |
| Canonical Module Registry | Module entries | Direct derivation permitted — each module entry maps to a file creation step |
| Module Identity Rules | Validity conditions | Direct derivation permitted — derive validation checks |
| Subsystem Contracts | Boundary definitions | Direct derivation permitted — derive import enforcement checks |
| Artifact Surface Definition | Surface assignments | Direct derivation permitted — derive directory isolation enforcement |
| Module Classification Types | Classification labels | Reference only — used in validation report interpretation |
| Header Schema Definition | Required fields, format, rules | Direct derivation permitted — derive header injection steps |
| Architecture Validation Rules | AVR-NNN checks, gate conditions | Direct derivation permitted — derive validation gate steps |
| Governance Rules | Non-deletion, change process | Reference only — do not derive implementation steps from governance rules |
| Implementation Sequence | Phase ordering | Direct derivation permitted — derive build phase sequencing |
| Enhancement Lifecycle | Stage workflow | Reference only — do not implement enhancement steps without Architect authorization |
| Integration Surfaces | Adjacent subsystem interfaces | Direct derivation permitted — derive integration wiring steps |
| Verification Criteria | V-NNN table | Direct derivation permitted — derive test steps |
| Deferments | Excluded scope | Reference only — do not generate prompts for deferred items |
| Open Questions | Unresolved items | **Do not derive prompts** for sections touched by unresolved blocking questions |
| Revision History | Change log | Reference only |

### 3.2 Implementation Guide Derivability

| Section | Title | GPT Action |
|---------|-------|-----------|
| Guide Identity | Full identity block | Direct derivation permitted — use for artifact headers |
| Overview | Summary | Reference only — context framing |
| Prerequisites | Dependency table | Direct derivation permitted — derive prerequisite verification steps |
| Deterministic Build Sequence | BS-NNN steps | Direct derivation permitted — this is the primary prompt derivation source |
| Header Injection Rules | HIR-NNN rules | Direct derivation permitted — derive injection enforcement steps |
| Spec Compliance Checks | SCC-NNN checks | Direct derivation permitted — derive validation steps |
| Module Generation Contract | Pre-generation conditions, rules | Direct derivation permitted — derive generation gate steps |
| Analog Reconciliation Process | Detection, reconciliation steps | Direct derivation permitted — derive reconciliation workflow steps |
| Enhancement Integration Rules | EI-NNN workflow, gate | **Architect review required** before deriving any enhancement integration prompt |
| Artifact Directory Rules | ADR-NNN rules | Direct derivation permitted — derive directory enforcement steps |
| Drift Detection Audit | DD-NNN checks | Direct derivation permitted — derive audit execution steps |
| Architecture Validation Gate | Gate rule, gated stages, validator | Direct derivation permitted — derive validation gate invocation |
| Stages | Stage entries with modules | Direct derivation permitted — primary source for stage-by-stage prompts |
| Governance Enforcement Points | Enforcement entries | Reference only — do not override with prompt logic |
| Ambiguity Log | Unresolved ambiguities | **Do not derive prompts** for modules affected by unresolved blocking ambiguities |
| Revision History | Change log | Reference only |

---

## Section 4 — Ambiguity Flag List Format

Claude must declare any unresolved ambiguities in the handoff packet. Ambiguities that are blocking must be listed explicitly. GPT must not generate prompts for any module or section affected by a blocking ambiguity.

Format:

```
AMBIGUITY FLAG LIST

[Ambiguity ID]: [A-NNN]
  Question: [what is unresolved]
  Affects: [module ID or section number]
  Blocking: [Yes / No]
  Recommendation: [Claude's recommendation if any]
  Resolution required from: [Architect]
```

If there are no ambiguities: state `AMBIGUITY FLAG LIST: None`

---

## Section 5 — GPT Intake Requirements

When GPT's Prompt_Engineer receives a Claude handoff packet, it must:

1. Confirm the Handoff Cover Block is present. If absent, request it before proceeding.
2. Confirm `Preflight Status` is `PASSED` or `PASSED WITH FLAGS`. If preflight failed, do not proceed — escalate to Architect.
3. Read the Section Derivability Map before generating any prompt.
4. For any section marked "Architect review required" — do not derive prompts until Architect confirmation is received in session.
5. For any section affected by a blocking ambiguity — do not derive prompts until ambiguity is resolved.
6. For sections marked "Direct derivation permitted" — derive prompts mechanically from the artifact content. Do not interpret or redesign.
7. Any deviation from the artifact's stated logic must be flagged to the Architect, not silently corrected.

---

## Section 6 — Cross-Reference Format

When a Design Spec or Implementation Guide references another artifact, the reference must follow this canonical format to be machine-processable by GPT:

```
[ARTIFACT_TYPE-NNNN §SECTION_NUMBER]
```

Examples:
- `[SPEC-003 §4.2]` — references Design Specification SPEC-003, Section 4.2
- `[IMPL-002 §3]` — references Implementation Guide IMPL-002, Stage 3
- `[CON-007 §FR-002]` — references Concept Artifact CON-007, requirement FR-002

Free-text references (e.g., "as defined in the RGE spec") are not acceptable in artifacts intended for GPT consumption. Claude must use canonical reference format in all formal artifacts.

---

## Section 7 — Rejection Criteria

GPT must return an artifact to Claude (not proceed to prompt generation) when:

| Condition | Action |
|-----------|--------|
| Handoff Cover Block absent | Return with request for Cover Block |
| Preflight status is FAILED | Escalate to Architect — do not return to Claude without Architect instruction |
| Required section is missing or empty | Return to Claude for completion |
| Unresolved blocking ambiguity present | Hold — request Architect resolution before proceeding |
| Artifact status is `draft` | Confirm with Architect whether draft-stage prompt generation is authorized |
| Open questions with `blocking: Yes` are unresolved | Hold — request Architect resolution |

---

## Section 8 — Invocation

This format applies automatically to all Design Specification and Implementation Guide deliveries from Claude to GPT. No invocation phrase is required. Claude applies it as part of the output preflight process defined in `CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md`.

---

## End of Handoff Format Specification
