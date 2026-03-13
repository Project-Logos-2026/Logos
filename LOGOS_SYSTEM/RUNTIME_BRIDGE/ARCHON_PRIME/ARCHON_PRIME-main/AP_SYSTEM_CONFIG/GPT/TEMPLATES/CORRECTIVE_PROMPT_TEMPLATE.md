# Corrective_Prompt_Template

**System:** ARCHON_PRIME  
**Platform:** GPT → VS Code  
**Artifact Type:** Template / Corrective Prompt  
**Status:** Release_Candidate_v2  
**Version:** 2.0.0  

## Template

```text
BEGIN PROMPT

OBJECTIVE:
Correct the specific failure from [Stage / Prior Prompt Identifier].

BACKGROUND:
[What previously succeeded]
[What failed]

SOURCE ARTIFACTS:
- ...

TARGET FILES / TARGET SURFACES:
- ...

FAILURE TO CORRECT:
- ...

ROOT CAUSE:
- [If determinable]

CORRECTION STEPS:
1. ...
2. ...

OUTPUT ARTIFACTS:
- ...

VALIDATION:
1. ...
2. ...

LOGGING / REPORTING:
- ...

END PROMPT
```
