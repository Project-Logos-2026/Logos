
# ============================================================================
# LOGOS CANONICAL MODULE HEADER
#
# Module:        STARTUP/__main__.py
# Canonicality:  ENFORCED (PHASE 6C — Canonical Ignition Surface Enforcement)
# Authority:     Delegates exclusively to START_LOGOS.py
# Runtime:       No direct agent, protocol, or state modification
# Governance:    Fail-closed; all failures halt runtime
#
# Copyright (c) Project-Logos-2026
# ============================================================================

#!/usr/bin/env python3
"""
LOGOS Runtime Module Entry Point

Authority Model:
- Delegates exclusively to START_LOGOS.py
- Does not import execution core modules directly
- Does not initiate agents
- Does not perform protocol binding
- Does not modify runtime state

Fail-Closed:
Any failure during START_LOGOS execution halts runtime.
"""

from __future__ import annotations

# ================================================================
# LOGOS Repository Import Root Bootstrap
# ================================================================

import sys
import pathlib

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# ================================================================

from .START_LOGOS import main as start_logos_main


def main() -> None:
    start_logos_main()


if __name__ == "__main__":
    main()
