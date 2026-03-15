#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-RECON-PLAN
# module_name:          module_reconstruction_planner
# analysis_domain:      semantic_analysis
# module_role:          planning
# execution_entry:      run
# mutation_capability:  false
# safety_classification: READ_ONLY
# spec_reference:       [SPEC-AP-V2.1]
# ============================================================

"""
ARCHON PRIME — Module Reconstruction Planner
=============================================
Creates reconstruction blueprints (plans) for clean Logos modules
by joining cluster outputs with runtime domain mappings.

Inputs (from OUTPUT_ROOT):
    family_infrastructure_clusters.json
    family_reasoning_clusters.json
    family_math_clusters.json
    fragment_runtime_mapping.json
    logic_fragments.json            (for dependency extraction)

Output:
    fragment_module_reconstruction_plan.json

Each plan entry:
    module_name               — proposed module name (snake_case)
    cluster_source            — originating cluster_id
    fragment_count            — number of fragments in cluster
    target_runtime_domain     — SOP | SCP | ARP | MTP
    confidence_score          — from runtime mapper
    dependency_requirements   — inferred from fragment IDs / args
    integration_notes         — guidance for the engineer
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"

OUTPUT_ROOT = Path(
    os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT)
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SPLIT_RE = re.compile(r"[_\.\-\s]+")


def _snake(text: str) -> str:
    """Convert a token string to snake_case module name."""
    parts = [p for p in _SPLIT_RE.split(text.lower()) if p and len(p) > 1]
    return "_".join(parts) if parts else "unnamed_module"


def _infer_deps(fragment_ids: list[str], frag_lookup: dict) -> list[str]:
    """
    Extract dependency hints from fragment IDs and args.
    Returns a de-duplicated sorted list of plausible dependency tokens.
    """
    dep_signals: set[str] = set()
    stdlib = {"os", "sys", "re", "json", "math", "typing", "collections",
               "pathlib", "datetime", "functools", "itertools", "abc"}

    for fid in fragment_ids[:30]:
        frag = frag_lookup.get(fid)
        if not frag:
            continue
        # Inspect args for typed hints
        for arg in frag.get("args", []):
            token = _SPLIT_RE.split(str(arg).lower())[0]
            if token and token not in stdlib and len(token) > 2:
                dep_signals.add(token)
        # Inspect docstring
        doc = frag.get("docstring", "") or ""
        for tok in _SPLIT_RE.split(doc.lower()):
            if tok in {"numpy", "scipy", "torch", "sklearn", "pandas",
                       "networkx", "pydantic", "fastapi", "aiohttp"}:
                dep_signals.add(tok)

    return sorted(dep_signals)


def _integration_note(domain: str, theme: str, n_frags: int, confidence: float) -> str:
    notes = {
        "SCP": (
            "Integrate with the Semantic Coherence Protocol layer. "
            "Ensure all belief-update calls are wrapped in a coherence gate. "
            "Review contradiction handling before integration."
        ),
        "ARP": (
            "Integrate with the Adaptive Reasoning Protocol layer. "
            "Register inference functions with the ARP dispatcher. "
            "Annotate probabilistic outputs with confidence metadata."
        ),
        "MTP": (
            "Integrate with the Modal Translation Protocol layer. "
            "Ensure symbol translation functions accept and return canonical Modal AST nodes. "
            "Map ontology terms to the MTP vocabulary before use."
        ),
        "SOP": (
            "Integrate as a Standard Operating utility module. "
            "Register with the SOP registry if load-at-boot behaviour is required. "
            "Add governance assertion for any side-effecting calls."
        ),
    }
    base = notes.get(domain, "Review integration path before use.")
    conf_warn = " [LOW CONFIDENCE — manual domain review recommended]" if confidence < 0.5 else ""
    return (
        f"Cluster theme: '{theme}'. {n_frags} fragments. "
        f"Target domain: {domain}.{conf_warn} "
        f"{base}"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

CLUSTER_FILES = [
    "family_infrastructure_clusters.json",
    "family_reasoning_clusters.json",
    "family_math_clusters.json",
]


def run(output_root: Path = OUTPUT_ROOT) -> list[dict]:
    """Build reconstruction plans from cluster + mapping data."""
    output_root.mkdir(parents=True, exist_ok=True)

    print("ARCHON PRIME — Module Reconstruction Planner")
    print(f"  Output : {output_root}")

    # Load runtime mapping index: cluster_id → mapping record
    rmap_path = output_root / "fragment_runtime_mapping.json"
    if not rmap_path.exists():
        raise FileNotFoundError(
            "fragment_runtime_mapping.json not found — run fragment_runtime_mapper first."
        )
    rmap_data = json.loads(rmap_path.read_text(encoding="utf-8"))
    rmap_list = rmap_data.get("mappings", rmap_data) if isinstance(rmap_data, dict) else rmap_data
    rmap: dict[str, dict] = {m["cluster_id"]: m for m in rmap_list}

    # Load raw fragments for dependency mining
    frag_path = output_root / "logic_fragments.json"
    frag_list = json.loads(frag_path.read_text(encoding="utf-8")) if frag_path.exists() else []
    frag_lookup: dict[str, dict] = {f["fragment_id"]: f for f in frag_list}

    # Collect all clusters
    all_clusters: list[dict] = []
    for fname in CLUSTER_FILES:
        p = output_root / fname
        if not p.exists():
            print(f"  [SKIP] {fname}")
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        clusters = data.get("clusters", data) if isinstance(data, dict) else data
        all_clusters.extend(clusters)

    print(f"  Total clusters: {len(all_clusters)}")

    plans: list[dict] = []
    seen_names: dict[str, int] = defaultdict(int)

    for cluster in all_clusters:
        cid = cluster["cluster_id"]
        theme = cluster.get("cluster_theme", "unnamed")
        n_frags = cluster.get("fragment_count", len(cluster.get("fragment_members", [])))
        members = cluster.get("fragment_members", [])

        mapping = rmap.get(cid, {})
        domain = mapping.get("recommended_runtime_domain", "SOP")
        conf = mapping.get("confidence_score", 0.0)

        # Build proposed module name
        base_name = _snake(f"{domain.lower()}_{theme}")
        seen_names[base_name] += 1
        suffix = f"_{seen_names[base_name]}" if seen_names[base_name] > 1 else ""
        module_name = f"{base_name}{suffix}"

        deps = _infer_deps(members, frag_lookup)

        plans.append({
            "module_name": module_name,
            "cluster_source": cid,
            "fragment_count": n_frags,
            "target_runtime_domain": domain,
            "confidence_score": conf,
            "fragment_members": members,
            "dependency_requirements": deps,
            "integration_notes": _integration_note(domain, theme, n_frags, conf),
        })

    payload = {
        "generated_at": RUN_TS,
        "total_plans": len(plans),
        "plans": plans,
    }

    out_path = output_root / "fragment_module_reconstruction_plan.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [WRITE] {out_path}  ({len(plans)} plans)")

    return plans


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="ARCHON Module Reconstruction Planner")
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_ROOT,
        help="Directory to read inputs from and write plan to.",
    )
    args = parser.parse_args()
    run(output_root=args.output)


if __name__ == "__main__":
    main()
