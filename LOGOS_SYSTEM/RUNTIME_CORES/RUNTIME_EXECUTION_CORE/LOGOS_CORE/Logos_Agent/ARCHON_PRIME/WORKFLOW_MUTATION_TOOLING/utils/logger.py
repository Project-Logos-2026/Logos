# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-081
# module_name:          logger
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/utils/logger.py
# responsibility:       Utility module: logger
# runtime_stage:        utility
# execution_entry:      None
# allowed_targets:      []
# forbidden_targets:    ["SYSTEM", "WORKFLOW_NEXUS"]
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-AP-V2.1]
# implementation_phase: PHASE_2
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate

enforce_runtime_gate()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

import datetime
import json
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def log(event, data=None):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event": event,
        "data": data or {},
    }
    with open(LOG_DIR / "execution_log.json", "a") as f:
        f.write(json.dumps(entry) + "\n")
