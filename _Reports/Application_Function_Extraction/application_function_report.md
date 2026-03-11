# ARCHON PRIME — Application Function Extraction Report
**Generated:** 2026-03-10  
**Mode:** Semantic-Heuristic Analysis (Read-Only)  

---

## Summary

| Metric | Value |
|--------|-------|
| Total docstrings scanned | 3254 |
| Candidate application functions | 611 |
| Clusters detected | 20 |
| Unclassified entries | 0 |

---

## Target Directories

| Directory | Status |
|-----------|--------|
| `LOGOS_SYSTEM` | SCANNED |
| `STARTUP` | SCANNED |
| `System_Stack` | NOT FOUND — SKIPPED |
| `PYTHON_MODULES` | NOT FOUND — SKIPPED |

---

## Signal Keyword Hit Distribution

| Keyword | Occurrences |
|---------|-------------|
| `infer` | 401 |
| `inject` | 207 |
| `gate` | 54 |
| `apply` | 43 |
| `execute` | 30 |
| `select` | 24 |
| `normalize` | 21 |
| `compose` | 16 |
| `determine` | 14 |
| `resolve` | 10 |
| `translate` | 7 |
| `reconstruct` | 6 |

---

## Top 10 Files by Application Function Density

| File | Count |
|------|-------|
| `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Synthetic_Cognition_Protocol/SCP_Core/MVS_System/MVS_Core/mathematics/privation_mathematics.py` | 11 |
| `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Synthetic_Cognition_Protocol/SCP_Tools/Analysts/pxl_fractal_orbital_analysis.py` | 8 |
| `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Tools/language_modules/translation_engine.py` | 7 |
| `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Synthetic_Cognition_Protocol/SCP_Core/BDN_System/core/banach_data_nodes.py` | 6 |
| `LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Evaluation/Commutation_Balance_Score.py` | 6 |
| `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/engines/taxonomy_aggregator.py` | 5 |
| `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Logos_Agent/Tetra_Conscious/Cognitive_Resistor.py` | 5 |
| `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/I2_Agent/I2_Agent_Core/bridge_principle_operator.py` | 5 |
| `LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Evaluation/Recursion_Coupling_Coherence_Score.py` | 5 |
| `LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Evaluation/Divergence_Metric.py` | 5 |

---

## Cluster Summary

| Cluster | Size | Top Representative Terms |
|---------|------|--------------------------|
| cluster_00 | 359 | none, inferred, provides, logos_system, unknown |
| cluster_01 | 29 | with, outputs, aggregate, formula, engine |
| cluster_02 | 25 | trinity, modal, create, inference, vector |
| cluster_03 | 9 | natural, language, translate, structures, lambda |
| cluster_04 | 29 | apply, expression, operator, expr, args |
| cluster_05 | 10 | payload, input, analysis, never, triunesummary |
| cluster_06 | 24 | not, does, structural, infer, admissibility |
| cluster_07 | 9 | under, that, budget, tick, single |
| cluster_08 | 16 | phase, gate, closed, fail, drac |
| cluster_09 | 6 | iel, resolve, properties, determine, order |
| cluster_10 | 12 | based, select, task, the, concepts |
| cluster_11 | 11 | agent, whether, should, and, determine |
| cluster_12 | 6 | replay, event, reconstruct, action, automatic |
| cluster_13 | 13 | topology, telemetry, commutation, priority, per |
| cluster_14 | 9 | references, genesis_selector_state_machine, override, deterministic, rge |
| cluster_15 | 9 | axiom, system, list, formal, axioms |
| cluster_16 | 11 | domain, each, analysis, cross, iel |
| cluster_17 | 5 | and, output, compile, admitted, pipeline |
| cluster_18 | 9 | telemetrysnapshot, inject, object, triad, from |
| cluster_19 | 10 | the, one, propagation, contract, interface |

---

## Output Artifacts

| File | Description |
|------|-------------|
| `application_function_candidates.json` | All docstrings extracted via AST |
| `application_function_filtered.json` | Heuristic-filtered application function candidates |
| `application_function_embeddings.json` | TF-IDF semantic vectors per candidate |
| `application_function_clusters.json` | Cluster assignment per candidate |
| `application_function_registry.json` | Full DRAC registry with symbol, module, cluster, signature |
| `application_function_report.md` | This report |

---

## Governance Note

This pass is **read-only**. No repository mutations were performed.  
Registry entries are candidates for DRAC classification and require human review before activation.