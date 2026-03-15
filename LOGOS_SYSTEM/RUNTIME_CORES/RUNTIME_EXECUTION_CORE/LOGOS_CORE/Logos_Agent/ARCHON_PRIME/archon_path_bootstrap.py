"""
ARCHON PATH BOOTSTRAP
Registers Archon Prime root directory so its internal modules can be imported
without rewriting Archon source code.
"""

import sys
from pathlib import Path

ARCHON_ROOT = Path(
    "/workspaces/Logos/LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Agent/ARCHON_PRIME"
)

if str(ARCHON_ROOT) not in sys.path:
    sys.path.append(str(ARCHON_ROOT))
