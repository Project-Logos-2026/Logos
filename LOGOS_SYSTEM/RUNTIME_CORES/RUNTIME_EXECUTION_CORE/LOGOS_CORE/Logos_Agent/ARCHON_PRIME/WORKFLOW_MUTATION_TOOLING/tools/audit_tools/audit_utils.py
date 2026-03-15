# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-024
# module_name:          audit_utils
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/audit_utils.py
# responsibility:       Inspection module: audit utils
# runtime_stage:        audit
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
import hashlib
import json
from pathlib import Path

LOG_DIR = Path("/workspaces/ARCHON_PRIME/AUDIT_LOGS")
LOG_DIR.mkdir(exist_ok=True)


def generate_id(text):
    return hashlib.sha1(text.encode()).hexdigest()[:12]


def today():
    d = datetime.date.today()
    return f"{d.month}-{d.day}-{d.year}"


def write_log(name, target, error_type, issues):

    files = set([i["file"] for i in issues if "file" in i])

    data = {
        "header": {
            "audit": name,
            "target_directory": target,
            "identity_tag": generate_id(name + target),
            "error_type": error_type,
            "total_errors": len(issues),
            "files_affected": len(files),
            "date": today(),
        },
        "issues": issues,
    }

    out = LOG_DIR / (name + ".json")

    with open(out, "w") as f:
        json.dump(data, f, indent=2)
