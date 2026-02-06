# Metered Reasoning Enforcer (MRE)

## Purpose
- Fail-closed governor for recursive / combinatorial reasoning
- Prevent runaway recursion, explosion, infinite loops
- Dialable for tuning exploration intensity

## Non-Goals
- No reasoning
- No semantic evaluation
- No authorization
- No governance authority

## Governance Status
- DESIGN_ONLY
- FAIL_CLOSED
- Covered by existing A5 + TREE3 governance
- No runtime execution authority

## Operational Model
- States: GREEN, YELLOW, RED
- GREEN: monitor only
- YELLOW: diminishing returns detected -> taper
- RED: runaway / loop / explosion -> halt escalation

## Dial Semantics
- mre_level in [0.0, 1.0]
- Higher = tolerate inefficiency longer
- Lower = aggressive constraint
- Dial adjusts thresholds only, never overrides RED

## Metrics Observed (standard only)
- iteration count
- elapsed time
- output count
- novelty delta
- branching estimate

## Nexus Eligibility
- Mandatory for Reasoning Nexuses (SCP, ARP, MTP)
- Forbidden for DRAC, EMP, Logos Protocol core

## Testing Plan
- SCP sandbox
- Intentional runaway recursion
- Observe YELLOW then RED
- Manual Ctrl-C fallback
