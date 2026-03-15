#!/usr/bin/env python3
"""
ARCHON PRIME — Integration Compatibility Analyzer
==================================================
Analyzes each Python module's compatibility with LOGOS runtime integration
protocols: SCP (State Coordination Protocol), ARP (Axiom Reasoning Protocol),
MTP (Message Transport Protocol), and generic runtime agent contracts.
Scores modules 0.0–1.0 per protocol. Writes: integration_compatibility.json
"""
import argparse
import ast
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"
OUTPUT_ROOT = Path(os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
RUN_TS = datetime.now(timezone.utc).isoformat()

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache"}

# Protocol signal maps: protocol → (required_signals, optional_signals)
PROTOCOL_SIGNALS: dict[str, dict[str, list[str]]] = {
    "SCP": {
        "required": ["state", "coordinate", "sync", "consistency"],
        "optional": ["snapshot", "checkpoint", "rollback", "lock", "transaction", "delta"],
    },
    "ARP": {
        "required": ["axiom", "proof", "reason", "inference", "belief"],
        "optional": ["entail", "conclude", "derive", "hypothesis", "weight", "confidence"],
    },
    "MTP": {
        "required": ["message", "queue", "publish", "subscribe", "channel"],
        "optional": ["topic", "broker", "consumer", "producer", "route", "dispatch"],
    },
    "AGENT_CONTRACT": {
        "required": ["agent", "run", "step", "policy"],
        "optional": ["observe", "action", "reward", "loop", "episode", "terminate"],
    },
    "RUNTIME_API": {
        "required": ["api", "endpoint", "execute", "handler"],
        "optional": ["request", "response", "payload", "protocol", "interface", "register"],
    },
}

SIGNAL_WEIGHT = {"required": 2.0, "optional": 1.0}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon integration compatibility analyzer")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def collect_text_signals(path: Path) -> list[str]:
    signals: list[str] = list(path.stem.lower().split("_"))
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return signals
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            signals.extend(node.name.lower().split("_"))
        elif isinstance(node, ast.ClassDef):
            import re
            signals.extend(re.sub(r"([A-Z])", r"_\1", node.name).lower().split("_"))
        elif isinstance(node, ast.ImportFrom) and node.module:
            signals.extend(node.module.lower().split("."))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            for word in node.value.lower().split():
                signals.append(word[:20])
    return signals


def score_protocol(signals: list[str], protocol_def: dict[str, list[str]]) -> float:
    """Compute a 0–1 compatibility score for a single protocol."""
    max_score = (
        len(protocol_def["required"]) * SIGNAL_WEIGHT["required"]
        + len(protocol_def["optional"]) * SIGNAL_WEIGHT["optional"]
    )
    if max_score == 0:
        return 0.0
    actual = 0.0
    sig_set = set(signals)
    for kw in protocol_def["required"]:
        if any(kw in s for s in sig_set):
            actual += SIGNAL_WEIGHT["required"]
    for kw in protocol_def["optional"]:
        if any(kw in s for s in sig_set):
            actual += SIGNAL_WEIGHT["optional"]
    return round(min(actual / max_score, 1.0), 3)


def run(target: Path, out_dir: Path) -> None:
    print(f"[integration_compatibility_analyzer] Scanning: {target}")
    modules = []
    high_compat: list[dict] = []

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            module = rel.removesuffix(".py").replace(os.sep, ".")
            signals = collect_text_signals(fp)

            protocol_scores = {
                proto: score_protocol(signals, pdef)
                for proto, pdef in PROTOCOL_SIGNALS.items()
            }
            best_proto = max(protocol_scores, key=protocol_scores.__getitem__)
            best_score = protocol_scores[best_proto]
            overall = round(sum(protocol_scores.values()) / len(protocol_scores), 3)

            entry = {
                "module": module,
                "file": rel,
                "protocol_scores": protocol_scores,
                "best_protocol": best_proto,
                "best_protocol_score": best_score,
                "overall_compatibility": overall,
                "compatibility_tier": (
                    "HIGH" if best_score >= 0.5 else
                    "MEDIUM" if best_score >= 0.25 else
                    "LOW"
                ),
            }
            modules.append(entry)
            if best_score >= 0.5:
                high_compat.append({"module": module, "protocol": best_proto, "score": best_score})

    modules.sort(key=lambda x: x["best_protocol_score"], reverse=True)

    write_json(out_dir, "integration_compatibility.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_modules": len(modules),
        "high_compatibility_count": len(high_compat),
        "top_compatible_modules": high_compat[:20],
        "modules": modules,
    })
    print(f"  Modules: {len(modules)}  High-compatibility: {len(high_compat)}")


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
