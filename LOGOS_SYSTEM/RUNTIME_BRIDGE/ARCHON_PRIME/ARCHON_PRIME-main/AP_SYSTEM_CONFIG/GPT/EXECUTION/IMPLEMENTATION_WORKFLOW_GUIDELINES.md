# Implementation_Workflow_Guide

**System:** ARCHON_PRIME  
**Platform:** GPT  
**Artifact Type:** Execution Protocol / Implementation Workflow  
**Status:** Release_Candidate_v2  
**Version:** 2.0.0  

## Workflow Spine

```text
Spec / Guide / Audit
    ↓
Architect Approval
    ↓
GPT Source Review
    ↓
Prompt Stage Plan
    ↓
Stage Prompt
    ↓
Execution Result
    ↓
Validation
    ↓
Corrective Prompt If Needed
    ↓
Next Stage
```

## Pre-Prompt Checklist

1. confirm approved governing sources
2. confirm phase allows the work
3. confirm required prerequisites
4. identify governance enforcement points
5. identify relevant repo documents
6. plan one prompt per stage when staged execution is needed

## Stage Rules

1. one prompt per stage unless bundling is explicitly authorized
2. no stage skipping without authorization
3. every stage validates before the next begins
4. failures produce targeted corrective prompts
5. structural failures escalate instead of being patched blindly

## Corrective Prompt Rule

Use `TEMPLATES/Corrective_Prompt_Template.md`.
