SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Tooling_Spec
ARTIFACT_NAME: VS_CODE_ENVELOPE_LOADER_SPEC
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelope

---------------------------------------------------------------------

PURPOSE

Defines how VS Code loads execution envelopes prior to tooling execution.

---------------------------------------------------------------------

LOADER BEHAVIOR

1. discover manifest
2. validate envelope
3. load execution plan
4. resolve addendum artifacts
5. construct execution context

---------------------------------------------------------------------

FAILURE RULE

If validation fails:

• execution must not begin
• tooling pass must abort
