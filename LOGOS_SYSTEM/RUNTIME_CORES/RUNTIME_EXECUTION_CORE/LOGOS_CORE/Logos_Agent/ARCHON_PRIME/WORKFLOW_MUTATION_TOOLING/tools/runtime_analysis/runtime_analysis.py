#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-066
# module_name:          runtime_analysis
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/runtime_analysis/runtime_analysis.py
# responsibility:       Analysis module: runtime analysis
# runtime_stage:        validation
# execution_entry:      main
# allowed_targets:      []
# forbidden_targets:    ["SYSTEM", "WORKFLOW_NEXUS"]
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-AP-V2.1]
# implementation_phase: PHASE_2
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate

enforce_runtime_gate()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

"""
ARCHON Runtime Topology Analysis Script
========================================
Analyzes the LOGOS runtime surface directories and produces machine-readable
artifacts for ARCHON normalization and Canonical Import Facade integration.

Analysis-only — no repository mutation.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: runtime_analysis.py
tool_category: Static_Analysis
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python runtime_analysis.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import collections
import json
import os
import sys
from pathlib import Path
from typing import Any

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json

        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


# ── Configuration ─────────────────────────────────────────────────────────────

REPO_ROOT = Path("/workspaces/ARCHON_PRIME")

RUNTIME_DIRS = [
    REPO_ROOT / "LOGOS_SYSTEM",
    REPO_ROOT / "STARTUP",
    REPO_ROOT / "DOCUMENTS",
    REPO_ROOT / "BLUEPRINTS",
    REPO_ROOT / "_Governance",
]

OUTPUT_DIR = REPO_ROOT / "ARCHON_RUNTIME_ANALYSIS"

EXCLUDED_SEGMENTS = {
    "ARCHIVE",
    "ARCHIVES",
    "HISTORY",
    "REPORT",
    "REPORTS",
    "DATA",
    "DATASETS",
    "SNAPSHOT",
    "SNAPSHOTS",
    "EXPORT",
    "EXPORTS",
    "CACHE",
    "CACHE_FILES",
    "TEMP",
    "TMP",
    "LOG",
    "LOGS",
    "BUILD",
    "DIST",
    "VENV",
    ".VENV",
    "__pycache__",
}


# ── Helpers ────────────────────────────────────────────────────────────────────


def should_skip(path: Path) -> bool:
    """Return True if any segment of this path matches an excluded keyword."""
    for part in path.parts:
        if part.upper() in EXCLUDED_SEGMENTS:
            return True
    return False


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] Wrote {path.relative_to(REPO_ROOT)}")


def file_to_module_path(file_path: Path) -> str:
    """Convert an absolute file path to a dotted module path relative to REPO_ROOT."""
    try:
        rel = file_path.relative_to(REPO_ROOT)
    except ValueError:
        rel = file_path
    parts = list(rel.parts)
    if parts and parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


# ── STEP 1  —  Directory Tree ──────────────────────────────────────────────────


def build_tree(path: Path) -> dict | None:
    if should_skip(path):
        return None
    if path.is_file():
        return {"path": str(path.relative_to(REPO_ROOT)), "type": "file"}
    children = []
    try:
        for child in sorted(path.iterdir()):
            node = build_tree(child)
            if node is not None:
                children.append(node)
    except PermissionError:
        pass
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "type": "directory",
        "children": children,
    }


def step1_directory_tree() -> None:
    print("\n[STEP 1] Building runtime directory tree …")
    roots = []
    for d in RUNTIME_DIRS:
        if d.exists():
            node = build_tree(d)
            if node:
                roots.append(node)
        else:
            print(f"  [!] Directory not found: {d}")
    tree = {"path": str(REPO_ROOT), "type": "root", "children": roots}
    write_json(OUTPUT_DIR / "runtime_directory_tree.json", tree)


# ── STEP 2  —  Python File Inventory ──────────────────────────────────────────


def collect_python_files() -> list[Path]:
    py_files = []
    for d in RUNTIME_DIRS:
        if not d.exists():
            continue
        for f in d.rglob("*.py"):
            if not should_skip(f):
                py_files.append(f)
    return sorted(py_files)


def step2_python_inventory(py_files: list[Path]) -> None:
    print(f"\n[STEP 2] Inventorying {len(py_files)} Python files …")
    records = []
    for f in py_files:
        module_path = file_to_module_path(f)
        is_init = f.name == "__init__.py"
        # package = parent module path
        parts = module_path.split(".")
        package = ".".join(parts[:-1]) if len(parts) > 1 else ""
        if is_init:
            # __init__ → the package itself
            package = ".".join(parts[:-1]) if len(parts) > 1 else ""
        records.append(
            {
                "module_path": module_path,
                "file_path": str(f.relative_to(REPO_ROOT)),
                "package": package,
                "is_package": is_init,
            }
        )
    write_json(OUTPUT_DIR / "runtime_python_files.json", records)
    print(f"  [i] Total Python files: {len(records)}")


# ── STEP 3 & 4  —  Import Extraction + Symbol Graph ───────────────────────────

PARSE_ERRORS: list[str] = []


def parse_imports(file_path: Path):
    """
    Returns (imports_list, symbol_imports_list) for one file.
    Each entry in imports_list:
        { source_module, import_type, target_module, symbols }
    Each entry in symbol_imports_list:
        { source_module, target_module, symbol }
    """
    source = file_to_module_path(file_path)
    imports = []
    symbol_imports = []

    try:
        source_text = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source_text, filename=str(file_path))
    except SyntaxError as exc:
        PARSE_ERRORS.append(f"{file_path}: SyntaxError: {exc}")
        return [], []
    except Exception as exc:
        PARSE_ERRORS.append(f"{file_path}: {exc}")
        return [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "source_module": source,
                        "import_type": "import",
                        "target_module": alias.name,
                        "symbols": [],
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            target = node.module or ""
            if node.level:  # relative import — prepend package prefix
                parts = source.split(".")
                # go up `level` steps
                base_parts = parts[: max(0, len(parts) - node.level)]
                if target:
                    target = ".".join(base_parts) + "." + target
                else:
                    target = ".".join(base_parts)
            symbols = [alias.name for alias in node.names]
            imports.append(
                {
                    "source_module": source,
                    "import_type": "from",
                    "target_module": target,
                    "symbols": symbols,
                }
            )
            for sym in symbols:
                symbol_imports.append(
                    {
                        "source_module": source,
                        "target_module": target,
                        "symbol": sym,
                    }
                )

    return imports, symbol_imports


def step3_4_imports(py_files: list[Path]):
    print(f"\n[STEP 3/4] Extracting imports from {len(py_files)} files …")
    all_imports = []
    all_symbol_imports = []
    for f in py_files:
        imps, syms = parse_imports(f)
        all_imports.extend(imps)
        all_symbol_imports.extend(syms)

    write_json(OUTPUT_DIR / "runtime_imports.json", all_imports)
    write_json(OUTPUT_DIR / "runtime_symbol_imports.json", all_symbol_imports)

    if PARSE_ERRORS:
        print(f"  [!] Parse errors ({len(PARSE_ERRORS)} files skipped):")
        for e in PARSE_ERRORS[:20]:
            print(f"      {e}")
        if len(PARSE_ERRORS) > 20:
            print(f"      … and {len(PARSE_ERRORS) - 20} more")

    print(f"  [i] Total import edges: {len(all_imports)}")
    print(f"  [i] Total symbol-level imports: {len(all_symbol_imports)}")
    return all_imports, all_symbol_imports


# ── STEP 5  —  Dependency Graph ────────────────────────────────────────────────


def step5_dependency_graph(all_imports: list[dict], py_files: list[Path]) -> dict:
    print("\n[STEP 5] Building dependency graph …")
    # Nodes = all known modules (source + non-stdlib targets within repo)
    known_modules = {file_to_module_path(f) for f in py_files}
    node_set = set(known_modules)

    edges = []
    seen_edges = set()
    for imp in all_imports:
        src = imp["source_module"]
        tgt = imp["target_module"]
        key = (src, tgt)
        if key not in seen_edges:
            seen_edges.add(key)
            edges.append({"from": src, "to": tgt})
            node_set.add(src)
            node_set.add(tgt)

    graph = {"nodes": sorted(node_set), "edges": edges}
    write_json(OUTPUT_DIR / "runtime_dependency_graph.json", graph)
    print(f"  [i] Nodes: {len(node_set)}  Edges: {len(edges)}")
    return graph


# ── STEP 6  —  Runtime Surface Detection ──────────────────────────────────────


def step6_runtime_surfaces(graph: dict, py_files: list[Path]) -> list[dict]:
    print("\n[STEP 6] Computing runtime surface metrics …")
    known_modules = {file_to_module_path(f) for f in py_files}

    in_degree: dict[str, int] = collections.Counter()
    out_degree: dict[str, int] = collections.Counter()

    for edge in graph["edges"]:
        out_degree[edge["from"]] += 1
        in_degree[edge["to"]] += 1

    all_mods = known_modules | set(in_degree.keys()) | set(out_degree.keys())
    total = len(all_mods)

    records: list[dict[str, Any]] = []
    for mod in sorted(all_mods):
        ind = in_degree.get(mod, 0)
        outd = out_degree.get(mod, 0)
        # centrality ≈ harmonic mean of normalised degrees (avoid div-by-zero)
        norm_in = ind / max(total - 1, 1)
        norm_out = outd / max(total - 1, 1)
        if norm_in + norm_out > 0:
            centrality = 2 * norm_in * norm_out / (norm_in + norm_out)
        else:
            centrality = 0.0
        records.append(
            {
                "module": mod,
                "in_degree": ind,
                "out_degree": outd,
                "centrality_score": round(centrality, 6),
            }
        )

    records.sort(
        key=lambda r: (-r["centrality_score"], -r["in_degree"], -r["out_degree"])
    )
    write_json(OUTPUT_DIR / "runtime_surface_modules.json", records)

    top = records[:10]
    print("  [i] Top runtime surface modules (by centrality):")
    for r in top:
        print(
            f"      {r['module'][:80]}  in={r['in_degree']} out={r['out_degree']} c={r['centrality_score']:.4f}"
        )
    return records


# ── STEP 7  —  Deep Import Violations ─────────────────────────────────────────


def import_depth(module: str) -> int:
    """Count number of package separators → depth of the dotted path."""
    return module.count(".")


DEEP_THRESHOLD = 2  # more than 2 separators = depth > 2


def step7_deep_violations(all_imports: list[dict]) -> list[dict]:
    print("\n[STEP 7] Detecting deep import violations …")
    violations = []
    for imp in all_imports:
        tgt = imp["target_module"]
        depth = import_depth(tgt)
        if depth > DEEP_THRESHOLD:
            violations.append(
                {
                    "source_module": imp["source_module"],
                    "illegal_import": tgt,
                    "depth": depth,
                }
            )

    # de-duplicate (same source + target)
    seen = set()
    deduped = []
    for v in violations:
        key = (v["source_module"], v["illegal_import"])
        if key not in seen:
            seen.add(key)
            deduped.append(v)

    deduped.sort(key=lambda v: (-v["depth"], v["illegal_import"]))
    write_json(OUTPUT_DIR / "runtime_deep_import_violations.json", deduped)
    print(f"  [i] Deep import violations: {len(deduped)}")
    return deduped


# ── STEP 8  —  Canonical Facade Candidates ────────────────────────────────────


def guess_facade_namespace(module: str) -> str:
    """Assign a recommended facade namespace based on module path segments."""
    upper = module.upper()
    if "PROTOCOL" in upper or "INTERFACE" in upper:
        return "logos.imports.protocols"
    if "GOVERNANCE" in upper or "_GOVERNANCE" in upper or "GOV" in upper:
        return "logos.imports.governance"
    if "STARTUP" in upper or "BOOT" in upper or "INIT" in upper:
        return "logos.imports.startup"
    if "RUNTIME" in upper or "EXECUTION" in upper or "CORE" in upper:
        return "logos.imports.runtime"
    if "AGENT" in upper or "ORCHES" in upper:
        return "logos.imports.agents"
    if "BLUEPRINT" in upper:
        return "logos.imports.blueprints"
    if "DOCUMENT" in upper:
        return "logos.imports.documents"
    return "logos.imports.runtime"


def step8_facade_candidates(
    surface_modules: list[dict],
    all_symbol_imports: list[dict],
) -> None:
    print("\n[STEP 8] Identifying canonical facade candidates …")

    # Take modules with centrality above median among non-zero entries
    nonzero = [r for r in surface_modules if r["centrality_score"] > 0]
    if nonzero:
        sorted_scores = sorted(r["centrality_score"] for r in nonzero)
        median = sorted_scores[len(sorted_scores) // 2]
    else:
        median = 0.0

    high_centrality = {
        r["module"]
        for r in surface_modules
        if r["centrality_score"] >= median and r["centrality_score"] > 0
    }

    # Gather all symbols imported FROM high-centrality modules
    candidates = []
    seen = set()
    for sym_imp in all_symbol_imports:
        tgt = sym_imp["target_module"]
        sym = sym_imp["symbol"]
        if tgt in high_centrality:
            key = (tgt, sym)
            if key not in seen:
                seen.add(key)
                candidates.append(
                    {
                        "symbol": sym,
                        "source_module": tgt,
                        "recommended_facade": guess_facade_namespace(tgt),
                    }
                )

    candidates.sort(
        key=lambda c: (c["recommended_facade"], c["source_module"], c["symbol"])
    )
    write_json(OUTPUT_DIR / "canonical_facade_candidates.json", candidates)
    print(f"  [i] Canonical facade candidates: {len(candidates)}")


# ── STEP 9  —  Graphviz ────────────────────────────────────────────────────────


def step9_graphviz(graph: dict, surface_modules: list[dict]) -> None:
    print("\n[STEP 9] Generating Graphviz diagram …")

    # For readability cap at top-N modules by centrality
    MAX_NODES = 300
    top_modules = {r["module"] for r in surface_modules[:MAX_NODES]}

    # Filter edges to only those where both ends are in top_modules
    filtered_edges = [
        e for e in graph["edges"] if e["from"] in top_modules and e["to"] in top_modules
    ]

    dot_lines = [
        "digraph LOGOS_Runtime {",
        "  rankdir=LR;",
        '  node [shape=box fontname="Helvetica" fontsize=8];',
        "  edge [fontsize=7];",
    ]

    # Color nodes by facade namespace
    def node_color(mod: str) -> str:
        ns = guess_facade_namespace(mod)
        palette = {
            "logos.imports.runtime": "#AED6F1",
            "logos.imports.protocols": "#A9DFBF",
            "logos.imports.governance": "#F9E79F",
            "logos.imports.startup": "#F0B27A",
            "logos.imports.agents": "#D2B4DE",
            "logos.imports.blueprints": "#FAD7A0",
            "logos.imports.documents": "#D5DBDB",
        }
        return palette.get(ns, "#EAECEE")

    for mod in sorted(top_modules):
        label = mod.split(".")[-1] or mod
        color = node_color(mod)
        safe_id = mod.replace(".", "_").replace("-", "_")
        dot_lines.append(
            f'  "{safe_id}" [label="{label}" fillcolor="{color}" style=filled tooltip="{mod}"];'
        )

    for e in filtered_edges:
        src_id = e["from"].replace(".", "_").replace("-", "_")
        tgt_id = e["to"].replace(".", "_").replace("-", "_")
        dot_lines.append(f'  "{src_id}" -> "{tgt_id}";')

    dot_lines.append("}")
    dot_content = "\n".join(dot_lines)

    dot_path = OUTPUT_DIR / "runtime_dependency_graph.dot"
    dot_path.write_text(dot_content, encoding="utf-8")
    print(f"  [✓] Wrote {dot_path.relative_to(REPO_ROOT)}")

    # Render to PNG using graphviz CLI
    png_path = OUTPUT_DIR / "runtime_dependency_graph.png"
    ret = os.system(f'dot -Tpng "{dot_path}" -o "{png_path}" 2>&1')
    if ret == 0 and png_path.exists():
        print(f"  [✓] Rendered {png_path.relative_to(REPO_ROOT)}")
    else:
        print(f"  [!] Graphviz render failed (exit={ret}). DOT file still available.")
        # Try with neato as fallback
        ret2 = os.system(f'neato -Tpng "{dot_path}" -o "{png_path}" 2>&1')
        if ret2 == 0 and png_path.exists():
            print(f"  [✓] Rendered via neato: {png_path.relative_to(REPO_ROOT)}")
        else:
            # Write a placeholder so artifact list is complete
            png_path.write_bytes(b"")
            print("  [!] Graphviz not available. Empty placeholder written.")


# ── STEP 10  —  Topology Report ───────────────────────────────────────────────


def step10_report(
    py_files: list[Path],
    all_imports: list[dict],
    graph: dict,
    surface_modules: list[dict],
    violations: list[dict],
) -> None:
    print("\n[STEP 10] Writing architecture report …")

    total_files = len(py_files)
    total_edges = len(graph["edges"])
    total_nodes = len(graph["nodes"])

    top10 = surface_modules[:10]

    # Cluster detection — group modules by top-level package
    clusters: collections.Counter[str] = collections.Counter()
    for mod in graph["nodes"]:
        top = mod.split(".")[0] if "." in mod else mod
        clusters[top] += 1
    top_clusters = clusters.most_common(15)

    violation_count = len(violations)

    facade_map: dict[str, list[str]] = collections.defaultdict(list)
    for r in surface_modules[:50]:
        facade_map[guess_facade_namespace(r["module"])].append(r["module"])

    lines = [
        "# LOGOS Runtime Topology Report",
        "",
        f"**Generated:** {__import__('datetime').datetime.utcnow().isoformat()} UTC",
        "",
        "---",
        "",
        "## 1. Summary Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Runtime Python files | {total_files} |",
        f"| Dependency graph nodes | {total_nodes} |",
        f"| Dependency graph edges | {total_edges} |",
        f"| Deep import violations | {violation_count} |",
        f"| Parse errors (skipped) | {len(PARSE_ERRORS)} |",
        "",
        "---",
        "",
        "## 2. Architectural Layers",
        "",
        "The runtime surface is organized into the following top-level layers:",
        "",
        "| Layer | Description |",
        "|-------|-------------|",
        "| `LOGOS_SYSTEM` | Core runtime — execution engines, reasoning protocols, runtime cores |",
        "| `STARTUP` | Boot sequence, proof gates (Coq/PXL), initialization logic |",
        "| `BLUEPRINTS` | Architectural specifications, compliance reports, design artifacts |",
        "| `DOCUMENTS` | System-level documentation and specification files |",
        "| `_Governance` | Governance artifacts, policies, phase locks, authorizations |",
        "",
        "---",
        "",
        "## 3. Top 10 Runtime Surface Modules",
        "",
        "Ranked by centrality score (harmonic mean of normalized in/out degree):",
        "",
        "| Rank | Module | In-Degree | Out-Degree | Centrality |",
        "|------|--------|-----------|------------|------------|",
    ]
    for i, r in enumerate(top10, 1):
        lines.append(
            f"| {i} | `{r['module']}` | {r['in_degree']} | {r['out_degree']} | {r['centrality_score']:.4f} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 4. Largest Dependency Clusters",
        "",
        "| Package Root | Module Count |",
        "|-------------|--------------|",
    ]
    for pkg, count in top_clusters:
        lines.append(f"| `{pkg}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## 5. Deep Import Violations",
        "",
        f"Detected **{violation_count}** imports exceeding 2 package-depth levels.",
        "These represent direct cross-layer dependencies that should be mediated by facade surfaces.",
        "",
    ]
    if violations:
        lines += [
            "### Sample violations (top 20 by depth):",
            "",
            "| Source Module | Target (Illegal Import) | Depth |",
            "|---------------|------------------------|-------|",
        ]
        for v in violations[:20]:
            src = (
                v["source_module"][-60:]
                if len(v["source_module"]) > 60
                else v["source_module"]
            )
            tgt = (
                v["illegal_import"][-80:]
                if len(v["illegal_import"]) > 80
                else v["illegal_import"]
            )
            lines.append(f"| `{src}` | `{tgt}` | {v['depth']} |")

    lines += [
        "",
        "---",
        "",
        "## 6. Recommended Canonical Import Facade Boundaries",
        "",
        "Based on centrality analysis, the following facade namespaces are recommended:",
        "",
    ]
    for facade_ns, mods in sorted(facade_map.items()):
        lines.append(f"### `{facade_ns}`")
        lines.append("")
        for m in mods[:8]:
            lines.append(f"- `{m}`")
        if len(mods) > 8:
            lines.append(f"- _… and {len(mods)-8} more_")
        lines.append("")

    lines += [
        "---",
        "",
        "## 7. Architecture Narrative",
        "",
        "The LOGOS runtime topology is a multi-layer system organized around a central",
        "execution spine (`LOGOS_SYSTEM`) that branches into runtime cores, reasoning",
        "protocol stacks, agent orchestration infrastructure, and governance enforcement.",
        "",
        "**LOGOS_SYSTEM** houses the deepest implementation layers including:",
        "- `RUNTIME_CORES` — execution engines, operation cores, advanced reasoning protocols",
        "- `RUNTIME_OPERATIONS` — task execution, epistemic library, utility services",
        "- `System_Stack` — agent definitions, message bus, RabbitMQ/Redis connectors",
        "",
        "**STARTUP** implements the system's boot sequence including the PXL proof gate",
        "(Coq-verified logic), session initialization, and pre-flight validation.",
        "",
        "**BLUEPRINTS** provides architecture blueprints and compliance reports.",
        "These are design-only artifacts cataloguing the intended system topology.",
        "",
        "**_Governance** enforces behavioral constraints across all layers through",
        "phase lock artifacts, authorization manifests, and semantic projection records.",
        "",
        "The primary architectural risk is **deep cross-layer imports** — direct",
        f"`from X.Y.Z.W import Symbol` patterns create fragile coupling. The {violation_count}",
        "detected violations should be routed through the Canonical Import Facade.",
        "",
        "---",
        "",
        "## 8. Parse Errors",
        "",
    ]
    if PARSE_ERRORS:
        lines.append(f"{len(PARSE_ERRORS)} files could not be parsed:")
        lines.append("")
        for e in PARSE_ERRORS[:30]:
            lines.append(f"- `{e}`")
        if len(PARSE_ERRORS) > 30:
            lines.append(f"- _… and {len(PARSE_ERRORS)-30} more_")
    else:
        lines.append("No parse errors — all runtime Python files parsed successfully.")

    lines += ["", "---", "", "_End of LOGOS Runtime Topology Report_", ""]

    report_path = OUTPUT_DIR / "runtime_topology_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [✓] Wrote {report_path.relative_to(REPO_ROOT)}")


# ── Main ───────────────────────────────────────────────────────────────────────


def main():
    print("=" * 70)
    print("  ARCHON RUNTIME TOPOLOGY ANALYSIS")
    print("  LOGOS Repository — Runtime Surface Only")
    print("=" * 70)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # STEP 1
    step1_directory_tree()

    # STEP 2
    py_files = collect_python_files()
    if not py_files:
        print("\n[FATAL] No Python files found in runtime directories. Halting.")
        sys.exit(1)
    step2_python_inventory(py_files)

    # STEP 3 + 4
    all_imports, all_symbol_imports = step3_4_imports(py_files)
    if not all_imports:
        print("\n[FATAL] No import edges found. Halting.")
        sys.exit(1)

    # STEP 5
    graph = step5_dependency_graph(all_imports, py_files)
    if not graph["nodes"]:
        print("\n[FATAL] Dependency graph is empty. Halting.")
        sys.exit(1)

    # STEP 6
    surface_modules = step6_runtime_surfaces(graph, py_files)

    # STEP 7
    violations = step7_deep_violations(all_imports)

    # STEP 8
    step8_facade_candidates(surface_modules, all_symbol_imports)

    # STEP 9
    step9_graphviz(graph, surface_modules)

    # STEP 10
    step10_report(py_files, all_imports, graph, surface_modules, violations)

    print("\n" + "=" * 70)
    print("  ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"  Runtime Python files  : {len(py_files)}")
    print(f"  Dependency graph nodes: {len(graph['nodes'])}")
    print(f"  Dependency graph edges: {len(graph['edges'])}")
    print(f"  Deep import violations: {len(violations)}")
    print(f"  Parse errors          : {len(PARSE_ERRORS)}")
    print(f"  Output directory      : {OUTPUT_DIR}")
    print("=" * 70)

    # Validation
    ok = True
    if len(py_files) == 0:
        print("[FAIL] Python files detected = 0")
        ok = False
    if len(all_imports) == 0:
        print("[FAIL] Import edges = 0")
        ok = False
    if len(graph["nodes"]) == 0:
        print("[FAIL] Graph nodes = 0")
        ok = False
    png = OUTPUT_DIR / "runtime_dependency_graph.png"
    if not png.exists():
        print("[FAIL] PNG not generated")
        ok = False

    if ok:
        print("\n[VALIDATION] All checks passed.")
    else:
        print("\n[VALIDATION] Some checks failed — see above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
