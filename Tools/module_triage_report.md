# ARCHON PRIME — Module Triage Report
**Generated:** 2026-03-10  
**Source:** `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`  
**Destinations:** `Blueprints/reasoning`, `Blueprints/utils`  

---

## Summary

| Metric | Value |
|--------|-------|
| Total Python files scanned | 414 |
| Excluded by rule (test/audit/nexus/boot) | 57 |
| Candidates analyzed | 357 |
| **Reasoning modules extracted** | **220** |
| **Utility modules extracted** | **54** |
| Stub modules deleted | 27 |
| Empty `__init__.py` deleted | 3 |
| Duplicates removed | 27 |
| Total files deleted | 57 |
| `__pycache__` directories removed | 5 |
| `*.pyc` files removed | 0 |
| Unclassified (remaining in source) | 26 |

---

## Reasoning Modules Extracted
**Destination:** `Blueprints/reasoning/`  **Total:** 220

| Module | Lines | Source |
|--------|-------|--------|
| `privation_mathematics.py` | 2374 | `Utilities/privation_mathematics.py` |
| `Memory_State_Persistence.py` | 1734 | `Memory/Memory_State_Persistence.py` |
| `ultima_safety.py` | 1610 | `Utilities/ultima_safety.py` |
| `iel_synthesizer.py` | 1556 | `Agents/iel_synthesizer.py` |
| `integrity_safeguard.py` | 1492 | `Utilities/integrity_safeguard.py` |
| `bayesian_inference.py` | 1355 | `Reasoning/bayesian_inference.py` |
| `logos_bridge.py` | 1254 | `Utilities/logos_bridge.py` |
| `iel_overlay.py` | 1196 | `Agents/iel_overlay.py` |
| `banach_data_nodes.py` | 1174 | `Utilities/banach_data_nodes.py` |
| `iel_schema.py` | 1161 | `Agents/iel_schema.py` |
| _(+210 more — see `reasoning_modules_moved.json`)_ | | |

---

## Utility Modules Extracted
**Destination:** `Blueprints/utils/`  **Total:** 54

| Module | Lines | Source |
|--------|-------|--------|
| `start_agent.py` | 4160 | `Agents/start_agent.py` |
| `logos_agi_adapter.py` | 1346 | `Tooling/logos_agi_adapter.py` |
| `logos_agent_system.py` | 1299 | `Agents/logos_agent_system.py` |
| `logos_gpt_server.py` | 1250 | `Utilities/logos_gpt_server.py` |
| `Memory_Recall_Integration.py` | 1229 | `Memory/Memory_Recall_Integration.py` |
| `iel_registryv1.py` | 906 | `Agents/iel_registryv1.py` |
| `deploy_full_stack.py` | 720 | `Utilities/deploy_full_stack.py` |
| `policy.py` | 632 | `Utilities/policy.py` |
| `logos_mathematical_core.py` | 601 | `Agents/logos_mathematical_core.py` |
| `logos_gpt_chat.py` | 542 | `Utilities/logos_gpt_chat.py` |
| _(+44 more — see `utility_modules_moved.json`)_ | | |

---

## Duplicates Removed
**Total:** 114

| Victim Module | Kept As | Fn Similarity | Line Similarity |
|--------------|---------|--------------|----------------|
| `protocol_integration.py` | `initialize_agent_system.py` | 1.0 | 0.949 |
| `run_cycle_smoke.py` | `run_pipeline_smoke.py` | 1.0 | 0.769 |
| `uwm.py` | `world_model.py` | 1.0 | 1.0 |
| `Temporal_Flow_Analyzer.py` | `bugfix.py` | 1.0 | 0.991 |
| `three_pillars_framework.py` | `three_pillars_alt.py` | 1.0 | 0.943 |
| `Cognition_Wrapper_Memgpt.py` | `Cognition_Wrapper_Micropsi.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Memgpt.py` | `Cognition_Wrapper_Openai.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Pgmpy.py` | `Cognition_Wrapper_Memgpt.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Memgpt.py` | `Cognition_Wrapper_Pydantic.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Sympy.py` | `Cognition_Wrapper_Memgpt.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Memgpt.py` | `NLP_Wrapper_Sentence_Transformers.py` | 0.667 | 0.91 |
| `Cognition_Wrapper_Memgpt.py` | `NLP_Wrapper_Transformers.py` | 0.667 | 0.91 |
| `Cognition_Wrapper_Openai.py` | `Cognition_Wrapper_Micropsi.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Pgmpy.py` | `Cognition_Wrapper_Micropsi.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Micropsi.py` | `Cognition_Wrapper_Pydantic.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Sympy.py` | `Cognition_Wrapper_Micropsi.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Micropsi.py` | `NLP_Wrapper_Sentence_Transformers.py` | 0.667 | 0.91 |
| `Cognition_Wrapper_Micropsi.py` | `NLP_Wrapper_Transformers.py` | 0.667 | 0.91 |
| `Cognition_Wrapper_Pgmpy.py` | `Cognition_Wrapper_Openai.py` | 0.667 | 0.921 |
| `Cognition_Wrapper_Openai.py` | `Cognition_Wrapper_Pydantic.py` | 0.667 | 0.921 |
_+94 more duplicates — see `modules_deleted.json`_

---

## Stub Deletions
**Total:** 30

| Module | Reason |
|--------|--------|
| `__init__.py` | no callables and minimal content |
| `exports.py` | no callables and minimal content |
| `__init__.py` | no callables and minimal content |
| `_init__.py` | only comment lines |
| `analogical_reasoning_engine.py` | only comment lines |
| `counterfactual_engine.py` | only comment lines |
| `counterfactual_reasoning_engine.py` | only comment lines |
| `deductive_reasoning_engine.py` | only comment lines |
| `ethical_engine.py` | only comment lines |
| `ethical_reasoning_engine.py` | only comment lines |
| `game_theoretic_engine.py` | only comment lines |
| `game_theoretic_reasoning_engine.py` | only comment lines |
| `heuristic_engine.py` | only comment lines |
| `heuristic_reasoning_engine.py` | only comment lines |
| `inductive_engine.py` | only comment lines |
| `inductive_reasoning_engine.py` | only comment lines |
| `meta_engine.py` | only comment lines |
| `meta_reasoning_engine.py` | only comment lines |
| `modal_engine.py` | only comment lines |
| `modal_reasoning_engine.py` | only comment lines |
| `optimization_engine.py` | only comment lines |
| `optimization_reasoning_engine.py` | only comment lines |
| `temporal_reasoning_engine.py` | only comment lines |
| `topological_engine.py` | only comment lines |
| `__init__.py` | no callables and minimal content |
| `lambda_engine_definitions.py` | all 35 function(s) are stub bodies (pass/NotImplementedError) |
| `trinity_vectors.py` | no callables and minimal content |
| `__init__.py` | empty __init__.py |
| `__init__.py` | empty __init__.py |
| `__init__.py` | empty __init__.py |

---

## Output Artifacts

| File | Description |
|------|-------------|
| `Tools/module_extraction_summary.json` | Aggregate metrics |
| `Tools/reasoning_modules_moved.json` | All reasoning modules with source/dest paths |
| `Tools/utility_modules_moved.json` | All utility modules with source/dest paths |
| `Tools/modules_deleted.json` | All deleted files with deletion reason |
| `Tools/module_triage_report.md` | This report |

---

## Governance Note

No changes were made to the live runtime stack (`LOGOS_SYSTEM/`, `STARTUP/`).  
All operations were scoped to `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`.  
Extracted modules in `Blueprints/reasoning/` and `Blueprints/utils/` are candidates;
integration into live subsystems requires a separate governance-approved pass.