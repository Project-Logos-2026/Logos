# Prompt Validation Tool

Script: validate_prompt.py

Purpose:

Ensure all prompts engineered by GPT conform to AP_PROMPT_SCHEMA_V1 before being executed by VS Code.

---

# Validation Steps

1. Load prompt artifact
2. Validate required schema fields
3. Verify spec_reference exists
4. Confirm mutation policy compliance
5. Confirm non_deletion_rule true
6. Verify expected outputs defined

---

# Failure Behavior

If validation fails:

Prompt execution MUST NOT proceed.

---

# Future Extension

Validation may integrate with:

• architecture spec registry  
• module registry  
• subsystem registry