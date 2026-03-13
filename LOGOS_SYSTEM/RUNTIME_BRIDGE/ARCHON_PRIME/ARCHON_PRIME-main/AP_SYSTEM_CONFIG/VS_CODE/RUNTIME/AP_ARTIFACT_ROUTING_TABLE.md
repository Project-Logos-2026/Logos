# AP_ARTIFACT_ROUTING_TABLE

Artifact ID: OPS-RUN-002  
System: ARCHON_PRIME  
Artifact Type: Artifact Routing Specification  
Status: Active

---

## Purpose

Defines where execution outputs must be written.

---

## Artifact Routing Table

Execution summaries  
Returned in chat

Audit logs  
AUDIT_LOGS/

Crawler mutations  
AUDIT_LOGS/crawl_mutations/

Diagnostics  
AUDIT_LOGS/diagnostics/

Simulation results  
AUDIT_LOGS/simulations/

---

## Output Rule

Execution outputs must always be written to artifact files.

Silent execution without artifact output is prohibited.