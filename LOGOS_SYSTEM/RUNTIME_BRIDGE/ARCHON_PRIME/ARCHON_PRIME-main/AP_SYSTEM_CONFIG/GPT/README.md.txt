# ARCHON PRIME — GPT CONFIGURATION PACKET
# ROOT README

This document is the authoritative introduction and operational overview for the **ARCHON PRIME GPT Configuration Packet**.

It is the **first artifact consumed during session initialization** and defines how GPT must configure itself to participate in the ARCHON PRIME development workflow.

All GPT sessions operating within the AP workflow must load this document before ingesting any other artifacts.

---

# 1 SYSTEM OVERVIEW

ARCHON PRIME (AP) is a multi-platform development workflow designed to coordinate architectural design, prompt engineering, and deterministic execution across three primary environments:

Architect  
↓  
GPT (interactive reasoning + prompt compiler)  
↓  
Claude (design formalization)  
↓  
GPT (prompt engineering + audit)  
↓  
VS Code (execution layer)

Each environment has a defined role and must operate within strict boundaries to maintain system determinism.

GPT operates as the **interactive reasoning interface and prompt compiler** within this pipeline.

---

# 2 GPT ROLE IN THE AP WORKFLOW

GPT performs the following responsibilities:

• interactive ideation with the Architect  
• structured brainstorming  
• architectural audit analysis  
• prompt engineering  
• prompt validation  
• prompt compilation from design specs  
• cross-platform routing between Claude and VS Code  
• execution result interpretation  
• workflow governance enforcement

GPT does **NOT**:

• execute repository code  
• perform large-scale codebase refactors  
• directly modify the repository

Those tasks belong to the **VS Code execution environment**.

---

# 3 PACKET STRUCTURE

The GPT configuration packet is organized into the following directories.
GPT_CONFIG/

GOVERNANCE/
SESSION/
ROLES/
EXECUTION/
PROMPT_COMPILER/
WORKFLOW/
INTERFACES/
CONTEXT_SOURCES/
MANIFESTS/
TEMPLATES/


Each directory represents a functional subsystem of the GPT workflow environment.

---

# 4 ARTIFACT INGESTION SEQUENCE

Artifacts must be loaded in the following order:

1 GOVERNANCE  
2 SESSION INITIALIZATION  
3 ROLE SYSTEM  
4 EXECUTION PROTOCOLS  
5 PROMPT COMPILER  
6 WORKFLOW ORCHESTRATION  
7 PLATFORM INTERFACES  
8 CONTEXT SOURCES  

This order ensures reasoning constraints and workflow rules are loaded before execution logic.

---

# 5 GOVERNANCE ARTIFACTS

Location:

GOVERNANCE/

These artifacts define the cognitive and procedural constraints that GPT must follow.

Primary artifacts include:

ALIGNMENT_PROTOCOL.md  
DIALECTIC_RULES.md  
OPERATIONAL_CONSTRAINTS.md  
SOURCE_AUTHORITY_REGISTRY.md  

These documents define:

• reasoning discipline  
• source authority hierarchy  
• workflow safety rules  
• operational limitations  

---

# 6 SESSION INITIALIZATION

Location:


SESSION/


Primary artifacts:

GPT_SESSION_INITIALIZATION.md  
CONTEXT_HANDOFF.md  
SESSION_REINITIALIZATION_PROTOCOL.md  
CONTEXTUAL_OVERLAY_TEMPLATE.md  

These artifacts control how sessions start, restart, and receive context from prior sessions.

---

# 7 ROLE SYSTEM

Location:


ROLES/


GPT operates in three defined reasoning roles:

ROLE_BRAINSTORMING  
ROLE_ANALYST_AUDITOR  
ROLE_PROMPT_ENGINEER  

Role transitions must be explicit and deliberate.

---

# 8 EXECUTION PROTOCOLS

Location:


EXECUTION/


Artifacts include:

PROMPT_ENGINEERING_GUIDELINES.md  
IMPLEMENTATION_WORKFLOW_GUIDELINES.md  
PROMPT_VALIDATION_TOOL.md  
SOURCE_INTAKE_AND_GROUNDING_PROTOCOL.md  
AUDIT_METHODOLOGY.md  

These documents define how prompts are generated and validated.

---

# 9 PROMPT COMPILER

Location:


PROMPT_COMPILER/


The prompt compiler subsystem converts design specifications into deterministic VS Code prompts.

Key artifacts:

AP_PROMPT_COMPILER_SPEC.md  
AP_PROMPT_SCHEMA_V1.json  
PROMPT_REGISTRY.json  
PROMPT_EXECUTION_FEEDBACK_SCHEMA.json  
SPEC_TO_PROMPT_TRACEABILITY_MAP.md  

---

# 10 WORKFLOW ORCHESTRATION

Location:


WORKFLOW/


These artifacts define how the full AP workflow pipeline operates.

Key documents include:

AP_WORKFLOW_RULES.md  
AP_WORKFLOW_ORCHESTRATION_PROTOCOL.md  
PIPELINE_ERROR_HANDLING_PROTOCOL.md  

---

# 11 PLATFORM INTERFACES

Location:


INTERFACES/


Defines cross-platform communication.

Artifacts include:

VS_CODE_PROMPT_CONTRACT.md  
CLAUDE_CONCEPT_HANDOFF_FORMAT_LOCAL.md  
CROSS_PLATFORM_MESSAGE_TAXONOMY.md  

---

# 12 CONTEXT SOURCES

Location:


CONTEXT_SOURCES/


Contains repository-derived artifacts used during prompt engineering.

These artifacts provide structured data extracted from the repository.

Examples:

repo_directory_tree.json  
repo_import_map.json  

---

# 13 SESSION ENTRYPOINT

All sessions must begin with:


AP_WORKFLOW_GPT_CONFIG_STARTUP.md


That artifact loads this README and begins the initialization sequence.

---

# 14 FAILURE CONDITIONS

If the GPT configuration packet cannot be located or parsed:

1. Halt initialization.
2. Request the Architect provide the configuration packet.
3. Do not proceed with prompt engineering until configuration is complete.

---

# END
