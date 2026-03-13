AP_NEXUS_EA.md
Execution Addendum

Special governance constraints.

Directory Creation Contract

All directory creation must call

validate_directory_contract(path)

before creation.

Mutation Safety

Mutation allowed only in

WORKFLOW_NEXUS
WORKFLOW_EXECUTION_ENVELOPES
SYSTEM/REPORTS

Forbidden

LOGOS_SYSTEM
SYSTEM_CORE
Runtime Fail Closed

On violation

halt_pipeline()
rollback_mutations()
restore_checkpoint()