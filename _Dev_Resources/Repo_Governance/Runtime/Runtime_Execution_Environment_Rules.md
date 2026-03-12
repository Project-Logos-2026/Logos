# Runtime_Execution_Environment_Rules

**Governance Domain:** Runtime  
**Scope:** All Runtime_Tools and LOGOS_SYSTEM runtime modules during execution  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Runtime  

---

## 1. Purpose

This document defines the behavioral constraints and execution rules for all runtime modules and Runtime_Tools during execution. These rules enforce LOGOS's governance-first, fail-closed posture.

---

## 2. Core Execution Principles

### 2.1 No Autonomous Action

Runtime modules and tools MUST NOT:

- Take autonomous action with real-world effect (network calls, file system mutations outside canonical paths, process spawning).
- Initiate external communications.
- Modify source files, governance artifacts, or Coq proof artifacts.
- Delete, rename, or restructure directories outside explicitly authorized paths.

### 2.2 Fail-Closed Default

The default failure posture is `FAIL_CLOSED`:

- On unexpected input: refuse and log.
- On missing dependency: raise `ImportError` or log and skip, never silently continue.
- On filesystem write failure: raise; never swallow the error.
- On governance constraint detection: halt and report.

### 2.3 Determinism

- Runtime execution must be deterministic for identical inputs.
- No use of `random`, `uuid`, `time.time()` as primary keys in output.
- All output ordering (lists, keys) must be stable: sort before writing.

---

## 3. I/O Rules

### 3.1 Input

- CLI tools: input only via `argparse`; no interactive prompts.
- Runtime modules: input via explicit function arguments or constructor parameters.
- No reading from environment variables to determine behavioral logic (only for path resolution if the variable is documented).

### 3.2 Output — Canonical Routing

All write operations must target canonical paths:

| Operation Type | Permitted Target |
|---|---|
| Tool reports | `_Dev_Resources/Reports/Tool_Outputs/Runtime/` |
| Governance reports | `_Dev_Resources/Reports/_Dev_Governance/` |
| Dependency wiring logs | `_Dev_Resources/Repo_Inventory/Master_Indexes/Runtime/` |
| Environment indexes | `_Dev_Resources/Repo_Inventory/Master_Indexes/Environment/` |
| Manifests | `_Dev_Resources/Repo_Inventory/Master_Manifests/` |

Writing to any path outside these targets is prohibited without explicit authorization.

### 3.3 Read Access

- Runtime_Tools may read any file in the repository for analysis purposes.
- They must not cache files outside of in-process memory during the run.
- They must not write temporary files unless to a designated `_Reports/` subdirectory with cleanup.

---

## 4. Import Rules

- stdlib only by default; third-party packages must be declared in `requirements.txt`.
- No circular imports.
- No import of dev tooling (`_Dev_Resources/Dev_Tools/`) into runtime modules.
- No import of runtime modules (`LOGOS_SYSTEM/`) into dev tools that would trigger runtime boot.

---

## 5. Process Isolation

- Runtime_Tools execute as standalone scripts; they must not assume any global state from a prior tool run.
- Each tool invocation must be idempotent: running the same tool twice with the same arguments produces the same output (overwriting the previous report at the canonical path).
- No shared mutable global state between tool executions.

---

## 6. Security Constraints

- No execution of shell commands via `subprocess`, `os.system`, or `os.popen` unless the command is safe and sandboxed to the workspace.
- No external network access.
- No writing of credentials, tokens, or environment secrets to any artifact.
- No eval, exec, or dynamic code construction from user-supplied input.
- SQL/command injection prevention: use parameterized patterns; never format user input into command strings.

---

## 7. Execution Classification

Each Runtime_Tool must declare one of the following execution classes in its header:

| Class | Behavior |
|---|---|
| `READ_ONLY` | Reads data; writes only to canonical report path |
| `WRITE_SAFE` | Writes to canonical paths only; no source modifications |
| `DESTRUCTIVE` | May modify, move, or delete source content (requires explicit authorization) |

Destructive class tools must be listed in `Tool_Index/destructive_tools_index.json` and require additional governance authorization to invoke.

---

## 8. Exclusion Zones

Runtime tools and runtime modules MUST NEVER inspect, read, modify, or interact with:

- `STARTUP/PXL_Gate/` (Coq proof gate — hard exclusion)
- `STARTUP/Runtime_Compiler/` (Coq compilation artifacts — hard exclusion)
- Any file with `.v` extension (Coq proofs)
- `CoqMakefile`, `_CoqProject` (build artifacts)

Attempts to access exclusion zones must cause hard failure and log a governance violation.

---

## 9. Logging Requirements

Every tool execution must produce a log/report artifact. Silent operations are failures.

Minimum log content:
- Tool name
- Invocation timestamp (UTC)
- Arguments used
- Operations performed
- Errors encountered (or `[]` if none)
- Final status: `PASS` / `FAIL` / `PARTIAL` / `SKIPPED`

---

## 10. Cross-References

| Document | Location |
|---|---|
| Runtime_Artifact_Formatting_Spec.md | `Repo_Governance/Runtime/` |
| Dependency_Wiring_Log_Contract.md | `Repo_Governance/Runtime/` |
| Dev_Resources_Freeze_Protocol.md | `Repo_Governance/Developer/` |
| Development_Rules.json | `Repo_Governance/Developer/` |
