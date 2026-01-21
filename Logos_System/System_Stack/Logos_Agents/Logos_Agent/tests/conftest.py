import sys
from pathlib import Path

# Ensure repository root is on sys.path for imports like Logos_System.*
ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
