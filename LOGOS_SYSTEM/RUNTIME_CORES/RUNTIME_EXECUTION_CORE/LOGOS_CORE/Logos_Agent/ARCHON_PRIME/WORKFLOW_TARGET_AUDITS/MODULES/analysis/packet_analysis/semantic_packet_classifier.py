#!/usr/bin/env python3
"""
ARCHON PRIME — Semantic Packet Classifier
==========================================
Standalone semantic classification of Python modules into domain-specific
packets. Uses keyword signal scoring across module names, imports, function
names, and docstrings. Packet classes: reasoning, agent, utility, safety,
math, semantic, data, interface, config, test.
Writes: semantic_packets_classified.json
"""
import argparse
import ast
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"
OUTPUT_ROOT = Path(os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
RUN_TS = datetime.now(timezone.utc).isoformat()

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache"}

PACKET_CLASSES: dict[str, list[str]] = {
    "reasoning":  ["reason", "infer", "deduce", "conclude", "logic", "proof", "axiom",
                   "hypothesis", "belief", "inference", "entail", "derive"],
    "agent":      ["agent", "actor", "run_loop", "step", "policy", "action", "observe",
                   "reward", "environment", "episode", "rollout", "trajectory"],
    "utility":    ["util", "helper", "convert", "format", "parse", "serialize", "transform",
                   "sanitize", "normalize", "encode", "decode", "adapter"],
    "safety":     ["validate", "guard", "constraint", "forbidden", "deny", "restrict",
                   "allow", "authorize", "permission", "boundary", "check"],
    "math":       ["matrix", "vector", "norm", "gradient", "optimize", "loss", "sample",
                   "distribution", "probability", "entropy", "tensor", "algebra"],
    "semantic":   ["embed", "token", "similarity", "cluster", "classify", "nlp", "corpus",
                   "vocab", "syntax", "semantic", "language", "sentence"],
    "data":       ["dataset", "loader", "schema", "db", "database", "query", "record",
                   "row", "table", "store", "cache", "fetch", "persist", "repository"],
    "interface":  ["api", "endpoint", "route", "handler", "request", "response", "http",
                   "server", "client", "socket", "protocol", "rpc", "controller"],
    "config":     ["config", "settings", "env", "environment", "setup", "configure",
                   "options", "parameters", "preferences", "profile"],
    "test":       ["test", "spec", "assert", "fixture", "mock", "stub", "patch",
                   "benchmark", "profile", "coverage"],
}

MIN_SCORE_THRESHOLD = 2  # Minimum signal hits to classify


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon semantic packet classifier")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def collect_signals(path: Path) -> list[str]:
    """Collect all text signals from a Python file: names, imports, docstrings."""
    signals: list[str] = []
    # Add path-based signals
    signals.extend(re.sub(r"[^a-z]", " ", str(path).lower()).split())

    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return signals

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            signals.extend(re.sub(r"([A-Z])", r" \1", node.name).lower().split())
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module:
                signals.extend(node.module.lower().split("."))
            for alias in node.names:
                signals.extend(alias.name.lower().split("."))
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                signals.extend(re.sub(r"[^a-z]", " ", node.value.value.lower()).split())

    return signals


def classify(signals: list[str]) -> tuple[str, dict[str, int]]:
    scores: dict[str, int] = {}
    for packet, keywords in PACKET_CLASSES.items():
        score = sum(1 for sig in signals for kw in keywords if kw in sig)
        if score >= MIN_SCORE_THRESHOLD:
            scores[packet] = score
    if not scores:
        return "utility", {}
    best = max(scores, key=scores.__getitem__)
    return best, scores


def run(target: Path, out_dir: Path) -> None:
    print(f"[semantic_packet_classifier] Scanning: {target}")
    packets: dict[str, list[str]] = {k: [] for k in PACKET_CLASSES}
    packets["unclassified"] = []
    modules = []

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            signals = collect_signals(fp)
            packet, scores = classify(signals)
            packets.setdefault(packet, []).append(rel)
            modules.append({
                "file": rel,
                "module": rel.removesuffix(".py").replace(os.sep, "."),
                "packet": packet,
                "scores": scores,
            })

    packet_counts = {k: len(v) for k, v in packets.items() if v}

    write_json(out_dir, "semantic_packets_classified.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "packet_counts": packet_counts,
        "packets": {k: v for k, v in packets.items() if v},
        "modules": modules,
    })
    print(f"  Modules: {len(modules)}  Packet distribution: {packet_counts}")


def main() -> None:
    args = parse_args()
    target = Path(args.target).resolve()
    out_dir = Path(args.output)
    if not target.exists():
        print(f"[FATAL] Target not found: {target}", file=sys.stderr)
        sys.exit(1)
    run(target, out_dir)


if __name__ == "__main__":
    main()
