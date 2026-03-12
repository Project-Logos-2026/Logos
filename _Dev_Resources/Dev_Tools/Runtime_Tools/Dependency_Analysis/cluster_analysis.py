#!/usr/bin/env python3
"""
ARCHON Runtime Dependency Graph Clustering Analysis
====================================================
Ingests LOGOS runtime topology artifacts and performs:
  1. Louvain community detection
  2. Strongly connected component detection
  3. Betweenness centrality (bridge module identification)
  4. Cluster boundary & density analysis
  5. Cross-cluster deep-import violation classification
  6. Facade candidate identification
  7. Deterministic repair feasibility assessment

Analysis only — no repository mutation.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: cluster_analysis.py
tool_category: Dependency_Analysis
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python cluster_analysis.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import collections
import json
import math
import sys
from pathlib import Path
from datetime import datetime, timezone

# ── Paths ──────────────────────────────────────────────────────────────────────

REPO_ROOT = Path("/workspaces/Logos")

# Source artifacts (from previous topology analysis pass)
ARTIFACT_DIR = REPO_ROOT / "ARCHON_RUNTIME_ANALYSIS"

SOURCES = {
    "dependency_graph":    ARTIFACT_DIR / "runtime_dependency_graph.json",
    "symbol_imports":      ARTIFACT_DIR / "runtime_symbol_imports.json",
    "surface_modules":     ARTIFACT_DIR / "runtime_surface_modules.json",
    "deep_violations":     ARTIFACT_DIR / "runtime_deep_import_violations.json",
}

OUTPUT_DIR = REPO_ROOT / "_Reports" / "Runtime_Cluster_Analysis"

# ── Imports ────────────────────────────────────────────────────────────────────

try:
    import networkx as nx
    from networkx.algorithms.community import louvain_communities
except ImportError as exc:
    print(f"[FATAL] Missing dependency: {exc}")
    print("        Install with: pip install networkx")
    sys.exit(1)


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_json(path: Path, label: str) -> object:
    if not path.exists():
        print(f"[FATAL] Artifact missing: {label} — expected at {path}")
        sys.exit(1)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: object) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {path.relative_to(REPO_ROOT)}")


def top_level_package(module: str) -> str:
    return module.split(".")[0] if module else "unknown"


def guess_layer(module: str) -> str:
    """Map a module to a high-level architectural layer label."""
    upper = module.upper()
    if "LOGOS_SYSTEM" in upper:
        if "RUNTIME_BRIDGE" in upper or "RGE" in upper:
            return "Runtime Bridge"
        if "RUNTIME_CORES" in upper or "RUNTIME_CORE" in upper:
            if "EXECUTION" in upper:
                return "Execution Core"
            if "OPPERATIONS" in upper or "OPERATIONS" in upper:
                return "Operations Core"
            return "Runtime Cores"
        if "RUNTIME_SHARED" in upper or "SHARED_UTILS" in upper:
            return "Shared Utilities"
        if "SYSTEM_STACK" in upper or "AGENTS" in upper:
            return "Agent Stack"
        if "_GOVERNANCE" in upper or "GOV" in upper:
            return "Governance"
        return "LOGOS_SYSTEM"
    if "STARTUP" in upper:
        return "Startup / Boot"
    if "BLUEPRINT" in upper:
        return "Blueprints"
    if "DOCUMENT" in upper:
        return "Documents"
    if "_GOVERNANCE" in upper or "GOVERNANCE" in upper:
        return "Governance"
    return "External / Stdlib"


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Load Artifacts
# ══════════════════════════════════════════════════════════════════════════════

def load_artifacts():
    print("\n[STEP 1] Loading source artifacts …")
    data = {}
    for key, path in SOURCES.items():
        data[key] = load_json(path, key)
        print(f"  [✓] Loaded {key} ({path.stat().st_size // 1024} KB)")
    return data


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Build Directed Graph
# ══════════════════════════════════════════════════════════════════════════════

def build_graph(dep_graph: dict) -> nx.DiGraph:
    print("\n[STEP 2] Building directed graph …")
    G = nx.DiGraph()
    for node in dep_graph["nodes"]:
        G.add_node(node)
    for edge in dep_graph["edges"]:
        G.add_edge(edge["from"], edge["to"])
    print(f"  [i] Nodes: {G.number_of_nodes()}  Edges: {G.number_of_edges()}")
    return G


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Louvain Community Detection
# ══════════════════════════════════════════════════════════════════════════════

def detect_communities(G: nx.DiGraph) -> dict[str, int]:
    """
    Louvain works on undirected graphs. Convert, detect, then map back to
    cluster IDs sorted deterministically by dominant layer label.
    """
    print("\n[STEP 3] Running Louvain community detection …")
    UG = G.to_undirected()

    # Ensure all nodes are present (isolated nodes survive undirected conversion)
    communities = louvain_communities(UG, seed=42)

    # Sort communities by dominant layer for deterministic labelling
    def dominant_layer(community_set):
        counter = collections.Counter(guess_layer(m) for m in community_set)
        return counter.most_common(1)[0][0]

    sorted_communities = sorted(
        communities,
        key=lambda c: (dominant_layer(c), -len(c)),
    )

    membership: dict[str, int] = {}
    for cluster_id, comm in enumerate(sorted_communities):
        for module in comm:
            membership[module] = cluster_id

    # Assign any graph node not covered (shouldn't happen, but safety net)
    next_id = len(sorted_communities)
    for node in G.nodes():
        if node not in membership:
            membership[node] = next_id
            next_id += 1

    print(f"  [i] Clusters detected: {len(sorted_communities)}")
    return membership, sorted_communities


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Strongly Connected Components
# ══════════════════════════════════════════════════════════════════════════════

def find_sccs(G: nx.DiGraph) -> list[list[str]]:
    print("\n[STEP 4] Finding strongly connected components (SCCs) …")
    sccs = list(nx.strongly_connected_components(G))
    non_trivial = [s for s in sccs if len(s) > 1]
    non_trivial.sort(key=lambda s: -len(s))
    print(f"  [i] SCCs (total): {len(sccs)}  Non-trivial (cyclic): {len(non_trivial)}")
    for i, scc in enumerate(non_trivial[:5]):
        members = sorted(scc)[:3]
        print(f"      SCC-{i} size={len(scc)}  sample={members}")
    return non_trivial


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Betweenness Centrality (Bridge Modules)
# ══════════════════════════════════════════════════════════════════════════════

def compute_betweenness(G: nx.DiGraph) -> dict[str, float]:
    print("\n[STEP 5] Computing betweenness centrality …")
    # Approximate for speed on large graphs (k=min(200, n))
    n = G.number_of_nodes()
    k = min(200, n)
    bc = nx.betweenness_centrality(G, k=k, normalized=True, seed=42)
    top = sorted(bc.items(), key=lambda x: -x[1])[:10]
    print("  [i] Top bridge modules by betweenness:")
    for mod, score in top:
        print(f"      {score:.4f}  {mod[:90]}")
    return bc


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Cluster Boundary & Density Analysis
# ══════════════════════════════════════════════════════════════════════════════

def cluster_boundary_analysis(
    G: nx.DiGraph,
    membership: dict[str, int],
    communities: list,
) -> list[dict]:
    print("\n[STEP 6] Analysing cluster boundaries …")

    num_clusters = len(communities)
    # Pre-build per-cluster node sets as lists of modules
    cluster_modules: dict[int, set] = collections.defaultdict(set)
    for mod, cid in membership.items():
        cluster_modules[cid].add(mod)

    summaries = []
    for cid in range(num_clusters):
        mods = cluster_modules[cid]
        internal = 0
        external_out = 0
        external_in = 0

        for mod in mods:
            for tgt in G.successors(mod):
                if membership.get(tgt) == cid:
                    internal += 1
                else:
                    external_out += 1
            for src in G.predecessors(mod):
                if membership.get(src) != cid:
                    external_in += 1

        n = len(mods)
        possible_internal = n * (n - 1) if n > 1 else 1
        density = internal / possible_internal

        # Dominant layer
        layer_counts: dict[str, int] = collections.Counter(guess_layer(m) for m in mods)
        dominant = layer_counts.most_common(1)[0][0]

        # Top-level packages present
        top_pkgs = sorted({top_level_package(m) for m in mods})

        summaries.append({
            "cluster_id": cid,
            "dominant_layer": dominant,
            "module_count": n,
            "internal_edges": internal,
            "external_edges_out": external_out,
            "external_edges_in": external_in,
            "density": round(density, 6),
            "top_level_packages": top_pkgs,
            "layer_distribution": dict(layer_counts),
        })

    summaries.sort(key=lambda s: -s["module_count"])
    print(f"  [i] Cluster summary computed for {len(summaries)} clusters")
    return summaries


# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — Cluster Dependency Graph (cluster→cluster)
# ══════════════════════════════════════════════════════════════════════════════

def cluster_dependency_graph(
    G: nx.DiGraph,
    membership: dict[str, int],
) -> dict:
    print("\n[STEP 7] Building cluster dependency graph …")
    cluster_edges: dict[tuple[int, int], int] = collections.Counter()
    for src, tgt in G.edges():
        src_c = membership.get(src)
        tgt_c = membership.get(tgt)
        if src_c is not None and tgt_c is not None and src_c != tgt_c:
            cluster_edges[(src_c, tgt_c)] += 1

    edges_list = [
        {"from_cluster": k[0], "to_cluster": k[1], "edge_count": v}
        for k, v in sorted(cluster_edges.items(), key=lambda x: -x[1])
    ]

    # Detect cycles in the cluster graph
    CG = nx.DiGraph()
    for e in edges_list:
        CG.add_edge(e["from_cluster"], e["to_cluster"], weight=e["edge_count"])
    cycles = list(nx.simple_cycles(CG))

    print(f"  [i] Cross-cluster edges: {len(edges_list)}")
    print(f"  [i] Cluster-level cycles: {len(cycles)}")

    return {
        "cluster_nodes": sorted(set(membership.values())),
        "cluster_edges": edges_list,
        "cluster_cycles": [list(c) for c in cycles],
        "is_dag": len(cycles) == 0,
    }


# ══════════════════════════════════════════════════════════════════════════════
# STEP 8 — Cross-Cluster Boundary Violation Classification
# ══════════════════════════════════════════════════════════════════════════════

def classify_violations(
    violations: list[dict],
    membership: dict[str, int],
) -> list[dict]:
    print("\n[STEP 8] Classifying cross-cluster boundary violations …")

    classified = []
    for v in violations:
        src = v["source_module"]
        tgt = v["illegal_import"]
        src_c = membership.get(src)
        tgt_c = membership.get(tgt)

        depth = v["depth"]

        if src_c is None or tgt_c is None:
            classification = "unresolved"
        elif src_c == tgt_c:
            classification = "intra-cluster"
        else:
            classification = "cross-cluster"
            if depth > 4:
                classification = "deep-cross-cluster"

        classified.append({
            "source_module": src,
            "illegal_import": tgt,
            "depth": depth,
            "source_cluster": src_c,
            "target_cluster": tgt_c,
            "classification": classification,
        })

    classified.sort(key=lambda v: (v["classification"], -v["depth"]))

    type_counts: dict[str, int] = collections.Counter(v["classification"] for v in classified)
    print("  [i] Violation classification breakdown:")
    for t, cnt in sorted(type_counts.items()):
        print(f"      {t}: {cnt}")

    return classified


# ══════════════════════════════════════════════════════════════════════════════
# STEP 9 — Facade Candidate Identification
# ══════════════════════════════════════════════════════════════════════════════

def identify_facade_candidates(
    G: nx.DiGraph,
    membership: dict[str, int],
    bc: dict[str, float],
    surface_records: list[dict],
    violations_classified: list[dict],
) -> list[dict]:
    print("\n[STEP 9] Identifying facade candidates …")

    # Build a map: target_module → set of source clusters that import it
    target_source_clusters: dict[str, set[int]] = collections.defaultdict(set)
    for src, tgt in G.edges():
        src_c = membership.get(src)
        tgt_c = membership.get(tgt)
        if src_c is not None and tgt_c is not None and src_c != tgt_c:
            target_source_clusters[tgt].add(src_c)

    # Modules imported from 2+ different clusters are strong candidates
    multi_cluster_imports = {
        mod: clusters
        for mod, clusters in target_source_clusters.items()
        if len(clusters) >= 2
    }

    # Build surface centrality lookup
    surface_lookup = {r["module"]: r for r in surface_records}

    # Collect violation target modules
    violation_targets = {v["illegal_import"] for v in violations_classified
                         if v["classification"] in ("cross-cluster", "deep-cross-cluster")}

    candidates = []
    for mod, importing_clusters in sorted(
        multi_cluster_imports.items(), key=lambda x: -len(x[1])
    ):
        surface = surface_lookup.get(mod, {})
        in_deg = surface.get("in_degree", G.in_degree(mod))
        out_deg = surface.get("out_degree", G.out_degree(mod))
        centrality = surface.get("centrality_score", 0.0)
        betweenness = bc.get(mod, 0.0)
        is_violation_target = mod in violation_targets

        # Recommended facade namespace
        upper = mod.upper()
        if "PROTOCOL" in upper or "INTERFACE" in upper:
            facade_ns = "logos.imports.protocols"
        elif "GOVERNANCE" in upper or "_GOVERNANCE" in upper:
            facade_ns = "logos.imports.governance"
        elif "STARTUP" in upper or "BOOT" in upper:
            facade_ns = "logos.imports.startup"
        elif "RUNTIME" in upper or "EXECUTION" in upper or "CORE" in upper:
            facade_ns = "logos.imports.runtime"
        elif "AGENT" in upper:
            facade_ns = "logos.imports.agents"
        elif "BLUEPRINT" in upper:
            facade_ns = "logos.imports.blueprints"
        else:
            facade_ns = "logos.imports.runtime"

        candidates.append({
            "module": mod,
            "importing_cluster_count": len(importing_clusters),
            "importing_clusters": sorted(importing_clusters),
            "own_cluster": membership.get(mod),
            "in_degree": in_deg,
            "out_degree": out_deg,
            "centrality_score": centrality,
            "betweenness_centrality": round(betweenness, 6),
            "is_violation_target": is_violation_target,
            "recommended_facade_namespace": facade_ns,
        })

    candidates.sort(key=lambda c: (-c["importing_cluster_count"], -c["betweenness_centrality"]))
    print(f"  [i] Facade candidates: {len(candidates)}")
    return candidates


# ══════════════════════════════════════════════════════════════════════════════
# STEP 10 — Repair Feasibility Assessment
# ══════════════════════════════════════════════════════════════════════════════

def repair_feasibility(
    violations_classified: list[dict],
    candidates: list[dict],
    membership: dict[str, int],
) -> dict:
    """
    Assess whether deep imports can be repaired algorithmically.
    Rewrite rule: for each violation where target_cluster has a known facade,
    the import can be rewritten as:
        from <facade_namespace> import <symbol>

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")

    """
    # Build facade map: cluster_id → best facade module
    cluster_facade: dict[int, str] = {}
    for c in candidates:
        cid = c["own_cluster"]
        if cid is not None and cid not in cluster_facade:
            cluster_facade[cid] = c["recommended_facade_namespace"]

    repairable = 0
    not_repairable = 0
    repair_rules = []

    seen = set()
    for v in violations_classified:
        if v["classification"] not in ("cross-cluster", "deep-cross-cluster"):
            continue
        tgt_c = v["target_cluster"]
        facade = cluster_facade.get(tgt_c)
        key = (v["source_module"], v["illegal_import"])
        if key in seen:
            continue
        seen.add(key)

        if facade:
            repairable += 1
            rule = {
                "source_module": v["source_module"],
                "illegal_import": v["illegal_import"],
                "target_cluster": tgt_c,
                "proposed_facade": facade,
                "rewrite_rule": f"replace 'from {v['illegal_import']} import X' with 'from {facade} import X'",
                "feasibility": "AUTO",
            }
        else:
            not_repairable += 1
            rule = {
                "source_module": v["source_module"],
                "illegal_import": v["illegal_import"],
                "target_cluster": tgt_c,
                "proposed_facade": None,
                "rewrite_rule": None,
                "feasibility": "MANUAL — no facade identified for target cluster",
            }
        repair_rules.append(rule)

    return {
        "total_cross_cluster_violations": repairable + not_repairable,
        "auto_repairable": repairable,
        "require_manual_review": not_repairable,
        "repair_rules": repair_rules,
    }


# ══════════════════════════════════════════════════════════════════════════════
# STEP 11 — Write Output Artifacts
# ══════════════════════════════════════════════════════════════════════════════

def write_artifacts(
    membership: dict[str, int],
    cluster_summaries: list[dict],
    cluster_graph: dict,
    violations_classified: list[dict],
    facade_candidates: list[dict],
    sccs: list,
    bc: dict[str, float],
    repair: dict,
) -> None:
    print("\n[STEP 11] Writing output artifacts …")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # cluster_membership.json
    write_json(OUTPUT_DIR / "cluster_membership.json", membership)

    # cluster_summary.json — include SCC info
    non_trivial_scc_mods = set()
    for scc in sccs:
        non_trivial_scc_mods.update(scc)

    enhanced_summaries = []
    for s in cluster_summaries:
        cid = s["cluster_id"]
        # count how many modules in this cluster are in a non-trivial SCC
        s["cyclic_module_count"] = sum(
            1 for mod, c in membership.items()
            if c == cid and mod in non_trivial_scc_mods
        )
        enhanced_summaries.append(s)

    write_json(OUTPUT_DIR / "cluster_summary.json", enhanced_summaries)

    # cluster_dependency_graph.json
    write_json(OUTPUT_DIR / "cluster_dependency_graph.json", cluster_graph)

    # cluster_boundary_violations.json
    write_json(OUTPUT_DIR / "cluster_boundary_violations.json", violations_classified)

    # facade_candidates.json
    write_json(OUTPUT_DIR / "facade_candidates.json", facade_candidates)

    # repair_feasibility.json (bonus — deterministic repair assessment)
    write_json(OUTPUT_DIR / "repair_feasibility.json", repair)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 12 — Architecture Report
# ══════════════════════════════════════════════════════════════════════════════

def write_report(
    G: nx.DiGraph,
    membership: dict[str, int],
    cluster_summaries: list[dict],
    cluster_graph: dict,
    violations_classified: list[dict],
    facade_candidates: list[dict],
    sccs: list,
    bc: dict[str, float],
    repair: dict,
) -> None:
    print("\n[STEP 12] Writing architecture report …")

    num_clusters = len(cluster_summaries)
    cross_cluster_count = sum(
        1 for v in violations_classified
        if v["classification"] in ("cross-cluster", "deep-cross-cluster")
    )
    intra_cluster_count = sum(1 for v in violations_classified if v["classification"] == "intra-cluster")
    total_violations = len(violations_classified)

    top_bc = sorted(bc.items(), key=lambda x: -x[1])[:15]

    lines = [
        "# LOGOS Runtime Cluster Analysis Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()} UTC",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
        f"The LOGOS runtime module graph contains **{G.number_of_nodes()} nodes** and "
        f"**{G.number_of_edges()} edges**. Louvain community detection identified "
        f"**{num_clusters} natural architectural subsystems** (clusters). "
        f"A total of **{total_violations} deep import violations** were classified; "
        f"**{cross_cluster_count}** are cross-cluster boundary violations and "
        f"**{repair['auto_repairable']}** of these are auto-repairable via facade substitution.",
        "",
        "---",
        "",
        "## 2. Cluster Summary",
        "",
        f"| Cluster | Dominant Layer | Modules | Internal Edges | External Out | Density | Cyclic |",
        f"|---------|---------------|---------|---------------|-------------|---------|--------|",
    ]
    for s in cluster_summaries[:30]:
        lines.append(
            f"| {s['cluster_id']} | {s['dominant_layer']} | {s['module_count']} "
            f"| {s['internal_edges']} | {s['external_edges_out']} "
            f"| {s['density']:.4f} | {s['cyclic_module_count']} |"
        )
    if len(cluster_summaries) > 30:
        lines.append(f"| … | … | … | … | … | … | … |")

    lines += [
        "",
        "---",
        "",
        "## 3. Strongly Connected Components (Cycles)",
        "",
        f"Detected **{len(sccs)} non-trivial SCCs** (cyclic dependency cores).",
        "",
        "| SCC | Size | Sample Modules |",
        "|-----|------|----------------|",
    ]
    for i, scc in enumerate(sccs[:10]):
        sample = ", ".join(f"`{m.split('.')[-1]}`" for m in sorted(scc)[:3])
        lines.append(f"| {i} | {len(scc)} | {sample} |")

    lines += [
        "",
        "---",
        "",
        "## 4. Bridge Modules (Betweenness Centrality)",
        "",
        "Modules with high betweenness centrality are architectural bridges — "
        "removing or replacing them would disconnect significant parts of the graph. "
        "These are primary facade candidates.",
        "",
        "| Rank | Module | Betweenness |",
        "|------|--------|-------------|",
    ]
    for i, (mod, score) in enumerate(top_bc, 1):
        short = mod if len(mod) <= 80 else "…" + mod[-78:]
        lines.append(f"| {i} | `{short}` | {score:.4f} |")

    lines += [
        "",
        "---",
        "",
        "## 5. Cluster Dependency Graph",
        "",
        f"Cross-cluster edges: **{len(cluster_graph['cluster_edges'])}**",
        f"Is cluster graph a DAG (cycle-free): **{cluster_graph['is_dag']}**",
    ]
    if cluster_graph["cluster_cycles"]:
        lines += [
            "",
            "### Cluster-level cycles detected:",
            "",
        ]
        for cyc in cluster_graph["cluster_cycles"][:10]:
            lines.append(f"- Clusters: {' → '.join(str(c) for c in cyc)}")

    lines += [
        "",
        "### Top cross-cluster dependency flows:",
        "",
        "| From Cluster | To Cluster | Edge Count |",
        "|-------------|-----------|------------|",
    ]
    for e in cluster_graph["cluster_edges"][:20]:
        lines.append(f"| {e['from_cluster']} | {e['to_cluster']} | {e['edge_count']} |")

    lines += [
        "",
        "---",
        "",
        "## 6. Deep Import Violation Classification",
        "",
        f"Total violations analysed: **{total_violations}**",
        "",
        "| Classification | Count |",
        "|---------------|-------|",
    ]
    type_counts: dict[str, int] = collections.Counter(v["classification"] for v in violations_classified)
    for t, cnt in sorted(type_counts.items()):
        lines.append(f"| `{t}` | {cnt} |")

    lines += [
        "",
        "### Cross-cluster violations (top 20 by depth):",
        "",
        "| Source Module | Illegal Import | Depth | Src Cluster | Tgt Cluster |",
        "|--------------|----------------|-------|-------------|-------------|",
    ]
    cross = [v for v in violations_classified
              if v["classification"] in ("cross-cluster", "deep-cross-cluster")]
    cross_sorted = sorted(cross, key=lambda v: -v["depth"])[:20]
    for v in cross_sorted:
        src = v["source_module"][-50:] if len(v["source_module"]) > 50 else v["source_module"]
        tgt = v["illegal_import"][-60:] if len(v["illegal_import"]) > 60 else v["illegal_import"]
        lines.append(
            f"| `{src}` | `{tgt}` | {v['depth']} "
            f"| {v['source_cluster']} | {v['target_cluster']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 7. Canonical Facade Candidates",
        "",
        f"**{len(facade_candidates)} modules** identified as canonical facade candidates "
        "(imported from 2+ distinct clusters).",
        "",
        "| Module | Importing Clusters | Betweenness | Recommended Facade |",
        "|--------|--------------------|-------------|-------------------|",
    ]
    for c in facade_candidates[:25]:
        short = c["module"] if len(c["module"]) <= 70 else "…" + c["module"][-68:]
        lines.append(
            f"| `{short}` | {c['importing_cluster_count']} "
            f"| {c['betweenness_centrality']:.4f} | `{c['recommended_facade_namespace']}` |"
        )

    lines += [
        "",
        "---",
        "",
        "## 8. Deterministic Repair Feasibility",
        "",
        f"Cross-cluster violations assessed: **{repair['total_cross_cluster_violations']}**",
        f"Auto-repairable via facade substitution: **{repair['auto_repairable']}**",
        f"Require manual review: **{repair['require_manual_review']}**",
        "",
        "### Rewrite Rule",
        "",
        "For each auto-repairable violation, the rewrite rule is:",
        "",
        "```",
        "from <deep.internal.module.path> import Symbol",
        "  ↓",
        "from logos.imports.<layer> import Symbol",
        "```",
        "",
        "This substitution is safe when the facade namespace re-exports the target symbol.",
        "",
        "### Sample Repair Rules:",
        "",
        "| Source | Illegal Import | Proposed Facade |",
        "|--------|---------------|-----------------|",
    ]
    for rule in repair["repair_rules"][:15]:
        src = rule["source_module"][-45:] if len(rule["source_module"]) > 45 else rule["source_module"]
        ill = rule["illegal_import"][-55:] if len(rule["illegal_import"]) > 55 else rule["illegal_import"]
        facade = rule["proposed_facade"] or "MANUAL"
        lines.append(f"| `{src}` | `{ill}` | `{facade}` |")

    lines += [
        "",
        "---",
        "",
        "## 9. Architectural Narrative",
        "",
        "The LOGOS runtime module graph is a **multi-cluster system** where each cluster",
        "represents a natural architectural subsystem. The dominant layers are:",
        "",
        "- **Execution Core** — reasoning engines, protocol stacks (ARP, SCP, MTP, LP)",
        "- **Operations Core** — cognitive state, epistemic library, memory systems",
        "- **Runtime Bridge** — Radial Genesis Engine, telemetry, dispatch infrastructure",
        "- **Shared Utilities** — system_imports, shared constants, utility services",
        "- **Agent Stack** — I2/I3 agents, Logos Core, orchestration",
        "- **Startup / Boot** — PXL proof gate, initialization, pre-flight validation",
        "- **Governance** — phase locks, authorization manifests, compliance enforcement",
        "",
        "**Primary risk:** Cross-cluster deep imports couple subsystems at implementation",
        "depth, preventing safe structural refactoring. The Canonical Import Facade",
        "addresses this by routing all cross-cluster imports through stable namespace",
        "surfaces (`logos.imports.*`).",
        "",
        "**Recommended action:** Install facade shims at the modules identified as",
        "candidates above, then systematically repair violations using the auto-rewrite",
        "rules in `repair_feasibility.json`.",
        "",
        "---",
        "",
        "_End of LOGOS Runtime Cluster Analysis Report_",
        "",
    ]

    report_path = OUTPUT_DIR / "cluster_analysis_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [✓] {report_path.relative_to(REPO_ROOT)}")


# ══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

def validate(
    G: nx.DiGraph,
    membership: dict[str, int],
    cluster_graph: dict,
    violations_classified: list[dict],
) -> bool:
    print("\n[VALIDATION] Running checks …")
    ok = True

    # Every graph node must be in membership
    missing = [n for n in G.nodes() if n not in membership]
    if missing:
        print(f"  [FAIL] {len(missing)} nodes not assigned to any cluster: {missing[:5]}")
        ok = False
    else:
        print(f"  [✓] All {G.number_of_nodes()} graph nodes assigned to a cluster")

    # All violations have a classification
    unclassified = [v for v in violations_classified if "classification" not in v]
    if unclassified:
        print(f"  [FAIL] {len(unclassified)} violations lack classification")
        ok = False
    else:
        print(f"  [✓] All {len(violations_classified)} violations classified")

    # Cluster graph cycles documented
    if not cluster_graph["is_dag"]:
        print(f"  [i] Cluster graph has {len(cluster_graph['cluster_cycles'])} cycle(s) — documented in report")
    else:
        print("  [✓] Cluster dependency graph is acyclic (DAG)")

    # All output files exist
    expected_files = [
        "cluster_membership.json",
        "cluster_summary.json",
        "cluster_dependency_graph.json",
        "cluster_boundary_violations.json",
        "facade_candidates.json",
        "cluster_analysis_report.md",
        "repair_feasibility.json",
    ]
    for fname in expected_files:
        p = OUTPUT_DIR / fname
        if not p.exists():
            print(f"  [FAIL] Missing artifact: {fname}")
            ok = False
        else:
            print(f"  [✓] {fname} ({p.stat().st_size // 1024} KB)")

    return ok


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("  ARCHON RUNTIME CLUSTER ANALYSIS")
    print("  LOGOS Repository — Dependency Graph Clustering")
    print("=" * 70)

    # STEP 1
    data = load_artifacts()

    # STEP 2
    G = build_graph(data["dependency_graph"])

    # STEP 3 — Louvain
    membership, communities = detect_communities(G)

    # STEP 4 — SCCs
    sccs = find_sccs(G)

    # STEP 5 — Betweenness
    bc = compute_betweenness(G)

    # STEP 6 — Cluster boundary analysis
    cluster_summaries = cluster_boundary_analysis(G, membership, communities)

    # STEP 7 — Cluster dependency graph
    cluster_graph = cluster_dependency_graph(G, membership)

    # STEP 8 — Cross-cluster violation classification
    violations_classified = classify_violations(data["deep_violations"], membership)

    # STEP 9 — Facade candidates
    facade_candidates = identify_facade_candidates(
        G, membership, bc, data["surface_modules"], violations_classified
    )

    # STEP 10 — Repair feasibility
    repair = repair_feasibility(violations_classified, facade_candidates, membership)

    # STEP 11 — Write artifacts
    write_artifacts(
        membership, cluster_summaries, cluster_graph,
        violations_classified, facade_candidates, sccs, bc, repair,
    )

    # STEP 12 — Report
    write_report(
        G, membership, cluster_summaries, cluster_graph,
        violations_classified, facade_candidates, sccs, bc, repair,
    )

    # VALIDATION
    ok = validate(G, membership, cluster_graph, violations_classified)

    # Summary
    print("\n" + "=" * 70)
    print("  CLUSTER ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"  Clusters detected                : {len(communities)}")
    for s in cluster_summaries[:10]:
        print(f"    Cluster {s['cluster_id']:3d} ({s['dominant_layer']:20s}) — {s['module_count']} modules")
    if len(cluster_summaries) > 10:
        print(f"    … and {len(cluster_summaries) - 10} more clusters")
    print(f"  Cross-cluster import edges       : {len(cluster_graph['cluster_edges'])}")
    cross_viol = sum(1 for v in violations_classified
                     if v["classification"] in ("cross-cluster", "deep-cross-cluster"))
    print(f"  Deep-import violations (cross)   : {cross_viol}")
    print(f"  Auto-repairable                  : {repair['auto_repairable']}")
    print(f"  Facade candidates                : {len(facade_candidates)}")
    print(f"  Output directory                 : {OUTPUT_DIR}")
    print("=" * 70)

    if not ok:
        print("\n[VALIDATION] One or more checks failed. See above.")
        sys.exit(1)
    else:
        print("\n[VALIDATION] All checks passed.")


if __name__ == "__main__":
    main()
