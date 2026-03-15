# ARCHON PRIME IMPORT GRAPH
**Generated:** 2026-03-13  
**Audit Tool:** grep-based static extraction + runtime_analysis.py  
**Target:** `LOGOS_SYSTEM/RUNTIME_BRIDGE/ARCHON_PRIME/ARCHON_PRIME-main/WORKFLOW_MUTATION_TOOLING`  

---

## 1. Import Surface Overview

All imports were extracted from AP's 88 Python files in `WORKFLOW_MUTATION_TOOLING/`. Imports fall into four categories:

| Category | Examples | Count (approx) |
|----------|---------|----------------|
| Standard library | json, os, sys, ast, pathlib, argparse, re, hashlib, importlib, logging, datetime, collections | ~30 unique |
| Internal AP (relative bare) | `from controllers.config_loader import ConfigLoader`, `from crawler.core.crawl_engine import CrawlEngine` | ~25 unique |
| Internal AP (cross-module) | `import circular_dependency_audit`, `import facade_bypass_audit`, etc. | ~15 unique |
| AP governance gate | `from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate` | 1 (universal) |
| Pre-migration path reference | `from Tools.Scripts.classifier import classify_record` | ~4 unique |
| Test utilities | `import pytest`, `from python_file_list import PYTHON_FILE_LIST` | ~2 |

**No imports from LOGOS_SYSTEM.* namespace were found in any AP module.**

---

## 2. Governance Gate (Universal Dependency)

Every AP controller module carries this import at line 21:

```python
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate
```

This import resolves to:
```
ARCHON_PRIME-main/WORKFLOW_NEXUS/Governance/workflow_gate.py
```

The `enforce_runtime_gate` function is the single governance control point for all AP workflow execution. Every controller (audit, analysis, repair, simulation, crawler, pipeline) is gated through this function.

**LOGOS normalization requirement:** This import path (`WORKFLOW_NEXUS.Governance.workflow_gate`) is an AP-internal namespace that will not resolve from within LOGOS's standard Python path unless AP's working directory is `ARCHON_PRIME-main/`. This is the primary integration blocker for AP import resolution.

---

## 3. Controller Import Graph

```
pipeline_controller.py
  ├── WORKFLOW_NEXUS.Governance.workflow_gate → enforce_runtime_gate
  ├── controllers.config_loader → ConfigLoader
  ├── [standard library: importlib, json, os, sys, traceback, datetime, typing]
  └── [dynamically loads: audit_controller, analysis_controller, simulation_controller,
       crawler_controller, repair_controller via importlib]

audit_controller.py
  ├── WORKFLOW_NEXUS.Governance.workflow_gate → enforce_runtime_gate
  ├── controllers.config_loader → ConfigLoader
  └── [standard library: datetime, json, os, sys, traceback, typing]
  └── [os.chdir() to tools/audit_tools/ then invokes tool modules via import]

analysis_controller.py
  ├── WORKFLOW_NEXUS.Governance.workflow_gate → enforce_runtime_gate
  ├── controllers.config_loader → ConfigLoader
  └── [standard library: importlib, json, os, sys, traceback, typing]

repair_controller.py
  ├── WORKFLOW_NEXUS.Governance.workflow_gate → enforce_runtime_gate
  ├── controllers.config_loader → ConfigLoader
  └── [standard library: importlib, json, os, sys, traceback, typing]

simulation_controller.py
  ├── WORKFLOW_NEXUS.Governance.workflow_gate → enforce_runtime_gate
  ├── controllers.config_loader → ConfigLoader
  └── [standard library: importlib, json, os, sys, traceback, typing]

crawler_controller.py
  ├── WORKFLOW_NEXUS.Governance.workflow_gate → enforce_runtime_gate
  ├── controllers.config_loader → ConfigLoader
  ├── crawler.core.crawl_engine → CrawlEngine
  ├── crawler.core.crawl_monitor → CrawlMonitor
  └── crawler.utils.file_scanner → scan_directory, summarize_index

config_loader.py
  ├── WORKFLOW_NEXUS.Governance.workflow_gate → enforce_runtime_gate
  └── [standard library: json, os]
```

---

## 4. Audit Tools Import Graph (tools/audit_tools/)

The audit tools use a distinctive pattern: they import *sibling modules* by bare name (no package prefix), which only resolves when `sys.path` includes the `tools/audit_tools/` directory:

```python
import circular_dependency_audit
import cross_package_dependency_audit
import duplicate_module_audit
import facade_bypass_audit
import file_size_audit
import governance_contract_audit
import governance_coverage_map
import governance_module_audit
import header_schema_audit
import import_surface_audit
import module_path_ambiguity_audit
import namespace_shadow_audit
import orphan_module_audit
import runtime_entry_audit
import symbol_collision_audit
import unused_import_audit
```

These imports are collected in `run_audit_suite.py` and `_run_audit.py`. The pattern requires that `tools/audit_tools/` be on sys.path — this is typically achieved via `os.chdir()` or sys.path injection in the controller.

Additionally:
```python
from audit_utils import generate_id, write_log
```

---

## 5. Semantic Extraction Tools Import Graph (tools/semantic_extraction/)

```
tools/semantic_extraction/extract.py
  ├── from Tools.Scripts.classifier import classify_record     ← PRE-MIGRATION PATH
  ├── from Tools.Scripts.registry_writer import build_entry, write_registry  ← PRE-MIGRATION PATH
  ├── from Tools.Scripts.scanner import collect                ← PRE-MIGRATION PATH
  └── from Tools.Scripts.semantic_extractor import extract_record  ← PRE-MIGRATION PATH

tools/semantic_extraction/legacy_extract.py
  └── from drac_af_extractor.ast_parser import parse_file     ← UNRESOLVED PACKAGE
```

**Critical Finding:** The `semantic_extraction/extract.py` module imports from `Tools.Scripts.*` — a path that does not exist in the current Archon Prime deployment at `ARCHON_PRIME-main/`. This was an upstream path that resolved in the pre-migration environment. These imports will fail at runtime.

`legacy_extract.py` imports from `drac_af_extractor.ast_parser` — also unresolved.

---

## 6. Import Graph Summary — Resolved vs. Unresolved

| Import Category | Status |
|----------------|--------|
| Standard library imports | RESOLVED |
| `WORKFLOW_NEXUS.Governance.workflow_gate` | RESOLVED (if run from ARCHON_PRIME-main/) |
| `controllers.*`, `crawler.*`, `repair.*` etc. (internal bare) | RESOLVED (if sys.path includes WORKFLOW_MUTATION_TOOLING/) |
| `audit_utils`, `config_loader` (bare) | RESOLVED (if sys.path includes tools/audit_tools/) |
| `python_file_list` | RESOLVED (from Dev_Utilities) |
| `Tools.Scripts.*` | **UNRESOLVED** — pre-migration path no longer valid |
| `drac_af_extractor.ast_parser` | **UNRESOLVED** — package not present |
| `LOGOS_SYSTEM.*` | **NOT PRESENT** — AP does not import from LOGOS at all |

---

## 7. Cross-Boundary Import Findings

The execution_core_isolation_audit confirmed:
- **0 violations** — AP does not import from LOGOS execution cores
- **0 LOGOS_SYSTEM imports** — AP is completely isolated from LOGOS

This isolation is **total**: AP knows nothing about LOGOS's SCP, CSP, EMP, DRAC, MSPC, MTP, or RGE namespaces. The DRAC, CSP, EMP, MSPC, and MTP names only appear as target *specifications* in `WORKFLOW_TARGET_PROCESSING/INCOMING_TARGETS/TARGETS/Logos/`, not as live imports.

---

## 8. Import Graph — Notation Legend

```
A → B      Module A imports from module B
A ⤳ B      Module A dynamically loads module B (importlib / os.chdir)
[?] X      Import X is unresolved in current deployment context
```

---

*Report produced by: LOGOS Archon Prime Integration Audit — 2026-03-13*
