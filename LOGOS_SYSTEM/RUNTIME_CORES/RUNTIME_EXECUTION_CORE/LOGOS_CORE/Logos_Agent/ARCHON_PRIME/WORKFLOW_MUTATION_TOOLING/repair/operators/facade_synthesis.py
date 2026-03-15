#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-015
# module_name:          facade_synthesis
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/facade_synthesis.py
# responsibility:       Mutation module: facade synthesis
# runtime_stage:        repair
# execution_entry:      main
# allowed_targets:      ["WORKFLOW_TARGET_PROCESSING/PROCESSING"]
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

import collections
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

"""
ARCHON PRIME — Runtime Facade Synthesis Pass
=============================================
Derives canonical import facades and generates automated rewrite mappings
"""
"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: facade_synthesis.py
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
python facade_synthesis.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

"""
from the runtime topology artifacts.

Analysis only — no repository mutation.
"""

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


# ── Root paths ─────────────────────────────────────────────────────────────────
REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
ARCHON = REPO_ROOT / "ARCHON_RUNTIME_ANALYSIS"
BLUEPRINTS_CIF = REPO_ROOT / "BLUEPRINTS" / "Canonical_Import_Facade"
CLUSTER_DIR = REPO_ROOT / "_Reports" / "Runtime_Cluster_Analysis"
OUTPUT_DIR = REPO_ROOT / "Runtime_Facade_Synthesis"

# ── Canonical package-root clusters ────────────────────────────────────────────
MACRO_CLUSTER_ROOTS = [
    "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE",
    "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE",
    "LOGOS_SYSTEM.RUNTIME_BRIDGE",
    "LOGOS_SYSTEM.RUNTIME_SHARED_UTILS",
    "LOGOS_SYSTEM._Governance",
    "LOGOS_SYSTEM.System_Stack",
    "BLUEPRINTS",
    "STARTUP",
    "_Governance",
    "DOCUMENTS",
]


# ── Facade namespace assignment ─────────────────────────────────────────────────
def facade_namespace_for_root(root: str) -> str:
    u = root.upper()
    if "EXECUTION" in u:
        return "logos.imports.execution"
    if "OPPERATIONS" in u or "OPERATIONS" in u:
        return "logos.imports.operations"
    if "RUNTIME_BRIDGE" in u:
        return "logos.imports.bridge"
    if "SHARED_UTILS" in u or "SHARED" in u:
        return "logos.imports.shared"
    if "GOVERNANCE" in u or "_GOVERNANCE" in u:
        return "logos.imports.governance"
    if "SYSTEM_STACK" in u or "AGENTS" in u:
        return "logos.imports.agents"
    if "STARTUP" in u or "BOOT" in u:
        return "logos.imports.startup"
    if "BLUEPRINT" in u:
        return "logos.imports.blueprints"
    if "DOCUMENT" in u:
        return "logos.imports.documents"
    return "logos.imports.runtime"


# ── Helpers ────────────────────────────────────────────────────────────────────
def load(path: Path, label: str):
    if not path.exists():
        print(f"  [MISSING] {label} — {path}")
        return None
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def require(path: Path, label: str):
    data = load(path, label)
    if data is None:
        print(f"[FATAL] Required artifact absent: {label} at {path}")
        sys.exit(1)
    return data


def write_json(path: Path, data) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {path.relative_to(REPO_ROOT)}")


def write_text(path: Path, text: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  [✓] {path.relative_to(REPO_ROOT)}")


def depth(mod: str) -> int:
    return mod.count(".")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Load Runtime Graph & Module Metadata
# ══════════════════════════════════════════════════════════════════════════════
def step1_load_graph():
    print("\n[STEP 1] Loading runtime dependency graph …")
    dep_graph = require(
        ARCHON / "runtime_dependency_graph.json", "runtime_dependency_graph"
    )
    py_runtime = require(ARCHON / "runtime_python_files.json", "runtime_python_files")
    py_repo = load(REPO_ROOT / "repo_python_files.json", "repo_python_files")
    if py_repo is None:
        py_repo = load(
            BLUEPRINTS_CIF / "repo_python_files.json", "repo_python_files(blueprints)"
        )
    if py_repo is None:
        py_repo = []

    # Build adjacency for degree computation
    in_deg = collections.Counter()
    out_deg = collections.Counter()
    for edge in dep_graph["edges"]:
        out_deg[edge["from"]] += 1
        in_deg[edge["to"]] += 1

    # Combined module set
    all_modules = set(dep_graph["nodes"])
    for rec in py_runtime:
        if isinstance(rec, dict):
            all_modules.add(rec.get("module_path", ""))
        else:
            all_modules.add(str(rec))
    for rec in py_repo:
        if isinstance(rec, dict):
            all_modules.add(rec.get("module_path", ""))
        else:
            all_modules.add(str(rec))

    print(
        f"  [i] Graph nodes: {len(dep_graph['nodes'])}"
        f"  edges: {len(dep_graph['edges'])}"
    )
    print(f"  [i] Total known modules: {len(all_modules)}")
    return dep_graph, in_deg, out_deg, all_modules


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Load & Merge Violation Sets
# ══════════════════════════════════════════════════════════════════════════════
def _normalise_violation(v: object) -> dict | None:
    """
    Accept three known violation schemas and return a normalised dict, or None to skip.

    Schema A (ARCHON / cluster_boundary):
        {source_module, illegal_import, depth, ...}

    Schema B (BLUEPRINTS Deep_Import_Violations):
        {file, line, content:"from X.Y.Z import ...", forbidden_prefix, ...}
    """
    if not isinstance(v, dict):
        return None

    # Schema A — direct fields
    if "source_module" in v:
        src = v.get("source_module", "")
        tgt = v.get("illegal_import") or v.get("target_module", "")
        d = v.get("depth", tgt.count(".") if tgt else 0)
        return (
            {
                "source_module": src,
                "illegal_import": tgt,
                "depth": d,
                "classification": v.get("classification", ""),
                "source_cluster": v.get("source_cluster"),
                "target_cluster": v.get("target_cluster"),
            }
            if src and tgt
            else None
        )

    # Schema B — BLUEPRINTS format
    if "file" in v and "content" in v:
        file_path = v.get("file", "")
        content = v.get("content", "").strip()
        # Convert file path to module path: strip .py, replace / with .
        src = file_path.replace("/", ".").replace("\\", ".")
        if src.endswith(".py"):
            src = src[:-3]

        # Extract target module from "from X.Y.Z import ..." or "import X.Y.Z"
        tgt = ""
        if content.startswith("from "):
            parts = content.split()  # from TARGET import ...
            if len(parts) >= 2:
                tgt = parts[1]
        elif content.startswith("import "):
            parts = content.split()
            if len(parts) >= 2:
                tgt = parts[1].split(" as ")[0].rstrip(",")

        d = tgt.count(".") if tgt else 0
        return (
            {
                "source_module": src,
                "illegal_import": tgt,
                "depth": d,
                "classification": "",
                "source_cluster": None,
                "target_cluster": None,
            }
            if src and tgt
            else None
        )

    return None


def step2_load_violations():
    print("\n[STEP 2] Loading violation datasets …")

    v1_raw = load(
        BLUEPRINTS_CIF / "Deep_Import_Violations.json", "Deep_Import_Violations"
    )
    v2 = load(
        ARCHON / "runtime_deep_import_violations.json", "runtime_deep_import_violations"
    )
    v3 = load(
        CLUSTER_DIR / "cluster_boundary_violations.json", "cluster_boundary_violations"
    )

    # Schema B wraps violations inside a top-level dict
    if isinstance(v1_raw, dict) and "violations" in v1_raw:
        v1 = v1_raw["violations"]
    elif isinstance(v1_raw, list):
        v1 = v1_raw
    else:
        v1 = []

    raw_entries = []
    for dataset in (v1, v2, v3):
        if dataset:
            raw_entries.extend(dataset)

    seen: set[tuple] = set()
    violations: list[dict] = []
    for entry in raw_entries:
        norm = _normalise_violation(entry)
        if norm is None:
            continue
        key = (norm["source_module"], norm["illegal_import"])
        if key in seen or not norm["source_module"] or not norm["illegal_import"]:
            continue
        seen.add(key)
        violations.append(norm)

    print(f"  [i] Violations loaded: {len(violations)}  (after dedup)")
    return violations


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Load Facade Candidates
# ══════════════════════════════════════════════════════════════════════════════
def step3_load_candidates():
    print("\n[STEP 3] Loading facade candidates …")

    c1 = load(
        ARCHON / "canonical_facade_candidates.json",
        "canonical_facade_candidates(archon)",
    )
    c2 = load(CLUSTER_DIR / "facade_candidates.json", "facade_candidates(cluster)")

    candidate_facade_map: dict[str, str] = {}  # symbol or module → facade namespace

    for dataset in (c1, c2):
        if not dataset:
            continue
        for rec in dataset:
            # c1 format: {symbol, source_module, recommended_facade}
            if "source_module" in rec and "recommended_facade" in rec:
                mod = rec["source_module"]
                candidate_facade_map[mod] = rec["recommended_facade"]
            # c2 format: {module, recommended_facade_namespace, ...}
            if "module" in rec and "recommended_facade_namespace" in rec:
                mod = rec["module"]
                candidate_facade_map[mod] = rec["recommended_facade_namespace"]

    print(f"  [i] Candidate facade entries: {len(candidate_facade_map)}")
    return candidate_facade_map


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Derive Architectural Cluster Map
# ══════════════════════════════════════════════════════════════════════════════
def step4_build_cluster_map(all_modules: set[str]) -> dict[str, str]:
    print("\n[STEP 4] Building macro-cluster map …")

    cluster_map: dict[str, str] = {}

    def best_root(mod: str) -> str:
        best = None
        best_len = -1
        for root in MACRO_CLUSTER_ROOTS:
            if mod == root or mod.startswith(root + "."):
                if len(root) > best_len:
                    best = root
                    best_len = len(root)
        return best or mod.split(".")[0]

    for mod in all_modules:
        if mod:
            cluster_map[mod] = best_root(mod)

    cluster_counts = collections.Counter(cluster_map.values())
    print(f"  [i] Distinct macro-clusters: {len(cluster_counts)}")
    for root, cnt in cluster_counts.most_common(12):
        print(f"      {root[:70]:<70} {cnt:>4} modules")

    return cluster_map


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Build Canonical Facade Map
# ══════════════════════════════════════════════════════════════════════════════
def step5_build_facade_map(
    cluster_map: dict[str, str],
    candidate_facade_map: dict[str, str],
    in_deg: dict[str, int],
    out_deg: dict[str, int],
) -> dict[str, dict]:
    print("\n[STEP 5] Building canonical facade map …")

    # Group modules by cluster root
    root_modules: dict[str, list[str]] = collections.defaultdict(list)
    for mod, root in cluster_map.items():
        root_modules[root].append(mod)

    facade_map: dict[str, dict] = {}

    for root, mods in sorted(root_modules.items()):
        # Check if any module in this cluster has an explicit candidate facade
        explicit: str | None = None
        best_explicit_score = -1
        for mod in mods:
            if mod in candidate_facade_map:
                score = in_deg.get(mod, 0) + out_deg.get(mod, 0)
                if score > best_explicit_score:
                    explicit = candidate_facade_map[mod]
                    best_explicit_score = score

        if explicit:
            facade_ns = explicit
            facade_mod = None
            # Find the highest-centrality module matching that facade ns
            for mod in mods:
                if candidate_facade_map.get(mod) == explicit:
                    facade_mod = mod
                    break
        else:
            facade_ns = facade_namespace_for_root(root)
            # Choose highest centrality module in cluster
            facade_mod = max(
                mods,
                key=lambda m: in_deg.get(m or "", 0) + out_deg.get(m or "", 0),
                default=None,
            )

        facade_map[root] = {
            "cluster_root": root,
            "facade_namespace": facade_ns,
            "facade_module": facade_mod,
            "module_count": len(mods),
            "selection_method": "explicit_candidate" if explicit else "max_centrality",
        }

    print(f"  [i] Facade map entries: {len(facade_map)}")
    for root, entry in sorted(facade_map.items())[:12]:
        print(f"      {root[:55]:<55} → {entry['facade_namespace']}")

    return facade_map


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Build Import Rewrite Table
# ══════════════════════════════════════════════════════════════════════════════
def step6_rewrite_table(
    violations: list[dict],
    cluster_map: dict[str, str],
    facade_map: dict[str, dict],
) -> list[dict]:
    print("\n[STEP 6] Building import rewrite table …")

    rewrite_table: list[dict] = []

    for v in violations:
        src = v["source_module"]
        tgt = v["illegal_import"]

        target_cluster = cluster_map.get(tgt)
        if not target_cluster:
            # Fallback: use first matching macro-root prefix
            for root in MACRO_CLUSTER_ROOTS:
                if tgt.startswith(root + ".") or tgt == root:
                    target_cluster = root
                    break
            if not target_cluster:
                target_cluster = tgt.split(".")[0]

        # target_cluster is always str at this point (fallback guaranteed above)
        assert target_cluster is not None
        facade_entry = facade_map.get(target_cluster)
        if facade_entry:
            replacement = facade_entry["facade_namespace"]
        else:
            replacement = f"logos.imports.{target_cluster.lower().replace('.','_')}"

        rewrite_table.append(
            {
                "source_module": src,
                "illegal_import": tgt,
                "target_cluster": target_cluster,
                "replacement_import": replacement,
                "repair_type": "facade_substitution",
                "depth": v["depth"],
                "classification": v.get("classification", ""),
            }
        )

    rewrite_table.sort(key=lambda r: (-r["depth"], r["source_module"]))
    print(f"  [i] Rewrite rules generated: {len(rewrite_table)}")
    return rewrite_table


# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — Repair Feasibility Classification
# ══════════════════════════════════════════════════════════════════════════════
def step7_feasibility(
    rewrite_table: list[dict],
    facade_map: dict[str, dict],
    cluster_map: dict[str, str],
) -> list[dict]:
    print("\n[STEP 7] Classifying repair feasibility …")

    feasibility: list[dict] = []

    for rule in rewrite_table:
        reasons: list[str] = []
        ok = True

        # Check 1: facade module exists in map
        tc = rule["target_cluster"]
        entry = facade_map.get(tc)
        if not entry or not entry.get("facade_module"):
            reasons.append("No explicit facade module identified for cluster")
            ok = False

        # Check 2: replacement does not itself become a deep import
        rep = rule["replacement_import"]
        if rep.count(".") > 3:
            reasons.append(
                f"Replacement namespace is still deep ({rep.count('.')} levels)"
            )
            ok = False

        # Check 3: source and target are not in the same cluster (intra OK to skip)
        src_cluster = cluster_map.get(rule["source_module"], "")
        if src_cluster == tc and tc not in ("", "unknown"):
            reasons.append(
                "Intra-cluster import — facade rewrite optional, not mandatory"
            )
            # still auto-repairable structurally, but flag as optional
            status = "OPTIONAL_INTRA_CLUSTER"
        elif ok:
            status = "AUTO_REPAIRABLE"
        else:
            status = "MANUAL_REVIEW_REQUIRED"

        feasibility.append(
            {
                "source_module": rule["source_module"],
                "illegal_import": rule["illegal_import"],
                "replacement_import": rule["replacement_import"],
                "target_cluster": tc,
                "status": status,
                "reasons": reasons,
                "depth": rule["depth"],
            }
        )

    counts = collections.Counter(f["status"] for f in feasibility)
    print("  [i] Feasibility breakdown:")
    for status, cnt in sorted(counts.items()):
        print(f"      {status}: {cnt}")

    return feasibility


# ══════════════════════════════════════════════════════════════════════════════
# STEP 8 — Facade Surface Specification
# ══════════════════════════════════════════════════════════════════════════════
def step8_surface_spec(
    facade_map: dict[str, dict],
    cluster_map: dict[str, str],
    symbol_imports_path: Path,
) -> dict:
    print("\n[STEP 8] Building facade surface specification …")

    sym_data = load(symbol_imports_path, "runtime_symbol_imports")
    if sym_data is None:
        sym_data = []

    # Group exported symbols by the module they come FROM
    module_exports: dict[str, set[str]] = collections.defaultdict(set)
    for rec in sym_data:
        tgt = rec.get("target_module", "")
        sym = rec.get("symbol", "")
        if tgt and sym:
            module_exports[tgt].add(sym)

    spec: dict[str, dict] = {}

    for root, entry in facade_map.items():
        ns = entry["facade_namespace"]
        mod = entry["facade_module"]

        # Modules that belong to this cluster
        cluster_mods = [m for m, r in cluster_map.items() if r == root]

        # Symbols exported by any module in this cluster
        exported: dict[str, list[str]] = {}
        for cm in cluster_mods:
            syms = sorted(module_exports.get(cm, set()))
            if syms:
                exported[cm] = syms

        spec[ns] = {
            "facade_namespace": ns,
            "canonical_facade_module": mod,
            "cluster_root": root,
            "cluster_module_count": len(cluster_mods),
            "exported_symbols": exported,
            "total_exported_symbols": sum(len(v) for v in exported.values()),
        }

    print(f"  [i] Facade surface entries: {len(spec)}")
    return spec


# ══════════════════════════════════════════════════════════════════════════════
# STEP 9 — Auto-Repair Plan (Markdown)
# ══════════════════════════════════════════════════════════════════════════════
def step9_repair_plan(
    violations: list[dict],
    rewrite_table: list[dict],
    feasibility: list[dict],
    facade_map: dict[str, dict],
) -> str:
    now = datetime.now(timezone.utc).isoformat()
    total = len(violations)
    auto = sum(1 for f in feasibility if f["status"] == "AUTO_REPAIRABLE")
    optional = sum(1 for f in feasibility if f["status"] == "OPTIONAL_INTRA_CLUSTER")
    manual = sum(1 for f in feasibility if f["status"] == "MANUAL_REVIEW_REQUIRED")

    lines = [
        "# ARCHON — Automated Facade Repair Plan",
        "",
        f"**Generated:** {now}",
        "**Mode:** Analysis Only — No Repository Mutation",
        "",
        "---",
        "",
        "## 1. Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|\n",
        f"| Total deep import violations | {total} |",
        f"| Auto-repairable (facade substitution) | {auto} |",
        f"| Optional repairs (intra-cluster) | {optional} |",
        f"| Manual review required | {manual} |",
        f"| Canonical facade namespaces | {len(facade_map)} |",
        "",
        "---",
        "",
        "## 2. Cluster → Facade Mapping",
        "",
        "| Cluster Root | Facade Namespace | Facade Module | Selection |",
        "|-------------|-----------------|---------------|-----------|",
    ]
    for root, entry in sorted(facade_map.items(), key=lambda x: x[0]):
        mod = (entry["facade_module"] or "")[-60:] if entry["facade_module"] else "—"
        lines.append(
            f"| `{root[:55]}` | `{entry['facade_namespace']}` "
            f"| `{mod}` | {entry['selection_method']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 3. Rewrite Rule Summary",
        "",
        "Pattern: for each violation, replace the deep import"
        " with the facade namespace.",
        "",
        "```",
        "BEFORE:  from LOGOS_SYSTEM.RUNTIME_CORES."
        "RUNTIME_EXECUTION_CORE.X.Y.Z import Symbol",
        "AFTER:   from logos.imports.execution import Symbol",
        "```",
        "",
        "Full rewrite rules are enumerated in `import_rewrite_table.json`.",
        "",
        "### Top 20 Auto-Repairable Rewrites (by depth):",
        "",
        "| Source Module | Illegal Import | Replacement | Depth |",
        "|--------------|----------------|-------------|-------|",
    ]
    auto_rules = [f for f in feasibility if f["status"] == "AUTO_REPAIRABLE"]
    auto_rules.sort(key=lambda x: -x["depth"])
    for r in auto_rules[:20]:
        src = (
            r["source_module"][-50:]
            if len(r["source_module"]) > 50
            else r["source_module"]
        )
        ill = (
            r["illegal_import"][-55:]
            if len(r["illegal_import"]) > 55
            else r["illegal_import"]
        )
        lines.append(
            f"| `{src}` | `{ill}` | `{r['replacement_import']}` | {r['depth']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 4. Modules Requiring Manual Intervention",
        "",
    ]
    manual_rules = [f for f in feasibility if f["status"] == "MANUAL_REVIEW_REQUIRED"]
    if manual_rules:
        lines += [
            "| Source Module | Illegal Import | Reason |",
            "|--------------|----------------|--------|",
        ]
        for r in manual_rules[:30]:
            src = (
                r["source_module"][-50:]
                if len(r["source_module"]) > 50
                else r["source_module"]
            )
            ill = (
                r["illegal_import"][-50:]
                if len(r["illegal_import"]) > 50
                else r["illegal_import"]
            )
            reason = "; ".join(r["reasons"])[:80]
            lines.append(f"| `{src}` | `{ill}` | {reason} |")
    else:
        lines.append("_No modules require manual intervention._")

    lines += [
        "",
        "---",
        "",
        "## 5. Execution Instructions",
        "",
        "1. Install facade shim modules at each `facade_namespace` path listed above.",
        "2. Each shim re-exports all symbols catalogued in `facade_surface_spec.json`.",
        "3. Apply rewrites from `import_rewrite_table.json` using a deterministic",
        "   AST rewrite pass (e.g., `libcst`, `rope`, or custom rewriter).",
        "4. Verify with `python -m pytest` and the ARCHON validation suite.",
        "5. Re-run `run_archon_runtime_analysis.py` to confirm"
        " violation count drops to 0.",
        "",
        "---",
        "",
        "_End of ARCHON Automated Facade Repair Plan_",
        "",
    ]
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 10 — Write Artifacts
# ══════════════════════════════════════════════════════════════════════════════
def step10_write(
    facade_map: dict,
    cluster_map: dict,
    rewrite_table: list,
    feasibility: list,
    surface_spec: dict,
    repair_plan: str,
) -> None:
    print("\n[STEP 10] Writing output artifacts …")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_json(OUTPUT_DIR / "facade_map.json", facade_map)
    write_json(OUTPUT_DIR / "cluster_map.json", cluster_map)
    write_json(OUTPUT_DIR / "import_rewrite_table.json", rewrite_table)
    write_json(OUTPUT_DIR / "repair_feasibility.json", feasibility)
    write_json(OUTPUT_DIR / "facade_surface_spec.json", surface_spec)
    write_text(OUTPUT_DIR / "auto_repair_plan.md", repair_plan)


# ══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
def validate(
    facade_map: dict,
    rewrite_table: list,
    feasibility: list,
) -> bool:
    print("\n[VALIDATION] Running exit checks …")
    ok = True

    expected = [
        "facade_map.json",
        "cluster_map.json",
        "import_rewrite_table.json",
        "repair_feasibility.json",
        "facade_surface_spec.json",
        "auto_repair_plan.md",
    ]
    for fname in expected:
        p = OUTPUT_DIR / fname
        if not p.exists() or p.stat().st_size == 0:
            print(f"  [FAIL] {fname} missing or empty")
            ok = False
        else:
            print(f"  [✓] {fname} ({p.stat().st_size // 1024} KB)")

    if len(facade_map) == 0:
        print("  [FAIL] facade_map.json is empty")
        ok = False
    else:
        print(f"  [✓] facade_map has {len(facade_map)} entries")

    if len(rewrite_table) < 1:
        print("  [FAIL] import_rewrite_table contains 0 rules")
        ok = False
    else:
        print(f"  [✓] import_rewrite_table has {len(rewrite_table)} rules")

    unclassified = [f for f in feasibility if "status" not in f]
    if unclassified:
        print(f"  [FAIL] {len(unclassified)} feasibility entries lack status")
        ok = False
    else:
        print(f"  [✓] All {len(feasibility)} violations classified")

    return ok


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 70)
    print("  ARCHON PRIME — RUNTIME FACADE SYNTHESIS PASS")
    print("  Mode: Analysis Only — No Repository Mutation")
    print("=" * 70)

    dep_graph, in_deg, out_deg, all_modules = step1_load_graph()
    violations = step2_load_violations()
    cand_map = step3_load_candidates()
    cluster_map = step4_build_cluster_map(all_modules)
    facade_map = step5_build_facade_map(cluster_map, cand_map, in_deg, out_deg)
    rewrite_table = step6_rewrite_table(violations, cluster_map, facade_map)
    feasibility = step7_feasibility(rewrite_table, facade_map, cluster_map)
    surface_spec = step8_surface_spec(
        facade_map,
        cluster_map,
        ARCHON / "runtime_symbol_imports.json",
    )
    repair_plan = step9_repair_plan(violations, rewrite_table, feasibility, facade_map)
    step10_write(
        facade_map, cluster_map, rewrite_table, feasibility, surface_spec, repair_plan
    )

    ok = validate(facade_map, rewrite_table, feasibility)

    auto = sum(1 for f in feasibility if f["status"] == "AUTO_REPAIRABLE")
    optional = sum(1 for f in feasibility if f["status"] == "OPTIONAL_INTRA_CLUSTER")
    manual = sum(1 for f in feasibility if f["status"] == "MANUAL_REVIEW_REQUIRED")

    print("\n" + "=" * 70)
    print("  FACADE SYNTHESIS COMPLETE")
    print("=" * 70)
    print(f"  Canonical facade namespaces : {len(facade_map)}")
    print(f"  Total violations ingested   : {len(violations)}")
    print(f"  Rewrite rules generated     : {len(rewrite_table)}")
    print(f"  AUTO_REPAIRABLE             : {auto}")
    print(f"  OPTIONAL_INTRA_CLUSTER      : {optional}")
    print(f"  MANUAL_REVIEW_REQUIRED      : {manual}")
    print(f"  Output directory            : {OUTPUT_DIR}")
    print("=" * 70)

    if not ok:
        print("\n[VALIDATION] One or more exit checks FAILED.")
        sys.exit(1)
    else:
        print("\n[VALIDATION] All exit conditions satisfied.")


if __name__ == "__main__":
    main()
