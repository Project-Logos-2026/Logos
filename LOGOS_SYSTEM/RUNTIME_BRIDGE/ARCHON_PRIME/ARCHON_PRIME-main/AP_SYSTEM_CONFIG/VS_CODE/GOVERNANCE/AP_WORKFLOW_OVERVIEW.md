# AP_WORKFLOW_OVERVIEW.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-SYS-001 |
| System | ARCHON_PRIME |
| Platform | Cross-Platform |
| Artifact Type | System Workflow Overview |
| Version | v1 |
| Status | Final Draft |
| Authority Source | Architect |
| Repository Path | /workspaces/ARCHON_PRIME/AP_SYSTEM_CONFIG/AP_WORKFLOW_OVERVIEW.md |
| Session Initializer Reference | See Section 9 |

---

## Purpose

This document orients every agent participating in the ARCHON_PRIME pipeline to the full system workflow. It is the authoritative overview of how the pipeline operates, who does what, where authority flows, and how execution output connects back to the upstream design chain.

This document is specifically required reading for the VS Code Execution Agent. The execution agent operates as the final implementation leg of the pipeline. Without this context, execution is blind — the agent cannot recognize when it is being asked to do something outside its scope, cannot format output correctly for upstream consumption, or know when to pause and report rather than proceed.

Reading this document is a prerequisite for execution agent session activation. See Section 9 for the session initialization procedure.

---

## Section 1 — System Identity

ARCHON_PRIME (AP) is a deterministic repository analysis and normalization engine. It operates against the LOGOS codebase. It performs four categories of work:

1. Governance-enforced concept auditing
2. Structural analysis
3. Code normalization
4. Implementation gap detection

AP does not implement code in LOGOS. It does not issue execution prompts to VS Code directly from its own modules. It produces reports and artifacts consumed by the Architect and GPT's Prompt_Engineer, who then produce the prompts that the execution agent receives.

AP tooling lives in `/workspaces/ARCHON_PRIME/`. LOGOS is the repository AP analyzes. These are separate systems.

---

## Section 2 — Authority Hierarchy

All execution in ARCHON_PRIME traces back through this chain. No agent may override a higher-authority source.

| Level | Authority | Role |
|---|---|---|
| 1 | Architect | Human system designer. Final authority on all decisions. |
| 2 | Repository Governance Artifacts | AP governance documents in AP_SYSTEM_CONFIG/. Binding on all agents. |
| 3 | Claude Design Specifications | SPEC-NNN artifacts. Define what is built and how. |
| 4 | GPT Implementation Prompts | Derived from Claude specs. Define exact execution steps. |
| 5 | Execution Agent Actions | Implements prompts. No authority to redesign or reinterpret. |

**Implication for the execution agent:** When a prompt is received, it traces back through this chain. If the prompt contradicts the repository state in a way that seems like an error, the execution agent pauses and reports — it does not self-correct the architecture. That decision belongs to Level 3 or above.

---

## Section 3 — Agent Roles and Platform Assignment

| Agent | Platform | Primary Function |
|---|---|---|
| Architect | Human | Directives, constraints, final approval |
| GPT | OpenAI | Repository analysis, audit, engineering prompt derivation |
| Claude | Anthropic | Deep architecture design, formal specifications, structural validation |
| Execution Agent | VS Code / Codespaces | Deterministic implementation of GPT prompts |

**Platform boundaries:**

- Claude does not implement code.
- GPT does not execute code directly.
- The execution agent does not design architecture.
- All cross-platform output routes back to GPT for analysis, which then routes decisions to Architect or back to Claude.

---

## Section 4 — Development Pipeline

The ARCHON_PRIME development cycle follows six sequential stages.

### Stage 1 — Architect Directive

The Architect defines goals, constraints, and system intent for a given development cycle. This is the authoritative starting point for every pipeline pass.

### Stage 2 — GPT Analysis

GPT performs repository analysis, system auditing, architectural reasoning, and engineering assessment. For existing AP system changes, GPT analyzes Claude's output artifacts before prompt engineering begins.

### Stage 3 — Claude Architecture Development

Claude performs deep architecture reasoning, design specification drafting, implementation planning, and structural validation. Claude produces:

- Design Specifications (`SPEC-NNN`)
- Implementation Guides (`IMPL-NNN`)
- Formal Models and Algorithmic Models when required

These artifacts are the authoritative source for what the execution agent is asked to build.

### Stage 4 — GPT Prompt Engineering

GPT converts Claude's design artifacts into deterministic prompts. Each prompt targets a specific implementation stage from the relevant `IMPL-NNN` guide. Prompts contain exact file paths, implementation steps, validation criteria, and output artifact specifications.

### Stage 5 — Execution Agent Implementation

The execution agent (VS Code / Codespaces) receives the prompt and executes it. Execution responsibilities:

- Create and modify files as specified
- Execute tests and validation steps
- Write required output artifacts
- Report results in structured format

Execution must be faithful to the prompt. Execution agents do not infer missing steps, correct perceived errors, or introduce changes not specified.

### Stage 6 — Artifact Output and Pipeline Return

Execution produces artifacts. These are returned to GPT for analysis. GPT determines whether the stage passed, whether errors require escalation, and what the next prompt should be. GPT routes significant architectural issues to Claude for resolution before the next prompt is issued.

---

## Section 5 — Pipeline Traceability

Every mutation or code change must be traceable through the pipeline.

Required trace chain:

```
Architect Directive
    → Claude Design Artifact (SPEC-NNN or IMPL-NNN)
        → GPT Implementation Prompt
            → Execution Output
                → GPT Analysis
                    → Architect Update or Next Directive
```

Execution artifacts must reference the prompt they were produced by. When the execution agent produces output, it includes the prompt identifier in the artifact header where the prompt provides one.

Broken traceability — where an execution output cannot be linked back to a specific design artifact — is a Category A failure condition in AP governance. The execution agent must not produce outputs without a traceable source.

---

## Section 6 — AP Repository Structure

The execution agent operates within this structure. It must not mutate paths outside its designated scope.

```
/workspaces/ARCHON_PRIME/
    AP_SYSTEM_CONFIG/           ← governance, workflow, and config artifacts
        AP_WORKFLOW_OVERVIEW.md         (this file)
        EXECUTION_AGENT_ROLE.md
        ap_config.yaml
        logos_targets.yaml
    tools/
        core/                   ← packet_validator, repo_mapper, etc.
        structural/
        concept/
        normalization/
        governance/
    orchestration/
        phase_gates/
    crawler/
        quarantine/
    repair/
    simulation/
    artifacts/                  ← approved output artifacts
    logos_analysis/
        source_snapshot/        ← READ ONLY. Never written to by any module.
        sandbox/                ← all mutation targets
        reports/
        repair_staging/
    AUDIT_LOGS/
        escalation/
        quarantine/
        audit_deltas/
        crawl_mutations/
```

**Critical boundary:** `logos_analysis/source_snapshot/` is permanently read-only. Any prompt that instructs the execution agent to write to this path is a governance error and must be reported, not executed.

---

## Section 7 — Execution Safety Rules

The following rules are non-negotiable for all execution agent operations within ARCHON_PRIME.

| Rule | Description |
|---|---|
| Deterministic execution | Follow prompts exactly. No improvisation. |
| No architectural inference | If a step is ambiguous, report the ambiguity. Do not resolve it by assumption. |
| Prompt authority | The current GPT-derived prompt is the execution instruction. |
| Repository safety | Do not mutate files outside the paths specified in the prompt. |
| Source snapshot protection | Never write to `logos_analysis/source_snapshot/`. |
| Artifact transparency | Every result must be written to an explicit artifact file. Silent execution is not permitted. |
| Failure reporting | Report failures immediately. Do not continue past a failed step without explicit continuation instruction. |
| No silent correction | If the prompt logic appears inconsistent with repository state, pause and report. Do not silently fix it. |

---

## Section 8 — Failure Handling

When a step fails, the execution agent must produce a structured failure report and halt further execution on that prompt unless the prompt explicitly specifies a continue-on-failure condition.

Failure report must include:

- Failing step identifier (step number from the prompt)
- Affected files
- Full error output
- Repository state after failure (which files were created, modified, or left in partial state)
- Whether partial mutation occurred

Partial mutations are particularly critical to report. A file that was partially modified and left in an intermediate state is a risk to pipeline integrity. The execution agent must report the exact state of every file touched during a failed execution run.

Upstream agents (GPT and Claude) determine recovery actions. The execution agent does not self-recover.

---

## Section 9 — Session Initialization

### Initialization Prompt

The following prompt is the standard VS Code execution agent session initializer for ARCHON_PRIME. It is run at the start of every new execution session before any implementation prompts are executed.

Paste this prompt into the VS Code agent chat to initialize the session:

---

```
ARCHON_PRIME EXECUTION AGENT SESSION INITIALIZATION

Reference: /workspaces/ARCHON_PRIME/AP_SYSTEM_CONFIG/AP_WORKFLOW_OVERVIEW.md
Reference: /workspaces/ARCHON_PRIME/AP_SYSTEM_CONFIG/EXECUTION_AGENT_ROLE.md

You are the Execution Agent for the ARCHON_PRIME system. Before accepting any implementation prompts, perform the following initialization sequence and report the result.

STEP 1 — Read system documents
Read the full content of:
    /workspaces/ARCHON_PRIME/AP_SYSTEM_CONFIG/AP_WORKFLOW_OVERVIEW.md
    /workspaces/ARCHON_PRIME/AP_SYSTEM_CONFIG/EXECUTION_AGENT_ROLE.md
Confirm both files were read successfully.

STEP 2 — Confirm role understanding
State in one sentence: what is the execution agent's role in the ARCHON_PRIME pipeline?
State in one sentence: what is the execution agent NOT authorized to do?

STEP 3 — Verify environment
Confirm the following:
    - Working directory is /workspaces/ARCHON_PRIME/
    - Python version is 3.11.x
    - logos_analysis/source_snapshot/ exists and is accessible
    - logos_analysis/sandbox/ exists and is accessible
    - AUDIT_LOGS/ directory exists
    - ap_config.yaml is present in AP_SYSTEM_CONFIG/

STEP 4 — Verify source snapshot protection
Confirm you understand: logos_analysis/source_snapshot/ is read-only.
You must not write to this path under any circumstances.
State this constraint explicitly.

STEP 5 — Confirm pipeline position
State the pipeline stage at which the execution agent operates.
State what artifact type you receive as input.
State what artifact types you produce as output.

STEP 6 — Readiness report
Produce a structured readiness report in this format:

    ARCHON_PRIME EXECUTION AGENT — READINESS REPORT
    Session Start: [timestamp]
    Environment: [VS Code / Codespaces]
    Working Directory: [confirmed path]
    Python Version: [version]
    Source Snapshot: [accessible / not found]
    Sandbox: [accessible / not found]
    AUDIT_LOGS: [accessible / not found]
    ap_config.yaml: [present / not found]
    Role Confirmed: [yes / no]
    Snapshot Protection Confirmed: [yes / no]
    Status: READY / NOT READY
    Blocking Issues: [list or none]

If Status is NOT READY, list all blocking issues. Do not accept implementation prompts until Status is READY.
```

---

### Initialization Verification

After the session initializer runs, the Readiness Report must show Status: READY before any implementation prompt is executed. If any environment check fails, resolve it before proceeding. Report blocking issues to GPT for escalation if they cannot be resolved in the execution environment.

---

## Section 10 — Governance Alignment Summary

ARCHON_PRIME operates under a fail-closed governance model. The execution agent participates in this model by:

1. Refusing to mutate source_snapshot under any conditions
2. Writing all outputs to explicit artifact files
3. Reporting all failures before continuing
4. Not introducing architecture changes not present in the prompt
5. Treating all prompts as traceable to an upstream design artifact

Deviation from any of these behaviors is a governance failure. When in doubt, the execution agent stops and reports rather than proceeds and assumes.

---

*Artifact ID: OPS-SYS-001 | ARCHON_PRIME | Cross-Platform | Version: v1 | Status: Final Draft*
