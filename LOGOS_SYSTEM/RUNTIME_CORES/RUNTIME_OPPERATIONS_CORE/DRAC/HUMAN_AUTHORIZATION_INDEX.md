HUMAN_AUTHORIZATION_INDEX.md

(This answers your “A5 / A7 / where do I sign” concern)

Status: DRAFT | DESIGN-ONLY
Authority: Human Authorization Registry
Execution: NONE
Scope: Central index of human-only authorization points

Purpose

This document consolidates all locations in the LOGOS system where explicit human authorization is required.

It exists to prevent:

missed approval points

accidental implicit authorization

authority drift across phases

Human Authorization Domains
1. DRAC Rebuild Authorization

Artifact: DRAC_REBUILD_ENTRY_AUTHORITY.md

Human approval required to:

initiate DRAC rebuild

lift rebuild freeze

revoke rebuild mid-process

2. Runtime Authorization

Artifact: RUNTIME_AUTHORIZATION_V1.md

Human approval required to:

permit any runtime execution

define execution scope (passive / active)

3. Session Invocation Authorization

Artifact: SESSION_INVOCATION_CONTRACT_PASSIVE.md
(or future active variants)

Human approval required to:

start a specific session

define session mode

limit session duration and scope

4. Autonomy / Delegation (A5 / A7 Class)

Artifacts: Phase A5 / A7 governance documents

Human approval required to:

delegate decision authority

permit agent self-direction

enable persistence across sessions

allow adaptive behavior

Default state: DENIED

5. Observation & Exposure Authorization

Artifacts: (future)

Human approval required to:

expose metrics (e.g., Prometheus)

attach GUIs

permit external observation

allow telemetry export

Observation is not neutral and requires consent.

Authorization Properties (Global)

All human authorizations are:

Explicit

Non-inferable

Revocable

Non-persistent by default

Session-scoped unless stated otherwise

Subordinate to halt supremacy

Closing

If a behavior is not covered here, it is not authorized.

This index is the single place to audit:

“Where does a human have to say yes?”

End of index.
