# I1_Agent Stack Position

Runtime domain: Execution

Upstream dependencies (imports/callers):
- Imports: typing, dataclasses, uuid, time
- Core integrations depend on config.hashing.safe_hash and diagnostics.errors
- Callers: UNSPECIFIED

Downstream consumers (targets/emit paths):
- protocol_operations modules (SCP adapters, predictors, transformers)
- Registered Nexus participants implementing NexusParticipant

Runtime bridge interaction:
- No direct runtime bridge interaction observed.
