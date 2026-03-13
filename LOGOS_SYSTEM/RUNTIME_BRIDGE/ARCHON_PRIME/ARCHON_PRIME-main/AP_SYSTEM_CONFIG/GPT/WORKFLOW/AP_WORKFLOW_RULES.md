ARCHON_PRIME — WORKFLOW RULES

STATUS: CANONICAL
MODE: DETERMINISTIC REMEDIATION PIPELINE

---------------------------------------------------------------------

SECTION 1 — PURPOSE

Define the operational workflow for ARCHON PRIME remediation
and repository reconstruction.

This workflow ensures the repository converges to the
architecture specification while preserving all existing functionality.

---------------------------------------------------------------------

SECTION 2 — CORE PRINCIPLES

ARCHON PRIME workflow operates under five principles:

DETERMINISM  
SPEC AUTHORITY  
NON-DELETION  
PHASE ISOLATION  
VALIDATION FIRST

---------------------------------------------------------------------

SECTION 3 — WORKFLOW PHASES

The ARCHON PRIME remediation pipeline consists of five phases.

PHASE 1 — REPOSITORY DISCOVERY

• scan repository
• map modules
• generate structure reports

PHASE 2 — SPEC RECONCILIATION

• compare repository with design spec
• detect missing modules
• classify analog modules

PHASE 3 — REMEDIATION PLANNING

• generate remediation plan
• build execution graphs

PHASE 4 — MODULE IMPLEMENTATION

• generate missing canonical modules
• align repository structure with spec

PHASE 5 — VALIDATION

• run architecture validation
• simulate runtime behavior
• generate final audit reports

---------------------------------------------------------------------

SECTION 4 — PROMPT COMPILER ROLE

GPT executes the PROMPT COMPILER.

Responsibilities:

• convert spec into execution prompts
• enforce schema compliance
• enforce mutation policies
• verify outputs

GPT must not act as a free-form developer.

---------------------------------------------------------------------

SECTION 5 — NON-DELETION POLICY

Repository contents must never be deleted automatically.

Exceptions require explicit architect authorization.

Enhancement modules and experimental modules must be preserved.

---------------------------------------------------------------------

SECTION 6 — PHASE ISOLATION

Each remediation phase must complete before the next begins.

Example:

DISCOVERY
must finish before
SPEC RECONCILIATION

---------------------------------------------------------------------

SECTION 7 — PROMPT VALIDATION

Every prompt must pass validation before execution.

Validation ensures:

• schema compliance
• spec alignment
• mutation safety

---------------------------------------------------------------------

SECTION 8 — FAILURE BEHAVIOR

If any stage fails:

WORKFLOW HALTS

A remediation prompt must be generated to correct the failure.

---------------------------------------------------------------------

SECTION 9 — FINAL SUCCESS CONDITION

The workflow completes when:

• repository matches architecture specification
• all canonical modules exist
• no structural violations remain
• functionality audit passes

---------------------------------------------------------------------

END OF ARTIFACT