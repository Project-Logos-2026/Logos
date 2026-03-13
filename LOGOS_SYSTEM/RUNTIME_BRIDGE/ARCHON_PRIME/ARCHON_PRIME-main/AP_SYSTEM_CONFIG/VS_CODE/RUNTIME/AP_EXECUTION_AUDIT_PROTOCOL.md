# AP_EXECUTION_AUDIT_PROTOCOL

Artifact ID: OPS-RUN-001  
System: ARCHON_PRIME  
Artifact Type: Execution Logging Protocol  
Status: Active

---

## Purpose

Defines how execution runs are recorded and audited.

All execution activity must be traceable.

---

## Execution Log Types

Execution Summary  
Validation Reports  
Diagnostic Reports  
Mutation Reports

---

## Artifact Storage

Execution artifacts must be written to:

AUDIT_LOGS/

Subdirectories may include:

audit_deltas  
crawl_mutations  
diagnostics

---

## Traceability Requirement

Each artifact must reference:

Prompt ID  
Source Artifact  
Timestamp

---

## Failure Auditing

When execution fails the following must be recorded:

Failing step  
Affected files  
Error output  
Partial mutation state

Failure artifacts must never overwrite previous reports.