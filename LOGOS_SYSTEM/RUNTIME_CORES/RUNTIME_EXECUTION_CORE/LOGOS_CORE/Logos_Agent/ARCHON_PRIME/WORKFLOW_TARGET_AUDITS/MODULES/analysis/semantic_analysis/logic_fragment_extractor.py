#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-LOGIC-FRAG
# module_name:          logic_fragment_extractor
# analysis_domain:      semantic_analysis
# module_role:          extraction
# execution_entry:      run
# mutation_capability:  false
# safety_classification: READ_ONLY
# spec_reference:       [SPEC-AP-V2.1]
# ============================================================

"""
ARCHON PRIME — Logic Fragment Extractor
==========================================
Identifies reusable reasoning logic fragments from modules using Python AST.

Detected pattern categories:
  - reasoning_pipeline   : multi-step inference / belief update chains
  - symbolic_manipulation: AST / expression / token transformation
  - mathematical_algorithm: numeric / statistical / geometric computation
  - decision_tree        : condition-branching classification logic
  - utility_logic        : shared helper / transform utilities

Each fragment record includes:
  module, function, semantic_category, dependency_context, fragment_source_code

Outputs (written to OUTPUT_ROOT):
  logic_fragments.json
  logic_fragment_index.json
  fragment_origin_map.json
"""

import argparse
import ast
import collections
import inspect
import json
import os
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"

OUTPUT_ROOT = Path(
    os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT)
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# SEMANTIC CATEGORY SIGNALS
# ---------------------------------------------------------------------------

CATEGORY_SIGNALS: dict[str, set[str]] = {
    "reasoning_pipeline": {
        "infer", "deduce", "abduct", "update", "propagate", "reason",
        "step", "chain", "pipeline", "belief", "posterior", "prior",
        "hypothesis", "evidence", "bayesian", "conclude", "derive",
    },
    "symbolic_manipulation": {
        "ast", "parse", "token", "node", "tree", "expression", "symbol",
        "rewrite", "transform", "substitute", "evaluate", "compile",
        "encode", "decode", "serialize", "deserialize",
    },
    "mathematical_algorithm": {
        "compute", "calculate", "solve", "optimize", "minimize", "maximize",
        "gradient", "matrix", "vector", "norm", "divergence", "entropy",
        "probability", "distribution", "variance", "covariance", "integral",
        "derivative", "polynomial", "fractal", "orbital", "bijection",
    },
    "decision_tree": {
        "classify", "categorize", "triage", "score", "rank", "weight",
        "threshold", "branch", "split", "rule", "condition", "label",
        "verdict", "decision", "choose", "select", "filter",
    },
    "utility_logic": {
        "load", "save", "read", "write", "convert", "format", "normalize",
        "validate", "sanitize", "merge", "flatten", "chunk", "batch",
        "index", "map", "reduce", "accumulate", "aggregate",
    },
}


def classify_fragment(func_name: str, args: list[str], docstring: str,
                      body_tokens: list[str]) -> str:
    combined = " ".join(
        [func_name] + args + [docstring] + body_tokens
    ).lower()
    best, best_score = "utility_logic", 0
    for cat, signals in CATEGORY_SIGNALS.items():
        score = sum(1 for s in signals if s in combined)
        if score > best_score:
            best_score, best = score, cat
    return best


def extract_body_tokens(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Collect name tokens from the function body for classification."""
    tokens: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            tokens.append(child.id)
        elif isinstance(child, ast.Attribute):
            tokens.append(child.attr)
        elif isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
            tokens.append(child.func.id)
    return tokens


def get_source_segment(src_lines: list[str], node: ast.AST) -> str:
    """Extract the raw source lines for a function node."""
    try:
        start = node.lineno - 1  # type: ignore[attr-defined]
        end = node.end_lineno     # type: ignore[attr-defined]
        segment = "".join(src_lines[start:end])
        return textwrap.dedent(segment)
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# FILE ANALYSIS
# ---------------------------------------------------------------------------

def analyze_file(path: Path, rel_path: str) -> list[dict]:
    """Extract all top-level function fragments from a Python file."""
    fragments: list[dict] = []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return fragments

    src_lines = raw.splitlines(keepends=True)
    try:
        tree = ast.parse(raw, filename=str(path))
    except SyntaxError:
        return fragments

    # Collect top-level imports for dependency_context
    import_ctx: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_ctx.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            import_ctx.append(node.module)

    module_name = rel_path.replace(os.sep, ".").removesuffix(".py")

    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name.startswith("_"):
            # Skip private helpers unless they look algorithmically significant
            body_size = sum(1 for _ in ast.walk(node))
            if body_size < 20:
                continue

        args = [a.arg for a in node.args.args]
        docstring = ast.get_docstring(node) or ""
        body_tokens = extract_body_tokens(node)
        category = classify_fragment(node.name, args, docstring, body_tokens)
        source_segment = get_source_segment(src_lines, node)

        fragments.append({
            "module": module_name,
            "function": node.name,
            "lineno": node.lineno,
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "args": args,
            "semantic_category": category,
            "dependency_context": import_ctx[:20],  # top imports only
            "docstring": docstring[:300],
            "fragment_source_code": source_segment[:2000],  # truncated for index
            "body_node_count": sum(1 for _ in ast.walk(node)),
        })

    return fragments


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def write_artifact(name: str, data: object) -> None:
    p = OUTPUT_ROOT / name
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def collect_python_files(target: Path) -> list[Path]:
    py_files: list[Path] = []
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            if f.endswith(".py"):
                py_files.append(Path(root) / f)
    return py_files


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run(target_dir: Path = Path("."), output_root: Path = OUTPUT_ROOT) -> bool:
    global OUTPUT_ROOT
    OUTPUT_ROOT = output_root
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  ARCHON PRIME — Logic Fragment Extractor")
    print(f"  Target : {target_dir}")
    print(f"  Output : {OUTPUT_ROOT}")
    print(f"  Run    : {RUN_TS}")
    print("=" * 60)

    # Try to load module_index for file list, fall back to filesystem scan
    module_index_path = OUTPUT_ROOT / "module_index.json"
    if module_index_path.exists():
        try:
            mod_index = json.loads(module_index_path.read_text(encoding="utf-8"))
            py_paths = [(target_dir / m["file"], m["file"]) for m in mod_index
                        if (target_dir / m["file"]).exists()]
            print(f"  Using module_index.json ({len(py_paths)} modules)")
        except Exception:
            py_paths = [(p, str(p.relative_to(target_dir)))
                        for p in collect_python_files(target_dir)]
    else:
        py_paths = [(p, str(p.relative_to(target_dir)))
                    for p in collect_python_files(target_dir)]
        print(f"  Filesystem scan: {len(py_paths)} Python files")

    print(f"\n[STEP 1] Extracting logic fragments from {len(py_paths)} modules …")
    all_fragments: list[dict] = []
    category_dist: dict[str, int] = collections.Counter()
    origin_map: dict[str, list[str]] = {}  # module → [function names]

    for path, rel in py_paths:
        frags = analyze_file(path, rel)
        all_fragments.extend(frags)
        if frags:
            origin_map[rel] = [f["function"] for f in frags]
            for f in frags:
                category_dist[f["semantic_category"]] += 1

    all_fragments.sort(key=lambda f: (-f["body_node_count"], f["module"]))

    print(f"\n[STEP 2] Writing artifacts …")

    # logic_fragments.json — full records
    write_artifact("logic_fragments.json", {
        "generated_at": RUN_TS,
        "total_fragments": len(all_fragments),
        "category_distribution": dict(category_dist),
        "fragments": all_fragments,
    })

    # logic_fragment_index.json — lightweight index (no source code)
    index_entries = [
        {
            "module": f["module"],
            "function": f["function"],
            "lineno": f["lineno"],
            "semantic_category": f["semantic_category"],
            "args": f["args"],
            "body_node_count": f["body_node_count"],
        }
        for f in all_fragments
    ]
    write_artifact("logic_fragment_index.json", {
        "generated_at": RUN_TS,
        "total_fragments": len(index_entries),
        "category_distribution": dict(category_dist),
        "index": index_entries,
    })

    # fragment_origin_map.json — module → functions extracted
    write_artifact("fragment_origin_map.json", {
        "generated_at": RUN_TS,
        "modules_with_fragments": len(origin_map),
        "origin_map": {
            rel: {"fragment_count": len(fns), "functions": fns}
            for rel, fns in sorted(origin_map.items())
        },
    })

    print(f"\n  Modules scanned          : {len(py_paths)}")
    print(f"  Modules with fragments   : {len(origin_map)}")
    print(f"  Total fragments extracted: {len(all_fragments)}")
    print(f"  Category breakdown:")
    for cat, cnt in sorted(category_dist.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {cnt}")

    print("\n[✓] Logic Fragment Extractor complete.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARCHON Logic Fragment Extractor")
    parser.add_argument("--target", type=Path, default=Path("."),
                        help="Target repository root")
    parser.add_argument("--output", type=Path, default=OUTPUT_ROOT,
                        help="Output directory (overrides ARCHON_OUTPUT_ROOT)")
    args = parser.parse_args()
    ok = run(target_dir=args.target, output_root=args.output)
    sys.exit(0 if ok else 1)
