#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-FRAG-CLUSTER
# module_name:          fragment_cluster_analyzer
# analysis_domain:      semantic_analysis
# module_role:          clustering
# execution_entry:      run
# mutation_capability:  false
# safety_classification: READ_ONLY
# spec_reference:       [SPEC-AP-V2.1]
# ============================================================

"""
ARCHON PRIME — Fragment Cluster Analyzer
==========================================
Groups fragments within each family into algorithmic clusters using
multi-signal similarity:

    1. Function-name token overlap (Jaccard similarity on word tokens)
    2. Shared dependency/import term signals from fragment_id tokens
    3. Shared source module (same file → strong cohesion signal)
    4. Symbol overlap from fragment_id suffix

Clustering algorithm: greedy union-find based agglomeration.
A pair is merged when combined similarity score ≥ MERGE_THRESHOLD.

Inputs (from OUTPUT_ROOT):
    fragment_family_infrastructure.json
    fragment_family_reasoning.json
    fragment_family_math_symbolic.json

Outputs:
    family_infrastructure_clusters.json
    family_reasoning_clusters.json
    family_math_clusters.json

Each cluster record:
    cluster_id, cluster_theme, fragment_members, representative_functions
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

MERGE_THRESHOLD = 0.25  # combined similarity score to merge two fragments


# ---------------------------------------------------------------------------
# Tokenisation helpers
# ---------------------------------------------------------------------------

_SPLIT_RE = re.compile(r"[_\.\-\s]+")


def _tokens(text: str) -> set[str]:
    """Lower-case word tokens, splitting on underscores, dots, dashes."""
    parts = _SPLIT_RE.split(text.lower())
    return {p for p in parts if len(p) > 2}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------------------
# Similarity scoring (0.0 – 1.0)
# ---------------------------------------------------------------------------

def _similarity(f1: dict, f2: dict) -> float:
    """Multi-signal similarity between two fragment records."""
    name_sim = _jaccard(
        _tokens(f1["function_name"]),
        _tokens(f2["function_name"]),
    )

    id_sim = _jaccard(
        _tokens(f1["fragment_id"]),
        _tokens(f2["fragment_id"]),
    )

    # Same source module → high cohesion bonus
    same_module = 0.4 if f1["source_module"] == f2["source_module"] else 0.0

    # Docstring token overlap
    doc_sim = _jaccard(
        _tokens(f1["fragment_body"].get("docstring", "") or ""),
        _tokens(f2["fragment_body"].get("docstring", "") or ""),
    )

    # Weighted average
    score = 0.35 * name_sim + 0.25 * id_sim + 0.25 * same_module + 0.15 * doc_sim
    return round(score, 4)


# ---------------------------------------------------------------------------
# Union-Find
# ---------------------------------------------------------------------------

class _UF:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------

def _cluster_fragments(records: list[dict], family: str) -> list[dict]:
    """Greedy agglomerative clustering for a list of fragment records."""
    n = len(records)
    if n == 0:
        return []

    uf = _UF(n)

    for i in range(n):
        for j in range(i + 1, n):
            if _similarity(records[i], records[j]) >= MERGE_THRESHOLD:
                uf.union(i, j)

    # Collect groups
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)

    clusters = []
    for cid, (root, members) in enumerate(sorted(groups.items())):
        frags = [records[m] for m in members]
        # Derive cluster theme from the most common function-name token
        all_tokens: list[str] = []
        for f in frags:
            all_tokens.extend(_tokens(f["function_name"]))
        theme_token = max(set(all_tokens), key=all_tokens.count) if all_tokens else family
        rep_fns = sorted({f["function_name"] for f in frags})

        clusters.append({
            "cluster_id": f"{family.upper()}-C{cid:04d}",
            "cluster_theme": theme_token,
            "fragment_count": len(frags),
            "fragment_members": [f["fragment_id"] for f in frags],
            "representative_functions": rep_fns[:10],
            "source_modules": sorted({f["source_module"] for f in frags}),
        })

    return clusters


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

FAMILY_FILES = {
    "infrastructure": ("fragment_family_infrastructure.json", "family_infrastructure_clusters.json"),
    "reasoning": ("fragment_family_reasoning.json", "family_reasoning_clusters.json"),
    "math_symbolic": ("fragment_family_math_symbolic.json", "family_math_clusters.json"),
}


def run(output_root: Path = OUTPUT_ROOT) -> dict[str, list[dict]]:
    """
    Load each family JSON, cluster, and write cluster JSON files.
    Returns dict mapping family → cluster list.
    """
    output_root.mkdir(parents=True, exist_ok=True)

    print("ARCHON PRIME — Fragment Cluster Analyzer")
    print(f"  Output : {output_root}")

    result: dict[str, list[dict]] = {}

    for family, (in_file, out_file) in FAMILY_FILES.items():
        in_path = output_root / in_file
        if not in_path.exists():
            print(f"  [SKIP] {in_file} not found — run fragment_family_builder first")
            result[family] = []
            continue

        data = json.loads(in_path.read_text(encoding="utf-8"))
        records = data.get("fragments", data) if isinstance(data, dict) else data
        print(f"  Clustering {family}: {len(records)} fragments …")

        clusters = _cluster_fragments(records, family)
        result[family] = clusters

        payload = {
            "generated_at": RUN_TS,
            "family": family,
            "merge_threshold": MERGE_THRESHOLD,
            "fragment_count": len(records),
            "cluster_count": len(clusters),
            "clusters": clusters,
        }
        out_path = output_root / out_file
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  [WRITE] {out_path}  ({len(clusters)} clusters)")

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="ARCHON Fragment Cluster Analyzer")
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_ROOT,
        help="Directory containing family JSON files and where clusters are written.",
    )
    args = parser.parse_args()
    run(output_root=args.output)


if __name__ == "__main__":
    main()
