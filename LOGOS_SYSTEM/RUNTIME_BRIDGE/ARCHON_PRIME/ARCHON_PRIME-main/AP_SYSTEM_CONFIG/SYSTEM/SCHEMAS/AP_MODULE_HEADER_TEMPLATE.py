# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-NNN
# module_name:          <module_name>
# subsystem:            <subsystem>
# module_role:          <role>
# canonical_path:       <path/from/repo/root>
# responsibility:       <one sentence description>
# runtime_stage:        <stage>
# execution_entry:      <function|None>
# allowed_targets:      []
# forbidden_targets:    []
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-ID.section]
# implementation_phase: PHASE_N
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================

from SYSTEM.workflow_guard import enforce_runtime_guard

enforce_runtime_guard()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------
