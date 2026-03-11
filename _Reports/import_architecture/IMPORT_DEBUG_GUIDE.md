# Import Debug Guide
**Toolkit Location:** `Tools/import_architecture/`
**Scope:** LOGOS Runtime Architecture — Import Compliance

---

## Architecture Rule

```
DIRECT_CROSS_CLUSTER == 0
```

No module may import directly from a module belonging to a different cluster.
All cross-cluster access must go exclusively through the designated **facade surface** for that cluster.

### What Counts as a Violation

| Scenario | Status |
|----------|--------|
| Module in Cluster A imports from Cluster B's internal module | **VIOLATION** |
| Module in Cluster A imports from Cluster B's facade surface | ALLOWED |
| Module imports within its own cluster | ALLOWED |
| Module imports from `logos.imports.*` | ALLOWED |

Violation evidence is recorded in:
- `cluster_boundary_violations.json` — raw violation edges
- `runtime_deep_import_violations.json` — deep transitive violations
- `boundary_violation_report.json` — post-repair residual violations
- `architecture_edge_classification.json` — full edge classification (ALLOWED / VIOLATION / INTERNAL)

---

## Import Standard

All internal cross-cluster imports must use the facade namespace:

```python
# WRONG — direct internal import across cluster boundary
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.SomeModule import SomeClass

# CORRECT — via facade surface
from logos.imports.some_cluster import SomeClass
```

The canonical rewrite table is:

```
import_rewrite_table.json
```

Each entry maps:

```json
{
  "old_import": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.SomeModule",
  "new_import": "logos.imports.some_cluster",
  "symbol": "SomeClass",
  "cluster": "cluster_03"
}
```

Facade surfaces and their allowed symbols are defined in:

```
facade_surface_spec.json
facade_map.json
```

---

## Repair Workflow

### Step 1 — Regenerate Dependency Graph

Re-scan the codebase and rebuild the import graph:

```
# Outputs:
runtime_python_files.json
runtime_imports.json
runtime_dependency_graph.json
runtime_dependency_graph.dot
```

Then re-derive clusters:

```
# Outputs:
cluster_map.json
cluster_membership.json
cluster_summary.json
cluster_dependency_graph.json
```

### Step 2 — Detect Illegal Imports

Run the boundary violation detector against the updated graph.

Consult:
- `cluster_boundary_violations.json` — direct cluster boundary crossings
- `runtime_deep_import_violations.json` — transitive violations (A → B → C where A and C are in different clusters)
- `boundary_violation_report.json` — summary of all violations with severity

Confirm the metric:

```
architecture_metrics.json → DIRECT_CROSS_CLUSTER
```

Target: `0`

### Step 3 — Consult import_rewrite_table.json

For each violation, look up the offending import path in:

```
import_rewrite_table.json
```

If no entry exists, create one following the schema:

```json
{
  "old_import": "<current.import.path>",
  "new_import": "logos.imports.<cluster_name>",
  "symbol": "<SymbolName>",
  "cluster": "<cluster_id>",
  "facade_module": "<path to facade module>"
}
```

Ensure the target symbol is exported by the cluster's facade surface (`facade_surface_spec.json`).
If not, update the facade surface first.

### Step 4 — Run Facade Rewrite Pass

Apply the rewrite table across the codebase.

Pass outputs:
- `facade_rewrite_changes.json` — files modified
- `facade_rewrite_diff.patch` — unified diff for review
- `facade_rewrite_validation.json` — post-pass validation
- `facade_rewrite_report.md` — summary

After the pass completes:

1. Re-run architecture validation → `architecture_validation_report.md`
2. Verify `DIRECT_CROSS_CLUSTER == 0` in `architecture_metrics.json`
3. Confirm `boundary_violation_report.json` shows no remaining critical violations

---

## Quick Reference: Files by Debugging Phase

| Debugging Phase | Files to Consult |
|-----------------|-----------------|
| Finding violations | `cluster_boundary_violations.json`, `runtime_deep_import_violations.json`, `boundary_violation_report.json` |
| Understanding clusters | `cluster_map.json`, `cluster_membership.json`, `cluster_summary.json` |
| Finding rewrite path | `import_rewrite_table.json`, `facade_surface_spec.json`, `facade_map.json` |
| Reviewing past repairs | `boundary_repair_report.md`, `boundary_repair_diff.patch`, `facade_rewrite_report.md` |
| Validating conformance | `architecture_metrics.json`, `architecture_validation_report.md`, `architecture_edge_classification.json` |

---

## Governance Note

Import compliance is a **governance-enforced constraint** under the LOGOS architecture model.  
Violations resolved through this workflow must have a corresponding repair record in the Repair Pass Logs.  
Any facade surface extension (adding symbols to `facade_surface_spec.json`) requires a governance artifact update under `_Governance/`.
