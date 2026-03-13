# AP SPEC METADATA SCHEMA

This artifact defines optional metadata used when Claude returns design specifications within the ARCHON PRIME workflow.

The metadata allows downstream components to interpret the origin and status of a specification.

---

# SPEC METADATA STRUCTURE


=== AP_SPEC_METADATA ===
STATE:
TARGET_PLATFORM:
SPEC_ID:
TRACE:
ORIGIN:
TIMESTAMP:
=== END_AP_SPEC_METADATA ===


---

# FIELD DEFINITIONS

STATE

Workflow state when the specification was produced.

Example:


STATE: SPECIFICATION


---

TARGET_PLATFORM

Usually:


GPT


because GPT will convert the specification into prompts.

---

SPEC_ID

Identifier for the specification.

Example:


SPEC_004


---

TRACE

Spec lineage reference.

Example:


ARCHON_DESIGN_2026_03


---

ORIGIN

Always:


CLAUDE_SPEC_ENGINE


---

TIMESTAMP

UTC timestamp.

Example:


2026-03-09T18:10Z


---

# PURPOSE

Spec metadata provides:

• spec traceability  
• pipeline coordination  
• prompt compilation context  

without modifying the specification itself.

---

# END