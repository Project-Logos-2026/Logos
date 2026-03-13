# AP_PROMPT_SCHEMA

Artifact ID: OPS-PRO-001  
System: ARCHON_PRIME  
Artifact Type: Prompt Contract Specification  
Status: Active

---

## Purpose

Defines the required structure for GPT-derived implementation prompts.

All prompts delivered to the execution agent must conform to this schema.

---

## Required Prompt Sections

PROMPT ID  
SOURCE ARTIFACT  
OBJECTIVE  
BACKGROUND  
TARGET FILES  
CONSTRAINTS  
IMPLEMENTATION STEPS  
VALIDATION STEPS  
OUTPUT ARTIFACTS  
EXIT GATE

---

## Execution Rules

Steps execute sequentially.

The execution agent must not skip steps.

If a step fails:

execution halts  
failure report generated

---

## Schema Validation

Prompts missing required sections are invalid.

The execution agent must report schema violations and refuse execution.