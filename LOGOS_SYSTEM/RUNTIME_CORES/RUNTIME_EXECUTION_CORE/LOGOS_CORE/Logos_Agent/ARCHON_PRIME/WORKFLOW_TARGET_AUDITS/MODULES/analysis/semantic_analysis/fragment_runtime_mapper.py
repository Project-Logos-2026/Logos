#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-FRAG-RTMAP
# module_name:          fragment_runtime_mapper
# analysis_domain:      semantic_analysis
# module_role:          mapping
# execution_entry:      run
# mutation_capability:  false
# safety_classification: READ_ONLY
# spec_reference:       [SPEC-AP-V2.1]
# ============================================================

"""
ARCHON PRIME — Fragment Runtime Mapper
========================================
Determines which Logos runtime domain each cluster belongs to.

Runtime domains:
    SOP  — Standard Operating Procedures (utility / orchestration)
    SCP  — Semantic Coherence Protocol   (belief / coherence / proof)
    ARP  — Adaptive Reasoning Protocol   (inference / deduction / bayes)
    MTP  — Modal Translation Protocol    (symbol / ontology / NLP)

Mapping signals analysed for each cluster:
    - representative function names
    - source module paths
    - cluster theme token
    - fragment IDs

Output:
    fragment_runtime_mapping.json

Each record:
    cluster_id
    recommended_runtime_domain
    confidence_score          (0.0–1.0)
    signal_scores             (per-domain raw scores)
    reasoning                 (human-readable rationale)
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"

OUTPUT_ROOT = Path(
    os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT)
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# Domain signal lexicons
# ---------------------------------------------------------------------------

DOMAIN_SIGNALS: dict[str, set[str]] = {
    "SCP": {
        "scp", "coherence", "contradiction", "belief", "proof",
        "modal", "consistency", "verify", "validate", "truth",
        "axiom", "logic", "resolution", "entail",
    },
    "ARP": {
        "arp", "reason", "infer", "inference", "logic", "bayesian",
        "bayes", "deduct", "deduction", "abduct", "abduction",
        "hypothesis", "evidence", "probability", "posterior",
        "prior", "plan", "decision", "reasoning",
    },
    "MTP": {
        "mtp", "semantic", "translate", "translation", "ontology",
        "symbol", "nlp", "token", "embed", "embedding", "parse",
        "natural", "language", "text", "transform", "encode",
    },
    "SOP": {
        "util", "utility", "helper", "config", "registry",
        "log", "logger", "monitor", "load", "loader", "bridge",
        "init", "setup", "run", "execute", "dispatch",
        "pipeline", "workflow", "orchestrat",
    },
}

_SPLIT_RE = re.compile(r"[_\.\-\s]+")


def _tokens(text: str) -> list[str]:
    parts = _SPLIT_RE.split(text.lower())
    return [p for p in parts if len(p) > 2]


def _score_domain(texts: list[str], domain: str) -> float:
    """Count signal keyword hits in combined text for a domain."""
    signals = DOMAIN_SIGNALS[domain]
    all_toks = []
    for t in texts:
        all_toks.extend(_tokens(t))
    hits = sum(1 for t in all_toks if t in signals)
    return hits / max(len(all_toks), 1)


# ---------------------------------------------------------------------------
# Core mapping logic
# ---------------------------------------------------------------------------

def _map_cluster(cluster: dict) -> dict:
    texts = (
        cluster.get("representative_functions", [])
        + cluster.get("source_modules", [])
        + [cluster.get("cluster_theme", "")]
        + cluster.get("fragment_members", [])[:20]
    )

    scores = {d: round(_score_domain(texts, d), 4) for d in DOMAIN_SIGNALS}

    best_domain = max(scores, key=lambda d: scores[d])
    best_score = scores[best_domain]

    # If all scores are 0.0 (no signals) default to SOP
    if best_score == 0.0:
        best_domain = "SOP"
        confidence = 0.1
    else:
        # Normalise score to rough confidence: cap at 1.0
        raw_conf = min(best_score * 10, 1.0)
        # Penalty if two domains are tied (ambiguous)
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) >= 2 and sorted_scores[1] > 0 and (sorted_scores[0] / max(sorted_scores[1], 1e-9)) < 1.5:
            confidence = round(raw_conf * 0.8, 4)
        else:
            confidence = round(raw_conf, 4)

    reasoning = (
        f"Domain '{best_domain}' scored highest ({scores[best_domain]:.4f}). "
        f"Full scores: {scores}. "
        f"Theme token: '{cluster.get('cluster_theme', '')}'. "
        f"Fragment count: {cluster.get('fragment_count', 0)}."
    )

    return {
        "cluster_id": cluster["cluster_id"],
        "recommended_runtime_domain": best_domain,
        "confidence_score": confidence,
        "signal_scores": scores,
        "reasoning": reasoning,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

CLUSTER_FILES = [
    "family_infrastructure_clusters.json",
    "family_reasoning_clusters.json",
    "family_math_clusters.json",
]


def run(output_root: Path = OUTPUT_ROOT) -> list[dict]:
    """Load all cluster files, map each cluster to a runtime domain, write output."""
    output_root.mkdir(parents=True, exist_ok=True)

    print("ARCHON PRIME — Fragment Runtime Mapper")
    print(f"  Output : {output_root}")

    all_clusters: list[dict] = []
    for fname in CLUSTER_FILES:
        p = output_root / fname
        if not p.exists():
            print(f"  [SKIP] {fname} not found")
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        clusters = data.get("clusters", data) if isinstance(data, dict) else data
        all_clusters.extend(clusters)

    print(f"  Total clusters to map: {len(all_clusters)}")

    mappings = [_map_cluster(c) for c in all_clusters]

    # Summary counts per domain
    from collections import Counter
    domain_counts = Counter(m["recommended_runtime_domain"] for m in mappings)

    payload = {
        "generated_at": RUN_TS,
        "total_clusters": len(mappings),
        "domain_distribution": dict(domain_counts),
        "mappings": mappings,
    }

    out_path = output_root / "fragment_runtime_mapping.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [WRITE] {out_path}  ({len(mappings)} mappings)")
    print(f"  Domain distribution: {dict(domain_counts)}")

    return mappings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="ARCHON Fragment Runtime Mapper")
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_ROOT,
        help="Directory containing cluster JSON files and where mapping is written.",
    )
    args = parser.parse_args()
    run(output_root=args.output)


if __name__ == "__main__":
    main()
