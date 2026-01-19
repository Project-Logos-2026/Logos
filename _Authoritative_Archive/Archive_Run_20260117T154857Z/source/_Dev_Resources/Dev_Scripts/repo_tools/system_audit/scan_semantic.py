#!/usr/bin/env python3
"""
Phase 6 — Semantic Audit (Attempt 1 only)

Checks exactly three things:
1. Naming convention (Title_Case_With_Underscores, ALLCAPS abbreviations)
2. Required standardized header presence and correctness
3. Abbreviation usage correctness against Abbreviations.json

Non-mutating. Emits schema-compliant diagnostics only.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

try:
    from ._diagnostic_record import diag
except ImportError:  # script execution fallback
    from _diagnostic_record import diag

REPO = Path("/workspaces/Logos_System")
ABBREV_CANDIDATES = [
    REPO / "_Dev_Resources/Abbreviations.json",
    REPO / "_Dev_Resources/Dev_Scripts/repo_tools/audit_normalize_automation/Abbreviations.json",
    REPO / "Documentation/Abbreviations.json",
]
HEADER_MARKER = "LOGOS SYSTEM FILE HEADER"
TITLE_CASE_RE = re.compile(r"^[A-Z][a-z0-9]*(?:_[A-Z0-9][a-z0-9]*)*$")
ALL_CAPS_RE = re.compile(r"^[A-Z0-9]+$")


def load_abbreviations() -> dict:
    for cand in ABBREV_CANDIDATES:
        if cand.exists():
            return json.loads(cand.read_text(encoding="utf-8"))
    raise SystemExit("Missing Abbreviations.json (checked multiple standard locations)")


def check_naming(path: Path):
    diags = []
    name = path.stem
    if not TITLE_CASE_RE.match(name):
        diags.append(
            diag(
                error_type="NamingConventionViolation",
                line=1,
                char_start=0,
                char_end=len(name),
                details="File name must be Title_Case_With_Underscores",
                source="semantic_naming",
            )
        )
    for part in name.split("_"):
        if part.isupper() and not ALL_CAPS_RE.match(part):
            diags.append(
                diag(
                    error_type="AbbreviationFormatViolation",
                    line=1,
                    char_start=0,
                    char_end=len(part),
                    details=f"Abbreviation '{part}' must be ALL CAPS",
                    source="semantic_naming",
                )
            )
    return diags


def check_header(path: Path):
    diags = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return diags
    if HEADER_MARKER not in text[:500]:
        diags.append(
            diag(
                error_type="MissingStandardHeader",
                line=1,
                char_start=0,
                char_end=0,
                details="Required LOGOS standard header not found",
                source="semantic_header",
            )
        )
    return diags


def check_abbreviations(path: Path, abbrevs: dict):
    diags = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for abbr, full in abbrevs.items():
        if not abbr:
            continue
        # simple word-boundary match to reduce false positives
        if re.search(rf"\b{re.escape(abbr)}\b", text):
            expansions: List[str] = []
            if isinstance(full, str):
                expansions = [full]
            elif isinstance(full, (list, tuple)):
                expansions = [f for f in full if isinstance(f, str)]
            else:
                expansions = []

            if expansions and not any(exp in text for exp in expansions):
                diags.append(
                    diag(
                        error_type="AbbreviationExpansionMismatch",
                        line=1,
                        char_start=0,
                        char_end=0,
                        details=f"Abbreviation '{abbr}' missing canonical expansion",
                        source="semantic_abbreviations",
                    )
                )
    return diags


def run(targets):
    abbrevs = load_abbreviations()
    results = {}
    for path in targets:
        if not path.suffix == ".py":
            continue
        diags = []
        diags.extend(check_naming(path))
        diags.extend(check_header(path))
        diags.extend(check_abbreviations(path, abbrevs))
        if diags:
            results[str(path)] = diags
    return results


def main(argv=None):
    import sys

    args = argv if argv is not None else sys.argv[1:]
    files = [Path(p) for p in args]
    out = run(files)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
