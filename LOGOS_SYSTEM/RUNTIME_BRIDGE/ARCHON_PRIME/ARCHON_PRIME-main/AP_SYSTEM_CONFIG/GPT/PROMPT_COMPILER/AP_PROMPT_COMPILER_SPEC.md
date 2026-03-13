# ARCHON PRIME — PROMPT COMPILER SPECIFICATION

## Purpose

Define the deterministic translation process from Design Spec → Implementation Guide → VS Code Execution Prompt.

GPT operates as a **Prompt Compiler**, not a free-form developer.

---

# Pipeline

Design Spec  
↓  
Implementation Guide  
↓  
Prompt Compiler  
↓  
Prompt Artifact  
↓  
VS Code Executor  

---

# Compiler Responsibilities

1. Parse Design Spec modules
2. Parse Implementation Guide operations
3. Map modules to canonical paths
4. Generate deterministic execution prompts
5. Enforce mutation policies
6. Attach validation gates

---

# Compiler Constraints

Prompts MUST:

• reference a spec section  
• define mutation scope  
• list deterministic operations  
• define expected outputs  
• include validation steps  

Prompts MUST NOT:

• introduce modules not defined in spec  
• delete files unless explicitly authorized  
• perform speculative enhancements  

---

# Compiler Output

Each prompt must conform to:

AP_PROMPT_SCHEMA_V1

---

# Enhancement Governance

Enhancements cannot modify prompts directly.

Required sequence:

Enhancement Proposal  
→ Spec Update  
→ Implementation Guide Update  
→ Prompt Regeneration  

---

# Validation Stage

Before execution every prompt must pass:

1. Prompt schema validation
2. Spec-reference verification
3. Mutation policy compliance