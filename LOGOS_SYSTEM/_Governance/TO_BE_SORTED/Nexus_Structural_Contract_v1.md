# Nexus Structural Contract v1

## Tier-1 Execution Nexus Invariants
- Must define a primary class with methods: `tick`, `register_participant`, `ingest`
- Must import and invoke MRE (MeteredReasoningEnforcer)
- Must enforce mesh validation (MeshEnforcer)
- Must raise fail-closed exceptions (NexusViolation, MeshRejection, MREHalt)
- No dynamic imports or sys.path/sys.modules manipulation
- Must not call other Nexus classes directly
- Must have only one primary execution class

## Tier-1 Pipeline Nexus Invariants
- Must define a primary class with method: `process`
- Must raise fail-closed exceptions
- No dynamic imports or sys.path/sys.modules manipulation
- Must not call other Nexus classes directly

## Tier-2 Subnexus Invariants
- May define auxiliary classes
- Must not expose public execution methods
- Must not invoke MRE or mesh enforcement
- No dynamic imports or sys.path/sys.modules manipulation

## Infrastructure Nexus Invariants
- May define utility classes
- Must not expose public execution methods
- No dynamic imports or sys.path/sys.modules manipulation

## Invalid Classification Criteria
- Multiple primary execution classes
- Dynamic imports or sys.path/sys.modules manipulation
- Calls to other Nexus classes
- Missing required invariants
- Parse errors or non-deterministic structure

## AST-Verifiable Structural Signals
- Method presence (tick, register_participant, ingest, process)
- Import statements (MRE, MeshEnforcer, protocol core)
- Exception raising
- Class count and naming
- Attribute assignments
- Function calls
- Illegal constructs (dynamic import, sys.path, sys.modules)

## Hierarchy Model
- Tier-1 Execution Nexus > Tier-1 Pipeline Nexus > Tier-2 Subnexus > Infrastructure > Invalid

## Retroactive Enforcement Statement
- All Nexus modules are subject to retroactive structural contract enforcement via deterministic AST validation.
- Violations are reported, not auto-remediated.
