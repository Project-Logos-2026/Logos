# AP PROMPT ENVELOPE INTERPRETER

This artifact defines how the VS Code execution environment must interpret prompts received from GPT.

Prompts may contain a workflow metadata envelope.

The execution environment must ignore this metadata.

---

# PROMPT STRUCTURE

Incoming prompts may contain:


AP_WORKFLOW_METADATA
EXECUTION_PROMPT


Example:


=== AP_WORKFLOW_METADATA ===
STATE: PROMPT_ENGINEERING
TARGET_PLATFORM: VSCODE
PROMPT_ID: PROMPT_MOD_021
TRACE: SPEC-004 §3.2
ORIGIN: GPT_PROMPT_COMPILER
TIMESTAMP: 2026-03-09T18:10Z
=== END_AP_WORKFLOW_METADATA ===

=== EXECUTION_PROMPT ===
<execution instructions>
=== END_EXECUTION_PROMPT ===


---

# INTERPRETER BEHAVIOR

When a prompt is received:

1 Detect the metadata envelope.

2 Remove the metadata block.

3 Extract the EXECUTION_PROMPT block.

4 Execute only the content inside EXECUTION_PROMPT.

---

# CRITICAL SAFETY RULE

Workflow metadata must never be:

• written to repository files  
• inserted into generated code  
• included in artifacts  

Metadata is **control-plane information only**.

It exists solely to coordinate the AP workflow pipeline.

---

# END