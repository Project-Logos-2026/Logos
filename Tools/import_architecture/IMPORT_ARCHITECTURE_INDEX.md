# Import Architecture Toolkit — Index
**Location:** `Tools/import_architecture/`
**Consolidated:** 2026-03-10
**Total Artifacts:** 36 files (35 canonical names; `repair_feasibility.json` had two source copies, preserved as `_facade` / `_cluster` variants)

---

## 1. Dependency Graph Artifacts

Files capturing the full runtime import graph, module topology, and deep analysis outputs.

| File | Description |
|------|-------------|
| `runtime_dependency_graph.json` | Full dependency graph in JSON adjacency format |
| `runtime_dependency_graph.dot` | GraphViz DOT source for the dependency graph |
| `runtime_dependency_graph.png` | Rendered PNG visualization of the dependency graph |
| `runtime_directory_tree.json` | Directory tree snapshot used during graph construction |
| `runtime_imports.json` | Raw import records extracted from all scanned Python files |
| `runtime_python_files.json` | Inventory of all Python files included in the analysis |
| `runtime_symbol_imports.json` | Per-symbol import resolution table |
| `runtime_deep_import_violations.json` | Deep violations — imports crossing forbidden architectural boundaries |
| `runtime_surface_modules.json` | Modules designated as surface/facade entry-points |
| `runtime_topology_report.md` | Human-readable topology summary and violation narrative |

**Source directory:** `ARCHON_RUNTIME_ANALYSIS/`

---

## 2. Cluster Analysis

Files produced by the architectural clustering pass — module grouping, membership, and boundary detection.

| File | Description |
|------|-------------|
| `cluster_map.json` | Mapping of modules to cluster identifiers |
| `cluster_summary.json` | Per-cluster statistics: size, cohesion, coupling |
| `cluster_dependency_graph.json` | Inter-cluster dependency graph |
| `cluster_membership.json` | Full module → cluster membership table |
| `cluster_boundary_violations.json` | Edges that cross cluster boundaries illegally |
| `repair_feasibility_cluster.json` | Repair feasibility assessment (cluster analysis version) |

**Source directories:** `Runtime_Facade_Synthesis/`, `_Reports/Runtime_Cluster_Analysis/`

---

## 3. Facade Synthesis

Files produced by the facade surface synthesis pass — defining the allowed public surface for each cluster.

| File | Description |
|------|-------------|
| `facade_map.json` | Cluster → facade module mapping |
| `facade_surface_spec.json` | Specification of allowed symbols per facade surface |
| `import_rewrite_table.json` | Rewrite rules: old import path → facade-compliant path |
| `auto_repair_plan.md` | Automated repair plan generated from the rewrite table |
| `repair_feasibility_facade.json` | Repair feasibility assessment (facade synthesis version) |

**Source directory:** `Runtime_Facade_Synthesis/`

---

## 4. Import Rewrite Tables

Files providing the canonical mapping from current imports to architecture-compliant imports.

| File | Description |
|------|-------------|
| `import_rewrite_table.json` | Primary rewrite table — direct import path substitutions |
| `facade_rewrite_summary.json` | Summary of symbols rewritten in the facade rewrite pass |
| `facade_rewrite_changes.json` | File-by-file change list from the facade rewrite pass |

**Source directories:** `Runtime_Facade_Synthesis/`, `Reports/Facade_Rewrite_Pass/`

---

## 5. Architecture Validation

Files produced by the formal architecture verification pass.

| File | Description |
|------|-------------|
| `architecture_dependency_graph.json` | Post-rewrite architecture-level dependency graph |
| `architecture_edge_classification.json` | Classification of every edge: ALLOWED / VIOLATION / INTERNAL |
| `architecture_metrics.json` | Metrics: DIRECT_CROSS_CLUSTER count, coupling scores, etc. |
| `architecture_validation_report.md` | Formal validation report with pass/fail adjudication |
| `boundary_violation_report.json` | All remaining boundary violations post-rewrite |

**Source directory:** `Reports/Architecture_Verification/`

---

## 6. Repair Pass Logs

Logs and diffs from boundary repair and facade rewrite execution passes.

| File | Description |
|------|-------------|
| `boundary_repair_summary.json` | Summary: files touched, violations resolved, errors |
| `boundary_repair_changes.json` | File-by-file change list from the boundary repair pass |
| `boundary_repair_diff.patch` | Unified diff of all boundary repair changes |
| `boundary_repair_validation.json` | Post-repair validation results |
| `boundary_repair_report.md` | Human-readable boundary repair execution report |
| `facade_rewrite_validation.json` | Post-rewrite validation results |
| `facade_rewrite_diff.patch` | Unified diff of all facade rewrite changes |
| `facade_rewrite_report.md` | Human-readable facade rewrite execution report |

**Source directories:** `Reports/Boundary_Repair/`, `Reports/Facade_Rewrite_Pass/`

---

## Canonical Workflow Order

```
runtime_python_files.json
  └─ runtime_imports.json
       └─ runtime_dependency_graph.*
            ├─ runtime_surface_modules.json
            ├─ runtime_deep_import_violations.json
            └─ cluster_map.json / cluster_membership.json
                 ├─ cluster_summary.json
                 ├─ cluster_dependency_graph.json
                 ├─ cluster_boundary_violations.json
                 ├─ facade_map.json / facade_surface_spec.json
                 │    ├─ import_rewrite_table.json
                 │    └─ auto_repair_plan.md
                 ├─ boundary_repair_* (repair pass)
                 ├─ facade_rewrite_* (rewrite pass)
                 └─ architecture_* (validation)
```
