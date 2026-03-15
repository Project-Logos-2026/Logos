# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-041
# module_name:          run_audit_suite
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/run_audit_suite.py
# responsibility:       Inspection module: run audit suite
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

import sys

import circular_dependency_audit
import cross_package_dependency_audit
import duplicate_module_audit
import facade_bypass_audit
import file_size_audit
import header_schema_audit
import import_surface_audit
import module_path_ambiguity_audit
import namespace_shadow_audit
import orphan_module_audit
import runtime_entry_audit
import symbol_collision_audit
import unused_import_audit


def run(target):

    import_surface_audit.run(target)
    circular_dependency_audit.run(target)
    header_schema_audit.run(target)
    unused_import_audit.run(target)
    duplicate_module_audit.run(target)
    file_size_audit.run(target)
    runtime_entry_audit.run(target)
    orphan_module_audit.run(target)
    symbol_collision_audit.run(target)
    cross_package_dependency_audit.run(target)
    namespace_shadow_audit.run(target)
    module_path_ambiguity_audit.run(target)
    facade_bypass_audit.run(target)


if __name__ == "__main__":

    target = sys.argv[1]

    run(target)
