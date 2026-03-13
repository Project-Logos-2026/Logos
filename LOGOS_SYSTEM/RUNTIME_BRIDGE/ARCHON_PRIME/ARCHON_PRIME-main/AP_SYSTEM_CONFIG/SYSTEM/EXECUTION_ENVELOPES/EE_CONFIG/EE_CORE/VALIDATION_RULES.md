SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Envelope_Validation_Rules
ARTIFACT_NAME: ENVELOPE_VALIDATION_RULES
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelope

------------------------------------------------

RULE 1 — MANIFEST INTEGRITY

The execution envelope must contain:

ENVELOPE_MANIFEST.json

The manifest must reference:

DS
IG
EP
EA artifacts

All paths must resolve successfully.

------------------------------------------------

RULE 2 — ARTIFACT METADATA

All envelope artifacts must contain ARCHON metadata headers:

SYSTEM
ARTIFACT_TYPE
ARTIFACT_NAME
STATUS
VERSION
DATE
AUTHORITY

Artifacts missing metadata are rejected.

------------------------------------------------

RULE 3 — EXECUTION PHASE ORDER

Execution plans must include the following ordered phases:

environment_verification
artifact_discovery
static_analysis
simulation_pass
controlled_mutation
validation
reporting

------------------------------------------------

RULE 4 — ADDENDUM RESOLUTION

All EA artifacts referenced in the manifest must exist in:

ADDENDA/

No missing or duplicate entries are allowed.

------------------------------------------------

RULE 5 — GOVERNANCE CONSISTENCY

Envelope artifacts must not conflict with:

GPT configuration governance
Claude artifact schema
VS Code execution contracts

Any governance conflict halts execution.
