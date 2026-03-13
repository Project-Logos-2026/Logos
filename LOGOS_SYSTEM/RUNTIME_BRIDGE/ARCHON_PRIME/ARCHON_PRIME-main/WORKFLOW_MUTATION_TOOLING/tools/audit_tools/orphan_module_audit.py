# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-039
# module_name:          orphan_module_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/orphan_module_audit.py
# responsibility:       Inspection module: orphan module audit
# runtime_stage:        audit
# execution_entry:      run
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

import ast
from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    imports = set()
    files = set()

    issues = []

    for p in Path(target).rglob("*.py"):

        files.add(p.stem)

        try:
            tree = ast.parse(open(p).read())

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.add(n.name.split(".")[0])

        except Exception:
            pass

    for f in files:
        if f not in imports:

            issues.append({"id": generate_id(f), "module": f, "issue": "orphan_module"})

    write_log("orphan_module_audit", target, "orphan_module", issues)
