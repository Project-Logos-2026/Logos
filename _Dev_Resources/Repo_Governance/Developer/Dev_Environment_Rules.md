# Dev_Environment_Rules

**Governance Domain:** Developer  
**Scope:** `/workspaces/Logos/_Dev_Resources` and all tooling invoked within the LOGOS codespace  
**Status:** ACTIVE  
**Version:** 1.0  
**Authority:** Repo_Governance/Developer  

---

## 1. Purpose

This document defines the authoritative rules governing the developer environment within the LOGOS repository. All agent activity, automated tooling, and manual operations executed inside the dev container must comply with these rules.

---

## 2. Environment Baseline

### 2.1 Runtime

- **Container OS:** Ubuntu 24.04 LTS (dev container)
- **Python interpreter:** `/workspaces/Logos/.venv/bin/python3`
- **Active virtual environment:** `/workspaces/Logos/.venv`
- **Repository root:** `/workspaces/Logos`
- **Workspace root marker:** `pytest.ini`, `requirements.txt`, `pyrightconfig.json`

### 2.2 Virtual Environment Rules

- All Python execution MUST use the `.venv` interpreter.
- The `.venv` directory is a runtime artifact. It MUST NOT be committed to version control.
- Package installation MUST reference `requirements.txt`; ad-hoc installs to `.venv` must be followed by an update to `requirements.txt`.
- The active venv MUST be sourced before any dev tool invocation:  
  `source /workspaces/Logos/.venv/bin/activate`

### 2.3 Python Environment Constraints

- No wildcard imports (`from module import *`) anywhere in `_Dev_Resources`.
- All imports must be explicit and fully qualified where cross-package.
- `__pycache__` directories are ephemeral and must not be governed or committed as artifacts.

---

## 3. Tool Invocation Rules

### 3.1 Runtime_Tools

- All Runtime_Tool scripts MUST be invoked from the repository root or with explicit path resolution anchored to `/workspaces/Logos`.
- CLI entry points must use `argparse`; no interactive prompts are permitted.
- All tool output must route to canonical paths (see `Dev_Tool_Generation_Policy.md`).

### 3.2 Repo_Governance_Tools

- Governance tools may only read, classify, or report. They must never modify source files without explicit authorization artifacts.
- Governance tools must reference `Header_Schemas` for output template compliance.

### 3.3 Dev Environment Tooling Availability

The following tools are available in the dev environment and may be used by automated agents and tooling scripts:

| Tool | Use |
|---|---|
| `python3` / `.venv` | Script execution |
| `pytest` | Test execution (scoped by `pytest.ini`) |
| `git` | Version control |
| `find`, `grep`, `tree` | Repository inspection |
| `coq_makefile`, `make` | Coq proof compilation only |

---

## 4. Environment Mutation Rules

### 4.1 Permitted Mutations

- Writing output artifacts to `_Reports/` subdirectories.
- Writing output artifacts to `_Dev_Resources/Repo_Inventory/`.
- Modifying tool scripts inside `Dev_Tools/Runtime_Tools/` (when authorized).
- Installing packages (must update `requirements.txt`).

### 4.2 Prohibited Mutations

- Modifying any file under `STARTUP/PXL_Gate/` or `STARTUP/Runtime_Compiler/`.
- Modifying any Coq proof artifact (`.v`, `CoqMakefile`, `_CoqProject`).
- Modifying `Header_Schemas/` (frozen — see `Dev_Resources_Freeze_Protocol.md`).
- Creating directories outside explicitly authorized paths (see `Directory_Creation_Authorization_Rules.md`).
- Deleting or renaming `Processing_Center/` or any of its four immediate subdirectories.

---

## 5. Test Execution Rules

- Default `pytest` scope is governed by `pytest.ini` (governance and agent tests).
- Extended test runs must use `pytest <path>` with explicit target.
- Tests must never modify runtime modules, governance artifacts, or Coq stacks.
- Test artifacts (output files) must route to `_Reports/Test_Artifacts/`.

---

## 6. Logging and Auditability

- All automated dev environment operations must produce a report artifact in `_Reports/`.
- Silent operations are treated as failures (per `governance_auditability` in Development_Rules.json).
- Report naming: `<tool_name>_<operation>_report.json` in `Title_Case_With_Underscores`.
- Timestamps in all log artifacts must be UTC ISO-8601.

---

## 7. Security and Isolation

- Dev tooling must never establish external network connections.
- No credentials, secrets, or environment variables containing sensitive data may be logged.
- Agent operations are sandboxed to the workspace root; no paths outside `/workspaces/Logos` may be targeted.

---

## 8. Cross-References

| Document | Location |
|---|---|
| Development_Rules.json | `Repo_Governance/Developer/Development_Rules.json` |
| Dev_Resources_Directory_Contract.md | `Repo_Governance/Developer/Dev_Resources_Directory_Contract.md` |
| Dev_Resources_Freeze_Protocol.md | `Repo_Governance/Developer/Dev_Resources_Freeze_Protocol.md` |
| Header_Schemas | `Repo_Governance/Header_Schemas/` (FROZEN) |
