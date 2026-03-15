# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-025
# module_name:          circular_dependency_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/circular_dependency_audit.py
# responsibility:       Inspection module: circular dependency audit
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

    imports = {}
    issues = []

    for p in Path(target).rglob("*.py"):

        try:
            tree = ast.parse(open(p).read())

            deps = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):
                    for n in node.names:
                        deps.append(n.name)

                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        deps.append(node.module)

            imports[str(p)] = deps

        except Exception:
            pass

    for a in imports:
        for b in imports[a]:
            if b in imports:
                if a in imports[b]:

                    issues.append(
                        {
                            "id": generate_id(a + b),
                            "file_a": a,
                            "file_b": b,
                            "issue": "circular_dependency",
                        }
                    )

    write_log("circular_dependency_audit", target, "dependency_cycle", issues)
