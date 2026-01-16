#!/usr/bin/env python3
"""
Phase 5 rewrite implementation (deterministic).

- Attempt 1: full rewrite with canonical header + normalized filename.
- Attempt 2: targeted rewrite (same output for now).

Behaviors:
- Normalizes filename to Title_Case_With_Underscores.
- Installs canonical LOGOS header (with semantic audit marker).
- Removes existing LOGOS header or leading comment block, preserves remaining code.
- Writes rewritten artifact into the packet directory and records rewrite attempt in packet JSON.
"""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

REPO = Path("/workspaces/Logos_System").resolve()
PACKET_ROOT = REPO / "_Dev_Resources/AUTOMATION_ORCHESTRATOR/END_TO_END_PACKET"

CANONICAL_HEADER = """#!/usr/bin/env python3
# LOGOS SYSTEM FILE HEADER
# LOGOS_HEADER: v1
# updated_utc: {timestamp}
# path: {legacy_path}
# role: phase_5_rewrite_artifact
# phase: phase_5_rewrite
# origin: AUTOMATION_ORCHESTRATOR
# intended_bucket: REWRITE_PROMOTE
# side_effects: none
# entrypoints: module
# depends_on: {depends_on}
# abbreviations: notes=Rewrite rule: any promoted/reintegrated script must use canonical abbreviations; legacy aliases are allowed only in historical comments/quotes.
# notes: Rewrite rule: any promoted/reintegrated script must use canonical abbreviations; legacy aliases are allowed only in historical comments/quotes.
# END_LOGOS_HEADER

"""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_name(name: str) -> str:
    parts = re.split(r"[^a-zA-Z0-9]+", name)
    return "_".join(p.capitalize() for p in parts if p)


def _normalize_path(value: str | None, fallback: str) -> str:
    if value in (None, "", "unknown"):
        return fallback
    return value


def _collect_depends_on(text: str) -> str:
    mods = set()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m_from = re.match(r"from\s+([A-Za-z0-9_.]+)", stripped)
        m_import = re.match(r"import\s+([A-Za-z0-9_.]+)", stripped)
        target = None
        if m_from:
            target = m_from.group(1)
        elif m_import:
            target = m_import.group(1).split(",")[0].strip()
        if target:
            mods.add(target)
    return ", ".join(sorted(mods)) if mods else "stdlib"


def _strip_header(text: str) -> str:
    lines = text.splitlines()
    out = []
    skip = False
    started = False
    for ln in lines:
        if ln.startswith("# LOGOS SYSTEM FILE HEADER"):
            skip = True
            started = True
            continue
        if ln.startswith("# LOGOS_HEADER"):
            skip = True
            started = True
            continue
        if skip and ln.startswith("# END_LOGOS_HEADER"):
            skip = False
            continue
        if skip:
            continue
        if not started and (ln.lstrip().startswith("#") or ln.startswith("#!")):
            continue
        out.append(ln)
    # Trim leading blank lines
    while out and not out[0].strip():
        out.pop(0)
    body = "\n".join(out)
    if body and not body.endswith("\n"):
        body += "\n"
    return body


def rewrite(src: Path, attempt: int) -> Path:
    packet_dir = PACKET_ROOT / src.stem
    packet_dir.mkdir(parents=True, exist_ok=True)
    json_path = packet_dir / f"{src.stem}.json"

    data = {
        "metadata": {
            "packet_name": src.stem,
            "original_path": str(src),
            "legacy_path": str(src),
            "type_cast_name": normalize_name(src.stem),
            "test_template": "default",
            "file_hash": "pending",
            "batch_id": "BATCH_PHASE5",
            "init_timestamp": _now_iso(),
        },
        "phases": {"phase_5_rewrite_attempts": []},
    }

    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    meta = data.setdefault("metadata", {})
    meta["original_path"] = _normalize_path(meta.get("original_path"), str(src))
    meta["legacy_path"] = _normalize_path(meta.get("legacy_path"), str(src))
    # Always emit a canonical filename derived only from the normalized type_cast_name
    type_name = normalize_name(meta.get("type_cast_name") or src.stem)
    meta["type_cast_name"] = type_name
    target_path = packet_dir / f"{type_name}.py"

    source_text = src.read_text(encoding="utf-8", errors="ignore")
    body = _strip_header(source_text)
    depends_on = _collect_depends_on(body)
    header = CANONICAL_HEADER.format(
        timestamp=_now_iso(),
        legacy_path=str(src),
        depends_on=depends_on,
    )
    rewritten = header + body
    target_path.write_text(rewritten, encoding="utf-8")

    # Persist the canonical rewrite output path for downstream consumers
    meta["rewrite_output"] = str(target_path)

    attempts = data.setdefault("phases", {}).setdefault("phase_5_rewrite_attempts", [])
    attempts.append({
        "attempt": attempt,
        "rewrite_path": str(target_path),
        "rewrite_hash": "sha256:" + hashlib.sha256(rewritten.encode("utf-8")).hexdigest(),
        "timestamp": _now_iso(),
        "status": "complete",
    })

    json_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return dst


def main(argv=None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        return 0
    src = Path(args[0]).resolve()
    attempt = int(args[1]) if len(args) > 1 else 1
    rewrite(src, attempt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
