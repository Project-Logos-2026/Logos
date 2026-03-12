# LOGOS MTP Protocol — Implementation Guide

**Version**: 1.0.0  
**Status**: AUTHORITATIVE  
**Date**: 2026-03-06  
**Entailed From**: MTP_Design_Specification_v1.md  
**Scope**: GPT-processable implementation obligations for MTP system  
**Purpose**: Remove ambiguity at spec→code translation boundary

---

## 1. Overview

This guide translates the Multi-Tick Processing Protocol Design Specification into concrete implementation obligations. MTP provides the infrastructure for task state persistence and continuity management across multiple execution ticks.

**Core Principle** (§1, §3.2): MTP manages state; Logos Core manages execution. MTP has no cognitive authority, only persistence authority.

**Critical Dependency** (§8.1, INV-MTP-18): MTP Nexus must be injected into RuntimeLoop and all agent wrappers before any multi-tick processing can occur.

---

## 2. Component Inventory

### 2.1 Required New Modules

All paths relative to: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/Multi_Tick_Processing_Protocol/`

| Module | Path | Purpose | Spec Reference |
|--------|------|---------|----------------|
| MTP_Nexus.py | MTP_Core/ | Central state management | §6 |
| Task_Classifier.py | MTP_Core/ | Single vs multi-tick classification | §9 |
| Continuity_Token.py | MTP_Core/ | Token serialization/deserialization | §5 |
| Budget_Tracker.py | MTP_Core/ | Tick budget enforcement | §4.6 |

### 2.2 Integration Touch Points

**Existing modules requiring modification**:
- `Logos_Core/Orchestration/Runtime_Loop.py`: MTP Nexus injection (§8.1)
- `Logos_Core/Orchestration/Agent_Wrappers.py`: MTP Nexus reference, task classification queries (§8.1, §4.1)
- `CSP_Core/Unified_Working_Memory/SMP_Store.py`: Context_link AA attachment (§7)

---

## 3. Implementation Obligations by Spec Section

### 3.1 Task Lifecycle (§4)

**Obligation**: Implement task classification, multi-tick execution path, and termination protocols.

**Task Classification Method** (§4.1, §9):
```python
# From Task_Classifier.py
class TaskClassifier:
    def classify_task(self, task: dict) -> str:
        """
        Classifies task as SINGLE_TICK or MULTI_TICK_REQUIRED.
        
        Classification logic (§9):
        - SINGLE_TICK if:
          * task_type == "observation"
          * task.get("single_tick") == True
          * No prior EA references
        
        - MULTI_TICK_REQUIRED if:
          * task_type == "plan_fragment"
          * Involves axiom reconciliation
          * Explicit multi-tick declaration
          * References prior EAs
        
        - Default: MULTI_TICK_REQUIRED (§9.3, INV-MTP-22)
        
        Returns: "SINGLE_TICK" | "MULTI_TICK_REQUIRED"
        """
```

**Multi-Tick Execution Protocol** (§4.3):

**Tick 1 - Initialization**:
```python
# In Logos Agent _process_task()
if mtp_classification == "MULTI_TICK_REQUIRED":
    # 1. Process task, collect sub-agent results
    tick_result = self._on_tick(task_context)
    
    # 2. Request MTP to persist state
    token = self.mtp_nexus.create_token(
        task_id=task["id"],
        context={
            "task_type": task["type"],
            "partial_results": tick_result,
            "active_ea_ids": self._get_produced_ea_ids(),
            "current_tick": 1
        }
    )
    
    # 3. Request context_link AA proposal
    context_link_aa = self.mtp_nexus.propose_context_link_aa(
        task_id=task["id"],
        tick=1,
        prior_ea_ids=[]
    )
    
    # 4. Attach AA via SMP_Store (Logos Agent authority)
    self.smp_store.append_aa(
        smp_id=current_ea_id,
        aa_type="context_link",
        content=context_link_aa["content"],
        producer="mtp_nexus"
    )
    
    # 5. Return in_progress status
    return {"task_status": "in_progress", "tick": 1}
```

**Ticks 2...N - Continuation**:
```python
# In Logos Agent _process_task() at tick N+1
if task_status == "in_progress":
    # 1. Restore prior state
    prior_context = self.mtp_nexus.restore_token(task_id)
    
    # 2. Merge with current tick input
    tick_context = {
        **prior_context,
        "current_input": task,
        "tick": prior_context["current_tick"] + 1
    }
    
    # 3. Distribute to sub-agents
    tick_result = self._on_tick(tick_context)
    
    # 4. Update MTP state
    updated_token = self.mtp_nexus.update_token(
        task_id=task_id,
        context={
            **prior_context,
            "partial_results": tick_result,
            "current_tick": prior_context["current_tick"] + 1
        }
    )
    
    # 5. Propose new context_link AA
    context_link_aa = self.mtp_nexus.propose_context_link_aa(
        task_id=task_id,
        tick=tick_context["tick"],
        prior_ea_ids=prior_context["active_ea_ids"]
    )
    
    # 6. Attach AA
    self.smp_store.append_aa(...)
    
    # 7. Check if complete
    if self._is_task_complete(tick_result):
        self.mtp_nexus.discard_token(task_id)
        return {"task_status": "completed", "tick": tick_context["tick"]}
    else:
        return {"task_status": "in_progress", "tick": tick_context["tick"]}
```

**Termination Protocol** (§4.4):
```python
def terminate_task(self, task_id: str, reason: str):
    """
    Terminate task before completion.
    
    Reasons (§4.4):
    - "budget_exhausted"
    - "governance_violation"
    - "explicit_rejection"
    - "resource_exhaustion"
    
    Protocol:
    1. Mark task as terminated in MTP
    2. Propose governance_annotation AA
    3. Discard continuity token
    4. Clear task state
    """
    # 1. Signal MTP
    self.mtp_nexus.mark_terminated(task_id, reason)
    
    # 2. Attach governance_annotation
    self.smp_store.append_aa(
        smp_id=self._get_current_ea_id(task_id),
        aa_type="governance_annotation",
        content={"termination_reason": reason, "task_id": task_id},
        producer="logos_agent"
    )
    
    # 3. Discard token (INV-MTP-04, INV-MTP-05)
    self.mtp_nexus.discard_token(task_id)
```

**Tick Budget Enforcement** (§4.6, INV-MTP-07, INV-MTP-08):
```python
# In MTP Nexus before each token update
def update_token(self, task_id: str, context: dict) -> str:
    current_tick = context["current_tick"]
    
    # Check budget (default 50 ticks)
    if current_tick >= TICK_BUDGET_LIMIT:
        # Log exhaustion event (§8.4, §12.2)
        self.operational_logger.log_event(
            "mtp_budget_exhausted",
            {"task_id": task_id, "final_tick": current_tick}
        )
        
        # Raise error (fail-closed, INV-MTP-29)
        raise BudgetExhaustionError(f"Task {task_id} exceeded tick budget at tick {current_tick}")
    
    # Budget warning at 80% threshold (§8.4)
    if current_tick == 40:
        self.operational_logger.log_event(
            "mtp_budget_warning",
            {"task_id": task_id, "ticks_remaining": 10}
        )
    
    # Normal update
    ...
```

### 3.2 Continuity Token Model (§5)

**Obligation**: Implement token structure, generation, restoration, and lifecycle management.

**Token Structure** (§5.1):
```python
# From Continuity_Token.py
@dataclass
class ContinuityToken:
    task_id: str
    task_type: str
    current_tick: int
    tick_budget_remaining: int
    active_ea_ids: list[str]
    partial_results: dict
    progression_markers: dict
    metadata: dict  # creation_time, session_id
    
    def to_dict(self) -> dict:
        """Serialize to dict (INV-MTP-09)"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ContinuityToken':
        """Deserialize from dict (INV-MTP-09)"""
        return cls(**data)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate token schema and constraints (§5.3, INV-MTP-12).
        
        Checks:
        - All required fields present
        - No executable content (INV-MTP-10, INV-MTP-24)
        - tick_budget_remaining >= 0
        - current_tick > 0
        
        Returns: (is_valid, error_message)
        """
```

**Token Generation** (§5.2, INV-MTP-11):
```python
# From MTP_Nexus.py
def create_token(self, task_id: str, context: dict) -> str:
    """
    Generate initial continuity token.
    
    Pre-conditions:
    - Called at end of Tick 1 (INV-MTP-11)
    - task_id must be unique
    - context must contain required fields
    
    Post-conditions:
    - Token stored in Nexus keyed by task_id
    - Event logged to SOP (§8.4)
    - Returns serialized token string
    
    Error handling:
    - Duplicate task_id → raise TokenAlreadyExistsError
    - Invalid context → raise TokenCreationError
    """
    # 1. Construct token
    token = ContinuityToken(
        task_id=task_id,
        task_type=context["task_type"],
        current_tick=context.get("current_tick", 1),
        tick_budget_remaining=TICK_BUDGET_LIMIT - context.get("current_tick", 1),
        active_ea_ids=context.get("active_ea_ids", []),
        partial_results=context.get("partial_results", {}),
        progression_markers=context.get("progression_markers", {}),
        metadata={
            "created_at": datetime.utcnow().isoformat(),
            "session_id": self.session_id
        }
    )
    
    # 2. Validate (INV-MTP-10, INV-MTP-24)
    is_valid, error = token.validate()
    if not is_valid:
        raise TokenCreationError(f"Token validation failed: {error}")
    
    # 3. Serialize to JSON (INV-MTP-09)
    token_json = json.dumps(token.to_dict())
    
    # 4. Store in Nexus (§6.1)
    self.storage[task_id] = {
        "token": token_json,
        "status": "in_progress",
        "created_at": token.metadata["created_at"],
        "last_updated_tick": token.current_tick
    }
    
    # 5. Log event (§8.4)
    self.operational_logger.log_event(
        "mtp_token_created",
        {
            "task_id": task_id,
            "tick": token.current_tick,
            "token_size_bytes": len(token_json)
        }
    )
    
    return token_json
```

**Token Restoration** (§5.3, INV-MTP-12):
```python
def restore_token(self, task_id: str) -> dict:
    """
    Restore continuity token to task context.
    
    Pre-conditions:
    - task_id must exist in Nexus
    - Token must be valid
    
    Post-conditions:
    - Returns deserialized task context dict
    - Event logged to SOP
    
    Error handling (§11, INV-MTP-12):
    - Missing task_id → raise TokenNotFoundError
    - Corrupted token → raise TokenCorruptionError
    - Schema invalid → raise SchemaVersionError
    """
    # 1. Retrieve from storage
    if task_id not in self.storage:
        # Critical error (§11.2, INV-MTP-32)
        self.operational_logger.log_error(
            "mtp_token_missing",
            {"task_id": task_id}
        )
        raise TokenNotFoundError(f"No token found for task {task_id}")
    
    token_entry = self.storage[task_id]
    
    # 2. Deserialize JSON
    try:
        token_dict = json.loads(token_entry["token"])
        token = ContinuityToken.from_dict(token_dict)
    except (json.JSONDecodeError, TypeError) as e:
        # Token corruption (§11.1, INV-MTP-31)
        self.operational_logger.log_error(
            "mtp_token_corrupted",
            {"task_id": task_id, "error": str(e)}
        )
        raise TokenCorruptionError(f"Token deserialization failed: {e}")
    
    # 3. Validate (INV-MTP-12)
    is_valid, error = token.validate()
    if not is_valid:
        raise TokenCorruptionError(f"Token validation failed: {error}")
    
    # 4. Log restoration (§8.4)
    self.operational_logger.log_event(
        "mtp_token_restored",
        {
            "task_id": task_id,
            "tick": token.current_tick + 1,  # Restoring for next tick
            "prior_tick": token.current_tick
        }
    )
    
    # 5. Return context (§5.3)
    return {
        "task_id": token.task_id,
        "task_type": token.task_type,
        "current_tick": token.current_tick,
        "active_ea_ids": token.active_ea_ids,
        "partial_results": token.partial_results,
        "progression_markers": token.progression_markers
    }
```

**Token Discard** (§5.4, INV-MTP-04, INV-MTP-13):
```python
def discard_token(self, task_id: str) -> bool:
    """
    Discard continuity token on task completion/termination.
    
    Pre-conditions:
    - task_id must exist
    
    Post-conditions:
    - Token removed from storage
    - Task marked complete/terminated
    - Event logged
    
    Guarantees (INV-MTP-04):
    - Immediate discard, no persistence beyond session
    """
    if task_id not in self.storage:
        return False
    
    # Remove from storage
    token_entry = self.storage.pop(task_id)
    
    # Log completion (§8.4)
    self.operational_logger.log_event(
        "mtp_task_completed",
        {
            "task_id": task_id,
            "total_ticks": token_entry["last_updated_tick"],
            "completion_status": token_entry["status"]
        }
    )
    
    return True
```

### 3.3 MTP Nexus (§6)

**Obligation**: Implement centralized state management with session-scoped storage and lifecycle hooks.

**Class Structure** (§6.1, §6.2):
```python
# From MTP_Nexus.py
class MTPNexus:
    def __init__(self, session_id: str, operational_logger: Logger):
        """
        Initialize MTP Nexus.
        
        Parameters:
        - session_id: Unique session identifier
        - operational_logger: SOP logger instance
        
        Storage Model (§6.1):
        - In-memory dict keyed by task_id
        - Cleared at session end (INV-MTP-14, INV-MTP-28)
        """
        self.session_id = session_id
        self.operational_logger = operational_logger
        self.storage: dict[str, dict] = {}  # Session-scoped storage
    
    # Token lifecycle methods
    def create_token(self, task_id: str, context: dict) -> str:
        """§5.2"""
    
    def update_token(self, task_id: str, context: dict) -> str:
        """§5.2, §4.6 (budget check)"""
    
    def restore_token(self, task_id: str) -> dict:
        """§5.3"""
    
    def discard_token(self, task_id: str) -> bool:
        """§5.4"""
    
    # Query interface (§6.2)
    def get_active_tasks(self) -> list[str]:
        """
        Returns: List of task_ids with active tokens
        """
        return [
            task_id for task_id, entry in self.storage.items()
            if entry["status"] == "in_progress"
        ]
    
    def check_budget(self, task_id: str) -> tuple[int, int]:
        """
        Returns: (current_tick, ticks_remaining)
        Raises: TokenNotFoundError if task_id not found
        """
        if task_id not in self.storage:
            raise TokenNotFoundError(f"Task {task_id} not found")
        
        token_dict = json.loads(self.storage[task_id]["token"])
        return (token_dict["current_tick"], token_dict["tick_budget_remaining"])
    
    # Context Link AA production (§7)
    def propose_context_link_aa(
        self,
        task_id: str,
        tick: int,
        prior_ea_ids: list[str]
    ) -> dict:
        """
        Generate context_link AA proposal for Logos Agent review.
        
        Returns AA dict per EA spec §5.2 (§7.2):
        {
            "aa_type": "context_link",
            "content": {
                "prior_tick": int,
                "prior_ea_ids": list[str],
                "continuation_type": str,
                "progression_marker": str
            },
            "producer": "mtp_nexus",
            "timestamp": str (ISO-8601)
        }
        
        Note (INV-MTP-17): MTP never attaches AAs directly
        """
        token_dict = json.loads(self.storage[task_id]["token"])
        
        return {
            "aa_type": "context_link",
            "content": {
                "prior_tick": tick - 1,
                "prior_ea_ids": prior_ea_ids,
                "continuation_type": "sequential",  # V1: always sequential
                "progression_marker": token_dict.get("progression_markers", {}).get("current", "")
            },
            "producer": "mtp_nexus",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Session lifecycle hooks (§8.1)
    def on_session_start(self):
        """Initialize storage (called by RuntimeLoop)"""
        self.storage = {}
    
    def on_session_end(self):
        """
        Clear all tokens (INV-MTP-28).
        Called by RuntimeLoop at session termination.
        """
        # Log all discarded tokens
        for task_id in list(self.storage.keys()):
            self.operational_logger.log_event(
                "mtp_session_cleanup",
                {"task_id": task_id, "session_id": self.session_id}
            )
        
        # Clear storage completely
        self.storage.clear()
```

### 3.4 Task Classifier (§9)

**Obligation**: Implement single vs multi-tick classification with conservative default.

**Class Structure** (§9):
```python
# From Task_Classifier.py
class TaskClassifier:
    def classify_task(self, task: dict) -> str:
        """
        Classify task as SINGLE_TICK or MULTI_TICK_REQUIRED.
        
        Classification Rules (§9):
        
        SINGLE_TICK if (§9.1):
        - task["type"] == "observation"
        - task.get("single_tick") == True
        - No prior EA references
        
        MULTI_TICK_REQUIRED if (§9.2):
        - task["type"] == "plan_fragment"
        - Involves axiom reconciliation
        - Explicit multi-tick declaration
        - References prior EAs
        
        Default (§9.3, INV-MTP-22):
        - When ambiguous → MULTI_TICK_REQUIRED (conservative)
        
        Returns: "SINGLE_TICK" | "MULTI_TICK_REQUIRED"
        """
        # Explicit single-tick indicators
        if task.get("single_tick") is True:
            return "SINGLE_TICK"
        
        if task.get("type") == "observation" and not task.get("prior_eas"):
            return "SINGLE_TICK"
        
        # Explicit multi-tick indicators
        if task.get("type") == "plan_fragment":
            return "MULTI_TICK_REQUIRED"
        
        if task.get("requires_axiom_reconciliation"):
            return "MULTI_TICK_REQUIRED"
        
        if task.get("multi_tick_required"):
            return "MULTI_TICK_REQUIRED"
        
        if task.get("prior_eas"):
            return "MULTI_TICK_REQUIRED"
        
        # Default: conservative (INV-MTP-22)
        return "MULTI_TICK_REQUIRED"
```

### 3.5 Budget Tracker (§4.6)

**Obligation**: Implement tick budget enforcement with warning threshold and hard limit.

**Class Structure** (§4.6, INV-MTP-07):
```python
# From Budget_Tracker.py
TICK_BUDGET_LIMIT = 50  # Per EA spec §12.2
WARNING_THRESHOLD = 40  # 80% of budget

class BudgetTracker:
    def check_budget(
        self,
        current_tick: int,
        limit: int = TICK_BUDGET_LIMIT
    ) -> tuple[str, int]:
        """
        Check tick budget and return status.
        
        Returns: (status, ticks_remaining)
        status: "OK" | "WARNING" | "EXHAUSTED"
        
        Enforcement (INV-MTP-07):
        - Hard fail at limit
        - Warning at 80% threshold
        """
        ticks_remaining = limit - current_tick
        
        if current_tick >= limit:
            return ("EXHAUSTED", 0)
        elif current_tick >= WARNING_THRESHOLD:
            return ("WARNING", ticks_remaining)
        else:
            return ("OK", ticks_remaining)
    
    def enforce_budget(
        self,
        task_id: str,
        current_tick: int,
        limit: int = TICK_BUDGET_LIMIT
    ) -> None:
        """
        Enforce budget with exception on violation (INV-MTP-33).
        
        Raises: BudgetExhaustionError if limit exceeded
        """
        status, _ = self.check_budget(current_tick, limit)
        
        if status == "EXHAUSTED":
            raise BudgetExhaustionError(
                f"Task {task_id} exceeded tick budget at tick {current_tick}"
            )
```

### 3.6 Integration Points (§8)

**RuntimeLoop Modification** (§8.1):
```python
# In Runtime_Loop.py
class RuntimeLoop:
    def __init__(
        self,
        session_id: str,
        operational_logger: Logger,
        # ... other params
    ):
        # Initialize MTP Nexus (INV-MTP-18)
        self.mtp_nexus = MTPNexus(session_id, operational_logger)
        
        # Inject into agent wrappers
        self.logos_agent = LogosAgentWrapper(
            uwm=uwm,
            mtp_nexus=self.mtp_nexus,  # Injection
            # ... other subsystems
        )
    
    def start_session(self):
        """Session initialization"""
        self.mtp_nexus.on_session_start()
        # ... rest of initialization
    
    def end_session(self):
        """Session cleanup (INV-MTP-28)"""
        self.mtp_nexus.on_session_end()
        # ... rest of cleanup
```

**Agent Wrapper Modification** (§8.1, §4):
```python
# In Agent_Wrappers.py
class LogosAgentWrapper:
    def __init__(
        self,
        uwm: UWM,
        mtp_nexus: MTPNexus,  # Injected dependency
        task_classifier: TaskClassifier,
        # ... other params
    ):
        self.uwm = uwm
        self.mtp_nexus = mtp_nexus
        self.task_classifier = task_classifier
    
    def _process_task(self, task: dict) -> dict:
        """
        Multi-tick task orchestration (§4.3).
        
        Flow:
        1. Classify task (single vs multi-tick)
        2. If single-tick → process and complete
        3. If multi-tick → engage MTP lifecycle
        """
        # 1. Classification (§4.1)
        classification = self.task_classifier.classify_task(task)
        
        if classification == "SINGLE_TICK":
            # Direct processing, no MTP
            return self._process_single_tick(task)
        
        # 2. Multi-tick path
        task_id = task["id"]
        
        # Check if continuation or new task
        if task.get("status") == "in_progress":
            # Restore state (§4.3 Ticks 2...N)
            context = self.mtp_nexus.restore_token(task_id)
            return self._continue_multi_tick_task(task, context)
        else:
            # Initialize (§4.3 Tick 1)
            return self._initialize_multi_tick_task(task)
```

**Sub-Agent Context Distribution** (§8.3):
```python
# In Agent_Wrappers.py (sub-agent wrappers)
class I2AgentWrapper:  # Example: I2 uses MTP for task decomposition
    def _on_tick(self, context: dict) -> dict:
        """
        Process with continuity context (INV-MTP-20).
        
        Context may include:
        - prior_tick_results: Previous tick's partial analysis
        - progression_markers: Which protocols have completed
        - active_ea_ids: EAs produced in prior ticks
        
        Sub-agent treats this as read-only.
        """
        # Extract continuity context if present
        prior_results = context.get("partial_results", {})
        progression = context.get("progression_markers", {})
        
        # Use context to inform current analysis
        current_analysis = self._analyze_with_context(
            input=context.get("current_input"),
            prior_results=prior_results,
            progression=progression
        )
        
        # Return updated results (not modifying prior context)
        return {
            "analysis": current_analysis,
            "tick": context.get("tick", 1)
        }
```

---

## 4. Error Handling Implementation

### 4.1 Token Corruption (§11.1, INV-MTP-31)

```python
# Custom exception classes
class TokenCorruptionError(Exception):
    """Raised when token fails validation or deserialization"""
    pass

# Handler in Logos Agent
try:
    context = self.mtp_nexus.restore_token(task_id)
except TokenCorruptionError as e:
    # Log to SOP
    self.operational_logger.log_error(
        "mtp_token_corruption",
        {"task_id": task_id, "error": str(e)}
    )
    
    # Terminate task (§11.1)
    self.terminate_task(task_id, reason="token_corruption")
    
    # Attach governance_annotation
    self.smp_store.append_aa(
        smp_id=self._get_current_ea_id(task_id),
        aa_type="governance_annotation",
        content={"error": "token_corruption", "details": str(e)},
        producer="logos_agent"
    )
```

### 4.2 Missing Token (§11.2, INV-MTP-32)

```python
class TokenNotFoundError(Exception):
    """Raised when token lookup fails"""
    pass

# Handler in Logos Agent
try:
    context = self.mtp_nexus.restore_token(task_id)
except TokenNotFoundError as e:
    # Critical error - operator alert (INV-MTP-32)
    self.operational_logger.log_critical(
        "mtp_token_missing",
        {
            "task_id": task_id,
            "session_id": self.session_id,
            "alert": "OPERATOR_INTERVENTION_REQUIRED"
        }
    )
    
    # Terminate session (possible runtime corruption)
    raise RuntimeCorruptionError(f"Missing token indicates critical failure: {e}")
```

### 4.3 Budget Exhaustion (§11.3, INV-MTP-33)

```python
class BudgetExhaustionError(Exception):
    """Raised when tick budget is exceeded"""
    pass

# Handler in MTP Nexus update_token()
try:
    budget_tracker.enforce_budget(task_id, current_tick)
except BudgetExhaustionError as e:
    # Log exhaustion (§8.4)
    self.operational_logger.log_event(
        "mtp_budget_exhausted",
        {"task_id": task_id, "final_tick": current_tick}
    )
    
    # Propagate to Logos Agent for termination
    raise  # Logos Agent catches and terminates task
```

---

## 5. File-Level Implementation Map

### 5.1 MTP_Nexus.py

**Path**: `Multi_Tick_Processing_Protocol/MTP_Core/MTP_Nexus.py`  
**Spec Reference**: §6  
**Status**: New module required

**Required methods**:
```python
class MTPNexus:
    def __init__(self, session_id: str, operational_logger: Logger)
    def create_token(self, task_id: str, context: dict) -> str
    def update_token(self, task_id: str, context: dict) -> str
    def restore_token(self, task_id: str) -> dict
    def discard_token(self, task_id: str) -> bool
    def get_active_tasks(self) -> list[str]
    def check_budget(self, task_id: str) -> tuple[int, int]
    def propose_context_link_aa(self, task_id: str, tick: int, prior_ea_ids: list[str]) -> dict
    def on_session_start(self)
    def on_session_end(self)
    def mark_terminated(self, task_id: str, reason: str)
```

### 5.2 Continuity_Token.py

**Path**: `Multi_Tick_Processing_Protocol/MTP_Core/Continuity_Token.py`  
**Spec Reference**: §5  
**Status**: New module required

**Required classes**:
```python
@dataclass
class ContinuityToken:
    task_id: str
    task_type: str
    current_tick: int
    tick_budget_remaining: int
    active_ea_ids: list[str]
    partial_results: dict
    progression_markers: dict
    metadata: dict
    
    def to_dict(self) -> dict
    @classmethod
    def from_dict(cls, data: dict) -> 'ContinuityToken'
    def validate(self) -> tuple[bool, Optional[str]]
```

### 5.3 Task_Classifier.py

**Path**: `Multi_Tick_Processing_Protocol/MTP_Core/Task_Classifier.py`  
**Spec Reference**: §9  
**Status**: New module required

**Required methods**:
```python
class TaskClassifier:
    def classify_task(self, task: dict) -> str
    # Returns: "SINGLE_TICK" | "MULTI_TICK_REQUIRED"
```

### 5.4 Budget_Tracker.py

**Path**: `Multi_Tick_Processing_Protocol/MTP_Core/Budget_Tracker.py`  
**Spec Reference**: §4.6  
**Status**: New module required

**Required methods**:
```python
class BudgetTracker:
    def check_budget(self, current_tick: int, limit: int) -> tuple[str, int]
    # Returns: (status, ticks_remaining)
    # status: "OK" | "WARNING" | "EXHAUSTED"
    
    def enforce_budget(self, task_id: str, current_tick: int, limit: int) -> None
    # Raises: BudgetExhaustionError on violation
```

### 5.5 Runtime_Loop.py (Modifications)

**Path**: `Logos_Core/Orchestration/Runtime_Loop.py`  
**Spec Reference**: §8.1  
**Status**: Requires integration changes

**Required additions**:
```python
class RuntimeLoop:
    def __init__(self, ...):
        # Add MTP Nexus initialization
        self.mtp_nexus = MTPNexus(session_id, operational_logger)
        
        # Inject into agent wrappers
        self.logos_agent = LogosAgentWrapper(
            ...,
            mtp_nexus=self.mtp_nexus
        )
    
    def start_session(self):
        # Add MTP lifecycle hook
        self.mtp_nexus.on_session_start()
    
    def end_session(self):
        # Add MTP lifecycle hook
        self.mtp_nexus.on_session_end()
```

### 5.6 Agent_Wrappers.py (Modifications)

**Path**: `Logos_Core/Orchestration/Agent_Wrappers.py`  
**Spec Reference**: §4, §8.1, §8.3  
**Status**: Requires integration changes

**Required additions**:
```python
class LogosAgentWrapper:
    def __init__(self, ..., mtp_nexus: MTPNexus, task_classifier: TaskClassifier):
        self.mtp_nexus = mtp_nexus
        self.task_classifier = task_classifier
    
    def _process_task(self, task: dict) -> dict:
        # Add task classification logic
        classification = self.task_classifier.classify_task(task)
        
        if classification == "SINGLE_TICK":
            return self._process_single_tick(task)
        else:
            # Multi-tick path with MTP integration
            ...
    
    def _initialize_multi_tick_task(self, task: dict) -> dict:
        # Tick 1 initialization logic
        ...
    
    def _continue_multi_tick_task(self, task: dict, context: dict) -> dict:
        # Tick 2...N continuation logic
        ...
    
    def terminate_task(self, task_id: str, reason: str):
        # Task termination protocol
        ...

class SubAgentWrapper:  # I1, I2, I3
    def _on_tick(self, context: dict) -> dict:
        # Add continuity context handling
        prior_results = context.get("partial_results", {})
        # ... use context in analysis
```

---

## 6. Testing Strategy

### 6.1 Unit Tests

**Continuity_Token tests**:
- to_dict() / from_dict() round-trip
- validate() with valid token → success
- validate() with missing fields → failure
- validate() with executable content → failure

**Task_Classifier tests**:
- classify_task() with observation type → SINGLE_TICK
- classify_task() with plan_fragment type → MULTI_TICK_REQUIRED
- classify_task() with ambiguous input → MULTI_TICK_REQUIRED (default)

**Budget_Tracker tests**:
- check_budget() at tick 40 → WARNING
- check_budget() at tick 50 → EXHAUSTED
- enforce_budget() at tick 50 → raises BudgetExhaustionError

**MTP_Nexus tests**:
- create_token() → token stored in Nexus
- restore_token() → returns original context
- discard_token() → token removed
- get_active_tasks() → returns in_progress tasks only

### 6.2 Integration Tests

**Multi-tick task execution (3 ticks)**:
1. Initialize task (Tick 1)
2. Verify token created
3. Verify context_link AA attached
4. Continue task (Tick 2)
5. Verify token updated
6. Verify second context_link AA attached
7. Complete task (Tick 3)
8. Verify token discarded

**Budget exhaustion scenario**:
1. Create task with budget limit set to 3 ticks
2. Execute ticks 1, 2, 3
3. Verify budget warning logged at tick 2 (80%)
4. Attempt tick 4
5. Verify BudgetExhaustionError raised
6. Verify governance_annotation AA attached
7. Verify task terminated

**Token restoration failure**:
1. Create task and generate token
2. Manually corrupt token JSON in Nexus storage
3. Attempt to restore token
4. Verify TokenCorruptionError raised
5. Verify task terminated
6. Verify error logged to SOP

### 6.3 Compliance Tests

**Session isolation (INV-MTP-27, INV-MTP-28)**:
1. Start session 1, create multi-tick task
2. Generate continuity token
3. End session 1
4. Verify MTP Nexus storage cleared
5. Start session 2
6. Verify session 1 tokens not accessible

**Inertness validation (INV-MTP-24)**:
1. Attempt to create token with executable content in partial_results
2. Verify validation fails
3. Verify TokenCreationError raised

**Determinism (INV-MTP-25, INV-MTP-26)**:
1. Create identical task context twice
2. Generate tokens
3. Verify tokens are byte-for-byte identical
4. Restore both tokens
5. Verify restored contexts are identical

---

## 7. Deployment Checklist

**Pre-deployment validation**:
- [ ] All 4 new modules implemented (MTP_Nexus, Continuity_Token, Task_Classifier, Budget_Tracker)
- [ ] RuntimeLoop modified with MTP Nexus injection
- [ ] Agent_Wrappers modified with task classification and multi-tick logic
- [ ] SOP integration points active (7 lifecycle events)
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All compliance tests pass

**Operational readiness**:
- [ ] MTP Nexus injected into all agent wrappers (INV-MTP-18)
- [ ] Session lifecycle hooks (on_session_start, on_session_end) operational
- [ ] Tick budget enforcement active with 50-tick limit
- [ ] Context_link AA production tested
- [ ] Token corruption recovery verified (fail-closed)
- [ ] Budget exhaustion recovery verified (governance_annotation)

---

## 8. Ambiguities and Escalation Points

### 8.1 Task Decomposition Depth

**Ambiguity**: Spec defines 50-tick budget but doesn't specify optimal task decomposition strategy.

**Resolution required**:
- Should Logos Agent proactively decompose tasks into smaller chunks?
- Should budget warnings trigger automatic decomposition?
- Should task complexity influence budget allocation?

**Recommendation**: Defer to task orchestration research. V1 uses fixed 50-tick budget universally.

### 8.2 Partial Results Schema

**Ambiguity**: Spec defines `partial_results` as dict but doesn't specify schema or required fields.

**Resolution required**:
- What minimum structure is required in partial_results?
- Should different task types have different result schemas?
- Should validation enforce schema compliance?

**Recommendation**: Escalate to protocol design review. Current implementation treats as unstructured dict.

### 8.3 Context Link Continuation Types

**Ambiguity**: §7.2 mentions continuation_type values: `sequential | branching | convergent`, but V1 only implements `sequential`.

**Resolution required**:
- When would branching continuations occur?
- When would convergent continuations occur?
- Should V1 implement these or defer to V1.1+?

**Recommendation**: V1 uses `sequential` only. Branching/convergent are forward compatibility placeholders.

---

*End of implementation guide.*
