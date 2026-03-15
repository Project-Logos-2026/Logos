# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-063
# module_name:          repo_scanner
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/repo_scanner.py
# responsibility:       Inspection module: repo scanner
# runtime_stage:        inspection
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

import json
import os
from pathlib import Path

ROOT = Path(".")
OUT = Path("logs/repo_scan.json")


def scan_repo():
    result = []
    for root, _dirs, files in os.walk(ROOT):
        for f in files:
            result.append(str(Path(root) / f))
    return result


if __name__ == "__main__":
    data = scan_repo()
    OUT.parent.mkdir(exist_ok=True)
    json.dump(data, open(OUT, "w"), indent=2)
    print("Repo scan complete:", len(data), "files")
