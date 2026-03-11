# ARCHON PRIME — Architecture Validation Report

**Date**: 2026-03-10  
**Mode**: Deterministic Architecture Verification  
**Pass**: Runtime Dependency Rebuild & Boundary Validation  

---

## Executive Summary

| Metric | Value |
|---|---|
| Total Modules Scanned | 1191 |
| Total Import Edges | 2025 |
| Intra-Cluster Edges | 239 |
| Facade Edges (`logos.imports.*`) | 89 |
| Stdlib / External Imports | 1646 |
| **Internal Direct Cross-Cluster** | **51** |
| **Architectural Compliance** | **❌ FAIL** |

> **Architectural Rule**: All cross-cluster imports between internal project modules must  
> route through `logos.imports.*` facade namespaces. Stdlib and third-party imports  
> are explicitly excluded from this governed boundary rule.

---

## Subsystem Boundary Compliance

### Raw Cross-Cluster Breakdown

| Category | Count |
|---|---|
| Total cross-cluster edges (raw) | 1697 |
| → Stdlib / external package imports | 1646 |
| → **Internal project violations** | **51** |

### Internal Violation Cluster Pairs

| Source Cluster | Target Cluster | Count |
|---|---|---|
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` | 19 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` | 7 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Core` | 6 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Cognition_Normalized` | 4 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM` | 3 |
| `LOGOS_SYSTEM` | `Logos_System` | 2 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `DRAC` | 1 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_V1` | 1 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `CONSCIOUS_Modal_Inference_System` | 1 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Logos_Protocol` | 1 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Agent_Resources` | 1 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `I2_Integration` | 1 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Nexus` | 1 |
| `LOGOS_SYSTEM.RUNTIME_BRIDGE` | `Nexus` | 1 |
| `STARTUP` | `LOGOS_SYSTEM` | 1 |
| `_Dev_Resources` | `LOGOS_SYSTEM._Governance` | 1 |

---

## Facade Usage Statistics

| Facade Namespace | Import Count |
|---|---|
| `logos.imports.agents` | 44 |
| `logos.imports.protocols` | 22 |
| `logos.imports.governance` | 14 |
| `logos.imports.runtime` | 6 |
| `logos.imports.startup` | 3 |


### Highest-Centrality Facade Modules (by in-degree)

| Module | In-Degree |
|---|---|
| `logos.imports.agents` | 44 |
| `logos.imports.protocols` | 22 |
| `logos.imports.governance` | 14 |
| `logos.imports.runtime` | 6 |
| `logos.imports.startup` | 3 |


---

## Dependency Density per Cluster

> Density = intra-cluster edges / (n × (n−1)) where n = module count in cluster.

| Cluster | Modules | Intra-Edges | Density |
|---|---|---|---|
| `Agent_Resources` | 1 | 0 | 0.000000 |
| `CONSCIOUS_Modal_Inference_System` | 1 | 0 | 0.000000 |
| `Cognition_Normalized` | 1 | 0 | 0.000000 |
| `DRAC` | 1 | 0 | 0.000000 |
| `I2_Integration` | 1 | 0 | 0.000000 |
| `LOGOS_SYSTEM` | 64 | 11 | 0.002728 |
| `LOGOS_SYSTEM.RUNTIME_BRIDGE` | 34 | 45 | 0.040107 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | 782 | 178 | 0.000291 |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | 118 | 4 | 0.000290 |
| `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` | 3 | 0 | 0.000000 |
| `LOGOS_SYSTEM._Governance` | 1 | 0 | 0.000000 |
| `LOGOS_V1` | 1 | 0 | 0.000000 |
| `Logos_Protocol` | 1 | 0 | 0.000000 |
| `Logos_System` | 1 | 0 | 0.000000 |
| `MTP_Core` | 5 | 0 | 0.000000 |
| `MTP_Nexus` | 1 | 0 | 0.000000 |
| `Nexus` | 1 | 0 | 0.000000 |
| `PYTHON_MODULES` | 10 | 0 | 0.000000 |
| `STARTUP` | 10 | 1 | 0.011111 |
| `_Dev_Resources` | 23 | 0 | 0.000000 |
| `_Governance` | 3 | 0 | 0.000000 |
| `__future__` | 1 | 0 | 0.000000 |
| `aa` | 1 | 0 | 0.000000 |
| `abc` | 1 | 0 | 0.000000 |
| `advanced_fractal_analyzer` | 1 | 0 | 0.000000 |
| `argparse` | 1 | 0 | 0.000000 |
| `ast` | 1 | 0 | 0.000000 |
| `astor` | 1 | 0 | 0.000000 |
| `asyncio` | 1 | 0 | 0.000000 |
| `banach_generator` | 1 | 0 | 0.000000 |
| `base64` | 1 | 0 | 0.000000 |
| `bs4` | 1 | 0 | 0.000000 |
| `burt_module` | 1 | 0 | 0.000000 |
| `causallearn` | 2 | 0 | 0.000000 |
| `cmath` | 1 | 0 | 0.000000 |
| `collections` | 1 | 0 | 0.000000 |
| `concurrent` | 1 | 0 | 0.000000 |
| `contextlib` | 1 | 0 | 0.000000 |
| `copy` | 1 | 0 | 0.000000 |
| `core` | 5 | 0 | 0.000000 |
| `cryptography` | 2 | 0 | 0.000000 |
| `data_c_values` | 1 | 0 | 0.000000 |
| `dataclasses` | 1 | 0 | 0.000000 |
| `datasketch` | 1 | 0 | 0.000000 |
| `datetime` | 1 | 0 | 0.000000 |
| `development_environment` | 1 | 0 | 0.000000 |
| `dual_bijective_commutation_validator` | 1 | 0 | 0.000000 |
| `enum` | 1 | 0 | 0.000000 |
| `fastapi` | 2 | 0 | 0.000000 |
| `flask` | 1 | 0 | 0.000000 |
| `fractal_orbital` | 1 | 0 | 0.000000 |
| `functools` | 1 | 0 | 0.000000 |
| `glob` | 1 | 0 | 0.000000 |
| `gzip` | 1 | 0 | 0.000000 |
| `hashlib` | 1 | 0 | 0.000000 |
| `heapq` | 1 | 0 | 0.000000 |
| `hmac` | 1 | 0 | 0.000000 |
| `http` | 1 | 0 | 0.000000 |
| `iel_engine` | 1 | 0 | 0.000000 |
| `importlib` | 3 | 0 | 0.000000 |
| `inspect` | 1 | 0 | 0.000000 |
| `itertools` | 1 | 0 | 0.000000 |
| `json` | 1 | 0 | 0.000000 |
| `knowledge_catalog` | 1 | 0 | 0.000000 |
| `lambda_logos_core` | 1 | 0 | 0.000000 |
| `logging` | 1 | 0 | 0.000000 |
| `logos` | 5 | 0 | 0.000000 |
| `math` | 1 | 0 | 0.000000 |
| `math_engine` | 1 | 0 | 0.000000 |
| `matplotlib` | 3 | 0 | 0.000000 |
| `modal_inference` | 1 | 0 | 0.000000 |
| `modal_privative_overlays` | 1 | 0 | 0.000000 |
| `modal_verifier` | 1 | 0 | 0.000000 |
| `msgpack` | 1 | 0 | 0.000000 |
| `networkx` | 1 | 0 | 0.000000 |
| `nltk` | 3 | 0 | 0.000000 |
| `numpy` | 1 | 0 | 0.000000 |
| `onto_lattice` | 1 | 0 | 0.000000 |
| `ontological_node_class` | 1 | 0 | 0.000000 |
| `os` | 1 | 0 | 0.000000 |
| `pandas` | 1 | 0 | 0.000000 |
| `pathlib` | 1 | 0 | 0.000000 |
| `pickle` | 1 | 0 | 0.000000 |
| `plugins` | 1 | 0 | 0.000000 |
| `pprint` | 1 | 0 | 0.000000 |
| `principles` | 1 | 0 | 0.000000 |
| `pxl_engine` | 1 | 0 | 0.000000 |
| `pydantic` | 1 | 0 | 0.000000 |
| `pymc` | 1 | 0 | 0.000000 |
| `pytest` | 1 | 0 | 0.000000 |
| `python_file_list` | 1 | 0 | 0.000000 |
| `queue` | 1 | 0 | 0.000000 |
| `random` | 1 | 0 | 0.000000 |
| `re` | 1 | 0 | 0.000000 |
| `requests` | 1 | 0 | 0.000000 |
| `scipy` | 4 | 0 | 0.000000 |
| `secrets` | 1 | 0 | 0.000000 |
| `sentence_transformers` | 1 | 0 | 0.000000 |
| `shutil` | 1 | 0 | 0.000000 |
| `signal` | 1 | 0 | 0.000000 |
| `sklearn` | 5 | 0 | 0.000000 |
| `spacy` | 1 | 0 | 0.000000 |
| `sqlite3` | 1 | 0 | 0.000000 |
| `statistics` | 1 | 0 | 0.000000 |
| `subprocess` | 1 | 0 | 0.000000 |
| `sympy` | 1 | 0 | 0.000000 |
| `sys` | 1 | 0 | 0.000000 |
| `tempfile` | 1 | 0 | 0.000000 |
| `tenacity` | 1 | 0 | 0.000000 |
| `threading` | 1 | 0 | 0.000000 |
| `time` | 1 | 0 | 0.000000 |
| `tools` | 1 | 0 | 0.000000 |
| `torch` | 2 | 0 | 0.000000 |
| `traceback` | 1 | 0 | 0.000000 |
| `types` | 1 | 0 | 0.000000 |
| `typing` | 1 | 0 | 0.000000 |
| `unified_reasoning` | 1 | 0 | 0.000000 |
| `unittest` | 1 | 0 | 0.000000 |
| `uuid` | 1 | 0 | 0.000000 |
| `waitress` | 1 | 0 | 0.000000 |
| `warnings` | 1 | 0 | 0.000000 |
| `your_memory_system` | 1 | 0 | 0.000000 |
| `z3` | 1 | 0 | 0.000000 |
| `zlib` | 1 | 0 | 0.000000 |


---

## Internal Architectural Violations (51) — ❌ FAIL

> These are cross-cluster imports between internal project modules that bypass `logos.imports.*`.
> Stdlib and third-party imports are excluded (see below).

| Source Module | Target Module | Source Cluster | Target Cluster |
|---|---|---|---|
| `LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT.Agent_Invocation.Compliance.tests.test_agent_deployment_safety` | `Logos_System.System_Stack` | `LOGOS_SYSTEM` | `Logos_System` |
| `LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT.Agent_Invocation.Compliance.tests.test_agent_deployment_safety` | `Logos_System.System_Stack` | `LOGOS_SYSTEM` | `Logos_System` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.ORCHESTRATION_AND_ENTRYPOINTS.Canonical_System_Bootstrap_Pipeline` | `PYTHON_MODULES.SEMANTIC_CONTEXTS.Bootstrap_Runtime_Context` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.ORCHESTRATION_AND_ENTRYPOINTS.Canonical_System_Bootstrap_Pipeline` | `PYTHON_MODULES.SEMANTIC_CONTEXTS.Runtime_Mode_Context` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.ORCHESTRATION_AND_ENTRYPOINTS.Canonical_System_Bootstrap_Pipeline` | `PYTHON_MODULES.SEMANTIC_CONTEXTS.Agent_Policy_Decision_Context` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.ORCHESTRATION_AND_ENTRYPOINTS.Canonical_System_Bootstrap_Pipeline` | `PYTHON_MODULES.SEMANTIC_CONTEXTS.Privation_Handling_Context` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.ORCHESTRATION_AND_ENTRYPOINTS.Canonical_System_Bootstrap_Pipeline` | `PYTHON_MODULES.SEMANTIC_CONTEXTS.Trinitarian_Optimization_Context` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Runtime_Mode_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Runtime_Mode_Controller` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Runtime_Mode_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Runtime_Mode_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Trinitarian_Optimization_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Trinitarian_Alignment_Core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Trinitarian_Optimization_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Trinitarian_Optimization_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Bootstrap_Runtime_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Runtime_Context_Initializer` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Bootstrap_Runtime_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Runtime_Mode_Controller` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Bootstrap_Runtime_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Bootstrap_Runtime_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Privation_Handling_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Privation_Handling_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Agent_Policy_Decision_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Invariant_Constraints` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core.DRAC_Invariables.SEMANTIC_CONTEXTS.Agent_Policy_Decision_Context` | `PYTHON_MODULES.SEMANTIC_AXIOMS.Semantic_Capability_Gate` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `PYTHON_MODULES` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Tools.DRAC_Phase_Tracker` | `DRAC.CORE.DRAC_Core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE` | `DRAC` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.MVS_System.MVS_Core.mathematics.fractal_mvs` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.BDN_System.integration.logos_bridge` | `LOGOS_V1.core.verified_core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_V1` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.BDN_System.integration.logos_bridge` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Tools.Integrations.modal_support` | `CONSCIOUS_Modal_Inference_System` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `CONSCIOUS_Modal_Inference_System` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Tools.Recursion_Grounding.Phase_E_Tick_Engine` | `LOGOS_SYSTEM.Governance.exceptions` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Core.Identity_Generator.agent_identity` | `Logos_Protocol.logos_core.world_model` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Logos_Protocol` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Tetra_Conscious.Triune_Fractal_Convergence` | `Cognition_Normalized.Triune_Sierpinski_Core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Cognition_Normalized` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Tools.IEL_Generator.iel_synthesizer` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Tools.IEL_Generator.iel_error_handler` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Tools.IEL_Generator.iel_schema` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.I2_Agent_Tools.semantic_projection_monitor` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.repo_root` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.I2_Agent_Tools.aa` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.repo_root` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.I2_Agent_Core.I2_Triune_Fractal_Binding` | `Cognition_Normalized.Triune_Sierpinski_Core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Cognition_Normalized` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I3_Agent.I3_Agent_Core.I3_Triune_Fractal_Binding` | `Cognition_Normalized.Triune_Sierpinski_Core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Cognition_Normalized` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I3_Agent.I3_Agent_Core.fractal_trinity_engine.fractal_trinity_reasoner` | `Agent_Resources.Cognition_Normalized.Triune_Sierpinski_Core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Agent_Resources` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Agent_Safety_Shims.Memory_Substrate` | `LOGOS_SYSTEM.Agent_Safety_Shims.Capability_Router` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Agent_Safety_Shims.Phase_E_Memory_Substrate` | `LOGOS_SYSTEM.Agent_Safety_Shims.Phase_E_Capability_Router` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `LOGOS_SYSTEM` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.I1_Agent_Core.I1_Triune_Fractal_Binding` | `Cognition_Normalized.Triune_Sierpinski_Core` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `Cognition_Normalized` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core` | `MTP_Core.MTP_Projection_Engine` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Core` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core` | `MTP_Core.MTP_Semantic_Linearizer` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Core` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core` | `MTP_Core.MTP_Fractal_Evaluator` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Core` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core` | `MTP_Core.MTP_Output_Renderer` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Core` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core` | `MTP_Core.MTP_Validation_Gate` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Core` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.I2_Integration` | `I2_Integration.I2_Egress_Critique` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `I2_Integration` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Nexus.MTP_Nexus` | `MTP_Core.MTP_Output_Renderer` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Core` |
| `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Nexus` | `MTP_Nexus.MTP_Nexus` | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE` | `MTP_Nexus` |
| `LOGOS_SYSTEM.RUNTIME_BRIDGE.Bridge_Modules.execution_to_operations_exchanger` | `Nexus` | `LOGOS_SYSTEM.RUNTIME_BRIDGE` | `Nexus` |
| `STARTUP.LOGOS_SYSTEM` | `LOGOS_SYSTEM.System_Entry_Point.System_Entry_Point` | `STARTUP` | `LOGOS_SYSTEM` |
| `_Dev_Resources.scripts.Run_Nexus_Structural_Audit` | `LOGOS_SYSTEM._Governance.Nexus_Validation.Nexus_AST_Validator` | `_Dev_Resources` | `LOGOS_SYSTEM._Governance` |

---

## Artifacts Generated

| File | Description |
|---|---|
| `architecture_dependency_graph.json` | Full module-level dependency graph |
| `architecture_edge_classification.json` | Every edge classified (INTRA / FACADE / STDLIB / DIRECT) |
| `architecture_metrics.json` | Numeric metrics, cluster stats, violation pairs |
| `architecture_validation_report.md` | This report |
| `boundary_violation_report.json` | Internal cross-cluster violation detail |

---

*Generated by ARCHON PRIME — Runtime Dependency Rebuild & Boundary Validation*  
*MODE: Deterministic Architecture Verification | SAFETY: Read-Only / No Repository Mutation*
