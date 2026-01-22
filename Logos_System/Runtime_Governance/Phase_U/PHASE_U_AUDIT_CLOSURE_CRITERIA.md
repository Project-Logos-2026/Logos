# Phase-U Audit Closure Criteria

Phase-U (Agent Self-Continuation Authority) may close only when
self-continuation semantics are fully defined while continuation remains impossible.

## Required Artifacts

- continuation_semantics_schema.json
- continuation_invariants.json

- continuation_denial_conditions.json
- PHASE_U_README.md (updated to reference all artifacts)

## Required Guarantees

- Agents cannot schedule themselves
- Agents cannot resume themselves
- No looping or continuation exists
- No persistence across steps
- No autonomy or execution authority

## Closure Prohibitions

Phase-U MUST remain OPEN if any artifact:
- implies self-resumption or internal continuation
- references scheduling, looping, or timers
- introduces time, ticks, or persistence
- omits explicit negative capability guarantees

Failure of any check = Phase-U remains OPEN.
