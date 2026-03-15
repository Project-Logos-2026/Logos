SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Runtime_Contract
ARTIFACT_NAME: CRAWLER_ENVELOPE_INTERFACE_CONTRACT
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Context

---------------------------------------------------------------------

PURPOSE

Defines the interface contract between the ARCHON_PRIME crawler engine
and the execution envelope system.

---------------------------------------------------------------------

CONTRACT RULES

The crawler must consume the following from the execution envelope:

1. Execution Plan (EP)
   • phase ordering
   • mutation targets
   • traversal rules

2. Envelope Manifest
   • artifact bundle identity
   • addenda stack
   • execution configuration

3. Validation Rules
   • artifact integrity checks
   • governance compliance rules

---------------------------------------------------------------------

CRAWLER CONSTRAINTS

• The crawler must not self-govern
• The crawler inherits governance from the execution envelope
• The crawler must not mutate artifacts not declared in the EP
• The crawler must halt if manifest validation fails

---------------------------------------------------------------------

ABSTRACTION LAYER

ARCHON GOVERNANCE
      │
Execution Envelope
      │
Prompt Compiler
      │
Crawler Engine
      │
Repository Mutation

The crawler operates at the lowest abstraction layer.
Governance rules are inherited from the envelope, not defined by the crawler.

---------------------------------------------------------------------

FAILURE BEHAVIOR

If envelope consumption fails:

• Crawler must halt immediately
• Log failure event with manifest reference
• Do not begin traversal
