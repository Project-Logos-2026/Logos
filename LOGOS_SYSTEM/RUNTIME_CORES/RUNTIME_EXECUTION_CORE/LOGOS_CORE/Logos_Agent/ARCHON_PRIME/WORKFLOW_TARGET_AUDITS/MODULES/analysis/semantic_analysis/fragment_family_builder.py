#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-FRAG-FAMILY
# module_name:          fragment_family_builder
# analysis_domain:      semantic_analysis
# module_role:          classification
# execution_entry:      run
# mutation_capability:  false
# safety_classification: READ_ONLY
# spec_reference:       [SPEC-AP-V2.1]
# ============================================================

"""
ARCHON PRIME — Fragment Family Builder
========================================
Splits extracted logic fragments into three major structural families
based on their semantic category:

    utility_logic        → infrastructure
    decision_tree        → infrastructure
    reasoning_pipeline   → reasoning
    mathematical_algorithm → math_symbolic
    symbolic_manipulation  → math_symbolic

Inputs (from OUTPUT_ROOT):
    logic_fragments.json
    logic_fragment_index.json

Outputs (written to OUTPUT_ROOT):
    fragment_family_infrastructure.json
    fragment_family_reasoning.json
    fragment_family_math_symbolic.json

Each record includes:
    fragment_id, source_module, function_name, logic_category, fragment_body
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"

OUTPUT_ROOT = Path(
    os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT)
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# Family mapping
# ---------------------------------------------------------------------------

FAMILY_MAP: dict[str, str] = {
    "utility_logic": "infrastructure",
    "decision_tree": "infrastructure",
    "reasoning_pipeline": "reasoning",
    "mathematical_algorithm": "math_symbolic",
    "symbolic_manipulation": "math_symbolic",
}

FAMILY_NAMES = ["infrastructure", "reasoning", "math_symbolic"]


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def _load_fragments(out_dir: Path) -> list[dict]:
    p = out_dir / "logic_fragments.json"
    if not p.exists():
        raise FileNotFoundError(f"logic_fragments.json not found at {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def _to_record(frag: dict) -> dict:
    """Normalise a raw fragment into the canonical family record format."""
    return {
        "fragment_id": frag.get("fragment_id", ""),
        "source_module": frag.get("module", ""),
        "function_name": frag.get("function", ""),
        "logic_category": frag.get("category", "unknown"),
        "fragment_body": {
            "file": frag.get("file", ""),
            "lineno": frag.get("lineno", 0),
            "args": frag.get("args", []),
            "docstring": frag.get("docstring", ""),
            "is_async": frag.get("is_async", False),
            "body_lines": frag.get("body_lines", 0),
        },
    }


def _write(out_dir: Path, filename: str, records: list[dict]) -> None:
    payload = {
        "generated_at": RUN_TS,
        "total": len(records),
        "fragments": records,
    }
    p = out_dir / filename
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [WRITE] {p}  ({len(records)} fragments)")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run(output_root: Path = OUTPUT_ROOT) -> dict[str, list[dict]]:
    """
    Load fragments, split by family, write three JSON files.
    Returns a dict mapping family name → list of records.
    """
    output_root.mkdir(parents=True, exist_ok=True)

    print("ARCHON PRIME — Fragment Family Builder")
    print(f"  Output : {output_root}")

    fragments = _load_fragments(output_root)
    print(f"  Loaded : {len(fragments)} fragments")

    buckets: dict[str, list[dict]] = {name: [] for name in FAMILY_NAMES}

    for frag in fragments:
        cat = frag.get("category", "")
        family = FAMILY_MAP.get(cat)
        if family is None:
            # Unknown category falls into infrastructure as a safe default
            family = "infrastructure"
        buckets[family].append(_to_record(frag))

    filename_map = {
        "infrastructure": "fragment_family_infrastructure.json",
        "reasoning": "fragment_family_reasoning.json",
        "math_symbolic": "fragment_family_math_symbolic.json",
    }

    for family, records in buckets.items():
        _write(output_root, filename_map[family], records)

    summary = {k: len(v) for k, v in buckets.items()}
    print(f"  Summary: {summary}")
    return buckets


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="ARCHON Fragment Family Builder")
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_ROOT,
        help="Output directory (also used for input). Overrides ARCHON_OUTPUT_ROOT.",
    )
    args = parser.parse_args()
    run(output_root=args.output)


if __name__ == "__main__":
    main()
