#!/usr/bin/env python3
"""
ARCHON PRIME — DRAC Recovery Triage Pipeline
=============================================
Full 7-stage pipeline over STAGING directory.
Triage categories: DELETE | NORMALIZE | EXTRACT_LOGIC | INTEGRATE

READ-ONLY — does not modify any file in STAGING.
Output: ARCHON_OUTPUT_ROOT (default: _Dev_Resources/Reports/ARCHON_DIAGNOSTICS)
"""

from __future__ import annotations

import ast
import collections
import hashlib
import json
import os
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any

try:
    import networkx as nx
    _HAS_NX = True
except ImportError:
    _HAS_NX = False

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT   = pathlib.Path("/workspaces/Logos")
STAGING     = REPO_ROOT / "_Dev_Resources/Processing_Center/STAGING"
OUTPUT_ROOT = pathlib.Path(
    os.environ.get("ARCHON_OUTPUT_ROOT",
                   "/workspaces/Logos/_Dev_Resources/Reports/ARCHON_DIAGNOSTICS")
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUN_TS      = datetime.now(timezone.utc).isoformat()
SKIP_DIRS   = {"__pycache__", ".git", ".venv", "node_modules"}

# ── Protocol / semantic signals ────────────────────────────────────────────────
PACKET_CLASSES: dict[str, set[str]] = {
    "reasoning": {
        "infer","deduce","abduct","reason","logic","proof","bayesian","modal",
        "deductive","inductive","heuristic","counterfactual","game_theoretic",
        "probability","coherence","pxl_engine","meta_reason","optimization",
    },
    "semantic": {
        "translate","semantic","ontology","meaning","language","nlp","embedding",
        "transformer","encode","decode","annotation","symbol","mtp","mtp_nexus",
    },
    "agent": {
        "agent","identity","consciousness","principal","sign","agentic","axiom",
        "belief","collaboration","coordinator","dispatcher","planning","planner",
        "task_intake","iel","autonomous","sop_nexus",
    },
    "safety": {
        "safety","validate","constraint","ethics","policy","guard","gate",
        "integrity","ultima","monitor","attestation","guardrails","health",
    },
    "math": {
        "math","banach","fractal","orbital","topology","algebra","geometric",
        "bijection","divergence","arithmetic","lambda","lambda_engine",
        "symbolic_math",
    },
    "utility": {
        "schema","config","loader","registry","adapter","parser","serializer",
        "logging","wrapper","helper","tools","utility","utils","constants",
        "types","errors","hashing","router","bridge",
    },
}

SCP_SIGNALS     = {"scp","coherence","contradiction","belief","proof","modal"}
ARP_SIGNALS     = {"arp","reason","infer","logic","bayesian","deduct","abduct"}
MTP_SIGNALS     = {"mtp","semantic","translate","ontology","symbol","nlp"}
RUNTIME_SIGNALS = {"kernel","config","loader","registry","bridge","monitor","logging"}

LOGIC_FRAGMENT_CATEGORIES = {
    "reasoning_pipeline":     ["infer","reason","deduce","proof","logic","abduct","coherence","bayesian","modal"],
    "symbolic_manipulation":  ["symbol","parse","tokenize","syntax","grammar","lambda","ast","unparse","rewrite"],
    "mathematical_algorithm": ["solve","compute","calculate","matrix","vector","norm","integral","derivative","minimize","optimize","gradient"],
    "decision_tree":          ["decide","branch","if_then","evaluate","weigh","compare","threshold","score","rank","classify"],
    "utility_logic":          ["transform","convert","normalize","filter","map","reduce","aggregate","merge","split","encode","decode"],
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def write_json(name: str, data: Any) -> pathlib.Path:
    p = OUTPUT_ROOT / name
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"    [OK] {name}  ({p.stat().st_size:,} bytes)")
    return p


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def extract_imports(path: pathlib.Path) -> list[str]:
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


def annotation_str(node: ast.expr | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


# ── STEP 1 — Repository Mapping ───────────────────────────────────────────────

def step1_repo_mapper() -> list[dict]:
    print("\n" + "="*60)
    print("  STEP 1 — Repository Mapping")
    print("="*60)

    # Directory tree
    tree: dict[str, dict] = {}
    for root, dirs, files in os.walk(STAGING):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        rel = str(pathlib.Path(root).relative_to(STAGING))
        tree[rel] = {"dirs": sorted(dirs), "files": sorted(files)}
    write_json("repo_directory_tree.json", tree)

    # Python file inventory
    py_files = []
    for root, dirs, files in os.walk(STAGING):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for f in sorted(files):
            if f.endswith(".py"):
                p = pathlib.Path(root) / f
                rel = str(p.relative_to(STAGING))
                py_files.append({
                    "path":          rel,
                    "size":          p.stat().st_size,
                    "hash":          sha256_file(p),
                    "staging_subdir": pathlib.Path(rel).parts[0] if pathlib.Path(rel).parts else "",
                })
    write_json("repo_python_files.json", py_files)

    # Module index with imports
    modules = []
    for finfo in py_files:
        full  = STAGING / finfo["path"]
        mname = finfo["path"].replace(os.sep, ".").removesuffix(".py")
        modules.append({
            "module":        mname,
            "file":          finfo["path"],
            "size":          finfo["size"],
            "imports":       extract_imports(full),
            "staging_subdir":finfo["staging_subdir"],
        })
    write_json("module_index.json", modules)

    print(f"    Directories   : {len(tree)}")
    print(f"    Python files  : {len(py_files)}")
    print(f"    Modules       : {len(modules)}")
    return modules


# ── STEP 2 — Dependency Graph Analysis ────────────────────────────────────────

def step2_import_graph(modules: list[dict]) -> dict[str, list[str]]:
    print("\n" + "="*60)
    print("  STEP 2 — Dependency Graph Analysis")
    print("="*60)

    stem_map = {pathlib.Path(m["file"]).stem.lower(): m["module"] for m in modules}

    graph: dict[str, list[str]] = {m["module"]: [] for m in modules}
    for m in modules:
        for imp in m["imports"]:
            parts = imp.replace("-","_").split(".")
            for candidate in [parts[-1].lower(), parts[0].lower()]:
                if candidate in stem_map:
                    tgt = stem_map[candidate]
                    if tgt != m["module"] and tgt not in graph[m["module"]]:
                        graph[m["module"]].append(tgt)
                    break

    edges = [{"source": src, "target": tgt}
             for src, tgts in sorted(graph.items()) for tgt in sorted(tgts)]

    write_json("import_graph.json", {"nodes": sorted(graph.keys()), "edges": edges})
    write_json("import_edges.json", edges)

    # module→dependency index
    dep_index = {mod: sorted(deps) for mod, deps in sorted(graph.items()) if deps}
    write_json("module_dependency_index.json", dep_index)

    print(f"    Nodes: {len(graph)}  Edges: {len(edges)}")
    return graph


# ── STEP 3 — AST Symbol Extraction ────────────────────────────────────────────

def step3_ast_symbols(modules: list[dict]) -> dict[str, list[dict]]:
    print("\n" + "="*60)
    print("  STEP 3 — AST Symbol Extraction")
    print("="*60)

    symbol_index: list[dict] = []
    class_registry: list[dict] = []
    function_registry: list[dict] = []

    for m in modules:
        path = STAGING / m["file"]
        try:
            src  = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(src, filename=str(path))
        except Exception:
            continue
        for node in tree.body:
            base = {"module": m["module"], "file": m["file"]}
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [{"name": a.arg, "annotation": annotation_str(a.annotation)}
                        for a in node.args.args]
                rec = {
                    **base,
                    "kind":              "function",
                    "name":              node.name,
                    "lineno":            node.lineno,
                    "is_async":          isinstance(node, ast.AsyncFunctionDef),
                    "args":              args,
                    "return_annotation": annotation_str(node.returns),
                    "is_private":        node.name.startswith("_"),
                    "docstring":         ast.get_docstring(node),
                }
                symbol_index.append(rec)
                function_registry.append(rec)
            elif isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append({
                            "name":    item.name,
                            "lineno":  item.lineno,
                            "is_async": isinstance(item, ast.AsyncFunctionDef),
                        })
                rec = {
                    **base,
                    "kind":       "class",
                    "name":       node.name,
                    "lineno":     node.lineno,
                    "bases":      [annotation_str(b) for b in node.bases],
                    "methods":    methods,
                    "docstring":  ast.get_docstring(node),
                }
                symbol_index.append(rec)
                class_registry.append(rec)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        symbol_index.append({
                            **base,
                            "kind":   "constant",
                            "name":   target.id,
                            "lineno": node.lineno,
                        })

    write_json("symbol_index.json",    symbol_index)
    write_json("class_registry.json",  class_registry)
    write_json("function_registry.json", function_registry)

    # Build per-module symbol lookup for later stages
    mod_symbols: dict[str, list[dict]] = collections.defaultdict(list)
    for s in symbol_index:
        mod_symbols[s["module"]].append(s)

    print(f"    Total symbols : {len(symbol_index)}")
    print(f"    Classes       : {len(class_registry)}")
    print(f"    Functions     : {len(function_registry)}")
    return dict(mod_symbols)


# ── STEP 4 — Logic Fragment Extraction ────────────────────────────────────────

def _classify_fragment(name: str, docstring: str, body_tokens: str) -> str:
    combined = (name + " " + docstring + " " + body_tokens).lower()
    best_cat, best_score = "utility_logic", 0
    for cat, keywords in LOGIC_FRAGMENT_CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > best_score:
            best_score, best_cat = score, cat
    return best_cat


def step4_logic_fragments(modules: list[dict]) -> dict[str, list[dict]]:
    print("\n" + "="*60)
    print("  STEP 4 — Logic Fragment Extraction")
    print("="*60)

    all_fragments: list[dict] = []
    fragment_index: list[dict] = []
    origin_map: dict[str, list[str]] = {}

    for m in modules:
        path = STAGING / m["file"]
        try:
            src  = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(src, filename=str(path))
        except Exception:
            continue

        mod_fragments: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            # skip obviously trivial functions
            if len(node.body) <= 1:
                continue
            doc = ast.get_docstring(node) or ""
            # extract body token sample
            try:
                body_src = ast.unparse(node)
            except Exception:
                body_src = ""
            body_tokens = " ".join(body_src.split()[:60])

            category = _classify_fragment(node.name, doc, body_tokens)
            args = [a.arg for a in node.args.args]
            frag_id = f"{m['module']}.{node.name}"

            frag = {
                "fragment_id":  frag_id,
                "module":       m["module"],
                "file":         m["file"],
                "function":     node.name,
                "lineno":       node.lineno,
                "category":     category,
                "args":         args,
                "docstring":    doc[:300],
                "is_async":     isinstance(node, ast.AsyncFunctionDef),
                "body_lines":   len(node.body),
            }
            all_fragments.append(frag)
            mod_fragments.append(frag_id)

            fragment_index.append({
                "fragment_id": frag_id,
                "module":      m["module"],
                "function":    node.name,
                "category":    category,
                "lineno":      node.lineno,
            })

        if mod_fragments:
            origin_map[m["module"]] = mod_fragments

    write_json("logic_fragments.json",    all_fragments)
    write_json("logic_fragment_index.json", fragment_index)
    write_json("fragment_origin_map.json", origin_map)

    cat_dist: dict[str, int] = collections.Counter(f["category"] for f in all_fragments)
    print(f"    Total fragments     : {len(all_fragments)}")
    print(f"    Modules with frags  : {len(origin_map)}")
    for cat, cnt in sorted(cat_dist.items(), key=lambda x: -x[1]):
        print(f"      {cat}: {cnt}")

    return origin_map  # module → [fragment_id, ...]


# ── STEP 5 — Dead Module Detection ────────────────────────────────────────────

def step5_dead_modules(modules: list[dict], graph: dict[str, list[str]]) -> set[str]:
    print("\n" + "="*60)
    print("  STEP 5 — Dead Module Detection")
    print("="*60)

    EXEMPT = {"__main__","main","setup","conftest","__init__"}

    # modules that are imported by at least one other module
    imported_by_any: set[str] = set()
    for srcs in graph.values():
        imported_by_any.update(srcs)

    dead: list[dict] = []
    unused: list[dict] = []

    for m in modules:
        stem = m["module"].split(".")[-1].lower()
        is_exempt = any(ex in stem for ex in EXEMPT) or stem.startswith("_")
        has_inbound = m["module"] in imported_by_any

        if not has_inbound and not is_exempt:
            dead.append({
                "module":       m["module"],
                "file":         m["file"],
                "size":         m["size"],
                "reason":       "no_inbound_imports",
                "staging_subdir": m["staging_subdir"],
            })
        if not has_inbound:
            unused.append({
                "module":  m["module"],
                "file":    m["file"],
                "size":    m["size"],
                "exempt":  is_exempt,
            })

    write_json("dead_modules.json",  dead)
    write_json("unused_modules.json", unused)

    dead_set = {d["module"] for d in dead}
    print(f"    Dead modules   : {len(dead)}")
    print(f"    Unused (total) : {len(unused)}  (includes exempt)")
    return dead_set


# ── STEP 6 — Architecture Mapping ─────────────────────────────────────────────

LAYER_SIGNALS: dict[str, list[str]] = {
    "governance":  ["governance","policy","constraint","lifecycle","audit"],
    "agent":       ["agent","archon","orchestrat","executor","dispatcher"],
    "protocol":    ["protocol","interface","contract","gate","enforce"],
    "reasoning":   ["reasoning","inference","logic","epistemic","axiom","bayesian"],
    "semantic":    ["semantic","nlp","embedding","tokenize","corpus","ontology"],
    "math":        ["math","numeric","algebra","calculus","matrix","tensor","fractal"],
    "safety":      ["safety","guard","sanity","validate","quarantine","constraint"],
    "utility":     ["util","helper","common","shared","base","mixin","config"],
    "persistence": ["store","registry","persist","db","cache","repo"],
    "runtime":     ["runtime","core","startup","init","boot","main"],
}
LAYER_ORDER = list(LAYER_SIGNALS.keys())


def _infer_layer(label: str, signals: list[str] | None = None) -> str:
    combined = (label + " " + " ".join(signals or [])).lower()
    for layer, kws in LAYER_SIGNALS.items():
        if any(kw in combined for kw in kws):
            return layer
    return "utility"


def step6_architecture_mapper(modules: list[dict], graph: dict[str, list[str]]) -> dict:
    print("\n" + "="*60)
    print("  STEP 6 — Architecture Mapping")
    print("="*60)

    # Group modules into subsystems by staging_subdir → top-level directory
    subsystems: dict[str, dict] = {}
    for m in modules:
        parts = pathlib.PurePosixPath(m["file"].replace(os.sep, "/")).parts
        sub = parts[0] if parts else "root"
        if sub not in subsystems:
            subsystems[sub] = {"subsystem": sub, "modules": [], "inferred_layer": None, "module_count": 0}
        subsystems[sub]["modules"].append(m["module"])

    for name, sub in subsystems.items():
        sub["inferred_layer"] = _infer_layer(name, [m.split(".")[-1] for m in sub["modules"]])
        sub["module_count"] = len(sub["modules"])

    # Architecture layers
    layers: dict[str, dict] = {l: {"subsystems": [], "module_count": 0} for l in LAYER_ORDER}
    for sub_name, sub in subsystems.items():
        layer = sub.get("inferred_layer", "utility")
        if layer not in layers:
            layers[layer] = {"subsystems": [], "module_count": 0}
        layers[layer]["subsystems"].append(sub_name)
        layers[layer]["module_count"] += sub["module_count"]

    # Subsystem dependency graph
    mod_to_sub = {m: sub for sub, s in subsystems.items() for m in s["modules"]}
    edge_counts: dict[tuple[str,str], int] = collections.Counter()
    for src, tgts in graph.items():
        for tgt in tgts:
            ss, ds = mod_to_sub.get(src), mod_to_sub.get(tgt)
            if ss and ds and ss != ds:
                edge_counts[(ss, ds)] += 1

    arch_nodes = [{"id": n, "layer": s["inferred_layer"], "module_count": s["module_count"]}
                  for n, s in subsystems.items()]
    arch_edges = [{"source": s, "target": t, "weight": w}
                  for (s,t),w in sorted(edge_counts.items())]

    # Dependency flow matrix
    names = sorted(subsystems.keys())
    idx = {n: i for i, n in enumerate(names)}
    matrix = [[0]*len(names) for _ in range(len(names))]
    for (s,t), w in edge_counts.items():
        if s in idx and t in idx:
            matrix[idx[s]][idx[t]] += w

    # Cross-layer violations
    sub_to_layer  = {n: s["inferred_layer"] for n, s in subsystems.items()}
    layer_rank = {l: i for i, l in enumerate(LAYER_ORDER)}
    violations = []
    for src, tgts in graph.items():
        for tgt in tgts:
            ss, ds = mod_to_sub.get(src), mod_to_sub.get(tgt)
            if not ss or not ds or ss == ds:
                continue
            sr, dr = layer_rank.get(sub_to_layer.get(ss,"utility"),99), layer_rank.get(sub_to_layer.get(ds,"utility"),99)
            if sr > dr:
                violations.append({"source_module": src, "source_subsystem": ss,
                                    "target_module": tgt, "target_subsystem": ds,
                                    "source_layer": sub_to_layer.get(ss),
                                    "target_layer": sub_to_layer.get(ds),
                                    "violation_type": "cross_layer_inward"})

    meta = {"run_timestamp": RUN_TS, "target_directory": str(STAGING), "tool": "architecture_mapper"}
    write_json("architecture_graph.json",           {**meta, "graph": {"nodes": arch_nodes, "edges": arch_edges}})
    write_json("subsystem_registry.json",           {**meta, "subsystems": subsystems})
    write_json("architecture_layers.json",          {**meta, "layers": layers, "layer_order": LAYER_ORDER})
    write_json("architecture_dependency_flow.json", {**meta, "subsystems": names, "flow_matrix": matrix})
    write_json("architecture_violations.json",      {**meta, "violation_count": len(violations), "violations": violations})

    print(f"    Subsystems     : {len(subsystems)}")
    print(f"    Cross-layer violations: {len(violations)}")
    return subsystems


# ── STEP 7 — Module Triage Classification ─────────────────────────────────────

def _protocol_compat(m: dict) -> dict[str, bool]:
    path = STAGING / m["file"]
    try:
        content = path.read_text(encoding="utf-8", errors="replace").lower()
    except Exception:
        content = ""
    combined = (m["module"] + " " + content[:3000]).lower()
    return {
        "SCP":             any(s in combined for s in SCP_SIGNALS),
        "ARP":             any(s in combined for s in ARP_SIGNALS),
        "MTP":             any(s in combined for s in MTP_SIGNALS),
        "runtime_utility": any(s in combined for s in RUNTIME_SIGNALS),
    }


def _infer_triage(
    m: dict,
    dead_set: set[str],
    origin_map: dict[str, list[str]],
    compat: dict[str, bool],
) -> str:
    """
    4-way classification:
      EXTRACT_LOGIC — module contains reusable reasoning/logic fragments
      INTEGRATE     — structurally compatible with runtime protocols
      NORMALIZE     — useful but needs structural cleanup
      DELETE        — unused, no fragments, no protocol value
    """
    file_parts = pathlib.Path(m["file"]).parts
    mod = m["module"]

    # Explicit folder-encoded classification from STAGING structure
    if "EXTRACT_LOGIC" in file_parts:
        return "EXTRACT_LOGIC"

    # Has reusable logic fragments → EXTRACT_LOGIC
    has_fragments = mod in origin_map and len(origin_map[mod]) > 0
    if has_fragments:
        fragment_cats = {fi.split(".")[-2] if "." in fi else "" for fi in origin_map.get(mod, [])}
        # If fragments are substantive (non-utility) → EXTRACT_LOGIC
        substantive = {"reasoning_pipeline","symbolic_manipulation","mathematical_algorithm","decision_tree"}
        if any(fi.split(".")[-1] != "utility_logic" for fi in origin_map.get(mod, [])):
            return "EXTRACT_LOGIC"

    # Dead module with no fragments → DELETE
    is_dead = mod in dead_set
    if is_dead and not has_fragments:
        return "DELETE"

    # Compatible with runtime protocols → INTEGRATE
    compat_count = sum(compat.values())
    if compat_count >= 2:
        return "INTEGRATE"
    if compat_count == 1 and not is_dead:
        return "INTEGRATE"

    # Dead with only utility fragments → DELETE
    if is_dead:
        return "DELETE"

    # Remaining = needs structural work → NORMALIZE
    return "NORMALIZE"


def step7_triage(
    modules: list[dict],
    dead_set: set[str],
    origin_map: dict[str, list[str]],
) -> dict[str, str]:
    print("\n" + "="*60)
    print("  STEP 7 — Module Triage Classification")
    print("="*60)

    triage_map: dict[str, str] = {}
    triage_details: list[dict] = []

    for m in modules:
        compat = _protocol_compat(m)
        cat    = _infer_triage(m, dead_set, origin_map, compat)
        triage_map[m["module"]] = cat
        triage_details.append({
            "module":              m["module"],
            "file":                m["file"],
            "size":                m["size"],
            "staging_subdir":      m["staging_subdir"],
            "triage":              cat,
            "is_dead":             m["module"] in dead_set,
            "has_logic_fragments": m["module"] in origin_map,
            "fragment_count":      len(origin_map.get(m["module"], [])),
            "protocol_compat":     compat,
            "compatible_count":    sum(compat.values()),
        })

    counts: dict[str, int] = collections.Counter(triage_map.values())

    # ── master report ────────────────────────────────────────────────────────
    report = {
        "report_type":    "module_triage_report",
        "generated_at":   RUN_TS,
        "target":         str(STAGING),
        "total_modules":  len(modules),
        "summary":        dict(counts),
        "modules":        sorted(triage_details, key=lambda x: (x["triage"], x["module"])),
    }
    write_json("module_triage_report.json", report)

    # ── per-category files ───────────────────────────────────────────────────
    for cat, fname in [
        ("DELETE",       "delete_candidates.json"),
        ("NORMALIZE",    "normalize_candidates.json"),
        ("EXTRACT_LOGIC","logic_extraction_targets.json"),
        ("INTEGRATE",    "integration_candidates.json"),
    ]:
        records = [d for d in triage_details if d["triage"] == cat]
        write_json(fname, {
            "category":     cat,
            "count":        len(records),
            "generated_at": RUN_TS,
            "modules":      sorted(records, key=lambda x: x["module"]),
        })

    for cat in ["DELETE","NORMALIZE","EXTRACT_LOGIC","INTEGRATE"]:
        print(f"    {cat:15s}: {counts.get(cat, 0)}")

    return triage_map


# ── Validation ─────────────────────────────────────────────────────────────────

REQUIRED_OUTPUTS = [
    # Stage 1
    "repo_directory_tree.json", "repo_python_files.json", "module_index.json",
    # Stage 2
    "import_graph.json", "import_edges.json", "module_dependency_index.json",
    # Stage 3
    "symbol_index.json", "class_registry.json", "function_registry.json",
    # Stage 4
    "logic_fragments.json", "logic_fragment_index.json", "fragment_origin_map.json",
    # Stage 5
    "dead_modules.json", "unused_modules.json",
    # Stage 6
    "architecture_graph.json", "subsystem_registry.json", "architecture_layers.json",
    "architecture_dependency_flow.json", "architecture_violations.json",
    # Stage 7
    "module_triage_report.json", "delete_candidates.json", "normalize_candidates.json",
    "logic_extraction_targets.json", "integration_candidates.json",
]


def validate() -> bool:
    print("\n" + "="*60)
    print("  OUTPUT VALIDATION")
    print("="*60)
    ok = True
    for fname in REQUIRED_OUTPUTS:
        p = OUTPUT_ROOT / fname
        if p.exists():
            print(f"    [OK ]  {fname}  ({p.stat().st_size:,} bytes)")
        else:
            print(f"    [MISSING]  {fname}")
            ok = False
    return ok


# ── Summary ────────────────────────────────────────────────────────────────────

def print_summary(modules: list[dict], triage_map: dict[str, str]) -> None:
    counts: dict[str, int] = collections.Counter(triage_map.values())
    print()
    print("=" * 60)
    print("  ARCHON PRIME — DRAC TRIAGE PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Target            : {STAGING}")
    print(f"  Output            : {OUTPUT_ROOT}")
    print(f"  Run timestamp     : {RUN_TS}")
    print(f"  Total modules     : {len(modules)}")
    print()
    print("  Triage Results:")
    print(f"    DELETE          : {counts.get('DELETE', 0)}")
    print(f"    NORMALIZE       : {counts.get('NORMALIZE', 0)}")
    print(f"    EXTRACT_LOGIC   : {counts.get('EXTRACT_LOGIC', 0)}")
    print(f"    INTEGRATE       : {counts.get('INTEGRATE', 0)}")
    print()
    print(f"  Artifacts written : {len(REQUIRED_OUTPUTS)}")
    print(f"  Output directory  : {OUTPUT_ROOT}")
    print("=" * 60)


# ── Entry Point ────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("  ARCHON PRIME — DRAC TRIAGE PIPELINE")
    print(f"  Target  : {STAGING}")
    print(f"  Output  : {OUTPUT_ROOT}")
    print(f"  Run     : {RUN_TS}")
    print("=" * 60)

    if not STAGING.exists():
        print(f"ERROR: STAGING directory not found: {STAGING}")
        sys.exit(1)

    modules    = step1_repo_mapper()
    graph      = step2_import_graph(modules)
    _          = step3_ast_symbols(modules)
    origin_map = step4_logic_fragments(modules)
    dead_set   = step5_dead_modules(modules, graph)
    _          = step6_architecture_mapper(modules, graph)
    triage_map = step7_triage(modules, dead_set, origin_map)

    ok = validate()
    print_summary(modules, triage_map)

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
