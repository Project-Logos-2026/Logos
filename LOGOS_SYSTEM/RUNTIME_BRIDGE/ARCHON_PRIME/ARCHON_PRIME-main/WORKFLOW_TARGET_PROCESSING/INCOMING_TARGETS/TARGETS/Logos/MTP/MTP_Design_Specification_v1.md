# LOGOS Multi-Tick Processing Protocol (MTP) — Design Specification

**Version**: 1.0.0  
**Status**: DRAFT  
**Date**: 2026-03-06  
**Authority**: LOGOS V1 Architecture  
**Scope**: Multi-tick task execution, state persistence, and continuity management  
**Spec Type**: Non-executable design artifact  
**Tier**: T3 (Foundational Infrastructure)

---

## 1. Overview

The Multi-Tick Processing Protocol (MTP) governs how tasks span multiple execution ticks within a LOGOS session. MTP provides the infrastructure for task state persistence, continuity context, and resumption mechanics that enable complex cognitive processing beyond single-tick completion.

**Core Responsibility**: MTP transforms the runtime from a stateless tick executor into a stateful task processor capable of maintaining coherent work across temporal boundaries.

**Architectural Position**: MTP is operations-side infrastructure that bridges Logos Core's tick orchestration with the cognitive protocols (SCP, ARP) that require multi-tick execution depth.

**Key Principle**: Tasks are ephemeral; task state is persistent. MTP manages the state while Logos Core manages the execution.

---

## 2. Terminology

**Tick**: A single quantum of execution in the LOGOS runtime. Each tick is a complete pass through the Logos Agent's `_on_tick()` and `_process_task()` lifecycle.

**Multi-Tick Task**: A task that cannot complete within a single tick and requires state persistence across multiple ticks.

**Task State**: The complete context required to resume a task at a given tick, including partial results, cognitive context, and progression markers.

**Continuity Token**: A serialized representation of task state that MTP maintains between ticks.

**Task Lifecycle**: The progression from task reception through multi-tick processing to completion or termination.

**Tick Budget**: The maximum number of ticks allocated to a single task. Default: 50 ticks (per EA spec §12.2).

**Task Resumption**: The process of reconstructing task context from a continuity token at tick N+1.

**MTP Nexus**: The central coordination point for multi-tick task management, state persistence, and continuity context distribution.

**Context Link**: An AA type (`context_link`) that MTP produces to bind sequential processing steps across ticks.

---

## 3. Architectural Position

### 3.1 Dependency Relationships

**MTP depends on**:
- Logos Core (tick orchestration, agent lifecycle)
- UWM (EA state access for task context)
- SOP (operational logging for task lifecycle events)

**MTP provides to**:
- Logos Agent (task state persistence and resumption interface)
- Sub-agents I1, I2, I3 (continuity context for multi-tick analysis)
- CSP (task-in-progress context for semantic analysis)
- SCP (partial results for projection)
- ARP (intermediate reasoning states for axiom reconciliation)

### 3.2 Authority Boundaries

**MTP has authority to**:
- Persist task state between ticks
- Generate continuity tokens
- Propose `context_link` AAs to UWM
- Track tick budgets and enforce limits
- Determine task completion vs continuation

**MTP does NOT have authority to**:
- Create or modify SMPs (Logos Agent sovereignty)
- Attach AAs (Logos Agent sovereignty)
- Modify task definitions
- Execute cognitive analysis
- Make classification decisions

---

## 4. Task Lifecycle Model

### 4.1 Task Reception (Tick 0)

When Logos Core receives a new task:
1. Task enters Logos Agent's `_process_task()` method
2. Logos Agent queries MTP: "Is this continuable?"
3. MTP evaluates task complexity heuristics
4. MTP returns: `SINGLE_TICK` or `MULTI_TICK_REQUIRED`

**INV-MTP-01**: All tasks must be classified as single-tick or multi-tick before processing begins.

### 4.2 Single-Tick Execution Path

For `SINGLE_TICK` tasks:
1. Logos Agent processes task to completion in current tick
2. MTP is not engaged
3. Task completes, result returned

**INV-MTP-02**: Single-tick tasks must never produce continuity tokens.

### 4.3 Multi-Tick Execution Path

For `MULTI_TICK_REQUIRED` tasks:

**Tick 1 (Initialization)**:
1. Logos Agent begins task processing
2. Sub-agents produce partial analysis
3. Logos Agent requests MTP to persist state
4. MTP generates initial continuity token
5. MTP proposes `context_link` AA to bind tick 1 results
6. Tick completes with `task_status: in_progress`

**Ticks 2...N (Continuation)**:
1. Logos Agent requests MTP to restore state
2. MTP provides continuity token → task context
3. Sub-agents receive prior context + current tick input
4. Sub-agents extend analysis
5. Logos Agent requests MTP to update state
6. MTP generates updated continuity token
7. MTP proposes new `context_link` AA
8. Tick completes with `task_status: in_progress`

**Tick N (Completion)**:
1. Logos Agent determines task is complete
2. Logos Agent finalizes EA classification
3. MTP marks task as `completed`
4. MTP discards continuity token
5. Tick completes with `task_status: completed`

**INV-MTP-03**: Every multi-tick task must have exactly one active continuity token at any given tick.

**INV-MTP-04**: Continuity tokens must be discarded immediately upon task completion or termination.

### 4.4 Task Termination

Tasks may terminate before completion due to:
- Tick budget exhaustion (§4.6)
- Explicit rejection by Logos Agent
- Governance violation detected
- Resource budget exhaustion

**Termination protocol**:
1. Logos Agent signals termination to MTP
2. MTP marks task as `terminated`
3. MTP proposes `governance_annotation` AA with termination reason
4. MTP discards continuity token
5. Task state cleared

**INV-MTP-05**: Terminated tasks must never be resumable.

### 4.5 State Persistence Contract

**What MTP persists**:
- Task identifier and type
- Current tick count
- Partial EA identities produced
- Sub-agent intermediate results
- Progression markers (e.g., "SCP analysis complete, ARP pending")

**What MTP does NOT persist**:
- Mutable cognitive state (CSP's domain)
- Canonical SMPs (persistent in CSP Canonical Store)
- Sub-agent internal state (reconstructed per tick)
- Runtime configuration

**INV-MTP-06**: MTP state persistence must be session-scoped only; no cross-session continuity is permitted in V1.

### 4.6 Tick Budget Enforcement

**Default budget**: 50 ticks per task (aligned with EA spec §12.2)

**Enforcement mechanism**:
- MTP tracks tick count per task
- At tick 50, MTP signals Logos Agent: `BUDGET_EXHAUSTED`
- Logos Agent attaches `governance_annotation` AA
- Task terminated per §4.4

**INV-MTP-07**: Tick budgets must be enforced fail-closed; exceeding budget is a governance violation.

**INV-MTP-08**: Tick budget exhaustion must always produce an auditable governance_annotation AA.

---

## 5. Continuity Token Model

### 5.1 Token Structure

A continuity token is a serialized Python dict with the following structure:

```python
{
    "task_id": str,                    # Unique task identifier
    "task_type": str,                  # Task classification
    "current_tick": int,               # Current tick number (1-indexed)
    "tick_budget_remaining": int,      # Ticks remaining before exhaustion
    "active_ea_ids": list[str],        # SMPs produced so far
    "partial_results": dict,           # Sub-agent intermediate outputs
    "progression_markers": dict,       # Protocol completion flags
    "metadata": dict                   # Creation time, session_id, etc.
}
```

**INV-MTP-09**: Continuity tokens must be deterministically serializable and deserializable.

**INV-MTP-10**: Continuity tokens must contain no executable content, no code references, and no mutable state pointers.

### 5.2 Token Generation

Triggered by: Logos Agent requests state persistence after processing tick

**Generation protocol**:
1. Logos Agent provides current task context
2. MTP extracts task_id, tick count, EA IDs
3. MTP collects sub-agent partial results from tick_result
4. MTP constructs token dict
5. MTP serializes to JSON string
6. MTP stores in MTP Nexus keyed by task_id

**INV-MTP-11**: Token generation must occur before tick completion.

### 5.3 Token Restoration

Triggered by: Logos Agent requests state restoration at tick N+1

**Restoration protocol**:
1. Logos Agent provides task_id
2. MTP retrieves serialized token from MTP Nexus
3. MTP deserializes JSON → dict
4. MTP validates token integrity (schema, tick continuity)
5. MTP returns task context to Logos Agent
6. Logos Agent distributes context to sub-agents

**INV-MTP-12**: Token restoration must fail-closed if token is missing, corrupted, or schema-invalid.

### 5.4 Token Lifecycle

```
Task begins (Tick 1)
    ↓
Token created (end of Tick 1)
    ↓
Token stored in MTP Nexus
    ↓
[Tick 2...N-1: Token updated per tick]
    ↓
Task completes/terminates (Tick N)
    ↓
Token discarded (immediately)
```

**INV-MTP-13**: Tokens must never persist beyond the session in which they were created.

---

## 6. MTP Nexus

### 6.1 Architecture

The MTP Nexus is the centralized state management component for all active continuity tokens.

**Responsibilities**:
- Store/retrieve continuity tokens by task_id
- Enforce token lifecycle (create → update → discard)
- Provide query interface for active tasks
- Track tick budgets globally
- Emit task lifecycle events to SOP

**Storage Model**: In-memory dict keyed by task_id

```python
{
    "task_123": {
        "token": {...},           # Continuity token
        "status": str,            # in_progress | completed | terminated
        "created_at": str,        # ISO-8601
        "last_updated_tick": int  # Last tick token was modified
    }
}
```

**INV-MTP-14**: MTP Nexus storage must be session-scoped; cleared at session end.

### 6.2 Interface Methods

**Required methods** (entailed from §5, §4):

```python
class MTPNexus:
    def create_token(self, task_id: str, context: dict) -> str:
        # Generate initial continuity token
        
    def update_token(self, task_id: str, context: dict) -> str:
        # Update existing token with new tick context
        
    def restore_token(self, task_id: str) -> dict:
        # Retrieve token and deserialize to context
        
    def discard_token(self, task_id: str) -> bool:
        # Remove token and mark task complete/terminated
        
    def get_active_tasks(self) -> list[str]:
        # Return list of task_ids with active tokens
        
    def check_budget(self, task_id: str) -> tuple[int, int]:
        # Returns: (current_tick, ticks_remaining)
```

**INV-MTP-15**: All MTP Nexus methods must be idempotent and fail-closed.

### 6.3 Concurrency Model

**V1 Constraint**: LOGOS V1 operates single-threaded per session. MTP Nexus does not require concurrency control.

**V1.1+ Forward Compatibility**: If multi-session or concurrent execution is introduced, MTP Nexus must add locking mechanisms to prevent token corruption.

---

## 7. Context Link AA Production

### 7.1 Purpose

MTP produces `context_link` AAs to bind sequential processing ticks within the EA lifecycle. These AAs provide cognitive protocols with continuity context without violating EA immutability.

**Example**: SCP analyzing a multi-tick task needs to know which prior EAs contributed partial semantic projections. MTP's `context_link` AAs provide this chain.

### 7.2 AA Structure

Per EA spec §5.2, `context_link` AAs have the following content structure:

```python
{
    "aa_id": str,              # Format: <smp_id>:AA:<index>
    "aa_type": "context_link",
    "content": {
        "prior_tick": int,
        "prior_ea_ids": list[str],
        "continuation_type": str,  # sequential | branching | convergent
        "progression_marker": str   # e.g., "SCP_complete_ARP_pending"
    },
    "producer": "mtp_nexus",
    "timestamp": str
}
```

### 7.3 Production Protocol

**Trigger**: End of each multi-tick task tick (Ticks 1...N-1)

**Protocol**:
1. Logos Agent completes tick processing
2. Logos Agent requests MTP to persist state
3. MTP generates continuity token
4. MTP constructs `context_link` AA
5. MTP returns AA proposal to Logos Agent
6. Logos Agent reviews and attaches AA via SMP_Store.append_aa()

**INV-MTP-16**: MTP must propose exactly one context_link AA per multi-tick processing tick.

**INV-MTP-17**: MTP must never attach AAs directly; all attachment flows through Logos Agent review.

---

## 8. Integration Surface

### 8.1 Logos Core Integration

**Injection Point**: MTP Nexus injected into RuntimeLoop at construction

**Interface**:
- RuntimeLoop provides session_id to MTP Nexus
- RuntimeLoop invokes MTP Nexus lifecycle hooks:
  - `on_session_start()`: Initialize Nexus storage
  - `on_session_end()`: Discard all tokens, clear storage
- Logos Agent queries MTP Nexus via injected reference

**INV-MTP-18**: MTP Nexus must be injected into all agent wrappers via their constructors.

### 8.2 UWM Integration

**Read-only relationship**: MTP reads EA state to extract task context but does not modify EAs.

**Query patterns**:
- MTP queries UWM for active EA IDs associated with task
- MTP extracts partial results from EA AA catalogs
- MTP synthesizes continuity context from EA progression

**INV-MTP-19**: MTP must never write to UWM; all EA modifications flow through Logos Agent.

### 8.3 Sub-Agent Integration (I1, I2, I3)

**Continuity context distribution**:
- Logos Agent receives restored task context from MTP
- Logos Agent includes context in sub-agent `_on_tick()` input
- Sub-agents use context to inform current tick analysis
- Sub-agents return updated results in tick_result

**Protocol-specific integration**:
- **I1 (SCP)**: Receives prior semantic projection results
- **I2 (MTP)**: Receives task decomposition state (self-referential)
- **I3 (ARP)**: Receives intermediate axiom reconciliation results

**INV-MTP-20**: Sub-agents must treat continuity context as read-only; they cannot modify prior tick results.

### 8.4 SOP Integration

**Logging events** (entailed from EA spec §15.1):

```python
MTP_LIFECYCLE_EVENTS = {
    "mtp_task_classified": {
        "trigger": "Task classified as MULTI_TICK_REQUIRED",
        "data": ["task_id", "task_type", "tick"]
    },
    "mtp_token_created": {
        "trigger": "Continuity token generated",
        "data": ["task_id", "tick", "token_size_bytes"]
    },
    "mtp_token_restored": {
        "trigger": "Continuity token restored",
        "data": ["task_id", "tick", "prior_tick"]
    },
    "mtp_budget_warning": {
        "trigger": "Tick budget at 80% threshold",
        "data": ["task_id", "ticks_remaining"]
    },
    "mtp_budget_exhausted": {
        "trigger": "Tick budget limit reached",
        "data": ["task_id", "final_tick"]
    },
    "mtp_task_completed": {
        "trigger": "Multi-tick task completed",
        "data": ["task_id", "total_ticks", "completion_status"]
    },
    "mtp_task_terminated": {
        "trigger": "Task terminated before completion",
        "data": ["task_id", "termination_reason", "final_tick"]
    }
}
```

**INV-MTP-21**: MTP must emit all lifecycle events to SOP operational logger with no audit readback.

---

## 9. Task Classification Heuristics

### 9.1 Single-Tick Indicators

A task is classified as `SINGLE_TICK` if:
- Task type is `observation` (simple perception, no reasoning)
- Task has explicit `single_tick: true` metadata
- Task references no prior EAs (no continuity required)

### 9.2 Multi-Tick Indicators

A task is classified as `MULTI_TICK_REQUIRED` if:
- Task type is `plan_fragment` (requires decomposition)
- Task involves axiom reconciliation (ARP activation)
- Task explicitly declares multi-tick requirement
- Task references prior EAs requiring synthesis

### 9.3 Default Behavior

**INV-MTP-22**: When classification is ambiguous, MTP must default to `MULTI_TICK_REQUIRED` (conservative, fail-safe).

### 9.4 Reclassification

**INV-MTP-23**: Tasks classified as SINGLE_TICK must never transition to MULTI_TICK mid-execution.

**Edge case**: If a SINGLE_TICK task unexpectedly requires continuation, Logos Agent must terminate the task and create a new MULTI_TICK task with explicit chaining.

---

## 10. Governance Constraints

### 10.1 Inertness

**INV-MTP-24**: Continuity tokens must be inert data structures with no executable content.

**Prohibited content**:
- Code or lambda functions
- Template references
- Continuation pointers to runtime state
- Mutable external references

### 10.2 Determinism

**INV-MTP-25**: Identical task context at tick N must produce identical continuity token.

**INV-MTP-26**: Continuity token restoration must be deterministic; same token always produces same task context.

### 10.3 Session Isolation

**INV-MTP-27**: Continuity tokens must never escape their originating session.

**INV-MTP-28**: MTP Nexus storage must be cleared completely at session end with no persistence mechanism.

### 10.4 Fail-Closed Semantics

**INV-MTP-29**: All MTP errors (token corruption, missing token, budget violation) must halt task processing immediately.

**INV-MTP-30**: MTP must never silently recover from errors; all failures produce logged governance violations.

---

## 11. Error Handling

### 11.1 Token Corruption

**Scenario**: Continuity token fails schema validation or deserialization

**Response**:
1. MTP logs error to SOP
2. MTP raises `TokenCorruptionError`
3. Logos Agent terminates task
4. Logos Agent attaches `governance_annotation` AA with error details

**INV-MTP-31**: Corrupted tokens must never be partially restored; fail-closed only.

### 11.2 Missing Token

**Scenario**: Logos Agent requests restoration for non-existent task_id

**Response**:
1. MTP logs error to SOP
2. MTP raises `TokenNotFoundError`
3. Logos Agent terminates task
4. Operational alert raised (possible runtime corruption)

**INV-MTP-32**: Missing tokens indicate critical runtime failure and must trigger operator notification.

### 11.3 Budget Violations

**Scenario**: Task attempts to continue beyond tick budget

**Response**:
1. MTP detects budget exhaustion at tick 50
2. MTP signals Logos Agent: `BUDGET_EXHAUSTED`
3. Logos Agent attaches `governance_annotation` AA
4. Task terminated per §4.4
5. Event logged to SOP

**INV-MTP-33**: Budget violations must never result in silent continuation past limit.

### 11.4 Schema Evolution Failures

**Scenario**: V1.1+ introduces new token schema; V1 tokens incompatible

**Response** (forward compatibility guidance):
1. MTP Nexus detects schema version mismatch
2. MTP raises `SchemaVersionError`
3. Session terminated (cannot proceed with incompatible state)
4. Operator notified for manual intervention

**INV-MTP-34**: Schema version mismatches must be treated as critical failures with no automatic migration.

---

## 12. Observability

### 12.1 Metrics

**MTP exposes to SOP**:
- Active task count (current session)
- Average ticks per task
- Budget exhaustion rate
- Token size distribution
- Task completion rate (completed vs terminated ratio)

### 12.2 Audit Trail

Per §8.4, MTP lifecycle events provide:
- Complete task lineage (task_id → all ticks)
- Token creation/restoration timestamps
- Budget warnings and violations
- Termination reasons

**INV-MTP-35**: MTP audit events must be write-only to SOP with no readback into MTP runtime.

---

## 13. Implementation Constraints

### 13.1 File Locations

| Component | Path |
|-----------|------|
| MTP_Nexus.py | `RUNTIME_OPPERATIONS_CORE/Multi_Tick_Processing_Protocol/MTP_Core/MTP_Nexus.py` |
| Task_Classifier.py | `MTP_Core/Task_Classifier.py` |
| Continuity_Token.py | `MTP_Core/Continuity_Token.py` |
| Budget_Tracker.py | `MTP_Core/Budget_Tracker.py` |

All paths relative to: `LOGOS_SYSTEM/RUNTIME_CORES/`

### 13.2 Dependencies

**Required imports**:
- UWM (EA state query)
- SOP (operational logging)
- Logos Core (agent wrapper injection points)

**Prohibited imports**:
- CSP (operations-side protocol, no direct dependency)
- SCP (cognitive protocol, no direct dependency)
- ARP (cognitive protocol, no direct dependency)

**INV-MTP-36**: MTP must depend only on infrastructure components (Logos Core, UWM, SOP), never on cognitive protocols.

### 13.3 Testing Strategy

**Unit tests**:
- Token serialization/deserialization
- Budget tracking and enforcement
- Task classification heuristics
- Nexus storage operations

**Integration tests**:
- Multi-tick task execution (3-tick minimum)
- Budget exhaustion scenario
- Token restoration across ticks
- Context_link AA production

**Compliance tests**:
- Inertness validation (no executable content in tokens)
- Session isolation (tokens cleared at session end)
- Fail-closed error handling (all error paths verified)

---

## 14. Forward Compatibility

### 14.1 V1.1+ Considerations

**Cross-session continuity** (not V1):
- V1 tokens are session-scoped only
- V1.1+ may introduce persistent token storage
- Migration path: add `session_id` prefix to task_id, version token schema

**Concurrent execution** (not V1):
- V1 assumes single-threaded execution
- V1.1+ may require MTP Nexus locking
- Migration path: add mutex per task_id, token versioning

**Dynamic budget allocation** (not V1):
- V1 uses fixed 50-tick budget
- V1.1+ may allow per-task budget customization
- Migration path: add `tick_budget` field to task metadata

### 14.2 Schema Versioning

**Token schema version field** (recommended for V1.1+):

```python
{
    "schema_version": "1.0.0",  # Semantic version
    "task_id": ...,
    # ... rest of token
}
```

**INV-MTP-37**: Future schema changes must increment schema_version and provide explicit migration paths.

---

## 15. Invariant Summary

| ID | Invariant |
|----|-----------|
| INV-MTP-01 | All tasks classified before processing |
| INV-MTP-02 | Single-tick tasks never produce tokens |
| INV-MTP-03 | Exactly one active token per multi-tick task |
| INV-MTP-04 | Tokens discarded immediately on completion/termination |
| INV-MTP-05 | Terminated tasks never resumable |
| INV-MTP-06 | State persistence session-scoped only |
| INV-MTP-07 | Tick budgets enforced fail-closed |
| INV-MTP-08 | Budget exhaustion produces governance_annotation AA |
| INV-MTP-09 | Tokens deterministically serializable |
| INV-MTP-10 | Tokens contain no executable content |
| INV-MTP-11 | Token generation before tick completion |
| INV-MTP-12 | Token restoration fail-closed on errors |
| INV-MTP-13 | Tokens never persist beyond session |
| INV-MTP-14 | MTP Nexus storage session-scoped |
| INV-MTP-15 | All Nexus methods idempotent and fail-closed |
| INV-MTP-16 | Exactly one context_link AA per tick |
| INV-MTP-17 | MTP never attaches AAs directly |
| INV-MTP-18 | MTP Nexus injected into all agent wrappers |
| INV-MTP-19 | MTP never writes to UWM |
| INV-MTP-20 | Sub-agents treat context as read-only |
| INV-MTP-21 | All lifecycle events logged with no readback |
| INV-MTP-22 | Ambiguous classification defaults to MULTI_TICK |
| INV-MTP-23 | No SINGLE → MULTI reclassification mid-execution |
| INV-MTP-24 | Tokens are inert data structures |
| INV-MTP-25 | Token generation is deterministic |
| INV-MTP-26 | Token restoration is deterministic |
| INV-MTP-27 | Tokens never escape session |
| INV-MTP-28 | Nexus cleared completely at session end |
| INV-MTP-29 | All errors halt processing immediately |
| INV-MTP-30 | No silent error recovery |
| INV-MTP-31 | Corrupted tokens fail-closed |
| INV-MTP-32 | Missing tokens trigger operator alert |
| INV-MTP-33 | Budget violations never silently continue |
| INV-MTP-34 | Schema mismatches are critical failures |
| INV-MTP-35 | Audit events write-only to SOP |
| INV-MTP-36 | MTP depends only on infrastructure |
| INV-MTP-37 | Schema changes require migration paths |

**Total**: 37 invariants

---

*End of specification.*
