#!/usr/bin/env python3
"""
ARCHON PRIME — Module Packet Discovery
Builds an import dependency graph, detects SCCs, classifies packets,
and produces JSON + DOT output. Pure Python — no external dependencies.
"""

import ast
import json
import os
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

SCAN_ROOTS = [
    Path("/workspaces/Logos/_Dev_Resources/STAGING/APPLICATION_FUNCTIONS"),
    Path("/workspaces/Logos/Blueprints/reasoning"),
    Path("/workspaces/Logos/Blueprints/utils"),
]

TOOLS_DIR = Path("/workspaces/Logos/Tools")
TOOLS_DIR.mkdir(parents=True, exist_ok=True)

REPO_ROOT = Path("/workspaces/Logos")

# Semantic classification signals
PACKET_CLASSES = {
    "reasoning": {
        "infer", "deduce", "abduct", "reason", "logic", "proof",
        "bayesian", "modal", "deductive", "inductive", "heuristic",
        "counterfactual", "game_theoretic", "analogi", "pxl_engine",
        "meta_reason", "optimization", "topological", "temporal_reason",
        "categorical", "probability",
    },
    "semantic": {
        "translate", "semantic", "ontology", "ontoprops", "meaning",
        "language", "nlp", "embedding", "transformer", "mtp",
        "encode", "decode", "annotation", "symbol",
    },
    "agent": {
        "agent", "identity", "consciousness", "principal", "sign",
        "agentic", "axiom", "belief", "collaboration", "coordinator",
        "dispatcher", "planning", "planner", "task_intake", "smp",
        "iel", "autonomous",
    },
    "safety": {
        "safety", "validate", "constraint", "ethics", "policy", "guard",
        "gate", "privation", "privation_gate", "integrity", "ultima",
        "coherence", "monitor", "attestation", "etgc",
    },
    "math": {
        "math", "privation_mathematics", "banach", "fractal", "orbital",
        "topology", "algebra", "geometric", "bijection", "divergence",
        "symbolic_math", "arithmetic",
    },
    "utility": {
        "schema", "config", "loader", "registry", "adapter",
        "parser", "serializer", "logging", "wrapper", "helper",
        "tools", "utility", "utils", "constants", "types",
        "errors", "hashing", "router",
    },
}

# ---------------------------------------------------------------------------
# STEP 1 — MODULE SCAN
# ---------------------------------------------------------------------------

def collect_modules() -> dict[str, Path]:
    """Return {module_key: Path} for all Python files in scan roots."""
    modules = {}
    for root in SCAN_ROOTS:
        if not root.exists():
            print(f"  [SKIP] {root} — not found")
            continue
        for py in root.rglob("*.py"):
            if "__pycache__" in py.parts:
                continue
            key = py.stem  # use stem as the module node identifier
            # If collision, use relative path as key
            if key in modules:
                key = str(py.relative_to(REPO_ROOT))
            modules[key] = py
    return modules


# ---------------------------------------------------------------------------
# STEP 2 — BUILD DEPENDENCY GRAPH
# ---------------------------------------------------------------------------

def parse_imports(source: str, path: Path) -> list[str]:
    """Return list of module/name strings imported by this file."""
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []
    except Exception:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            imports.append(mod)
            for alias in node.names:
                if mod:
                    imports.append(f"{mod}.{alias.name}")
                else:
                    imports.append(alias.name)
    return imports


def build_graph(modules: dict[str, Path]) -> dict[str, list[str]]:
    """
    Build directed adjacency list: key → [keys of modules it imports].
    Only includes edges where the imported module is also in our scanned set.
    """
    # Build lookup sets: stem → key, and partial path fragment → key
    stem_to_key = {}
    for key, path in modules.items():
        stem = path.stem.lower()
        if stem not in stem_to_key:
            stem_to_key[stem] = key

    graph: dict[str, list[str]] = {k: [] for k in modules}

    for key, path in modules.items():
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        raw_imports = parse_imports(source, path)
        for imp in raw_imports:
            # Try to resolve the import to a known module
            # Take the last component (leaf module name)
            parts = imp.replace("-", "_").split(".")
            for candidate in [parts[-1].lower(), parts[0].lower()]:
                if candidate in stem_to_key:
                    target = stem_to_key[candidate]
                    if target != key and target not in graph[key]:
                        graph[key].append(target)
                    break

    return graph


# ---------------------------------------------------------------------------
# STEP 3 — SCC DETECTION (Tarjan's algorithm, iterative)
# ---------------------------------------------------------------------------

def tarjan_scc(graph: dict[str, list[str]]) -> list[list[str]]:
    """
    Iterative Tarjan's SCC algorithm.
    Returns list of SCCs (each SCC is a list of node keys).
    """
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    sccs = []
    nodes = list(graph.keys())

    def strongconnect(start):
        # Iterative DFS using explicit call stack
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
                # Root of SCC
                if lowlink[v] == index[v]:
                    scc = []
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        scc.append(w)
                        if w == v:
                            break
                    sccs.append(scc)

    for node in nodes:
        if node not in index:
            strongconnect(node)

    return sccs


# ---------------------------------------------------------------------------
# STEP 4 — SEMANTIC CLASSIFICATION
# ---------------------------------------------------------------------------

def classify_packet(nodes: list[str], modules: dict[str, Path]) -> str:
    """Classify an SCC packet by semantic signals in module names + first 500 chars."""
    combined = " ".join(nodes).lower()
    # Also look at file content signals
    for node in nodes[:5]:  # limit to first 5 to keep speed
        path = modules.get(node)
        if path and path.exists():
            try:
                combined += " " + path.read_text(encoding="utf-8", errors="replace")[:800].lower()
            except Exception:
                pass

    best_cls = "utility"
    best_score = 0
    for cls, signals in PACKET_CLASSES.items():
        score = sum(1 for s in signals if s in combined)
        if score > best_score:
            best_score = score
            best_cls = cls

    return best_cls


def classify_all_signals(nodes: list[str], modules: dict[str, Path]) -> dict[str, int]:
    """Return score for every class for this packet."""
    combined = " ".join(nodes).lower()
    for node in nodes[:5]:
        path = modules.get(node)
        if path and path.exists():
            try:
                combined += " " + path.read_text(encoding="utf-8", errors="replace")[:500].lower()
            except Exception:
                pass
    return {cls: sum(1 for s in signals if s in combined)
            for cls, signals in PACKET_CLASSES.items()}


# ---------------------------------------------------------------------------
# STEP 5 — PACKET REPORT CONSTRUCTION
# ---------------------------------------------------------------------------

def build_packet_records(sccs, graph, modules, repo_root):
    packets = []
    for i, scc in enumerate(sccs):
        # Determine all out-edges from this SCC to other SCCs
        scc_set = set(scc)
        external_deps = set()
        for node in scc:
            for target in graph.get(node, []):
                if target not in scc_set:
                    external_deps.add(target)

        cls = classify_packet(scc, modules)
        scores = classify_all_signals(scc, modules)
        is_cycle = len(scc) > 1

        # Collect file paths
        file_paths = []
        for node in scc:
            p = modules.get(node)
            if p:
                try:
                    file_paths.append(str(p.relative_to(repo_root)))
                except Exception:
                    file_paths.append(str(p))

        packets.append({
            "packet_id": f"PKT_{i:04d}",
            "module_count": len(scc),
            "is_cycle": is_cycle,
            "classification": cls,
            "class_scores": scores,
            "modules": sorted(scc),
            "file_paths": sorted(file_paths),
            "external_dependencies": sorted(external_deps),
            "external_dep_count": len(external_deps),
        })

    # Sort: cycles first, then by size desc
    packets.sort(key=lambda p: (-int(p["is_cycle"]), -p["module_count"]))

    # Re-number after sort
    for i, p in enumerate(packets):
        p["packet_id"] = f"PKT_{i:04d}"

    return packets


# ---------------------------------------------------------------------------
# STEP 6 — DOT GENERATION
# ---------------------------------------------------------------------------

PACKET_COLORS = {
    "reasoning": "#4A90D9",
    "semantic":  "#7B68EE",
    "agent":     "#50C878",
    "safety":    "#FF6B6B",
    "math":      "#FFB347",
    "utility":   "#B0B0B0",
}

def build_dot(packets, graph, modules):
    """
    Build a DOT graph where:
    - Each node is a packet (collapsed SCC)
    - Edges are inter-packet dependencies
    - Color coded by classification
    """
    # Map each module to its packet_id
    module_to_packet = {}
    for pkt in packets:
        for mod in pkt["modules"]:
            module_to_packet[mod] = pkt["packet_id"]

    # Collect inter-packet edges
    inter_edges = set()
    for pkt in packets:
        for mod in pkt["modules"]:
            for target in graph.get(mod, []):
                target_pkt = module_to_packet.get(target)
                if target_pkt and target_pkt != pkt["packet_id"]:
                    inter_edges.add((pkt["packet_id"], target_pkt))

    lines = [
        "digraph module_packet_graph {",
        "  graph [rankdir=LR, fontname=\"Helvetica\", splines=true, overlap=false];",
        "  node  [shape=box, style=filled, fontsize=10, fontname=\"Helvetica\"];",
        "  edge  [arrowsize=0.7, color=\"#666666\"];",
        "",
    ]

    for pkt in packets:
        pid   = pkt["packet_id"]
        label = "\\n".join(pkt["modules"][:5])
        if pkt["module_count"] > 5:
            label += f"\\n(+{pkt['module_count'] - 5} more)"
        color = PACKET_COLORS.get(pkt["classification"], "#CCCCCC")
        border = "2" if pkt["is_cycle"] else "1"
        lines.append(
            f'  "{pid}" [label="{pid}\\n{label}", '
            f'fillcolor="{color}", color="#333333", penwidth={border}];'
        )

    lines.append("")
    for src, dst in sorted(inter_edges):
        lines.append(f'  "{src}" -> "{dst}";')

    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run():
    print("=" * 60)
    print("ARCHON PRIME — Module Packet Discovery")
    print("=" * 60)

    # Step 1
    print("\n=== STEP 1: MODULE SCAN ===")
    modules = collect_modules()
    print(f"  Modules discovered: {len(modules)}")

    # Step 2
    print("\n=== STEP 2: BUILD DEPENDENCY GRAPH ===")
    graph = build_graph(modules)
    total_edges = sum(len(v) for v in graph.values())
    print(f"  Nodes: {len(graph)}")
    print(f"  Edges (intra-scan): {total_edges}")

    # Step 3
    print("\n=== STEP 3: SCC DETECTION (Tarjan's) ===")
    sccs = tarjan_scc(graph)
    cycles = [s for s in sccs if len(s) > 1]
    singletons = [s for s in sccs if len(s) == 1]
    print(f"  Total SCCs: {len(sccs)}")
    print(f"  Cyclic packets (>1 module): {len(cycles)}")
    print(f"  Singleton nodes: {len(singletons)}")

    # Step 4+5
    print("\n=== STEPS 4+5: CLASSIFICATION + PACKET RECORDS ===")
    packets = build_packet_records(sccs, graph, modules, REPO_ROOT)

    cls_dist = {}
    for p in packets:
        cls_dist[p["classification"]] = cls_dist.get(p["classification"], 0) + 1
    for cls, count in sorted(cls_dist.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {count} packets")

    # Write module_packets.json — all packets
    out_all = TOOLS_DIR / "module_packets.json"
    out_all.write_text(json.dumps(packets, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Written: {out_all} ({len(packets)} packets)")

    # Write module_packet_graph.json — graph structure
    graph_json = {
        "nodes": [
            {
                "id": pkt["packet_id"],
                "module_count": pkt["module_count"],
                "is_cycle": pkt["is_cycle"],
                "classification": pkt["classification"],
                "modules": pkt["modules"],
            }
            for pkt in packets
        ],
        "edges": [],
    }
    # Build edge list from inter-packet deps
    module_to_packet_id = {mod: pkt["packet_id"] for pkt in packets for mod in pkt["modules"]}
    edge_set = set()
    for pkt in packets:
        for dep in pkt["external_dependencies"]:
            tgt = module_to_packet_id.get(dep)
            if tgt and tgt != pkt["packet_id"]:
                key = (pkt["packet_id"], tgt)
                if key not in edge_set:
                    edge_set.add(key)
                    graph_json["edges"].append({"from": pkt["packet_id"], "to": tgt})

    out_graph = TOOLS_DIR / "module_packet_graph.json"
    out_graph.write_text(json.dumps(graph_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Written: {out_graph} ({len(graph_json['nodes'])} nodes, {len(graph_json['edges'])} edges)")

    # Write classification-specific files
    def write_class_file(cls_name: str, filename: str):
        matching = [p for p in packets if p["classification"] == cls_name]
        path = TOOLS_DIR / filename
        path.write_text(json.dumps(matching, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  Written: {path} ({len(matching)} packets)")
        return matching

    print("\n=== STEP 5: CLASSIFICATION-SPECIFIC REPORTS ===")
    write_class_file("reasoning", "reasoning_packets.json")
    write_class_file("semantic",  "semantic_packets.json")
    write_class_file("agent",     "arp_packets.json")   # ARP = agent reasoning packets

    # Step 6 — DOT file
    print("\n=== STEP 6: DOT DEPENDENCY MAP ===")
    dot_content = build_dot(packets, graph, modules)
    out_dot = TOOLS_DIR / "module_packet_graph.dot"
    out_dot.write_text(dot_content, encoding="utf-8")
    print(f"  Written: {out_dot}")

    # Print top cyclic packets
    print("\n=== TOP CYCLIC PACKETS ===")
    for pkt in [p for p in packets if p["is_cycle"]][:10]:
        mods = ", ".join(pkt["modules"][:4])
        if pkt["module_count"] > 4:
            mods += f"... (+{pkt['module_count'] - 4})"
        print(f"  {pkt['packet_id']} [{pkt['classification']}] {pkt['module_count']} modules: {mods}")

    print("\n" + "=" * 60)
    print("PACKET DISCOVERY COMPLETE")
    print(f"  Modules:   {len(modules)}")
    print(f"  Graph edges: {total_edges}")
    print(f"  Packets:   {len(packets)}")
    print(f"  Cycles:    {len(cycles)}")
    print("=" * 60)


if __name__ == "__main__":
    run()
