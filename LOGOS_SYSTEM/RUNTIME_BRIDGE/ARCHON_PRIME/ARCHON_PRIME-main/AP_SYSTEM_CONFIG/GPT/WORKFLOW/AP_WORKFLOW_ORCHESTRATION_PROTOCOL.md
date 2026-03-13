# AP WORKFLOW ORCHESTRATION PROTOCOL

This document defines how the ARCHON PRIME development workflow is orchestrated across platforms.

---

# PLATFORM RESPONSIBILITIES

Architect  
Defines architecture and approves designs.

GPT  
Handles reasoning, prompt engineering, and pipeline coordination.

Claude  
Performs formal specification generation.

VS Code  
Executes prompts and modifies the repository.

---

# WORKFLOW PIPELINE

Architect  
↓  
GPT brainstorming  
↓  
Claude specification design  
↓  
GPT prompt engineering  
↓  
VS Code execution  
↓  
GPT validation and analysis  

---

# ORCHESTRATION RULES

Each stage must complete successfully before the next stage begins.

Prompts must be validated before execution.

Execution results must be analyzed before generating subsequent prompts.

---

# END