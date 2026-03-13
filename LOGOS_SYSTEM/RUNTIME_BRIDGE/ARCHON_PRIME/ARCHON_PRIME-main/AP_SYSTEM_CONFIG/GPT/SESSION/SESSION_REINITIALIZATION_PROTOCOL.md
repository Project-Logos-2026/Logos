# Session_Reinitialization_Protocol

**System:** ARCHON_PRIME  
**Platform:** GPT  
**Artifact Type:** Session Control Protocol / Reinitialization  
**Status:** Release_Candidate_v2  
**Version:** 2.0.0  

## Reinitialize When

- new governance artifacts are introduced
- a correction invalidates prior logic
- a new overlay changes active constraints
- the packet version changes
- the Architect requests reinitialization
- drift is detected and baseline integrity is compromised

## Reinitialization Steps

1. stop downstream transformation work
2. re-load governance in canonical order
3. re-load current overlay or fallback constraints
4. re-identify role
5. revalidate carry-forward assumptions
6. mark superseded reasoning
7. resume only after readiness is restored
