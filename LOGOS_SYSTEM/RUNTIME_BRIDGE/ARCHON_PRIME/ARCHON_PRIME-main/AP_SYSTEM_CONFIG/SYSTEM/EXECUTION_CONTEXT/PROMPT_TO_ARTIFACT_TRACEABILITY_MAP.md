SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Governance_Map
ARTIFACT_NAME: PROMPT_TO_ARTIFACT_TRACEABILITY_MAP
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelope

---------------------------------------------------------------------

PURPOSE

Defines traceability relationships between prompts executed by GPT
and artifacts produced by the VS Code execution agent.

---------------------------------------------------------------------

TRACEABILITY MODEL

Prompt
   ↓
Execution Task
   ↓
Generated Artifact
   ↓
Artifact Metadata
   ↓
Report Entry

---------------------------------------------------------------------

REQUIREMENT

Every artifact produced by a tooling prompt must include:

• originating prompt identifier
• execution timestamp
• mutation scope
• validation result
