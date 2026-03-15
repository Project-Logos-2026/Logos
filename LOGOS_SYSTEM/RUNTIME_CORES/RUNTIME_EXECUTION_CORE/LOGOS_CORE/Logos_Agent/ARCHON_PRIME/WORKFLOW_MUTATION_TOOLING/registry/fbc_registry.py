#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-012
# module_name:          fbc_registry
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/registry/fbc_registry.py
# responsibility:       Utility module: fbc registry
# runtime_stage:        utility
# execution_entry:      run
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
ARCHON PRIME — DRAC Function Block Core (FBC) Registry Builder
Produces: fbc_master_registry.json, fbc_taxonomy.json, fbc_tag_dictionary.json
          af_core_compatibility_matrix.json, modular_library_manifest.json
Read-only — no source file mutations.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: fbc_registry.py
tool_category: Code_Extraction
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python fbc_registry.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Path constants ─────────────────────────────────────────────────────────────
REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
DRAC_INVAR = (
    REPO_ROOT
    / "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE"
    / "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
    / "DRAC_Core/DRAC_Invariables"
)
MODLIB_OUT = DRAC_INVAR / "Modular_Library"
AF_INVAR = DRAC_INVAR / "APPLICATION_FUNCTIONS"

# Source directories that contribute FBC candidates
AXIOM_DIR = DRAC_INVAR / "SEMANTIC_AXIOMS"
CONTEXT_DIR = DRAC_INVAR / "SEMANTIC_CONTEXTS"
ORCH_DIR = DRAC_INVAR / "ORCHESTRATION_AND_ENTRYPOINTS"
CORE_DIR = DRAC_INVAR / "CORE_CONFIGURATIONS"
AUDIT_DIR = DRAC_INVAR / "DRAC_INVARIABLES_AUDIT"

# ── Tag dictionary — shared compact vocabulary ─────────────────────────────────
# Format: tag_key → {definition, category}
TAG_DICTIONARY: dict[str, dict] = {
    "axiomatic": {
        "definition": "Invariant logical premise applied unconditionally",
        "category": "structural",
    },
    "constraint": {
        "definition": "Precondition or bound that limits execution space",
        "category": "structural",
    },
    "validation": {
        "definition": "Pass/fail gate over a data or state assertion",
        "category": "structural",
    },
    "semantic": {
        "definition": "Relates to meaning, ontology, or token interpretation",
        "category": "domain",
    },
    "reasoning": {
        "definition": "Inference, deduction, or logical derivation capability",
        "category": "domain",
    },
    "planning": {
        "definition": "Goal decomposition and task sequencing capability",
        "category": "domain",
    },
    "agent_runtime": {
        "definition": "Controls or participates in agent lifecycle execution",
        "category": "domain",
    },
    "safety_guard": {
        "definition": "Enforces fail-closed or governance-safe execution",
        "category": "domain",
    },
    "memory_access": {
        "definition": "Reads or writes to a persistent state or knowledge store",
        "category": "domain",
    },
    "tool_interface": {
        "definition": "Integrates with or wraps an external tool or LLM provider",
        "category": "domain",
    },
    "learning": {
        "definition": "Adapts behavior from observations or feedback signals",
        "category": "domain",
    },
    "numeric": {
        "definition": "Performs deterministic mathematical computation",
        "category": "domain",
    },
    "symbolic": {
        "definition": "Operates over symbolic or formal logic representations",
        "category": "domain",
    },
    "probabilistic": {
        "definition": "Incorporates stochastic or Bayesian inference",
        "category": "domain",
    },
    "protocol": {
        "definition": "Defines or enforces a structured communication protocol",
        "category": "structural",
    },
    "orchestration": {
        "definition": "Coordinates sequencing of multiple system components",
        "category": "structural",
    },
    "bootstrap": {
        "definition": "Involved in system startup or initialization",
        "category": "structural",
    },
    "identity": {
        "definition": "Manages or validates agent or resource identity",
        "category": "structural",
    },
    "bijective": {
        "definition": "Implements a one-to-one deterministic mapping",
        "category": "domain",
    },
    "temporal": {
        "definition": "Handles time-based ordering, supersession, or sequencing",
        "category": "domain",
    },
    "trinitarian": {
        "definition": "Applies three-part alignment or scoring logic (3OT)",
        "category": "structural",
    },
    "input_sanitation": {
        "definition": "Cleans and validates external inputs before processing",
        "category": "structural",
    },
    "governance": {
        "definition": "Subject to or enforces project governance contracts",
        "category": "structural",
    },
    "deterministic": {
        "definition": "Produces the same output for the same input (side-effect-free)",
        "category": "structural",
    },
    "stateless": {
        "definition": "Holds no persistent internal state between invocations",
        "category": "structural",
    },
    "stateful": {
        "definition": "Maintains state across invocations or sessions",
        "category": "structural",
    },
    "audited": {
        "definition": "Subject to audit logging or traceability requirements",
        "category": "structural",
    },
    "embedded": {
        "definition": "Directly embedded context in the DRAC invariant layer",
        "category": "structural",
    },
    "numeric_compute": {
        "definition": "Executes arithmetic or algebraic transformations",
        "category": "domain",
    },
    "support_services": {
        "definition": "General-purpose helper with no direct reasoning role",
        "category": "domain",
    },
}

# ── Taxonomy classification rules ──────────────────────────────────────────────
# Source directory → default taxonomy, refined by name heuristics afterward
DIR_TAXONOMY: dict[str, str] = {
    "SEMANTIC_AXIOMS": "axiomatic_core",
    "SEMANTIC_CONTEXTS": "semantic_core",
    "ORCHESTRATION_AND_ENTRYPOINTS": "protocol_core",
    "CORE_CONFIGURATIONS": "protocol_core",
    "DRAC_INVARIABLES_AUDIT": "protocol_core",
}


def _refine_taxonomy(stem: str, source_dir_name: str) -> str:
    s = stem.lower()
    if any(k in s for k in ["valid", "guard", "gate", "constraint", "sanitiz", "3pdn"]):
        return "safety_core"
    if any(
        k in s
        for k in [
            "inference",
            "logic",
            "trinitarian",
            "bijective",
            "recursion",
            "evidence",
            "hypostatic",
            "necessary_exist",
        ]
    ):
        return "inference_core"
    if "plan" in s:
        return "planning_core"
    if any(k in s for k in ["agent", "activation", "dispatch", "policy", "decision"]):
        return "agent_orchestration_core"
    if any(k in s for k in ["context", "initializ", "mode", "bootstrap", "privation"]):
        return "semantic_core"
    if any(k in s for k in ["temporal", "supersession"]):
        return "inference_core"
    if any(k in s for k in ["monolith", "uwm", "read_only", "runtime_input"]):
        return "protocol_core"
    if "memory" in s:
        return "memory_core"
    if any(k in s for k in ["numer", "math", "fractal", "bijection"]):
        return "numeric_core"
    return DIR_TAXONOMY.get(source_dir_name, "protocol_core")


# ── AST metadata extraction ───────────────────────────────────────────────────
def _extract_py_meta(path: Path) -> dict:
    meta: dict[str, Any] = {
        "functions": [],
        "classes": [],
        "docstring": "",
        "imports": [],
    }
    try:
        src = path.read_text(errors="replace")
        tree = ast.parse(src, filename=str(path))
    except SyntaxError:
        return meta
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            name = node.module if isinstance(node, ast.ImportFrom) else None
            if name:
                meta["imports"].append(name)
            elif isinstance(node, ast.Import):
                for a in node.names:
                    meta["imports"].append(a.name)
        elif isinstance(node, ast.FunctionDef):
            meta["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            meta["classes"].append(node.name)
    doc = ast.get_docstring(tree)
    if doc:
        meta["docstring"] = doc[:400]
    return meta


def _infer_tags(stem: str, taxonomy: str, meta: dict, src_dir: str) -> list[str]:
    s = stem.lower()
    h = (meta["docstring"] + " ".join(meta["functions"] + meta["classes"])).lower()
    tags = set()
    # taxonomy-driven base tags
    taxonomy_tags = {
        "axiomatic_core": ["axiomatic", "constraint", "governance"],
        "safety_core": ["safety_guard", "validation", "constraint", "audited"],
        "inference_core": ["reasoning", "symbolic", "deterministic"],
        "semantic_core": ["semantic", "embedded", "governance"],
        "planning_core": ["planning", "orchestration"],
        "agent_orchestration_core": ["agent_runtime", "orchestration", "stateful"],
        "numeric_core": ["numeric", "deterministic", "stateless"],
        "memory_core": ["memory_access", "stateful"],
        "protocol_core": ["protocol", "governance"],
    }
    tags.update(taxonomy_tags.get(taxonomy, ["protocol"]))
    # name / content heuristics
    if "bootstrap" in s or "bootstrap" in h:
        tags.add("bootstrap")
    if "identity" in s or "identity" in h:
        tags.add("identity")
    if "bijective" in s or "bijection" in h:
        tags.add("bijective")
    if "temporal" in s or "temporal" in h:
        tags.add("temporal")
    if "trinitarian" in s:
        tags.add("trinitarian")
    if "sanitiz" in s or "sanitiz" in h:
        tags.add("input_sanitation")
    if "probabilis" in h or "bayes" in h:
        tags.add("probabilistic")
    if "plan" in h:
        tags.add("planning")
    if "tool" in h:
        tags.add("tool_interface")
    if "learn" in h:
        tags.add("learning")
    if "memory" in h or "catalog" in h:
        tags.add("memory_access")
    if "numeric" in h or "math" in h:
        tags.add("numeric_compute")
    if "monolith" in s:
        tags.add("protocol")
    # trim to known vocabulary
    tags = {t for t in tags if t in TAG_DICTIONARY}
    return sorted(tags)


def _describe_purpose(stem: str, meta: dict, taxonomy: str) -> str:
    if meta["docstring"]:
        return meta["docstring"].split("\n")[0].strip()
    # Fallback: synthesize from stem
    words = stem.replace("_", " ")
    role_map = {
        "axiomatic_core": "Axiomatic invariant constraint",
        "safety_core": "Safety validation gate",
        "inference_core": "Inference or logic core",
        "semantic_core": "Semantic context module",
        "planning_core": "Planning or goal-sequencing core",
        "agent_orchestration_core": "Agent orchestration core",
        "numeric_core": "Numeric computation core",
        "memory_core": "Memory or knowledge access core",
        "protocol_core": "Runtime protocol module",
    }
    prefix = role_map.get(taxonomy, "Runtime core")
    return f"{prefix}: {words}"


def _reasoning_domain(taxonomy: str, stem: str) -> str:
    domain_map = {
        "axiomatic_core": "formal_logic",
        "safety_core": "safety_governance",
        "inference_core": "logical_inference",
        "semantic_core": "semantic_processing",
        "planning_core": "goal_planning",
        "agent_orchestration_core": "agent_lifecycle",
        "numeric_core": "mathematical_computation",
        "memory_core": "knowledge_management",
        "protocol_core": "system_protocol",
    }
    return domain_map.get(taxonomy, "general")


# ── Compatible cluster binding ─────────────────────────────────────────────────
# Map taxonomy class → which AF cluster names are directly compatible
TAXONOMY_CLUSTER_AFFINITY: dict[str, list[str]] = {
    "axiomatic_core": ["validation_guard", "reasoning_inference", "support_services"],
    "safety_core": ["validation_guard", "support_services", "agent_runtime"],
    "inference_core": ["reasoning_inference", "learning", "semantic_interpretation"],
    "semantic_core": ["semantic_interpretation", "tool_interface", "support_services"],
    "planning_core": ["planning", "agent_runtime"],
    "agent_orchestration_core": ["agent_runtime", "planning", "memory_access"],
    "numeric_core": ["numerical_compute", "support_services"],
    "memory_core": ["memory_access", "agent_runtime"],
    "protocol_core": ["agent_runtime", "support_services", "tool_interface"],
}


def _compatible_clusters_by_tags(
    fbc_tags: list[str], clusters: list[dict]
) -> list[str]:
    """Return cluster_names whose capability_tags intersect with fbc_tags."""
    fbc_set = set(fbc_tags)
    matched = []
    for cl in clusters:
        cl_tags = set(cl.get("capability_tags", []))
        # Also match by cluster name tokens
        name_tokens = set(cl["cluster_name"].replace("_", " ").split())
        if fbc_set & cl_tags or any(t in " ".join(fbc_tags) for t in name_tokens):
            matched.append(cl["cluster_name"])
    return sorted(set(matched))


# ── Main pipeline ──────────────────────────────────────────────────────────────
def run() -> None:
    print("=" * 60)
    print("ARCHON PRIME — DRAC FBC Registry Builder")
    print("=" * 60)

    # ── Ensure output directory ───────────────────────────────────────────────
    MODLIB_OUT.mkdir(parents=True, exist_ok=True)

    # ── Load AF cluster data ──────────────────────────────────────────────────
    with open(AF_INVAR / "af_cluster_index.json") as f:
        cluster_data = json.load(f)
    af_clusters: list[dict] = cluster_data["clusters"]

    with open(AF_INVAR / "af_master_index.json") as f:
        af_master = json.load(f)
    total_af = af_master["total_af_modules"]
    _af_modules_index = af_master["modules_index"]

    print(f"\n  AF modules from index : {total_af}")
    print(f"  AF clusters loaded    : {len(af_clusters)}")

    # ── Step 1: Discover FBC Candidates ───────────────────────────────────────
    print("\n=== STEP 1: DISCOVER FBC CANDIDATES ===")

    # (source_dir, path, source_dir_name)
    candidates: list[tuple[str, Path, str]] = []
    source_map = {
        "SEMANTIC_AXIOMS": AXIOM_DIR,
        "SEMANTIC_CONTEXTS": CONTEXT_DIR,
        "ORCHESTRATION_AND_ENTRYPOINTS": ORCH_DIR,
    }
    for dir_name, src_dir in source_map.items():
        py_files = sorted(f for f in src_dir.glob("*.py") if f.name != "__init__.py")
        print(f"  {dir_name:40s}: {len(py_files)} candidates")
        for pf in py_files:
            candidates.append((dir_name, pf, dir_name))

    # Also absorb SEMANTIC_AXIOMS catalog JSON entries that don't have Python files
    # (FAM_Axiom_Stub.md is editorial; SEMANTIC_AXIOMS.json is a catalog of active axioms)
    axiom_catalog_path = AXIOM_DIR / "SEMANTIC_AXIOMS.json"
    axiom_catalog_ids: set[str] = set()
    if axiom_catalog_path.exists():
        with open(axiom_catalog_path) as f:
            ax_cat = json.load(f)
        for ax in ax_cat.get("axioms", []):
            axiom_catalog_ids.add(ax["id"])

    # CoreConfig is structural — register as one protocol_core
    core_cfg_path = CORE_DIR / "CoreConfig_0001.json"

    print(f"\n  Total Python FBC candidates: {len(candidates)}")

    # ── Step 2 + 3: Semantic extraction + taxonomy ────────────────────────────
    print("\n=== STEP 2+3: EXTRACT METADATA + CLASSIFY ===")

    fbc_entries: list[dict] = []
    fbc_counter = 0
    taxonomy_dist: dict[str, int] = defaultdict(int)

    for _, py_file, src_dir_name in candidates:
        fbc_counter += 1
        fbc_id = f"FBC_{fbc_counter:04d}"
        stem = py_file.stem
        meta = _extract_py_meta(py_file)
        taxonomy = _refine_taxonomy(stem, src_dir_name)
        tags = _infer_tags(stem, taxonomy, meta, src_dir_name)
        purpose = _describe_purpose(stem, meta, taxonomy)
        domain = _reasoning_domain(taxonomy, stem)
        compat_c = _compatible_clusters_by_tags(tags, af_clusters)

        taxonomy_dist[taxonomy] += 1
        print(f"  {fbc_id}  {stem:45s} → {taxonomy}")

        fbc_entries.append(
            {
                "core_id": fbc_id,
                "core_name": stem,
                "source_file": str(py_file.relative_to(REPO_ROOT)),
                "source_directory": src_dir_name,
                "taxonomy_class": taxonomy,
                "reasoning_domain": domain,
                "purpose": purpose,
                "functions": meta["functions"],
                "classes": meta["classes"],
                "dependencies": meta["imports"],
                "tags": tags,
                "compatible_clusters": compat_c,
                "structural_role": taxonomy.replace("_core", "")
                .replace("_", " ")
                .title(),
            }
        )

    # Register CoreConfig as an additional protocol_core entry
    fbc_counter += 1
    fbc_entries.append(
        {
            "core_id": f"FBC_{fbc_counter:04d}",
            "core_name": "CoreConfig_0001",
            "source_file": str(core_cfg_path.relative_to(REPO_ROOT)),
            "source_directory": "CORE_CONFIGURATIONS",
            "taxonomy_class": "protocol_core",
            "reasoning_domain": "system_protocol",
            "purpose": "Canonical DRAC core configuration — axiom set binding, constraint flags",
            "functions": [],
            "classes": [],
            "dependencies": [],
            "tags": [
                "protocol",
                "axiomatic",
                "constraint",
                "governance",
                "deterministic",
            ],
            "compatible_clusters": ["agent_runtime", "support_services"],
            "structural_role": "Protocol",
        }
    )
    taxonomy_dist["protocol_core"] += 1
    print(
        f"  FBC_{fbc_counter:04d}  CoreConfig_0001                                    → protocol_core"
    )

    print(f"\n  Total FBCs: {len(fbc_entries)}")

    # ── Step 4: Build FBC taxonomy document ───────────────────────────────────
    print("\n=== STEP 4: BUILD TAXONOMY DOCUMENT ===")
    TAXONOMY_DEFINITIONS = {
        "axiomatic_core": "Invariant logical premises applied unconditionally before any reasoning step",
        "safety_core": "Fail-closed safety gates, validators, and governance enforcement modules",
        "inference_core": "Logical inference, symbolic reasoning, and deduction engines",
        "semantic_core": "Semantic context handlers and meaning-extraction scaffolding",
        "planning_core": "Goal decomposition, task sequencing, and plan representation",
        "agent_orchestration_core": "Agent lifecycle control, dispatch, and policy decision modules",
        "numeric_core": "Deterministic mathematical and algebraic computation modules",
        "memory_core": "Persistent-state access, knowledge catalog, and storage interfaces",
        "protocol_core": "System-level runtime protocol, orchestration, and bootstrap modules",
    }

    fbc_taxonomy = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "taxonomy_classes": {
            cls: {
                "definition": defn,
                "count": taxonomy_dist.get(cls, 0),
            }
            for cls, defn in TAXONOMY_DEFINITIONS.items()
        },
        "distribution": dict(sorted(taxonomy_dist.items())),
    }
    for cls, count in sorted(taxonomy_dist.items()):
        print(f"  {cls:30s}: {count}")

    # ── Step 5: Build compatibility matrix ────────────────────────────────────
    print("\n=== STEP 5: BUILD COMPATIBILITY MATRIX ===")

    # cluster_name → set of AF IDs
    cluster_to_af_ids: dict[str, list[str]] = {}
    for cl in af_clusters:
        cluster_to_af_ids[cl["cluster_name"]] = cl["modules"]

    # cluster_id → cluster_name lookup
    _cluster_id_to_name: dict[str, str] = {
        cl["cluster_id"]: cl["cluster_name"] for cl in af_clusters
    }

    compat_matrix: list[dict] = []
    total_bindings = 0

    for fbc in fbc_entries:
        compat_clusters = fbc["compatible_clusters"]
        compat_af_ids = []
        compat_scores: dict[str, float] = {}

        for cl_name in compat_clusters:
            af_ids = cluster_to_af_ids.get(cl_name, [])
            compat_af_ids.extend(af_ids)
            # Placeholder score: tag overlap depth / total tags (normalized)
            cl_obj = next(
                (c for c in af_clusters if c["cluster_name"] == cl_name), None
            )
            if cl_obj:
                cl_tags = set(cl_obj.get("capability_tags", []))
                fbc_tags = set(fbc["tags"])
                overlap = len(cl_tags & fbc_tags)
                score = round(overlap / max(len(fbc_tags), 1), 2) if overlap else 0.1
                compat_scores[cl_name] = score

        compat_af_ids_unique = sorted(set(compat_af_ids))
        total_bindings += len(compat_af_ids_unique)

        compat_matrix.append(
            {
                "core_id": fbc["core_id"],
                "core_name": fbc["core_name"],
                "taxonomy_class": fbc["taxonomy_class"],
                "compatible_clusters": compat_clusters,
                "compatible_af_ids": compat_af_ids_unique,
                "compatibility_score": compat_scores,
                "af_binding_count": len(compat_af_ids_unique),
            }
        )
        if compat_clusters:
            print(
                f"  {fbc['core_id']}  {fbc['core_name']:40s} ↔ {', '.join(compat_clusters)}"
            )

    print(f"\n  Total AF↔Core bindings: {total_bindings}")

    # ── Step 6: Master registry ───────────────────────────────────────────────
    print("\n=== STEP 6: MASTER REGISTRY ===")

    fbc_master_registry = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_cores": len(fbc_entries),
        "taxonomy_distribution": dict(sorted(taxonomy_dist.items())),
        "cores": fbc_entries,
    }

    # ── Step 7: Modular Library Manifest ─────────────────────────────────────
    tags_used = sorted(set(t for fbc in fbc_entries for t in fbc["tags"]))
    modular_manifest = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_af_modules": total_af,
        "total_af_clusters": len(af_clusters),
        "total_cores": len(fbc_entries),
        "compatibility_bindings": total_bindings,
        "tag_dictionary_size": len(TAG_DICTIONARY),
        "tags_in_use": len(tags_used),
        "taxonomy_classes": len(TAXONOMY_DEFINITIONS),
        "source_directories": list(source_map.keys()) + ["CORE_CONFIGURATIONS"],
        "output_files": [
            "fbc_master_registry.json",
            "fbc_taxonomy.json",
            "fbc_tag_dictionary.json",
            "af_core_compatibility_matrix.json",
            "modular_library_manifest.json",
        ],
    }

    # ── Step 8: Validation ────────────────────────────────────────────────────
    print("\n=== STEP 8: VALIDATION ===")
    core_ids = [f["core_id"] for f in fbc_entries]
    assert len(core_ids) == len(set(core_ids)), "DUPLICATE FBC IDs DETECTED"
    assert all(f["taxonomy_class"] for f in fbc_entries), "FBC missing taxonomy class"
    assert all(f["core_id"] for f in fbc_entries), "FBC missing core_id"
    # All AF clusters referenced in at least one core?
    all_compat = set(cl for fbc in fbc_entries for cl in fbc["compatible_clusters"])
    uncovered = set(cl["cluster_name"] for cl in af_clusters) - all_compat
    if uncovered:
        print(
            f"  NOTE: {len(uncovered)} clusters with no direct core binding: {sorted(uncovered)}"
        )
    else:
        print("  All AF clusters referenced in at least one FBC. ✓")
    assert TAG_DICTIONARY, "Tag dictionary is empty"
    print("  No duplicate FBC IDs. ✓")
    print("  All FBCs have taxonomy class. ✓")
    print(f"  Tag dictionary: {len(TAG_DICTIONARY)} entries. ✓")

    # ── Step 9: Write Output Files ────────────────────────────────────────────
    print("\n=== STEP 9: WRITE OUTPUT FILES ===")

    files = {
        "fbc_master_registry.json": fbc_master_registry,
        "fbc_taxonomy.json": fbc_taxonomy,
        "fbc_tag_dictionary.json": {"schema_version": "1.0.0", "tags": TAG_DICTIONARY},
        "af_core_compatibility_matrix.json": {
            "schema_version": "1.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "compatibility_matrix": compat_matrix,
        },
        "modular_library_manifest.json": modular_manifest,
    }

    for fname, content in files.items():
        out_path = MODLIB_OUT / fname
        with open(out_path, "w") as f:
            json.dump(content, f, indent=2)
        size_kb = out_path.stat().st_size / 1024
        print(f"  Written: {out_path.relative_to(REPO_ROOT)}  ({size_kb:.1f} KB)")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("FBC REGISTRY COMPLETE")
    print(f"  Cores discovered:        {len(fbc_entries)}")
    print(f"  Taxonomy classes:        {len(taxonomy_dist)}")
    print(f"  AF clusters linked:      {len(af_clusters)}")
    print(f"  Compatibility bindings:  {total_bindings}")
    print(f"  Tag dictionary size:     {len(TAG_DICTIONARY)}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run()
    except AssertionError as e:
        print(f"\n  VALIDATION FAILED: {e}")
        err = {"status": "FAILED", "error": str(e)}
        MODLIB_OUT.mkdir(parents=True, exist_ok=True)
        with open(MODLIB_OUT / "fbc_registry_error.json", "w") as f:
            json.dump(err, f, indent=2)
        sys.exit(1)
    except Exception as e:
        print(f"\n  UNEXPECTED ERROR: {e}")
        import traceback

        traceback.print_exc()

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


# [AP-NORM-REPAIR] orphaned exception handler body removed (duplicate of __main__ except block)
