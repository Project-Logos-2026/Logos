ARCHON_PRIME — PROMPT ENGINEERING GUIDELINES

STATUS: CANONICAL
ROLE: GPT PROMPT COMPILER
MODE: DETERMINISTIC / FAIL-CLOSED

---------------------------------------------------------------------

SECTION 1 — PURPOSE

These guidelines define how GPT converts ARCHON PRIME
architecture specifications into deterministic VS Code prompts.

Prompt engineering is treated as a compilation process.

GPT must not improvise implementations.

---------------------------------------------------------------------

SECTION 2 — PROMPT GENERATION PIPELINE

Prompt generation follows this pipeline:

DESIGN_SPEC
→ IMPLEMENTATION_GUIDE
→ PROMPT_COMPILATION
→ SCHEMA_VALIDATION
→ VS_CODE_EXECUTION

Each stage must complete before the next begins.

---------------------------------------------------------------------

SECTION 3 — PROMPT STRUCTURE

All prompts must conform to:

AP_PROMPT_SCHEMA_V1

Required prompt sections:

OBJECTIVE  
TARGET_SCOPE  
OPERATION_SEQUENCE  
MUTATION_POLICY  
EXPECTED_OUTPUTS  
VALIDATION_STEPS  

Prompts missing required sections are invalid.

---------------------------------------------------------------------

SECTION 4 — SPEC AUTHORITY

Prompts must reference architecture specification sections.

If a requested operation is not defined in the specification:

GPT must refuse execution.

Spec authority hierarchy:

ARCHITECT DIRECTIVE
> DESIGN SPEC
> IMPLEMENTATION GUIDE
> PROMPT ENGINEERING

---------------------------------------------------------------------

SECTION 5 — MODULE GENERATION RULES

When generating modules GPT must:

• use canonical module names
• place modules in canonical paths
• respect subsystem boundaries
• avoid duplicate implementations

Analog modules must not be introduced.

---------------------------------------------------------------------

SECTION 6 — NON-SPEC MODULE PRESERVATION

ARCHON PRIME remediation must preserve
all non-spec modules.

Non-spec modules may not be deleted or altered
unless explicitly authorized.

---------------------------------------------------------------------

SECTION 7 — PROMPT OPERATION SEQUENCING

Operations must be deterministic.

Example sequence:

1 REPOSITORY ANALYSIS  
2 STRUCTURAL VALIDATION  
3 MODULE GENERATION  
4 GOVERNANCE VALIDATION  
5 REPORT GENERATION  

Operation order must not change.

---------------------------------------------------------------------

SECTION 8 — PROMPT REGISTRY

Prompts must correspond to registered prompt types
defined in:

PROMPT_REGISTRY.json

Prompt types include:

REPO_SCAN  
SPEC_DIFF_ANALYSIS  
MODULE_GENERATION  
ARCHITECTURE_VALIDATION  

Prompts outside the registry require architect approval.

---------------------------------------------------------------------

SECTION 9 — VALIDATION REQUIREMENT

All prompts must pass:

VALIDATE_PROMPT_SPEC

If validation fails the prompt must be regenerated.

---------------------------------------------------------------------

SECTION 10 — ENHANCEMENT CONTROL

Enhancements must never be embedded in prompts.

Enhancement flow:

ENHANCEMENT_PROPOSAL
→ SPEC_UPDATE
→ IMPLEMENTATION_GUIDE_UPDATE
→ PROMPT_UPDATE

---------------------------------------------------------------------

END OF ARTIFACT