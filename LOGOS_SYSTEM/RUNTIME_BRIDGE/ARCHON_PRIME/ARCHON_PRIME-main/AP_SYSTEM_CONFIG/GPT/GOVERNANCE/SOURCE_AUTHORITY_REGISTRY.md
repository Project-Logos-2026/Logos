
# SOURCE_AUTHORITY_REGISTRY
SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Governance Registry
VERSION: 1.0
STATUS: Canonical

## Purpose
Defines authority precedence for artifacts used by the ARCHON PRIME workflow to prevent source drift, conflicting specifications, and prompt misalignment.

## Authority Levels

| Level | Meaning | Allowed Use |
|------|--------|-------------|
| Canonical | Official system source of truth | Must be followed |
| Provisional | Draft or candidate artifact | Use cautiously |
| Historical | Superseded artifact retained for reference | Do not use for execution |
| Unknown | Unclassified source | Treat as non-authoritative |

## Authority Precedence

1. Architect Directives
2. Canonical Design Specifications
3. Canonical Implementation Guides
4. Module Registry Artifacts
5. Prompt Schemas and Prompt Compiler Specs
6. Execution Protocol Artifacts
7. Provisional Artifacts
8. Historical Artifacts

## Conflict Resolution Rules

If two artifacts conflict:

1. Prefer higher authority level.
2. If same level, prefer newest version.
3. If unresolved, escalate to Architect.

## Source Registration Fields

Each authoritative artifact must declare:

- Artifact_ID
- Artifact_Name
- Version
- Authority_Level
- Supersedes (if applicable)
- Status
- Owner
