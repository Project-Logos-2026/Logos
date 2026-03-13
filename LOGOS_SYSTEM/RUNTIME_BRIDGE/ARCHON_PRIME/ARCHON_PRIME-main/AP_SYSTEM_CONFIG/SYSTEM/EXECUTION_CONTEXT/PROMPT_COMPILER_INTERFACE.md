SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Runtime_Contract
ARTIFACT_NAME: PROMPT_COMPILER_INTERFACE
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Context

---------------------------------------------------------------------

PURPOSE

Defines the interface contract between the ARCHON_PRIME prompt compiler
and the VS Code execution agent.

---------------------------------------------------------------------

INTERFACE CONTRACT

The prompt compiler must produce execution prompts that contain:

• execution_phase
• mutation_targets
• validation_procedures
• reporting_requirements
• rollback_instructions

The VS Code execution agent must consume prompts that conform to this
interface contract.

---------------------------------------------------------------------

PROMPT SCHEMA REFERENCE

AP_SYSTEM_CONFIG/GPT/PROMPT_COMPILER/AP_PROMPT_SCHEMA_V1.json

---------------------------------------------------------------------

EXECUTION SEQUENCE

1. Prompt compiler compiles execution envelope into prompt
2. Prompt delivered to VS Code execution agent
3. Execution agent validates prompt schema
4. Execution agent executes phases in declared order
5. Execution agent reports results back via artifact router

---------------------------------------------------------------------

FAILURE BEHAVIOR

If prompt schema validation fails:

• Reject prompt
• Halt execution
• Log schema violation event
• Do not begin execution phases
