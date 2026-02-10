# Template Authoring Brief (For External AI Assistants)

## Purpose
You are assisting with Phase 5 of the LOGOS System.
Your task is to draft language templates, not logic.

## What You Are Writing
- Sentence patterns with slots
- Explanation scaffolding
- Tone variants (technical / declarative / pedagogical)

## What You Are NOT Doing
- Defining meaning
- Explaining logic freely
- Summarizing proofs
- Omitting required information
- Inferring intent

## Template Rules
- Templates must be deterministic
- All information comes from slots
- No optional omissions
- No hedging language
- No creative inference

## Required Template Structure
- Template ID
- Associated Primitive
- Description
- Required Slots
- Allowed Modes

## Example (Conceptual)
TEMPLATE_ASSERTION_RESULT
Slots: subject, claim, justification_ref
Modes: declarative, pedagogical

## Delivery Format
Provide templates as plain text drafts.
Do not assume authority.
Final approval and normalization occur centrally.
