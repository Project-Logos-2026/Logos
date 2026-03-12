#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               abbreviation_registry_validator
governance_scope:        Abbreviation usage compliance across repository
policy_dependencies:
  - Repo_Governance/Runtime/Abbreviation_Usage_Policy.md
  - Repo_Governance/Runtime/Abbreviations.json
  - Repo_Governance/Runtime/Naming_Convention_Enforcement.md
purpose:
  Audit abbreviation usage across the repository. Checks that abbreviations
  referenced in code and governance documents exist in Abbreviations.json,
  logs undefined abbreviations, and reports missing long-form names.
  Read-only auditor.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - abbreviation_registry_validation_report.json
module_name:             abbreviation_registry_validator
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AUDITOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, json, os, pathlib, re, sys
provides:
  - load_registry, extract_abbreviation_tokens, scan_file,
    validate_abbreviations, main
depends_on_runtime_state: none
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/workspaces/Logos")
OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/_Dev_Governance")
DEV_RESOURCES = REPO_ROOT / "_Dev_Resources"
ABBREVIATIONS_JSON = DEV_RESOURCES / "Repo_Governance" / "Runtime" / "Abbreviations.json"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

# Pattern: 2+ consecutive uppercase letters as a word token
ABBREV_TOKEN_RE = re.compile(r"\b([A-Z]{2,})\b")

# Tokens to always ignore (English words, Python keywords, common terms)
ALWAYS_IGNORE = frozenset({
    "AS", "AND", "AT", "BE", "BY", "DO", "IF", "IN", "IS", "IT",
    "NO", "NOT", "OF", "OK", "ON", "OR", "TO", "UP", "VS",
    "ID", "IO", "OS", "IP",
    "ALL", "ANY", "ARE", "CAN", "DID", "END", "FOR", "GET",
    "HAS", "MAY", "NEW", "OLD", "OWN", "RUN", "SET", "THE",
    "USE", "VIA", "WAS", "PER", "MAX", "MIN", "LEN", "KEY",
    "VAL", "STR", "INT", "DIR", "ENV",
    # Common Python/tech
    "AST", "API", "CLI", "UTC", "ISO", "URI", "URL", "SDK",
    "TCP", "UDP", "HTTP", "HTTPS", "SMTP", "TLS", "SSL",
    "JSON", "YAML", "TOML", "CSV", "XML", "UTF", "BOM",
    "READ", "WRITE", "FILE", "PATH", "DICT", "LIST", "BOOL",
    "TRUE", "FALSE", "NONE", "PASS", "FAIL", "SKIP",
    "LOG", "ERR", "MSG", "SRC", "DST", "TMP", "LIB",
    "WARN", "INFO", "DEBUG", "ERROR", "CRITICAL",
})


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_registry() -> tuple:
    """
    Load Abbreviations.json.
    Returns (registered_set, long_form_map, error).
    registered_set: set of abbreviation strings
    long_form_map: dict mapping abbreviation -> long_form (may be None)
    """
    try:
        with open(ABBREVIATIONS_JSON, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return set(), {}, f"Abbreviations.json not found: {ABBREVIATIONS_JSON}"
    except json.JSONDecodeError as exc:
        return set(), {}, f"JSON decode error: {exc}"

    registered = set()
    long_form_map = {}

    if isinstance(data, dict):
        for key, value in data.items():
            abbrev = key.strip().upper()
            registered.add(abbrev)
            if isinstance(value, dict):
                long_form_map[abbrev] = value.get("long_form") or value.get("expansion") or value.get("meaning")
            elif isinstance(value, str):
                long_form_map[abbrev] = value
            else:
                long_form_map[abbrev] = None
    elif isinstance(data, list):
        for entry in data:
            if not isinstance(entry, dict):
                continue
            abbrev = (
                entry.get("abbreviation") or entry.get("key") or entry.get("abbrev", "")
            ).strip().upper()
            if abbrev:
                registered.add(abbrev)
                long_form_map[abbrev] = (
                    entry.get("long_form") or entry.get("expansion") or entry.get("meaning")
                )

    # Check for entries missing long_form
    missing_long_form = {k for k, v in long_form_map.items() if not v}
    return registered, long_form_map, None, missing_long_form


def extract_abbreviation_tokens(content: str) -> set:
    """Extract all ALL-CAPS token candidates from file content."""
    tokens = ABBREV_TOKEN_RE.findall(content)
    return {t for t in tokens if t not in ALWAYS_IGNORE}


def scan_file(py_path: Path, registered: set) -> dict:
    """Scan one file and return findings."""
    try:
        content = py_path.read_text(encoding="utf-8")
    except Exception as exc:
        return {"file": str(py_path.relative_to(REPO_ROOT)), "error": str(exc)}

    tokens = extract_abbreviation_tokens(content)
    unregistered = sorted(tokens - registered)
    rel = str(py_path.relative_to(REPO_ROOT))
    return {
        "file": rel,
        "tokens_found": sorted(tokens),
        "unregistered": unregistered,
        "unregistered_count": len(unregistered),
    }


def validate_abbreviations(
    scan_dirs: list,
    include_md: bool = False,
    sample_limit: int = 200,
) -> dict:
    load_result = load_registry()
    if len(load_result) == 4:
        registered, long_form_map, load_error, missing_long_form = load_result
    else:
        registered, long_form_map, load_error = load_result
        missing_long_form = set()

    registry_status = {
        "path": str(ABBREVIATIONS_JSON),
        "loaded": load_error is None,
        "error": load_error,
        "registered_count": len(registered),
        "entries_missing_long_form": sorted(missing_long_form),
        "missing_long_form_count": len(missing_long_form),
    }

    if load_error:
        return {
            "registry_status": registry_status,
            "file_scan": [],
            "aggregate": {},
            "error": load_error,
        }

    # Collect files to scan
    file_list = []
    for scan_dir in scan_dirs:
        d = Path(scan_dir)
        if not d.is_dir():
            continue
        extensions = ["*.py"]
        if include_md:
            extensions.append("*.md")
        for ext in extensions:
            for f in sorted(d.rglob(ext)):
                if "__pycache__" not in f.parts:
                    file_list.append(f)

    file_list = file_list[:sample_limit]
    file_results = [scan_file(f, registered) for f in file_list]

    # Aggregate unregistered tokens across all files
    global_unregistered: dict = defaultdict(list)
    for result in file_results:
        for token in result.get("unregistered", []):
            global_unregistered[token].append(result["file"])

    files_with_unregistered = [r for r in file_results if r.get("unregistered_count", 0) > 0]

    return {
        "registry_status": registry_status,
        "files_scanned": len(file_results),
        "files_with_unregistered_tokens": len(files_with_unregistered),
        "global_unregistered_tokens": {
            token: {"count": len(files), "in_files": files}
            for token, files in sorted(global_unregistered.items())
        },
        "unregistered_token_count": len(global_unregistered),
        "note": (
            "Unregistered tokens require architect review per Abbreviation_Usage_Policy. "
            "They are flagged, not automatically corrected."
        ),
        "file_results": file_results,
    }


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit abbreviation usage across repository."
    )
    parser.add_argument(
        "--scan-dirs",
        nargs="+",
        default=[
            str(DEV_RESOURCES / "Dev_Tools"),
            str(REPO_ROOT / "LOGOS_SYSTEM"),
        ],
        help="Directories to scan for abbreviation tokens",
    )
    parser.add_argument(
        "--include-md",
        action="store_true",
        help="Also scan .md files (not just .py)",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=200,
        help="Maximum number of files to scan",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="abbreviation_registry_validation_report.json",
        help="Output report filename",
    )
    args = parser.parse_args()

    results = validate_abbreviations(
        scan_dirs=args.scan_dirs,
        include_md=args.include_md,
        sample_limit=args.sample_limit,
    )

    registry_ok = results["registry_status"]["loaded"]
    unregistered_count = results.get("unregistered_token_count", 0)
    # Status: PASS if registry loaded; unregistered tokens are warnings, not failures
    status = "PASS" if registry_ok else "FAIL"

    report = {
        "artifact_type": "abbreviation_registry_validation",
        "generated_utc": _now_utc(),
        "tool_name": "abbreviation_registry_validator",
        "schema_version": "1.0",
        "status": status,
        "results": results,
    }
    write_report(args.output, report)
    print(f"Status: {status}")
    print(f"Registry entries: {results['registry_status']['registered_count']} | "
          f"Files scanned: {results.get('files_scanned', 0)} | "
          f"Unregistered tokens found: {unregistered_count}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
