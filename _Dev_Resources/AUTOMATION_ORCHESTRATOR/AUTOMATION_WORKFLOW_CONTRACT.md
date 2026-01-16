# AUTOMATION WORKFLOW CONTRACT (AUTHORITATIVE)

This file is the source-of-truth for automation workflow and file-flow.
It must be printed/read at the start of every batch run.

## Canonical directories
- SRC_ROOT: /workspaces/Logos_System/Logos_System
- AUDIT_SURFACE: /workspaces/Logos_System/_Dev_Resources/LEGACY_SCRIPTS_TO_EXAMINE
- PACKET_ROOT: /workspaces/Logos_System/_Dev_Resources/AUTOMATION_ORCHESTRATOR/END_TO_END_PACKET
- PASS_FINALS: /workspaces/Logos_System/_Dev_Resources/AUTO_NORMAL_FINALS
- FAIL_GROUP: /workspaces/Logos_System/_Dev_Resources/AUTOMATION_FAIL_GROUP
- UNKNOWN_GROUP: /workspaces/Logos_System/_Dev_Resources/AUTOMATION_UNKNOWN_GROUP
- Batch manifests: /workspaces/Logos_System/_Reports/Batch_Manifests

## Hard exclusions (never traverse; never touch)
- /workspaces/Logos_System/Logos_System/System_Entry_Point/Runtime_Compiler
- /workspaces/Logos_System/Logos_System/System_Stack/Advanced_Reasoning_Protocol/iel_domains
- /workspaces/Logos_System/Logos_System/System_Stack/Advanced_Reasoning_Protocol/mathematical_foundations/math_categories

## Global file exclusions (never touch anywhere)
- Coq / Coq-adjacent artifacts (at minimum: .v, .vo, .glob; plus any other blocked Coq build products)

## Phase 0 — Artifact generation (three sweeps)
Sweep 0.1: create PACKET_ROOT/<Type_Cast_Correct_Name>/ for every eligible .py under SRC_ROOT
Sweep 0.2: create <Type_Cast_Correct_Name>.json (schema-valid) per packet dir
Sweep 0.3: create test_<Type_Cast_Correct_Name>.py per packet dir

## Batch Collector — scheduling + staging only
- Reads/prints this contract at start of every run; stamps contract hash in manifest
- Selects up to N eligible .py files under SRC_ROOT (excluding deny dirs + Coq)
- Moves selected scripts into AUDIT_SURFACE
- Emits manifest under _Reports/Batch_Manifests
- Does not run audits/rewrites/tests

## Orchestrator — processing only on AUDIT_SURFACE
Phase 1–4: evidence-only audits; append diagnostics (line/char_start/char_end/error_type) to packet JSON
Phase 5: rewrite attempt 1 (GPT hook); MUST consult Abbreviations.json; enforce header and canonical abbreviation usage
Phase 6: semantic audit (attempt 1 only): naming, header, abbreviations correctness
Phase 7: re-audit (1–4) + tests; seal JSON; PASS→PASS_FINALS; else attempt 2
Phase 5b: targeted rewrite attempt 2 (GPT hook; diagnostics-only lines; no semantic normalize)
Phase 7b: re-audit (1–4) + tests if pass; else route FAIL/UNKNOWN; seal JSON

## Terminal states + shipping
- PASS packets only → AUTO_NORMAL_FINALS
- FAIL → AUTOMATION_FAIL_GROUP
- UNKNOWN → AUTOMATION_UNKNOWN_GROUP
