#!/usr/bin/env python3
"""
Phase 0 sweep: generate import smoke tests for packet modules.
Creates a test_<packet>.py in each END_TO_END_PACKET/<packet>/ if missing.
"""
from __future__ import annotations

from pathlib import Path

PACKET_ROOT = Path("/workspaces/Logos_System/_Dev_Resources/AUTOMATION_ORCHESTRATOR/END_TO_END_PACKET")

TEST_TEMPLATE = """\
def test_import():
    try:
        import {module}
    except Exception as e:
        assert False, f"Import failed: {{e}}"
"""

def main() -> int:
    if not PACKET_ROOT.exists():
        return 0
    for packet in PACKET_ROOT.iterdir():
        if not packet.is_dir():
            continue
        test_path = packet / f"test_{packet.name}.py"
        if test_path.exists():
            continue
        content = TEST_TEMPLATE.format(module=packet.name)
        test_path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
