#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-ARCH-MAPPER
# module_name:          architecture_mapper
# analysis_domain:      structure_analysis
# module_role:          synthesis
# execution_entry:      run
# mutation_capability:  false
# safety_classification: READ_ONLY
# spec_reference:       [SPEC-AP-V2.1]
# ============================================================

"""
ARCHON PRIME — Architecture Mapper
====================================
Synthesises prior analysis artifacts into a high-level architecture model.

Inputs (all optional with graceful degradation):
  repo_directory_tree.json
  module_index.json
  import_graph.json
  cluster_membership.json
  module_packets.json
  symbol_index.json
  semantic_packets.json

Outputs (all written to OUTPUT_ROOT):
  architecture_graph.json
  subsystem_registry.json
  architecture_layers.json
  architecture_dependency_flow.json
  architecture_violations.json
"""

import argparse
import collections
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"

OUTPUT_ROOT = Path(
    os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT)
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# LAYER INFERENCE SIGNALS
# ---------------------------------------------------------------------------

LAYER_SIGNALS: dict[str, set[str]] = {
    "governance":   {"governance", "policy", "gate", "constraint", "privation",
                     "authorization", "compliance", "enforce"},
    "safety":       {"safety", "guard", "attestation", "validate", "monitor",
                     "integrity", "health", "ethics"},
    "agent":        {"agent", "nexus", "identity", "consciousness", "sop",
                     "planner", "coordinator", "dispatcher"},
    "reasoning":    {"reason", "infer", "logic", "proof", "bayesian", "modal",
                     "deductive", "arp", "scp", "uip"},
    "semantic":     {"semantic", "translate", "ontology", "mtp", "nlp",
                     "embedding", "symbol", "ontoprops"},
    "math":         {"math", "fractal", "orbital", "banach", "topology",
                     "algebra", "arithmetic", "bijection", "lambda"},
    "runtime":      {"runtime", "execution", "boot", "startup", "kernel",
                     "dispatch", "bridge", "telemetry"},
    "utility":      {"utility", "utils", "config", "loader", "registry",
                     "adapter", "logging", "hashing", "router"},
    "testing":      {"test", "smoke", "integration_test", "coverage"},
}

# Layer dependency order (lower index = more foundational)
LAYER_ORDER = [
    "governance", "safety", "math", "utility",
    "runtime", "reasoning", "semantic", "agent", "testing",
]


def infer_layer(name: str, content_snippet: str = "") -> str:
    combined = (name + " " + content_snippet).lower()
    best, best_score = "utility", 0
    for layer, signals in LAYER_SIGNALS.items():
        score = sum(1 for s in signals if s in combined)
        if score > best_score:
            best_score, best = score, layer
    return best


# ---------------------------------------------------------------------------
# ARTIFACT LOADERS
# ---------------------------------------------------------------------------

def load_artifact(path: Path, label: str) -> object | None:
    if not path.exists():
        print(f"  [SKIP] {label} not found at {path}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        print(f"  [✓] Loaded {label}")
        return data
    except Exception as exc:
        print(f"  [WARN] Could not parse {label}: {exc}")
        return None


def write_artifact(name: str, data: object) -> None:
    p = OUTPUT_ROOT / name
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


# ---------------------------------------------------------------------------
# CORE ANALYSIS
# ---------------------------------------------------------------------------

def build_subsystem_registry(
    module_index: list[dict] | None,
    cluster_membership: dict[str, int] | None,
) -> dict[str, dict]:
    """
    Group modules into subsystems. Prefer cluster IDs from cluster_membership;
    fall back to directory-based grouping of module names.
    """
    subsystems: dict[str, dict] = {}

    if module_index is None:
        return subsystems

    for m in module_index:
        mod_name = m.get("module", "")
        file_path = m.get("file", "")

        # Cluster-based grouping
        if cluster_membership and mod_name in cluster_membership:
            ss_key = f"cluster_{cluster_membership[mod_name]}"
        else:
            # Directory-based grouping (first path component)
            parts = Path(file_path).parts
            ss_key = parts[0] if parts else "root"

        layer = infer_layer(mod_name)
        if ss_key not in subsystems:
            subsystems[ss_key] = {
                "subsystem": ss_key,
                "layer": layer,
                "modules": [],
                "module_count": 0,
            }
        subsystems[ss_key]["modules"].append(mod_name)
        subsystems[ss_key]["module_count"] += 1

    return subsystems


def build_architecture_layers(
    subsystems: dict[str, dict],
) -> list[dict]:
    """Aggregate subsystems into architectural layers."""
    layer_map: dict[str, dict] = {}
    for ss in subsystems.values():
        layer = ss["layer"]
        if layer not in layer_map:
            layer_map[layer] = {
                "layer": layer,
                "order": LAYER_ORDER.index(layer) if layer in LAYER_ORDER else 99,
                "subsystems": [],
                "total_modules": 0,
            }
        layer_map[layer]["subsystems"].append(ss["subsystem"])
        layer_map[layer]["total_modules"] += ss["module_count"]

    return sorted(layer_map.values(), key=lambda l: l["order"])


def build_architecture_graph(
    subsystems: dict[str, dict],
    import_graph: dict | None,
    cluster_membership: dict[str, int] | None,
) -> dict:
    """Build a subsystem-level dependency graph from the module import graph."""
    nodes = [
        {"id": ss, "layer": data["layer"], "module_count": data["module_count"]}
        for ss, data in subsystems.items()
    ]

    edges: dict[tuple[str, str], int] = collections.Counter()

    if import_graph:
        raw_edges = import_graph.get("edges", [])
        # Build module → subsystem map
        mod_to_ss: dict[str, str] = {}
        for ss, data in subsystems.items():
            for mod in data["modules"]:
                mod_to_ss[mod] = ss

        for edge in raw_edges:
            src = edge.get("from") or edge.get("source", "")
            tgt = edge.get("to") or edge.get("target", "")
            src_ss = mod_to_ss.get(src)
            tgt_ss = mod_to_ss.get(tgt)
            if src_ss and tgt_ss and src_ss != tgt_ss:
                edges[(src_ss, tgt_ss)] += 1

    edge_list = [
        {"from_subsystem": k[0], "to_subsystem": k[1], "edge_count": v}
        for k, v in sorted(edges.items(), key=lambda x: -x[1])
    ]

    return {"nodes": nodes, "edges": edge_list}


def build_dependency_flow(
    arch_graph: dict,
    layers: list[dict],
) -> list[dict]:
    """Map cross-layer dependency flows."""
    layer_of: dict[str, str] = {}
    for layer in layers:
        for ss in layer["subsystems"]:
            layer_of[ss] = layer["layer"]

    flow: dict[tuple[str, str], int] = collections.Counter()
    for edge in arch_graph["edges"]:
        src_layer = layer_of.get(edge["from_subsystem"], "unknown")
        tgt_layer = layer_of.get(edge["to_subsystem"], "unknown")
        if src_layer != tgt_layer:
            flow[(src_layer, tgt_layer)] += edge["edge_count"]

    return [
        {"from_layer": k[0], "to_layer": k[1], "total_edges": v}
        for k, v in sorted(flow.items(), key=lambda x: -x[1])
    ]


def detect_violations(
    dep_flow: list[dict],
    layers: list[dict],
) -> list[dict]:
    """
    Flag cross-layer imports where a lower-numbered (more foundational)
    layer depends on a higher-numbered (more application-level) layer —
    i.e. a governance module importing from an agent module.
    """
    order_of: dict[str, int] = {}
    for layer in layers:
        order_of[layer["layer"]] = layer["order"]

    violations = []
    for flow in dep_flow:
        src_order = order_of.get(flow["from_layer"], 99)
        tgt_order = order_of.get(flow["to_layer"], 99)
        if src_order < tgt_order:
            violations.append({
                "violation_type": "upward_layer_dependency",
                "from_layer": flow["from_layer"],
                "to_layer": flow["to_layer"],
                "edge_count": flow["total_edges"],
                "severity": "HIGH" if abs(src_order - tgt_order) > 2 else "MEDIUM",
                "description": (
                    f"Foundational layer '{flow['from_layer']}' (order {src_order}) "
                    f"imports from higher-level layer '{flow['to_layer']}' (order {tgt_order})."
                ),
            })

    violations.sort(key=lambda v: v["edge_count"], reverse=True)
    return violations


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run(target_dir: Path = Path("."), output_root: Path = OUTPUT_ROOT) -> bool:
    global OUTPUT_ROOT
    OUTPUT_ROOT = output_root
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  ARCHON PRIME — Architecture Mapper")
    print(f"  Target : {target_dir}")
    print(f"  Output : {OUTPUT_ROOT}")
    print(f"  Run    : {RUN_TS}")
    print("=" * 60)

    print("\n[STEP 1] Loading analysis artifacts …")
    module_index     = load_artifact(OUTPUT_ROOT / "module_index.json",      "module_index")
    import_graph     = load_artifact(OUTPUT_ROOT / "import_graph.json",      "import_graph")
    cluster_memb     = load_artifact(OUTPUT_ROOT / "cluster_membership.json","cluster_membership")
    # module_packets, symbol_index, semantic_packets loaded for future expansion
    load_artifact(OUTPUT_ROOT / "module_packets.json",    "module_packets")
    load_artifact(OUTPUT_ROOT / "symbol_index.json",      "symbol_index")
    load_artifact(OUTPUT_ROOT / "semantic_packets.json",  "semantic_packets")
    load_artifact(OUTPUT_ROOT / "repo_directory_tree.json", "repo_directory_tree")

    print("\n[STEP 2] Building subsystem registry …")
    subsystems = build_subsystem_registry(module_index, cluster_memb)
    write_artifact("subsystem_registry.json", {
        "generated_at": RUN_TS,
        "subsystem_count": len(subsystems),
        "subsystems": list(subsystems.values()),
    })

    print("\n[STEP 3] Inferring architectural layers …")
    layers = build_architecture_layers(subsystems)
    write_artifact("architecture_layers.json", {
        "generated_at": RUN_TS,
        "layer_count": len(layers),
        "layers": layers,
    })

    print("\n[STEP 4] Building architecture graph …")
    arch_graph = build_architecture_graph(subsystems, import_graph, cluster_memb)
    write_artifact("architecture_graph.json", {
        "generated_at": RUN_TS,
        "node_count": len(arch_graph["nodes"]),
        "edge_count": len(arch_graph["edges"]),
        **arch_graph,
    })

    print("\n[STEP 5] Mapping dependency flow …")
    dep_flow = build_dependency_flow(arch_graph, layers)
    write_artifact("architecture_dependency_flow.json", {
        "generated_at": RUN_TS,
        "cross_layer_flows": len(dep_flow),
        "flows": dep_flow,
    })

    print("\n[STEP 6] Detecting cross-layer violations …")
    violations = detect_violations(dep_flow, layers)
    write_artifact("architecture_violations.json", {
        "generated_at": RUN_TS,
        "violation_count": len(violations),
        "violations": violations,
    })

    print(f"\n  Subsystems: {len(subsystems)}")
    print(f"  Layers    : {len(layers)}")
    print(f"  Violations: {len(violations)}")
    print("\n[✓] Architecture Mapper complete.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARCHON Architecture Mapper")
    parser.add_argument("--target", type=Path, default=Path("."),
                        help="Target repository root")
    parser.add_argument("--output", type=Path, default=OUTPUT_ROOT,
                        help="Output directory (overrides ARCHON_OUTPUT_ROOT)")
    args = parser.parse_args()
    ok = run(target_dir=args.target, output_root=args.output)
    sys.exit(0 if ok else 1)
