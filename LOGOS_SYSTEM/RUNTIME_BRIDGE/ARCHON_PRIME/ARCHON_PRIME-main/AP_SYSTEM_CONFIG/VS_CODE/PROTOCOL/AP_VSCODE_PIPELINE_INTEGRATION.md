# AP_VSCODE_PIPELINE_INTEGRATION

## Document Identity

System: ARCHON_PRIME  
Artifact Type: Pipeline Integration Specification  
Status: Active

## Purpose

This document defines how the VS Code execution agent integrates into the ARCHON PRIME workflow pipeline.

The execution agent operates as the implementation layer that receives deterministic prompts from GPT and produces repository artifacts.

## Pipeline Chain

Architect Directive  
↓  
GPT Analysis / Audit  
↓  
Claude Architecture Design (SPEC / IMPL artifacts)  
↓  
GPT Prompt Engineering  
↓  
VS Code Execution Agent  
↓  
Execution Summary  
↓  
GPT Analysis of Results  
↓  
Architect Update / Next Directive

## Execution Agent Responsibilities

The execution agent must:

• consume deterministic prompts  
• create or modify repository artifacts only within TARGET FILES  
• validate exit-gate conditions  
• return structured execution summaries

The execution agent must NOT:

• infer architectural decisions  
• modify files outside prompt scope  
• alter governance artifacts without explicit instruction

## Session Initialization

At the start of each execution session the agent must:

1. ingest AP_WORKFLOW_CONTEXT.md
2. ingest EXECUTION_AGENT_ROLE.md
3. produce a readiness report
4. confirm environment readiness before accepting prompts

## Prompt Contract

All prompts must contain the following sections:

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

## Execution Summary

Each execution must return:

Execution Status  
Exit Gate Result  
Created / Modified Files  
Validation Evidence
