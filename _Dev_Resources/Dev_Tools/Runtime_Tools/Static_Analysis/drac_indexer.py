#!/usr/bin/env python3
"""
ARCHON PRIME — DRAC Application Function Master Index Builder
Produces: af_master_index.json, af_cluster_index.json, af_runtime_roles.json
Read-only analysis; no source-file mutations.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: drac_indexer.py
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
python drac_indexer.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


# ── Path constants ─────────────────────────────────────────────────────────────
REPO_ROOT   = Path("/workspaces/Logos")
AF_ROOT     = REPO_ROOT / "_Dev_Resources/STAGING/APPLICATION_FUNCTIONS"
TOOLS_DIR   = REPO_ROOT / "Tools"
DRAC_AF_OUT = (
    REPO_ROOT
    / "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE"
    / "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
    / "DRAC_Core/DRAC_Invariables/APPLICATION_FUNCTIONS"
)

# Only scan the new categorical subdirs (not legacy uppercase dirs)
CATEGORY_DIRS = {
    "agent":     "agent_control",
    "semantic":  "semantic_processing",
    "reasoning": "reasoning_engine",
    "utility":   "utility_support",
    "safety":    "safety_guard",
    "math":      "math_operator",
}

# ── Cluster detection patterns ─────────────────────────────────────────────────
# Each cluster maps to a set of keyword signals (checked against function names,
# class names, imports, docstrings — all lowercased).
CLUSTER_SIGNALS: dict[str, list[str]] = {
    "agent_runtime":          ["agent", "nexus", "dispatch", "start_agent", "boot", "lifecycle"],
    "planning":               ["plan", "goal", "task", "packet", "schedule", "objective"],
    "memory_access":          ["memory", "catalog", "store", "retriev", "cache", "knowledge"],
    "learning":               ["learn", "train", "adapt", "gradient", "improve", "self_improv"],
    "reasoning_inference":    ["infer", "syllog", "bayes", "probabilistic", "symbolic", "logic", "arp"],
    "semantic_interpretation":["semantic", "ontol", "embed", "vector", "meaning", "interpret", "token"],
    "tool_interface":         ["tool", "provider", "llm", "openai", "llama", "adapter", "api"],
    "validation_guard":       ["valid", "guard", "safety", "attestat", "monitor", "audit", "hardening"],
    "numerical_compute":      ["math", "numeric", "bijection", "tensor", "fractal", "modal", "vector"],
    "support_services":       ["util", "hash", "time", "resource", "health", "maintenance", "log"],
}

# Ordered for tie-breaking: first match wins
CLUSTER_ORDER = list(CLUSTER_SIGNALS.keys())


# ── AST helpers ────────────────────────────────────────────────────────────────
def _parse_module(path: Path) -> dict:
    """Return extracted metadata from a Python source file (best-effort)."""
    result = {
        "imports": [],
        "functions": [],
        "classes": [],
        "docstrings": [],
        "keywords": [],
    }
    try:
        src = path.read_text(errors="replace")
        tree = ast.parse(src, filename=str(path))
    except SyntaxError:
        return result

    for node in ast.walk(tree):
        # imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append(alias.name)
            else:
                mod = node.module or ""
                result["imports"].append(mod)
        # functions
        elif isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)
            doc = ast.get_docstring(node)
            if doc:
                result["docstrings"].append(doc[:300])
        # classes
        elif isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)
            doc = ast.get_docstring(node)
            if doc:
                result["docstrings"].append(doc[:300])

    # module-level docstring
    mod_doc = ast.get_docstring(tree)
    if mod_doc:
        result["docstrings"].insert(0, mod_doc[:400])

    # Derive keywords from identifiers and docstrings
    id_tokens = set(
        re.findall(r"[a-z][a-z0-9_]*", " ".join(
            result["functions"] + result["classes"] + result["imports"]
        ).lower())
    )
    doc_tokens = set(
        re.findall(r"[a-z][a-z0-9_]*", " ".join(result["docstrings"]).lower())
    )
    stop = {"self", "cls", "args", "kwargs", "none", "true", "false",
            "return", "pass", "import", "from", "def", "class", "and",
            "the", "for", "with", "not", "that", "this", "are", "used"}
    result["keywords"] = sorted((id_tokens | doc_tokens) - stop)[:40]

    return result


# ── Cluster assignment ─────────────────────────────────────────────────────────
def _assign_cluster(meta: dict, category: str, stem: str) -> str:
    haystack = " ".join([
        stem, category,
        " ".join(meta["functions"]),
        " ".join(meta["classes"]),
        " ".join(meta["imports"]),
        " ".join(meta["docstrings"]),
    ]).lower()

    best_cluster = None
    best_score   = 0
    for cluster in CLUSTER_ORDER:
        signals = CLUSTER_SIGNALS[cluster]
        score   = sum(1 for s in signals if s in haystack)
        if score > best_score:
            best_score   = score
            best_cluster = cluster

    # Fallback: role-based default
    if best_cluster is None or best_score == 0:
        fallback = {
            "agent":     "agent_runtime",
            "semantic":  "semantic_interpretation",
            "reasoning": "reasoning_inference",
            "utility":   "support_services",
            "safety":    "validation_guard",
            "math":      "numerical_compute",
        }
        best_cluster = fallback.get(category, "support_services")

    return best_cluster


# ── Packet data loader ─────────────────────────────────────────────────────────
def _load_packet_data() -> dict[str, dict]:
    """Return stem → {classification, packet_id, external_deps} from module_packets.json."""
    pkt_path = TOOLS_DIR / "module_packets.json"
    stem_map: dict[str, dict] = {}
    if not pkt_path.exists():
        return stem_map
    with open(pkt_path) as f:
        packets = json.load(f)
    for pkt in packets:
        for stem in pkt.get("modules", []):
            stem_map[stem] = {
                "packet_id":   pkt["packet_id"],
                "packet_class": pkt["classification"],
                "external_deps": pkt.get("external_dependencies", []),
            }
    return stem_map


# ── Compatibility tags ──────────────────────────────────────────────────────────
_COMPAT_RULES = {
    "reasoning": ["symbolic", "probabilistic", "formal"],
    "agent":     ["stateful", "orchestrated", "goal_driven"],
    "semantic":  ["embedded", "tokenized", "ontological"],
    "utility":   ["stateless", "reusable", "support"],
    "safety":    ["constrained", "audited", "monitored"],
    "math":      ["deterministic", "numeric", "algebraic"],
}

def _compat_tags(category: str, cluster: str, meta: dict) -> list[str]:
    tags = list(_COMPAT_RULES.get(category, []))
    if "test" in " ".join(meta["functions"]).lower():
        tags.append("testable")
    if meta["classes"]:
        tags.append("object_oriented")
    if any("async" in f.lower() for f in meta["functions"]):
        tags.append("async_capable")
    return sorted(set(tags))


# ── Main pipeline ──────────────────────────────────────────────────────────────
def run() -> None:
    print("=" * 60)
    print("ARCHON PRIME — DRAC AF Master Index Builder")
    print("=" * 60)

    # ── Step 1: Discover AF modules ───────────────────────────────────────────
    print("\n=== STEP 1: DISCOVER AF MODULES ===")
    DRAC_AF_OUT.mkdir(parents=True, exist_ok=True)

    packet_lookup = _load_packet_data()

    af_entries: list[dict] = []
    af_counter = 0

    for category, runtime_role in CATEGORY_DIRS.items():
        cat_dir = AF_ROOT / category
        if not cat_dir.exists():
            print(f"  [SKIP] {category}/ not found")
            continue
        py_files = sorted(cat_dir.glob("*.py"))
        print(f"  {category:12s}: {len(py_files)} modules")
        for py_file in py_files:
            af_counter += 1
            af_id  = f"AF_{af_counter:04d}"
            stem   = py_file.stem
            meta   = _parse_module(py_file)
            pkt    = packet_lookup.get(stem, {})
            cluster = _assign_cluster(meta, category, stem)
            compat  = _compat_tags(category, cluster, meta)

            entry = {
                "af_id":              af_id,
                "module_name":        py_file.name,
                "stem":               stem,
                "file_path":          str(py_file.relative_to(REPO_ROOT)),
                "category":           category,
                "runtime_role":       runtime_role,
                "cluster":            cluster,
                "packet_id":          pkt.get("packet_id", ""),
                "packet_class":       pkt.get("packet_class", ""),
                "imports":            meta["imports"],
                "functions":          meta["functions"],
                "classes":            meta["classes"],
                "keywords":           meta["keywords"],
                "dependencies":       pkt.get("external_deps", []),
                "compatibility_tags": compat,
            }
            af_entries.append(entry)

    print(f"\n  Total AF modules indexed: {len(af_entries)}")

    # ── Step 2: Build runtime roles map ──────────────────────────────────────
    print("\n=== STEP 2: RUNTIME ROLES ===")
    runtime_roles_map: dict[str, list[str]] = defaultdict(list)
    for e in af_entries:
        runtime_roles_map[e["runtime_role"]].append(e["af_id"])

    for role, ids in sorted(runtime_roles_map.items()):
        print(f"  {role:25s}: {len(ids)} modules")

    # ── Step 3: Build cluster index ───────────────────────────────────────────
    print("\n=== STEP 3: CLUSTER INDEX ===")
    cluster_members: dict[str, list[dict]] = defaultdict(list)
    for e in af_entries:
        cluster_members[e["cluster"]].append(e)

    cluster_entries: list[dict] = []
    cluster_counter = 0
    for cluster_name in sorted(cluster_members.keys()):
        members = cluster_members[cluster_name]
        cluster_counter += 1
        # Derive primary role (majority vote)
        role_votes: dict[str, int] = defaultdict(int)
        for m in members:
            role_votes[m["runtime_role"]] += 1
        primary_role = max(role_votes, key=role_votes.get)

        # Capability tags: union of all member compat tags
        capability_tags = sorted(set(
            tag for m in members for tag in m["compatibility_tags"]
        ))

        print(f"  {cluster_name:30s}: {len(members)} modules")
        cluster_entries.append({
            "cluster_id":        f"CLUSTER_{cluster_counter:03d}",
            "cluster_name":      cluster_name,
            "runtime_operation": cluster_name.replace("_", " "),
            "primary_role":      primary_role,
            "module_count":      len(members),
            "modules":           [m["af_id"] for m in members],
            "capability_tags":   capability_tags,
        })

    # ── Step 4: Build master index ────────────────────────────────────────────
    print("\n=== STEP 4: MASTER INDEX ===")

    master_index = {
        "schema_version":    "1.0.0",
        "generated_at":      datetime.now(timezone.utc).isoformat(),
        "source_directory":  str(AF_ROOT.relative_to(REPO_ROOT)),
        "total_af_modules":  len(af_entries),
        "total_clusters":    len(cluster_entries),
        "runtime_roles":     {role: len(ids) for role, ids in sorted(runtime_roles_map.items())},
        "clusters_index":    [
            {"cluster_id": c["cluster_id"], "cluster_name": c["cluster_name"],
             "module_count": c["module_count"]} for c in cluster_entries
        ],
        "modules_index":     [
            {"af_id": e["af_id"], "module_name": e["module_name"],
             "category": e["category"], "runtime_role": e["runtime_role"],
             "cluster": e["cluster"]} for e in af_entries
        ],
    }

    af_runtime_roles_doc = {
        "schema_version": "1.0.0",
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "role_definitions": {
            "agent_control":        "Modules that govern agent lifecycle, orchestration, and dispatch",
            "semantic_processing":  "Modules for token encoding, ontology mapping, and meaning extraction",
            "reasoning_engine":     "Modules implementing inference, logical deduction, and probabilistic reasoning",
            "utility_support":      "Stateless helper modules providing shared services",
            "safety_guard":         "Modules enforcing constraints, auditing, and integrity checks",
            "math_operator":        "Modules performing deterministic numeric and algebraic computation",
        },
        "assignment": {e["af_id"]: e["runtime_role"] for e in af_entries},
        "role_counts": {role: len(ids) for role, ids in sorted(runtime_roles_map.items())},
    }

    # ── Step 5: Validate ──────────────────────────────────────────────────────
    print("\n=== STEP 5: VALIDATION ===")
    af_ids = [e["af_id"] for e in af_entries]
    assert len(af_ids) == len(set(af_ids)), "DUPLICATE AF IDs DETECTED"
    assert all(e["runtime_role"] for e in af_entries), "Module missing runtime_role"
    assert all(e["cluster"] for e in af_entries), "Module missing cluster"
    clustered = {af_id for c in cluster_entries for af_id in c["modules"]}
    assert clustered == set(af_ids), "Cluster membership mismatch"
    print("  No duplicate AF IDs. ✓")
    print("  All modules assigned runtime role. ✓")
    print("  All modules assigned cluster. ✓")
    print("  Cluster membership complete. ✓")

    # ── Step 6: Write output files ────────────────────────────────────────────
    print("\n=== STEP 6: WRITE OUTPUT FILES ===")

    out_master      = DRAC_AF_OUT / "af_master_index.json"
    out_clusters    = DRAC_AF_OUT / "af_cluster_index.json"
    out_roles       = DRAC_AF_OUT / "af_runtime_roles.json"

    with open(out_master, "w") as f:
        json.dump(master_index, f, indent=2)
    print(f"  Written: {out_master.relative_to(REPO_ROOT)}")

    with open(out_clusters, "w") as f:
        json.dump({"clusters": cluster_entries}, f, indent=2)
    print(f"  Written: {out_clusters.relative_to(REPO_ROOT)}")

    with open(out_roles, "w") as f:
        json.dump(af_runtime_roles_doc, f, indent=2)
    print(f"  Written: {out_roles.relative_to(REPO_ROOT)}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("DRAC AF INDEX COMPLETE")
    print(f"  AF modules indexed:  {len(af_entries)}")
    print(f"  Clusters generated:  {len(cluster_entries)}")
    print(f"  Runtime roles:       {len(runtime_roles_map)}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run()
    except AssertionError as e:
        print(f"\n  VALIDATION FAILED: {e}")
        error_report = {"status": "FAILED", "error": str(e)}
        err_path = DRAC_AF_OUT / "af_index_error.json"
        DRAC_AF_OUT.mkdir(parents=True, exist_ok=True)
        with open(err_path, "w") as f:
            json.dump(error_report, f, indent=2)
        sys.exit(1)
