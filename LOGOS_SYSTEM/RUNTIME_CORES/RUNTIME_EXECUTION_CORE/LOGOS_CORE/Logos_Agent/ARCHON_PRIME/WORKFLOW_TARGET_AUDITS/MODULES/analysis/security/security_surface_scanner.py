#!/usr/bin/env python3
"""
ARCHON PRIME — Security Surface Scanner
=========================================
Scans Python source for security-sensitive code patterns: unsafe built-ins
(eval, exec), shell injection risks (subprocess shell=True), serialization
risks (pickle.load, yaml.load), SQL injection patterns, and hard-coded
credential patterns. READ-ONLY — never modifies target files.
Writes: security_surface.json
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

# AST-based pattern checks: (check_name, severity, description)
AST_CHECKS: list[dict] = []

# Regex-based source scan patterns
REGEX_PATTERNS: list[tuple[str, str, str]] = [
    # (pattern, severity, description)
    (r"\beval\s*\(", "CRITICAL", "eval() call — arbitrary code execution risk"),
    (r"\bexec\s*\(", "CRITICAL", "exec() call — arbitrary code execution risk"),
    (r"shell\s*=\s*True", "HIGH", "subprocess shell=True — command injection risk"),
    (r"pickle\.load[s]?\s*\(", "HIGH", "pickle.load — deserialization attack risk"),
    (r"yaml\.load\s*\([^)]*\)", "HIGH", "yaml.load without Loader — code execution risk"),
    (r"__import__\s*\(", "HIGH", "dynamic __import__() call — obfuscated import risk"),
    (r"os\.system\s*\(", "HIGH", "os.system() — command injection risk"),
    (r"subprocess\.Popen\s*\([^)]*shell\s*=\s*True", "HIGH", "Popen with shell=True"),
    (r"hashlib\.md5\s*\(|hashlib\.sha1\s*\(", "MEDIUM", "Weak hash algorithm (MD5/SHA1)"),
    (r"random\.random\s*\(|random\.randint\s*\(", "LOW", "Non-cryptographic random for security context"),
    (r"(?:password|passwd|secret|api_key|token)\s*=\s*['\"][^'\"]{6,}['\"]",
     "HIGH", "Potential hard-coded credential"),
    (r"SELECT\s+.*\s+FROM\s+.*\+|FROM\s+.*WHERE\s+.*\+", "HIGH", "Potential SQL injection via string concat"),
    (r"\.format\s*\(.*\)\s*(?:execute|query)\s*\(", "MEDIUM", "Potential SQL via .format()"),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon security surface scanner")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def scan_file(path: Path, target: Path) -> list[dict]:
    rel = str(path.relative_to(target))
    findings: list[dict] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    for pattern, severity, description in REGEX_PATTERNS:
        for m in re.finditer(pattern, src, re.IGNORECASE):
            # Compute line number
            lineno = src[:m.start()].count("\n") + 1
            findings.append({
                "file": rel,
                "lineno": lineno,
                "severity": severity,
                "description": description,
                "pattern": pattern,
                "matched_text": m.group(0)[:80],
            })
    return findings


def run(target: Path, out_dir: Path) -> None:
    print(f"[security_surface_scanner] Scanning: {target}")
    all_findings: list[dict] = []
    severity_counts: dict[str, int] = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    files_scanned = 0
    affected_files: set[str] = set()

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            if not fn.endswith(".py"):
                continue
            files_scanned += 1
            findings = scan_file(Path(root) / fn, target)
            for f in findings:
                severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1
                affected_files.add(f["file"])
            all_findings.extend(findings)

    # Sort by severity
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_findings.sort(key=lambda x: sev_order.get(x["severity"], 4))

    risk_level = (
        "CRITICAL" if severity_counts["CRITICAL"] > 0 else
        "HIGH" if severity_counts["HIGH"] > 0 else
        "MEDIUM" if severity_counts["MEDIUM"] > 0 else
        "LOW" if severity_counts["LOW"] > 0 else
        "NONE"
    )

    write_json(out_dir, "security_surface.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "files_scanned": files_scanned,
        "total_findings": len(all_findings),
        "affected_files": len(affected_files),
        "severity_counts": severity_counts,
        "overall_risk_level": risk_level,
        "findings": all_findings,
    })
    print(f"  Files: {files_scanned}  Findings: {len(all_findings)}  "
          f"Risk: {risk_level}  Severity: {severity_counts}")


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
