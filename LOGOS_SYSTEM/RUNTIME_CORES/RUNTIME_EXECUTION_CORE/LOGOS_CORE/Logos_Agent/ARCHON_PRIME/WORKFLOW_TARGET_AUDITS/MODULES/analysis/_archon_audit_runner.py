#!/usr/bin/env python3
"""
ARCHON PRIME — STAGING Recovery Audit Runner
=============================================
Full pipeline: repo mapping, cluster analysis, packet discovery,
module triage, logic extraction, integration candidate analysis.

Target : _Dev_Resources/Processing_Center/STAGING
Output : _Dev_Resources/Reports/ARCHON_DIAGNOSTICS
"""

import ast
import collections
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
REPO_ROOT   = Path("/workspaces/Logos")
STAGING     = REPO_ROOT / "_Dev_Resources/Processing_Center/STAGING"
OUTPUT_ROOT = Path(
    os.environ.get("ARCHON_OUTPUT_ROOT",
                   "/workspaces/Logos/_Dev_Resources/Reports/ARCHON_DIAGNOSTICS")
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# PACKET CLASS SIGNALS  (from packet_discovery.py)
# ---------------------------------------------------------------------------
PACKET_CLASSES = {
    "reasoning": {
        "infer","deduce","abduct","reason","logic","proof","bayesian",
        "modal","deductive","inductive","heuristic","counterfactual",
        "game_theoretic","analogi","pxl_engine","meta_reason",
        "optimization","topological","temporal_reason","categorical",
        "probability","bayesian_inferencer","bayesian_nexus",
        "bayesian_updates","bayesian_recursion","hierarchical_bayes",
        "modal_reasoner","modal_logic","modal_validator","proof_engine",
        "arp_nexus","scp_nexus","uip_nexus","coherence",
    },
    "semantic": {
        "translate","semantic","ontology","ontoprops","meaning","language",
        "nlp","embedding","transformer","mtp","encode","decode","annotation",
        "symbol","mtp_nexus","translation_engine","semantic_transformers",
        "ontology_inducer","commitment_ledger",
    },
    "agent": {
        "agent","identity","consciousness","principal","sign","agentic",
        "axiom","belief","collaboration","coordinator","dispatcher",
        "planning","planner","task_intake","smp","iel","autonomous",
        "agent_nexus","logos_memory","knowledge_catalog","sop_nexus",
        "evaluation_packet","plan_packet","agent_identity",
    },
    "safety": {
        "safety","validate","constraint","ethics","policy","guard","gate",
        "privation","integrity","ultima","coherence","monitor",
        "attestation","etgc","guardrails","reference_monitor","health",
        "privative_policies","safety_formalisms",
    },
    "math": {
        "math","privation_mathematics","banach","fractal","orbital",
        "topology","algebra","geometric","bijection","divergence",
        "symbolic_math","arithmetic","fractal_nexus","orbital_analysis",
        "logos_mathematical_core","dual_bijection","comprehensive_fractal",
        "fractal_orbit","pxl_fractal","pxl_modal_fractal","lambda",
        "lambda_engine","lambda_parser","arithmetic_engine",
    },
    "utility": {
        "schema","config","loader","registry","adapter","parser",
        "serializer","logging","wrapper","helper","tools","utility",
        "utils","constants","types","errors","hashing","router",
        "bridge","causal","class_extrapolator","io_normalizer",
        "iterative_loop","kernel","logos_monitor","regression_checker",
        "development_environment","cycle_ledger","resource_manager",
    },
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def write_json(name: str, data: object) -> Path:
    p = OUTPUT_ROOT / name
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")
    return p


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def extract_imports(path: Path) -> list[str]:
    imports: list[str] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return sorted(set(imports))


def classify_packet_signal(combined: str) -> str:
    best_cls, best_score = "utility", 0
    for cls, signals in PACKET_CLASSES.items():
        score = sum(1 for s in signals if s in combined)
        if score > best_score:
            best_score, best_cls = score, cls
    return best_cls


def classify_from_path_and_content(path: Path) -> str:
    combined = (path.stem + " " + str(path.parent)).lower()
    try:
        combined += " " + path.read_text(encoding="utf-8", errors="replace")[:1000].lower()
    except Exception:
        pass
    return classify_packet_signal(combined)


# ---------------------------------------------------------------------------
# STEP 2 — REPO MAPPER
# ---------------------------------------------------------------------------

def step_repo_mapper():
    print("\n=== STEP 2: REPO MAPPER ===")

    # directory tree
    tree: dict[str, dict] = {}
    for root, dirs, files in os.walk(STAGING):
        rel = os.path.relpath(root, STAGING)
        tree[rel] = {"dirs": sorted(dirs), "files": sorted(files)}
    write_json("repo_directory_tree.json", tree)

    # python files
    py_files = []
    for root, _, files in os.walk(STAGING):
        for f in sorted(files):
            if f.endswith(".py"):
                p = Path(root) / f
                rel = os.path.relpath(p, STAGING)
                py_files.append({
                    "path": rel,
                    "size": p.stat().st_size,
                    "hash": sha256_file(p),
                    "staging_subdir": str(Path(rel).parts[0] if Path(rel).parts else ""),
                })
    write_json("repo_python_files.json", py_files)

    # module index (with imports)
    modules = []
    for finfo in py_files:
        full = STAGING / finfo["path"]
        name = finfo["path"].replace(os.sep, ".").removesuffix(".py")
        imports = extract_imports(full)
        modules.append({
            "module": name,
            "file": finfo["path"],
            "size": finfo["size"],
            "imports": imports,
            "staging_subdir": finfo["staging_subdir"],
        })
    write_json("module_index.json", modules)

    print(f"  Directories: {len(tree)}")
    print(f"  Python files: {len(py_files)}")
    print(f"  Modules indexed: {len(modules)}")
    return modules


# ---------------------------------------------------------------------------
# STEP 3 — CLUSTER ANALYSIS
# ---------------------------------------------------------------------------

def step_cluster_analysis(modules: list[dict]):
    print("\n=== STEP 3: CLUSTER ANALYSIS ===")

    # Build directed graph: module stem → [imported stems]
    stem_map = {Path(m["file"]).stem.lower(): m["module"] for m in modules}
    G = nx.DiGraph()
    for m in modules:
        G.add_node(m["module"])

    for m in modules:
        for imp in m["imports"]:
            parts = imp.replace("-", "_").split(".")
            for candidate in [parts[-1].lower(), parts[0].lower()]:
                if candidate in stem_map:
                    tgt = stem_map[candidate]
                    if tgt != m["module"]:
                        G.add_edge(m["module"], tgt)
                    break

    print(f"  Nodes: {G.number_of_nodes()}  Edges: {G.number_of_edges()}")

    # Louvain community detection (undirected)
    UG = G.to_undirected()
    try:
        from networkx.algorithms.community import louvain_communities
        communities = louvain_communities(UG, seed=42)
    except Exception:
        # Fallback: each node is its own community
        communities = [{m["module"]} for m in modules]

    membership: dict[str, int] = {}
    for cid, comm in enumerate(communities):
        for node in comm:
            membership[node] = cid

    # cluster membership
    write_json("cluster_membership.json", membership)

    # cluster summary
    cluster_mods: dict[int, list] = collections.defaultdict(list)
    for mod, cid in membership.items():
        cluster_mods[cid].append(mod)

    summaries = []
    for cid, mods in sorted(cluster_mods.items()):
        internal = sum(
            1 for u in mods for v in G.successors(u) if membership.get(v) == cid
        )
        external_out = sum(
            1 for u in mods for v in G.successors(u) if membership.get(v) != cid
        )
        n = len(mods)
        possible = n * (n - 1) or 1
        # infer dominant classification from module names
        combined = " ".join(mods).lower()
        dominant = classify_packet_signal(combined)
        summaries.append({
            "cluster_id": cid,
            "dominant_classification": dominant,
            "module_count": n,
            "internal_edges": internal,
            "external_edges_out": external_out,
            "density": round(internal / possible, 6),
            "modules": sorted(mods),
        })
    summaries.sort(key=lambda s: -s["module_count"])
    write_json("cluster_summary.json", summaries)

    # cluster dependency graph
    cluster_edges: dict[tuple[int,int], int] = collections.Counter()
    for src, tgt in G.edges():
        sc, tc = membership.get(src), membership.get(tgt)
        if sc is not None and tc is not None and sc != tc:
            cluster_edges[(sc, tc)] += 1
    CG = nx.DiGraph()
    edge_list = [{"from_cluster": k[0], "to_cluster": k[1], "edge_count": v}
                 for k, v in sorted(cluster_edges.items(), key=lambda x: -x[1])]
    for e in edge_list:
        CG.add_edge(e["from_cluster"], e["to_cluster"])
    cycles = list(nx.simple_cycles(CG))
    write_json("cluster_dependency_graph.json", {
        "cluster_nodes": sorted(set(membership.values())),
        "cluster_edges": edge_list,
        "cluster_cycles": [list(c) for c in cycles],
        "is_dag": len(cycles) == 0,
    })

    # boundary violations — modules with cross-cluster deep imports
    violations = []
    for m in modules:
        src_c = membership.get(m["module"])
        for imp in m["imports"]:
            parts = imp.replace("-", "_").split(".")
            for candidate in [parts[-1].lower(), parts[0].lower()]:
                if candidate in stem_map:
                    tgt = stem_map[candidate]
                    tgt_c = membership.get(tgt)
                    if tgt_c is not None and tgt_c != src_c:
                        violations.append({
                            "source_module": m["module"],
                            "illegal_import": tgt,
                            "depth": len(imp.split(".")),
                            "source_cluster": src_c,
                            "target_cluster": tgt_c,
                            "classification": "cross-cluster",
                        })
                    break
    write_json("cluster_boundary_violations.json", violations)

    # facade candidates — modules imported from 2+ clusters
    target_source_clusters: dict[str, set] = collections.defaultdict(set)
    for src, tgt in G.edges():
        sc = membership.get(src)
        tc = membership.get(tgt)
        if sc is not None and tc is not None and sc != tc:
            target_source_clusters[tgt].add(sc)

    facade_candidates = [
        {
            "module": mod,
            "importing_cluster_count": len(clusters),
            "importing_clusters": sorted(clusters),
            "own_cluster": membership.get(mod),
            "in_degree": G.in_degree(mod),
            "out_degree": G.out_degree(mod),
        }
        for mod, clusters in sorted(
            target_source_clusters.items(), key=lambda x: -len(x[1])
        )
        if len(clusters) >= 2
    ]
    write_json("facade_candidates.json", facade_candidates)

    # repair feasibility
    write_json("repair_feasibility.json", {
        "total_cross_cluster_violations": len(violations),
        "auto_repairable": sum(1 for v in violations if v["target_cluster"] is not None),
        "require_manual_review": sum(1 for v in violations if v["target_cluster"] is None),
        "facade_candidates_count": len(facade_candidates),
        "generated_at": RUN_TS,
    })

    print(f"  Clusters: {len(summaries)}")
    print(f"  Cross-cluster violations: {len(violations)}")
    print(f"  Facade candidates: {len(facade_candidates)}")
    return G, membership, communities


# ---------------------------------------------------------------------------
# STEP 4 — PACKET DISCOVERY (Tarjan SCC + classification)
# ---------------------------------------------------------------------------

def step_packet_discovery(modules: list[dict]):
    print("\n=== STEP 4: PACKET DISCOVERY ===")

    stem_map = {Path(m["file"]).stem.lower(): m["module"] for m in modules}

    # build graph
    graph: dict[str, list[str]] = {m["module"]: [] for m in modules}
    for m in modules:
        for imp in m["imports"]:
            parts = imp.replace("-", "_").split(".")
            for candidate in [parts[-1].lower(), parts[0].lower()]:
                if candidate in stem_map:
                    tgt = stem_map[candidate]
                    if tgt != m["module"] and tgt not in graph[m["module"]]:
                        graph[m["module"]].append(tgt)
                    break

    # Tarjan SCC
    index_counter = [0]
    stack: list[str] = []
    lowlink: dict[str, int] = {}
    index: dict[str, int] = {}
    on_stack: dict[str, bool] = {}
    sccs: list[list[str]] = []

    def strongconnect(start):
        call_stack = [(start, iter(graph.get(start, [])))]
        index[start] = index_counter[0]
        lowlink[start] = index_counter[0]
        index_counter[0] += 1
        stack.append(start)
        on_stack[start] = True
        while call_stack:
            v, neighbors = call_stack[-1]
            try:
                w = next(neighbors)
                if w not in index:
                    index[w] = index_counter[0]
                    lowlink[w] = index_counter[0]
                    index_counter[0] += 1
                    stack.append(w)
                    on_stack[w] = True
                    call_stack.append((w, iter(graph.get(w, []))))
                elif on_stack.get(w, False):
                    lowlink[v] = min(lowlink[v], index[w])
            except StopIteration:
                call_stack.pop()
                if call_stack:
                    parent = call_stack[-1][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[v])
                if lowlink[v] == index[v]:
                    scc = []
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        scc.append(w)
                        if w == v:
                            break
                    sccs.append(scc)

    for node in list(graph.keys()):
        if node not in index:
            strongconnect(node)

    path_map = {m["module"]: STAGING / m["file"] for m in modules}

    # build packet records
    packets = []
    for i, scc in enumerate(sccs):
        scc_set = set(scc)
        ext_deps = set()
        for node in scc:
            for tgt in graph.get(node, []):
                if tgt not in scc_set:
                    ext_deps.add(tgt)
        combined = " ".join(scc).lower()
        for node in scc[:3]:
            p = path_map.get(node)
            if p and p.exists():
                try:
                    combined += " " + p.read_text(encoding="utf-8", errors="replace")[:600].lower()
                except Exception:
                    pass
        cls = classify_packet_signal(combined)
        file_paths = []
        for node in scc:
            p = path_map.get(node)
            if p:
                try:
                    file_paths.append(str(p.relative_to(STAGING)))
                except Exception:
                    file_paths.append(str(p))
        packets.append({
            "packet_id": f"PKT_{i:04d}",
            "module_count": len(scc),
            "is_cycle": len(scc) > 1,
            "classification": cls,
            "modules": sorted(scc),
            "file_paths": sorted(file_paths),
            "external_dependencies": sorted(ext_deps),
            "external_dep_count": len(ext_deps),
        })

    packets.sort(key=lambda p: (-int(p["is_cycle"]), -p["module_count"]))
    for i, p in enumerate(packets):
        p["packet_id"] = f"PKT_{i:04d}"

    write_json("module_packets.json", packets)

    # graph JSON
    mod_to_pkt = {mod: pkt["packet_id"] for pkt in packets for mod in pkt["modules"]}
    edge_set: set[tuple[str,str]] = set()
    for pkt in packets:
        for dep in pkt["external_dependencies"]:
            tgt_pkt = mod_to_pkt.get(dep)
            if tgt_pkt and tgt_pkt != pkt["packet_id"]:
                edge_set.add((pkt["packet_id"], tgt_pkt))
    write_json("module_packet_graph.json", {
        "nodes": [{"id": p["packet_id"], "module_count": p["module_count"],
                   "is_cycle": p["is_cycle"], "classification": p["classification"],
                   "modules": p["modules"]} for p in packets],
        "edges": [{"from": a, "to": b} for a, b in sorted(edge_set)],
    })

    # classification-specific reports
    for cls_name, fname in [
        ("reasoning", "reasoning_packets.json"),
        ("semantic", "semantic_packets.json"),
        ("agent", "arp_packets.json"),
    ]:
        write_json(fname, [p for p in packets if p["classification"] == cls_name])

    cls_dist: dict[str, int] = collections.Counter(p["classification"] for p in packets)
    print(f"  Packets: {len(packets)}")
    for cls, cnt in sorted(cls_dist.items(), key=lambda x: -x[1]):
        print(f"    {cls}: {cnt}")
    return packets


# ---------------------------------------------------------------------------
# STEP 5+6+7 — TRIAGE, EXTRACTION REGISTRY, INTEGRATION CANDIDATES
# ---------------------------------------------------------------------------

def infer_triage(m: dict) -> str:
    """Determine triage classification based on STAGING folder hint + signals."""
    rel = m["file"]
    parts = Path(rel).parts

    # Folder-encoded classifications
    if "EXTRACT_LOGIC" in parts:
        return "EXTRACT_LOGIC"
    if "KEEP_VERIFY" in parts:
        return "KEEP_VERIFY"
    if "NORMALIZE_INTGRATE" in parts:
        return "KEEP_VERIFY"
    if "Inspection_Targets" in parts:
        return "KEEP_VERIFY"

    # Test files → DELETE (no production value)
    stem = Path(rel).stem
    if stem.startswith("test_") or stem.endswith("_test"):
        return "DELETE"

    # Categorize by semantic category subfolder
    category_folders = {"reasoning", "safety", "semantic", "math", "agent", "utility", "utils"}
    for part in parts:
        if part.lower() in category_folders:
            return "KEEP_VERIFY"

    return "KEEP_VERIFY"


def extract_module_functions(path: Path) -> list[dict]:
    """Extract top-level functions and classes from a Python file."""
    extracts: list[dict] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception:
        return extracts
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if isinstance(node, ast.FunctionDef) and not isinstance(
                getattr(node, "parent", None), ast.ClassDef
            ):
                args = [a.arg for a in node.args.args]
                docstring = ast.get_docstring(node) or ""
                extracts.append({
                    "type": "function",
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": args,
                    "docstring": docstring[:200],
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                })
        elif isinstance(node, ast.ClassDef):
            methods = [
                n.name for n in ast.walk(node)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            docstring = ast.get_docstring(node) or ""
            extracts.append({
                "type": "class",
                "name": node.name,
                "lineno": node.lineno,
                "methods": methods,
                "docstring": docstring[:200],
            })
    return extracts


SCP_SIGNALS = {"scp", "coherence", "contradiction", "belief", "proof", "modal"}
ARP_SIGNALS = {"arp", "reason", "infer", "logic", "bayesian", "deduct", "abduct"}
MTP_SIGNALS = {"mtp", "semantic", "translate", "ontology", "ontoprops", "symbol", "nlp"}
RUNTIME_UTIL_SIGNALS = {"kernel", "config", "loader", "registry", "bridge", "monitor", "logging"}


def protocol_compatibility(m: dict, path: Path) -> dict[str, bool]:
    try:
        content = path.read_text(encoding="utf-8", errors="replace").lower()
    except Exception:
        content = ""
    combined = (m["module"] + " " + content[:2000]).lower()
    return {
        "SCP": any(s in combined for s in SCP_SIGNALS),
        "ARP": any(s in combined for s in ARP_SIGNALS),
        "MTP": any(s in combined for s in MTP_SIGNALS),
        "runtime_utilities": any(s in combined for s in RUNTIME_UTIL_SIGNALS),
    }


def steps_triage_and_reports(modules: list[dict], packets: list[dict]):
    print("\n=== STEP 5: MODULE TRIAGE ===")

    triage_map: dict[str, str] = {}
    for m in modules:
        triage_map[m["module"]] = infer_triage(m)

    counts: dict[str, int] = collections.Counter(triage_map.values())
    for category, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {category}: {cnt}")

    # ── module_triage_report.md ──────────────────────────────────────────────
    md_lines = [
        "# ARCHON PRIME — Module Triage Report",
        "",
        f"**Generated:** {RUN_TS}",
        f"**Target:** `{STAGING}`",
        f"**Total modules:** {len(modules)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Classification | Count |",
        "|---------------|-------|",
    ]
    for cls, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        md_lines.append(f"| `{cls}` | {cnt} |")

    for category in ["EXTRACT_LOGIC", "KEEP_VERIFY", "DELETE"]:
        mods = [m for m in modules if triage_map[m["module"]] == category]
        if not mods:
            continue
        md_lines += [
            "",
            "---",
            "",
            f"## {category} ({len(mods)} modules)",
            "",
            "| Module | File | Size (bytes) | Packet Class |",
            "|--------|------|-------------|-------------|",
        ]
        # Look up packet classification for each module
        mod_to_pkt_cls: dict[str, str] = {}
        for pkt in packets:
            for mod in pkt["modules"]:
                mod_to_pkt_cls[mod] = pkt["classification"]
        for m in sorted(mods, key=lambda x: x["module"]):
            pkt_cls = mod_to_pkt_cls.get(m["module"], "—")
            file_short = m["file"].split(os.sep)[-1]
            md_lines.append(
                f"| `{m['module'].split('.')[-1]}` | `{file_short}` "
                f"| {m['size']} | {pkt_cls} |"
            )

    triage_path = OUTPUT_ROOT / "module_triage_report.md"
    triage_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"  [✓] module_triage_report.md")

    # ── STEP 6: extracted_logic_registry.json ───────────────────────────────
    print("\n=== STEP 6: LOGIC EXTRACTION REGISTRY ===")
    registry = []
    extract_mods = [m for m in modules if triage_map[m["module"]] == "EXTRACT_LOGIC"]
    for m in extract_mods:
        path = STAGING / m["file"]
        extracts = extract_module_functions(path)
        registry.append({
            "module": m["module"],
            "file": m["file"],
            "size": m["size"],
            "reusable_constructs": extracts,
            "construct_count": len(extracts),
            "imports": m["imports"],
            "triage": "EXTRACT_LOGIC",
        })
    registry.sort(key=lambda r: -r["construct_count"])
    write_json("extracted_logic_registry.json", registry)
    total_constructs = sum(r["construct_count"] for r in registry)
    print(f"  Modules processed: {len(registry)}")
    print(f"  Total reusable constructs: {total_constructs}")

    # ── STEP 7: runtime_integration_candidates.md ───────────────────────────
    print("\n=== STEP 7: INTEGRATION CANDIDATE ANALYSIS ===")
    keep_mods = [m for m in modules if triage_map[m["module"]] == "KEEP_VERIFY"]
    candidates = []
    for m in keep_mods:
        path = STAGING / m["file"]
        compat = protocol_compatibility(m, path)
        candidates.append({
            "module": m["module"],
            "file": m["file"],
            "size": m["size"],
            "compatibility": compat,
            "compatible_count": sum(compat.values()),
        })
    candidates.sort(key=lambda c: -c["compatible_count"])

    md_lines = [
        "# ARCHON PRIME — Runtime Integration Candidates",
        "",
        f"**Generated:** {RUN_TS}",
        f"**Source:** STAGING/Pre-Processing/KEEP_VERIFY + related subdirs",
        f"**Total KEEP_VERIFY modules:** {len(candidates)}",
        "",
        "---",
        "",
        "## Compatibility Matrix",
        "",
        "| Module | File | SCP | ARP | MTP | Runtime Util |",
        "|--------|------|-----|-----|-----|-------------|",
    ]
    for c in sorted(candidates, key=lambda x: x["module"]):
        compat = c["compatibility"]
        row_vals = {k: "✓" if v else "—" for k, v in compat.items()}
        fname = c["file"].split(os.sep)[-1]
        md_lines.append(
            f"| `{c['module'].split('.')[-1]}` | `{fname}` "
            f"| {row_vals['SCP']} | {row_vals['ARP']} | {row_vals['MTP']} "
            f"| {row_vals['runtime_utilities']} |"
        )

    md_lines += ["", "---", "", "## High-Compatibility Candidates", ""]
    high = [c for c in candidates if c["compatible_count"] >= 2]
    md_lines.append(f"**{len(high)} modules** are compatible with 2+ runtime protocols:\n")
    for c in high:
        protocols = [k for k, v in c["compatibility"].items() if v]
        md_lines.append(f"- `{c['module'].split('.')[-1]}` — {', '.join(protocols)}")

    md_lines += [
        "", "---", "", "## Modules Requiring Protocol Bridging", "",
        "The following KEEP_VERIFY modules have no direct protocol signal "
        "and may require an adapter layer before integration:", "",
    ]
    zero = [c for c in candidates if c["compatible_count"] == 0]
    for c in zero:
        md_lines.append(f"- `{c['module'].split('.')[-1]}` (`{c['file']}`)")

    md_lines += [
        "", "---", "",
        "_End of Runtime Integration Candidates Report_",
    ]

    int_path = OUTPUT_ROOT / "runtime_integration_candidates.md"
    int_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"  [✓] runtime_integration_candidates.md")
    print(f"  Candidates analyzed: {len(candidates)}")
    print(f"  High compatibility (>=2 protocols): {len(high)}")

    return triage_map


# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

EXPECTED_OUTPUTS = [
    "repo_directory_tree.json",
    "repo_python_files.json",
    "module_index.json",
    "cluster_membership.json",
    "cluster_summary.json",
    "cluster_dependency_graph.json",
    "cluster_boundary_violations.json",
    "facade_candidates.json",
    "repair_feasibility.json",
    "module_packets.json",
    "module_packet_graph.json",
    "reasoning_packets.json",
    "semantic_packets.json",
    "arp_packets.json",
    "module_triage_report.md",
    "extracted_logic_registry.json",
    "runtime_integration_candidates.md",
]


def validate():
    print("\n=== VALIDATION ===")
    ok = True
    for fname in EXPECTED_OUTPUTS:
        p = OUTPUT_ROOT / fname
        if p.exists():
            print(f"  [✓] {fname} ({p.stat().st_size:,} bytes)")
        else:
            print(f"  [FAIL] MISSING: {fname}")
            ok = False
    print()
    print("Validation:", "PASS" if ok else "FAIL")
    return ok


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("  ARCHON PRIME — STAGING RECOVERY AUDIT")
    print(f"  Target : {STAGING}")
    print(f"  Output : {OUTPUT_ROOT}")
    print(f"  Run    : {RUN_TS}")
    print("=" * 70)

    modules = step_repo_mapper()
    G, membership, communities = step_cluster_analysis(modules)
    packets = step_packet_discovery(modules)
    triage_map = steps_triage_and_reports(modules, packets)

    print("\n" + "=" * 70)
    print("  AUDIT COMPLETE")
    print("=" * 70)

    ok = validate()
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
