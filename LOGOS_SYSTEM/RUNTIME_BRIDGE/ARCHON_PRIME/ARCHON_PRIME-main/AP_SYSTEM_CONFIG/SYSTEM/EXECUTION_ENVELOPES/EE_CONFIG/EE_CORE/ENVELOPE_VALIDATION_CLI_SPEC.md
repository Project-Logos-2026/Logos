SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Tooling_Spec
ARTIFACT_NAME: ENVELOPE_VALIDATION_CLI_SPEC
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelope

---------------------------------------------------------------------

PURPOSE

Defines a deterministic CLI command used to validate execution envelopes
before tooling execution.

---------------------------------------------------------------------

COMMAND

ap-envelope validate

---------------------------------------------------------------------

FUNCTIONS

• validate manifest
• verify referenced artifacts
• validate schemas
• check execution phases
• verify governance rules

---------------------------------------------------------------------

OUTPUT

validation_report.md

---------------------------------------------------------------------

FAILURE BEHAVIOR

Fail closed on:

• missing artifact
• schema violation
• invalid execution phase ordering
