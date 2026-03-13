#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-075
# module_name:          extract
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/semantic_extraction/extract.py
# responsibility:       Analysis module: extract
# runtime_stage:        analysis
# execution_entry:      None
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
ARCHON PRIME — Application Function Extraction Pass
Semantic-Heuristic Analysis Pipeline (Read-Only)
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: extract.py
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
python extract.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent

TARGET_DIRS = [
    REPO_ROOT / "LOGOS_SYSTEM",
    REPO_ROOT / "STARTUP",
]

# Also scan System_Stack and PYTHON_MODULES if they exist
OPTIONAL_DIRS = [
    REPO_ROOT / "System_Stack",
    REPO_ROOT / "PYTHON_MODULES",
]

EXCLUDE_PARTS = {"__pycache__", "tests", "test", "ARCHIVE", "archive", "reports"}

OUT_DIR = REPO_ROOT / "Application_Function_Extraction"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SIGNAL_KEYWORDS = {
    "execute",
    "resolve",
    "apply",
    "determine",
    "select",
    "infer",
    "gate",
    "normalize",
    "translate",
    "inject",
    "compose",
    "reconstruct",
}

# Minimum words in a docstring to consider it non-trivial
MIN_WORDS = 5

# TF-IDF / clustering
N_CLUSTERS_MIN = 10
N_CLUSTERS_MAX = 20


# ---------------------------------------------------------------------------
# STEP 1 — AST PARSING
# ---------------------------------------------------------------------------


def should_exclude(path: Path) -> bool:
    return bool(EXCLUDE_PARTS.intersection(path.parts))


def collect_python_files(dirs):
    files = []
    for base in dirs:
        if not base.exists():
            print(f"  [SKIP] {base} — does not exist")
            continue
        for py in base.rglob("*.py"):
            if not should_exclude(py):
                files.append(py)
    return files


def extract_docstrings(py_path: Path, repo_root: Path):
    rel = str(py_path.relative_to(repo_root))
    try:
        source = py_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  [WARN] Cannot read {rel}: {e}", file=sys.stderr)
        return []

    try:
        tree = ast.parse(source, filename=str(py_path))
    except SyntaxError as e:
        print(f"  [WARN] SyntaxError in {rel}:{e.lineno} — {e.msg}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  [WARN] AST error in {rel}: {e}", file=sys.stderr)
        return []

    records = []

    for node in ast.walk(tree):
        if isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            doc = ast.get_docstring(node, clean=True)
            if not doc:
                continue

            if isinstance(node, ast.Module):
                symbol = "<module>"
                lineno = 1
            else:
                symbol = getattr(node, "name", "<unknown>")
                lineno = getattr(node, "lineno", 0)

            records.append(
                {
                    "file_path": rel,
                    "symbol_name": symbol,
                    "docstring_text": doc,
                    "line_number": lineno,
                }
            )

    return records


def step1_ast_parse(dirs):
    print("\n=== STEP 1: AST PARSING ===")
    py_files = collect_python_files(dirs)
    print(f"  Python files found: {len(py_files)}")

    all_records = []
    for pf in py_files:
        recs = extract_docstrings(pf, REPO_ROOT)
        all_records.extend(recs)

    print(f"  Total docstrings extracted: {len(all_records)}")

    out = OUT_DIR / "application_function_candidates.json"
    out.write_text(json.dumps(all_records, indent=2, ensure_ascii=False))
    print(f"  Written: {out}")
    return all_records


# ---------------------------------------------------------------------------
# STEP 2 — HEURISTIC FILTERING
# ---------------------------------------------------------------------------


def score_docstring(text: str) -> dict:
    """Return match info for signal keywords in a docstring."""
    lower = text.lower()
    words = re.findall(r"\b\w+\b", lower)
    word_set = set(words)

    matched = SIGNAL_KEYWORDS.intersection(word_set)

    # also catch compound phrases like "gate_selection", "execute_block", etc.
    compound_matches = set()
    for kw in SIGNAL_KEYWORDS:
        if kw in lower:
            compound_matches.add(kw)

    all_matched = matched | compound_matches
    return {
        "matched_keywords": sorted(all_matched),
        "match_count": len(all_matched),
        "word_count": len(words),
    }


def is_trivial(doc: str) -> bool:
    words = re.findall(r"\b\w+\b", doc)
    if len(words) < MIN_WORDS:
        return True
    # Pure "documentation only" pattern: very short, no verbs/action words
    return False


def step2_filter(candidates: list):
    print("\n=== STEP 2: HEURISTIC FILTERING ===")
    filtered = []
    for rec in candidates:
        doc = rec["docstring_text"]
        if is_trivial(doc):
            continue
        score = score_docstring(doc)
        if score["match_count"] == 0:
            continue
        rec = dict(rec)  # copy
        rec["matched_keywords"] = score["matched_keywords"]
        rec["keyword_match_count"] = score["match_count"]
        rec["word_count"] = score["word_count"]
        filtered.append(rec)

    print(f"  Candidates after filtering: {len(filtered)}")

    out = OUT_DIR / "application_function_filtered.json"
    out.write_text(json.dumps(filtered, indent=2, ensure_ascii=False))
    print(f"  Written: {out}")
    return filtered


# ---------------------------------------------------------------------------
# STEP 3 — TF-IDF VECTORIZATION (Pure Python, no sklearn dependency)
# ---------------------------------------------------------------------------


def tokenize(text: str):
    return re.findall(r"\b[a-z][a-z0-9_]{2,}\b", text.lower())


def build_tfidf(docs: list):
    """
    Lightweight TF-IDF using pure Python.
    Returns: (doc_vectors as list of dict, idf_map)
    """
    N = len(docs)
    # Build term → document frequency
    df = Counter()
    tokenized = []
    for doc in docs:
        tokens = tokenize(doc)
        tokenized.append(tokens)
        for term in set(tokens):
            df[term] += 1

    # IDF
    idf = {term: math.log((N + 1) / (freq + 1)) + 1 for term, freq in df.items()}

    # TF-IDF vectors as dicts
    vectors = []
    for tokens in tokenized:
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        vec = {term: (count / total) * idf.get(term, 0) for term, count in tf.items()}
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vec = {k: v / norm for k, v in vec.items()}
        vectors.append(vec)

    return vectors, idf


def vec_to_list(vec: dict, vocab: list) -> list:
    return [vec.get(w, 0.0) for w in vocab]


def step3_vectorize(filtered: list):
    print("\n=== STEP 3: TF-IDF VECTORIZATION ===")
    docs = [r["docstring_text"] for r in filtered]
    vectors, idf = build_tfidf(docs)

    # Top 200 vocab by IDF weight (most discriminative)
    vocab = sorted(idf, key=lambda w: -idf[w])[:200]

    # Serialize: store top-10 terms per vector as readable signature
    embeddings = []
    for i, (rec, vec) in enumerate(zip(filtered, vectors, strict=False)):
        top_terms = sorted(vec, key=lambda w: -vec[w])[:10]
        _dense = vec_to_list(vec, vocab)
        embeddings.append(
            {
                "index": i,
                "file_path": rec["file_path"],
                "symbol_name": rec["symbol_name"],
                "line_number": rec["line_number"],
                "semantic_signature": top_terms,
                "vector_dim": len(vocab),
            }
        )

    out = OUT_DIR / "application_function_embeddings.json"
    out.write_text(json.dumps(embeddings, indent=2, ensure_ascii=False))
    print(f"  Vocabulary size: {len(vocab)}")
    print(f"  Vectors generated: {len(embeddings)}")
    print(f"  Written: {out}")
    return vectors, vocab, embeddings


# ---------------------------------------------------------------------------
# STEP 4 — CLUSTERING (Pure Python KMeans-style)
# ---------------------------------------------------------------------------


def dot(a: dict, b: dict) -> float:
    """Dot product of two sparse vectors."""
    # Iterate over smaller dict
    if len(a) > len(b):
        a, b = b, a
    return sum(a[k] * b.get(k, 0.0) for k in a)


def cosine_sim(a: dict, b: dict) -> float:
    return dot(a, b)  # vectors are already L2-normalized


def kmeans_cosine(vectors: list, k: int, max_iter: int = 50):
    """
    Simple KMeans with cosine distance on sparse dicts.
    Initialization: spread seeds by picking maximally distant items.
    """
    import random

    random.seed(42)

    n = len(vectors)
    if n <= k:
        return list(range(n))

    # KMeans++ init (simplified)
    centroids = [vectors[0]]
    for _ in range(k - 1):
        # Pick next centroid furthest from existing centroids
        best_idx, best_dist = 0, -1.0
        sample_size = min(n, 500)
        candidates = random.sample(range(n), sample_size)
        for i in candidates:
            min_sim = max(cosine_sim(vectors[i], c) for c in centroids)
            dist = 1.0 - min_sim
            if dist > best_dist:
                best_dist = dist
                best_idx = i
        centroids.append(vectors[best_idx])

    labels = [0] * n

    for iteration in range(max_iter):
        # Assignment
        new_labels = []
        for vec in vectors:
            sims = [cosine_sim(vec, c) for c in centroids]
            new_labels.append(sims.index(max(sims)))

        # Convergence check
        if new_labels == labels and iteration > 0:
            print(f"    Converged at iteration {iteration}")
            break
        labels = new_labels

        # Update centroids
        cluster_sums = defaultdict(lambda: defaultdict(float))
        cluster_counts = Counter(labels)
        for i, vec in enumerate(vectors):
            c = labels[i]
            for term, val in vec.items():
                cluster_sums[c][term] += val

        new_centroids = []
        for c in range(k):
            if cluster_counts[c] == 0:
                new_centroids.append(centroids[c])
                continue
            centroid = dict(cluster_sums[c])
            # Normalize
            norm = math.sqrt(sum(v * v for v in centroid.values())) or 1.0
            centroid = {term: v / norm for term, v in centroid.items()}
            new_centroids.append(centroid)
        centroids = new_centroids

    return labels


def pick_k(n: int) -> int:
    """Pick cluster count between 10 and 20 based on corpus size."""
    if n <= N_CLUSTERS_MIN:
        return max(2, n // 2)
    if n <= 50:
        return N_CLUSTERS_MIN
    if n <= 200:
        return 15
    return N_CLUSTERS_MAX


def cluster_top_terms(vectors: list, labels: list, k: int):
    """Return top 10 terms for each cluster centroid."""
    cluster_sums = defaultdict(lambda: defaultdict(float))
    for i, vec in enumerate(vectors):
        c = labels[i]
        for term, val in vec.items():
            cluster_sums[c][term] += val
    result = {}
    for c in range(k):
        top = sorted(cluster_sums[c], key=lambda w: -cluster_sums[c][w])[:10]
        result[c] = top
    return result


def step4_cluster(filtered: list, vectors: list, embeddings: list):
    print("\n=== STEP 4: CLUSTERING ===")
    n = len(vectors)
    k = pick_k(n)
    print(f"  Items to cluster: {n}, K={k}")

    if n < 2:
        labels = [0] * n
        k = 1
    else:
        labels = kmeans_cosine(vectors, k)

    top_terms = cluster_top_terms(vectors, labels, k)

    cluster_dist = Counter(labels)
    print(
        "  Cluster sizes: "
        + ", ".join(f"C{c}:{cluster_dist[c]}" for c in sorted(cluster_dist))
    )

    # Build output
    cluster_entries = []
    for i, (rec, emb) in enumerate(zip(filtered, embeddings, strict=False)):
        cluster_id = labels[i]
        cluster_entries.append(
            {
                "index": i,
                "cluster_id": cluster_id,
                "cluster_label": f"cluster_{cluster_id:02d}",
                "cluster_top_terms": top_terms.get(cluster_id, []),
                "file_path": rec["file_path"],
                "symbol_name": rec["symbol_name"],
                "line_number": rec["line_number"],
                "matched_keywords": rec["matched_keywords"],
                "semantic_signature": emb["semantic_signature"],
            }
        )

    out = OUT_DIR / "application_function_clusters.json"
    out.write_text(json.dumps(cluster_entries, indent=2, ensure_ascii=False))
    print(f"  Written: {out}")
    return cluster_entries, k, top_terms


# ---------------------------------------------------------------------------
# STEP 5 — REGISTRY GENERATION
# ---------------------------------------------------------------------------


def derive_module(file_path: str) -> str:
    """Convert file_path to module notation."""
    p = file_path.replace("/", ".").replace("\\", ".")
    if p.endswith(".py"):
        p = p[:-3]
    return p


def step5_registry(filtered: list, cluster_entries: list):
    print("\n=== STEP 5: REGISTRY GENERATION ===")
    registry = []
    cluster_map = {e["index"]: e for e in cluster_entries}

    for i, rec in enumerate(filtered):
        ce = cluster_map.get(i, {})
        entry = {
            "symbol": rec["symbol_name"],
            "module": derive_module(rec["file_path"]),
            "file_path": rec["file_path"],
            "line_number": rec["line_number"],
            "cluster": ce.get("cluster_label", "unclassified"),
            "cluster_id": ce.get("cluster_id", -1),
            "cluster_top_terms": ce.get("cluster_top_terms", []),
            "matched_keywords": rec["matched_keywords"],
            "docstring": rec["docstring_text"],
            "semantic_signature": ce.get("semantic_signature", []),
        }
        registry.append(entry)

    out = OUT_DIR / "application_function_registry.json"
    out.write_text(json.dumps(registry, indent=2, ensure_ascii=False))
    print(f"  Registry entries: {len(registry)}")
    print(f"  Written: {out}")
    return registry


# ---------------------------------------------------------------------------
# STEP 6 — REPORT
# ---------------------------------------------------------------------------


def step6_report(
    all_candidates: list,
    filtered: list,
    registry: list,
    k: int,
    top_terms: dict,
    cluster_entries: list,
):
    print("\n=== STEP 6: REPORT GENERATION ===")

    total_scanned = len(all_candidates)
    candidate_count = len(filtered)
    clusters_detected = k

    cluster_dist = Counter(e["cluster_id"] for e in cluster_entries)
    unclassified = sum(1 for e in cluster_entries if e.get("cluster_id", -1) == -1)

    # Keyword frequency map
    kw_freq = Counter()
    for rec in filtered:
        for kw in rec.get("matched_keywords", []):
            kw_freq[kw] += 1

    # Top files
    file_freq = Counter(rec["file_path"] for rec in filtered)
    top_files = file_freq.most_common(10)

    # Per-cluster summary
    cluster_rows = []
    for c in sorted(cluster_dist):
        terms = ", ".join(top_terms.get(c, [])[:5])
        cluster_rows.append(f"| cluster_{c:02d} | {cluster_dist[c]} | {terms} |")

    now = "2026-03-10"

    lines = [
        "# ARCHON PRIME — Application Function Extraction Report",
        f"**Generated:** {now}  ",
        "**Mode:** Semantic-Heuristic Analysis (Read-Only)  ",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total docstrings scanned | {total_scanned} |",
        f"| Candidate application functions | {candidate_count} |",
        f"| Clusters detected | {clusters_detected} |",
        f"| Unclassified entries | {unclassified} |",
        "",
        "---",
        "",
        "## Target Directories",
        "",
        "| Directory | Status |",
        "|-----------|--------|",
    ]

    for d in TARGET_DIRS + OPTIONAL_DIRS:
        status = "SCANNED" if d.exists() else "NOT FOUND — SKIPPED"
        lines.append(f"| `{d.relative_to(REPO_ROOT)}` | {status} |")

    lines += [
        "",
        "---",
        "",
        "## Signal Keyword Hit Distribution",
        "",
        "| Keyword | Occurrences |",
        "|---------|-------------|",
    ]
    for kw, count in sorted(kw_freq.items(), key=lambda x: -x[1]):
        lines.append(f"| `{kw}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Top 10 Files by Application Function Density",
        "",
        "| File | Count |",
        "|------|-------|",
    ]
    for fp, count in top_files:
        lines.append(f"| `{fp}` | {count} |")

    lines += (
        [
            "",
            "---",
            "",
            "## Cluster Summary",
            "",
            "| Cluster | Size | Top Representative Terms |",
            "|---------|------|--------------------------|",
        ]
        + cluster_rows
        + [
            "",
            "---",
            "",
            "## Output Artifacts",
            "",
            "| File | Description |",
            "|------|-------------|",
            "| `application_function_candidates.json` | All docstrings extracted via AST |",
            "| `application_function_filtered.json` | Heuristic-filtered application function candidates |",
            "| `application_function_embeddings.json` | TF-IDF semantic vectors per candidate |",
            "| `application_function_clusters.json` | Cluster assignment per candidate |",
            "| `application_function_registry.json` | Full DRAC registry with symbol, module, cluster, signature |",
            "| `application_function_report.md` | This report |",
            "",
            "---",
            "",
            "## Governance Note",
            "",
            "This pass is **read-only**. No repository mutations were performed.  ",
            "Registry entries are candidates for DRAC classification and require human review before activation.",
        ]
    )

    report_text = "\n".join(lines)
    out = OUT_DIR / "application_function_report.md"
    out.write_text(report_text, encoding="utf-8")
    print(f"  Written: {out}")
    return report_text


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("ARCHON PRIME — Application Function Extraction Pass")
    print("=" * 60)

    all_dirs = TARGET_DIRS + OPTIONAL_DIRS

    # Step 1
    candidates = step1_ast_parse(all_dirs)

    # Step 2
    filtered = step2_filter(candidates)

    if not filtered:
        print("\n[ABORT] No candidates passed heuristic filtering. Nothing to cluster.")
        sys.exit(1)

    # Step 3
    vectors, vocab, embeddings = step3_vectorize(filtered)

    # Step 4
    cluster_entries, k, top_terms = step4_cluster(filtered, vectors, embeddings)

    # Step 5
    registry = step5_registry(filtered, cluster_entries)

    # Step 6
    step6_report(candidates, filtered, registry, k, top_terms, cluster_entries)

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print(f"  Total scanned:   {len(candidates)}")
    print(f"  Filtered:        {len(filtered)}")
    print(f"  Clusters:        {k}")
    print(f"  Registry size:   {len(registry)}")
    print("=" * 60)
