# I2 SUB-AGENT — IMPLEMENTATION GUIDE v1.0

**Document Classification**: T3 Implementation Guide  
**Subsystem**: I2 Sub-Agent (MTP Pipeline Executor)  
**Tier**: T3 — Operational + Agent Layer  
**Status**: Canonical  
**Version**: 1.0  
**Last Updated**: 2026-03-06  
**Governed By**: I2_Design_Specification_v1.md

---

## DOCUMENT GOVERNANCE

**Authority**: This implementation guide is a **derivative artifact** of the I2 Design Specification v1.0. All implementation obligations in this document are **entailed** by the design specification and introduce **no new architectural decisions**.

**Scope**: This document translates design specification requirements into concrete implementation obligations processable by GPT + VS Code workflow. It defines module structure, class hierarchies, method signatures, integration protocols, error handling patterns, and testing requirements.

**Constraint**: This guide MUST NOT introduce new features, responsibilities, or architectural patterns not present in the design specification. All content is **entailment-only**.

**Conflict Resolution**: In case of conflict between this guide and the design specification, the design specification is authoritative. Implementation must conform to the design specification, not vice versa.

---

## TABLE OF CONTENTS

1. Implementation Overview
2. Module Hierarchy and File Structure
3. I2 Agent Core Implementation
4. Task Decomposition Engine Implementation
5. MTP Pipeline Coordinator Implementation
6. Tick Lifecycle Manager Implementation
7. EA Context Handler Implementation
8. Integration Point Implementations
9. Error Handling Protocols
10. Testing Requirements
11. Deployment and Configuration
12. Ambiguity Escalation Log

---

## 1. IMPLEMENTATION OVERVIEW

### 1.1 Implementation Scope

This guide defines implementation obligations for the following I2 components (per Design Spec §4):

1. **I2 Agent Core**: Central orchestration for task lifecycle
2. **Task Decomposition Engine**: Task analysis and subtask generation
3. **MTP Pipeline Coordinator**: MTP pipeline stage invocation
4. **Tick Lifecycle Manager**: Tick-level state and resource management
5. **EA Context Handler**: UWM EA context retrieval and transformation

### 1.2 Implementation Principles

**Entailment-Only**: All classes, methods, and protocols are derived from design specification requirements. No new architecture is introduced.

**Fail-Closed**: All error conditions trigger explicit exceptions. No silent fallbacks, no partial results.

**Logos Agent Sovereignty**: All task authority flows from Logos Agent. No autonomous operations.

**Session-Scoped State**: No cross-session persistence (V1 scope). All state is ephemeral or MTP Nexus-managed.

**Auditable**: All operations produce event logs. No silent execution.

### 1.3 Technology Stack Constraints

**Language**: Python 3.10+  
**Type Checking**: All modules MUST use type hints (PEP 484)  
**Async Support**: I2 operations are synchronous in V1 (async support deferred to V2)  
**Dependency Management**: Standard library preferred; external dependencies require governance approval  

---

## 2. MODULE HIERARCHY AND FILE STRUCTURE

### 2.1 Canonical Directory Structure

```
LOGOS_SYSTEM/
└── RUNTIME_CORES/
    └── RUNTIME_EXECUTION_CORE/
        └── Logos_Core/
            └── Logos_Protocol/
                └── LP_Core/
                    └── Agent_Integration/
                        └── I2/
                            ├── __init__.py
                            ├── I2.py                      # I2 Agent Core
                            ├── task_decomposition.py      # Task Decomposition Engine
                            ├── mtp_pipeline/
                            │   ├── __init__.py
                            │   ├── pipeline_coordinator.py  # MTP Pipeline Coordinator
                            │   └── pipeline_runner.py       # MTP stage execution
                            ├── tick_lifecycle/
                            │   ├── __init__.py
                            │   ├── tick_manager.py          # Tick Lifecycle Manager
                            │   └── resource_monitor.py      # Tick resource monitoring
                            ├── ea_context/
                            │   ├── __init__.py
                            │   └── context_handler.py       # EA Context Handler
                            ├── integration/
                            │   ├── __init__.py
                            │   ├── logos_interface.py       # Logos Agent integration
                            │   ├── mtp_nexus_interface.py   # MTP Nexus integration
                            │   ├── uwm_interface.py         # UWM integration
                            │   └── logger_interface.py      # Operational Logger
                            ├── types/
                            │   ├── __init__.py
                            │   ├── task_types.py            # Task, TaskAssignment, TaskResult
                            │   ├── decomposition_types.py   # DecompositionProposal, Subtask
                            │   ├── tick_types.py            # TickContext, TickResult
                            │   └── error_types.py           # I2Exception hierarchy
                            └── I2_Documentation/
                                ├── README.md
                                ├── GOVERNANCE_SCOPE.md
                                └── INVARIANT_TEST_SPEC.md
```

### 2.2 Module Import Hierarchy

**Canonical Import Pattern** (per Canonical Import Facade Blueprint):
```python
# Correct - facade imports
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Core.Agent_Integration.I2 import (
    I2Agent,
    TaskAssignment,
    TaskResult,
    DecompositionProposal
)

# Incorrect - deep imports (prohibited)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Core.Agent_Integration.I2.I2 import I2Agent  # VIOLATION
```

**Facade Export** (`__init__.py` in `I2/`):
```python
from .I2 import I2Agent
from .types.task_types import TaskAssignment, TaskResult, Task
from .types.decomposition_types import DecompositionProposal, Subtask
from .types.tick_types import TickContext, TickResult
from .types.error_types import I2Exception

__all__ = [
    "I2Agent",
    "TaskAssignment",
    "TaskResult",
    "Task",
    "DecompositionProposal",
    "Subtask",
    "TickContext",
    "TickResult",
    "I2Exception",
]
```

---

## 3. I2 AGENT CORE IMPLEMENTATION

### 3.1 Class Definition: `I2Agent`

**Location**: `I2/I2.py`

**Responsibilities** (per Design Spec §4.1):
- Receive task assignments from Logos Agent
- Coordinate task lifecycle (analysis, decomposition, execution, completion)
- Return task results to Logos Agent

**Class Signature**:
```python
from typing import Optional
from .types.task_types import TaskAssignment, TaskResult, Task
from .types.decomposition_types import DecompositionProposal
from .types.error_types import I2Exception, InvalidTaskException
from .task_decomposition import TaskDecompositionEngine
from .mtp_pipeline.pipeline_coordinator import MTPPipelineCoordinator
from .tick_lifecycle.tick_manager import TickLifecycleManager
from .ea_context.context_handler import EAContextHandler
from .integration.logos_interface import LogosInterface
from .integration.mtp_nexus_interface import MTPNexusInterface
from .integration.logger_interface import OperationalLoggerInterface

class I2Agent:
    """
    I2 Sub-Agent: MTP Pipeline Executor for multi-tick task processing.
    
    Responsibilities:
    - Execute multi-tick tasks assigned by Logos Agent
    - Decompose complex tasks into tick-bounded subtasks
    - Coordinate with MTP Nexus for continuity management
    - Return task results to Logos Agent
    
    Authority Constraints:
    - Operates ONLY under Logos Agent authority (INV-I2-01)
    - Evaluative authority only (proposals require Logos approval) (INV-I2-02)
    - Read-only EA access (INV-I2-15)
    - Session-scoped state (INV-I2-21)
    """
    
    def __init__(
        self,
        decomposition_engine: TaskDecompositionEngine,
        pipeline_coordinator: MTPPipelineCoordinator,
        tick_manager: TickLifecycleManager,
        ea_handler: EAContextHandler,
        logos_interface: LogosInterface,
        mtp_nexus_interface: MTPNexusInterface,
        logger_interface: OperationalLoggerInterface
    ):
        """
        Initialize I2 Agent with required dependencies.
        
        Args:
            decomposition_engine: Task decomposition component
            pipeline_coordinator: MTP pipeline orchestration component
            tick_manager: Tick lifecycle management component
            ea_handler: EA context retrieval and transformation component
            logos_interface: Logos Agent integration interface
            mtp_nexus_interface: MTP Nexus integration interface
            logger_interface: Operational Logger integration interface
        
        Raises:
            ValueError: If any dependency is None
        """
        # Validation + assignment
        pass
    
    def accept_task(
        self,
        assignment: TaskAssignment
    ) -> TaskResult:
        """
        Accept and execute task assigned by Logos Agent.
        
        Task lifecycle (per Design Spec §6.1):
        1. Validate Logos Agent authority
        2. Fetch EA context from UWM
        3. Analyze task complexity
        4. Decompose (if needed) → Submit proposal → Await approval
        5. Execute task (single-tick or multi-tick)
        6. Return task result to Logos Agent
        
        Args:
            assignment: TaskAssignment from Logos Agent
        
        Returns:
            TaskResult containing task outcome, resource usage, error details (if any)
        
        Raises:
            InvalidTaskException: Logos Agent signature invalid (INV-I2-01)
            TaskExecutionException: Task execution failure
            I2Exception: Other I2 errors
        
        Invariants Enforced:
        - INV-I2-01: Logos Agent authority validation
        - INV-I2-04: Task lifecycle event logging
        - INV-I2-17: EA context disposal after task completion
        - INV-I2-30: Task context disposal
        """
        # Implementation obligations:
        # 1. Validate Logos Agent signature
        # 2. Log task start event
        # 3. Fetch EA context via ea_handler
        # 4. Analyze task complexity
        # 5. If decomposition needed → generate proposal → submit to Logos → await approval
        # 6. Execute task (single-tick or multi-tick via tick_manager)
        # 7. Generate TaskResult
        # 8. Dispose EA context
        # 9. Dispose task context
        # 10. Log task completion event
        # 11. Return TaskResult
        pass
    
    def _execute_single_tick_task(
        self,
        task: Task,
        ea_context: "EAContext"
    ) -> TaskResult:
        """
        Execute task completable within single tick.
        
        Args:
            task: Task to execute
            ea_context: EA context for task execution
        
        Returns:
            TaskResult with task outcome
        
        Raises:
            TaskExecutionException: Execution failure
        """
        # Implementation obligations:
        # 1. Initialize single tick context
        # 2. Execute task via MTP pipeline
        # 3. Generate TaskResult
        # 4. Dispose tick context
        pass
    
    def _execute_multi_tick_task(
        self,
        task: Task,
        decomposition: DecompositionProposal,
        ea_context: "EAContext"
    ) -> TaskResult:
        """
        Execute task requiring multiple ticks.
        
        Multi-tick execution (per Design Spec §6.2):
        - Tick 1: Execute first subtask(s), save continuity state
        - Tick 2-N: Load continuity, execute subtask(s), save continuity
        - Tick N+1 (final): Load continuity, execute final subtask(s), generate result
        
        Args:
            task: Task to execute
            decomposition: Approved decomposition plan from Logos Agent
            ea_context: EA context for task execution
        
        Returns:
            TaskResult aggregated across all ticks
        
        Raises:
            TaskExecutionException: Execution failure in any tick
            MTPNexusUnavailableException: Continuity management failure (fail-closed)
        
        Invariants Enforced:
        - INV-I2-03: Tick transitions via MTP Nexus
        - INV-I2-24: Tick transition logging
        """
        # Implementation obligations:
        # 1. For each subtask in decomposition:
        #    a. Start tick via tick_manager
        #    b. Load continuity state from MTP Nexus
        #    c. Execute subtask via MTP pipeline
        #    d. Save continuity state to MTP Nexus
        #    e. End tick
        #    f. Log tick event
        # 2. Aggregate results across all ticks
        # 3. Generate final TaskResult
        pass
```

---

## 4. TASK DECOMPOSITION ENGINE IMPLEMENTATION

### 4.1 Class Definition: `TaskDecompositionEngine`

**Location**: `I2/task_decomposition.py`

**Responsibilities** (per Design Spec §4.2):
- Analyze task complexity
- Generate decomposition proposal for complex tasks
- Estimate resource usage per subtask

**Class Signature**:
```python
from typing import List
from .types.task_types import Task
from .types.decomposition_types import (
    DecompositionProposal,
    Subtask,
    ComplexityProfile,
    DecompositionPoint
)
from .types.error_types import DecompositionException

class TaskDecompositionEngine:
    """
    Decomposes complex tasks into tick-bounded subtasks.
    
    Decomposition triggers (per Design Spec §6.3):
    - Task complexity exceeds single-tick capacity
    - Task explicitly marked as DECOMPOSABLE
    - Resource estimate exceeds tick limits
    
    Decomposition constraints:
    - All subtasks MUST be tick-bounded (INV-I2-05)
    - Proposals MUST include resource estimates (INV-I2-06)
    - Proposals require Logos Agent approval (INV-I2-02)
    """
    
    def __init__(self, tick_resource_limits: "ResourceConstraints"):
        """
        Initialize decomposition engine with tick resource limits.
        
        Args:
            tick_resource_limits: Resource constraints per tick
        """
        # Assignment
        pass
    
    def analyze_complexity(self, task: Task) -> ComplexityProfile:
        """
        Analyze task complexity to determine decomposition need.
        
        Complexity factors:
        - Data volume (EA count, EA size)
        - Processing complexity (operation types, computation intensity)
        - Resource estimates (time, memory, MTP operations)
        
        Args:
            task: Task to analyze
        
        Returns:
            ComplexityProfile with complexity metrics
        
        Raises:
            DecompositionException: Analysis failure
        """
        # Implementation obligations:
        # 1. Estimate data volume from EA references
        # 2. Estimate processing complexity from task type
        # 3. Estimate resource usage (time, memory, MTP ops)
        # 4. Generate ComplexityProfile
        pass
    
    def requires_decomposition(self, profile: ComplexityProfile) -> bool:
        """
        Determine if task requires decomposition based on complexity profile.
        
        Args:
            profile: ComplexityProfile from analyze_complexity
        
        Returns:
            True if decomposition required, False otherwise
        """
        # Implementation: Compare profile against tick resource limits
        pass
    
    def generate_proposal(self, task: Task) -> DecompositionProposal:
        """
        Generate decomposition proposal for complex task.
        
        Decomposition strategy (per Design Spec §6.3):
        - Identify natural decomposition boundaries
        - Generate tick-bounded subtasks
        - Order subtasks by dependencies
        - Estimate resources per subtask
        
        Args:
            task: Task to decompose
        
        Returns:
            DecompositionProposal for Logos Agent approval
        
        Raises:
            DecompositionException: Proposal generation failure
        
        Invariants Enforced:
        - INV-I2-05: Subtasks are tick-bounded
        - INV-I2-06: Proposals include resource estimates
        - INV-I2-33: Subtask dependencies correctly ordered
        """
        # Implementation obligations:
        # 1. Analyze complexity
        # 2. Identify decomposition boundaries
        # 3. Generate subtasks (each tick-bounded)
        # 4. Order subtasks by dependencies
        # 5. Estimate resources per subtask
        # 6. Create DecompositionProposal
        pass
    
    def identify_boundaries(self, task: Task) -> List[DecompositionPoint]:
        """
        Identify natural decomposition boundaries within task.
        
        Boundary heuristics:
        - Data processing stages (load → transform → analyze → output)
        - Continuity points (state-saving boundaries)
        - Dependency boundaries (independent operations vs dependent operations)
        
        Args:
            task: Task to analyze
        
        Returns:
            List of DecompositionPoints marking boundaries
        """
        # Implementation: Heuristic-based boundary detection
        pass
    
    def generate_subtasks(
        self,
        task: Task,
        boundaries: List[DecompositionPoint]
    ) -> List[Subtask]:
        """
        Generate subtasks from task + decomposition boundaries.
        
        Args:
            task: Original task
            boundaries: Decomposition boundaries
        
        Returns:
            List of Subtasks, each tick-bounded
        
        Raises:
            DecompositionException: Subtask generation failure
        """
        # Implementation obligations:
        # 1. Split task at boundaries
        # 2. Create Subtask for each segment
        # 3. Validate each subtask is tick-bounded
        # 4. Assign subtask dependencies
        pass
```

---

## 5. MTP PIPELINE COORDINATOR IMPLEMENTATION

### 5.1 Class Definition: `MTPPipelineCoordinator`

**Location**: `I2/mtp_pipeline/pipeline_coordinator.py`

**Responsibilities** (per Design Spec §4.3):
- Invoke MTP pipeline stages for task/subtask execution
- Handle pipeline failures
- Return pipeline outputs

**Class Signature**:
```python
from typing import Optional
from ..types.task_types import Task
from ..types.tick_types import TickContext
from ..types.error_types import PipelineException
from .pipeline_runner import PipelineRunner

class MTPPipelineCoordinator:
    """
    Coordinates MTP pipeline execution for I2 tasks.
    
    MTP Pipeline stages (per MTP Design Spec):
    1. Semantic Projection: Map task semantics to MTP primitives
    2. Compilation: Compile MTP primitives into executable operations
    3. Validation: Validate operation correctness and resource compliance
    4. Externalization: Generate external-facing artifacts (if applicable)
    
    Constraints:
    - Pipeline execution MUST occur within tick boundaries (INV-I2-08)
    - Pipeline failures MUST be escalated to Logos Agent (INV-I2-09)
    - Pipeline state MUST persist across ticks (INV-I2-10)
    """
    
    def __init__(self, pipeline_runner: PipelineRunner):
        """
        Initialize MTP Pipeline Coordinator.
        
        Args:
            pipeline_runner: MTP pipeline stage executor
        """
        # Assignment
        pass
    
    def invoke_pipeline(
        self,
        task: Task,
        tick_context: TickContext
    ) -> "PipelineResult":
        """
        Invoke MTP pipeline for task/subtask execution.
        
        Pipeline stages executed sequentially:
        1. Semantic Projection
        2. Compilation
        3. Validation
        4. Externalization (if required)
        
        Args:
            task: Task or subtask to execute via pipeline
            tick_context: Tick context for resource monitoring
        
        Returns:
            PipelineResult with pipeline output and status
        
        Raises:
            PipelineException: Pipeline execution failure (INV-I2-09)
            ResourceExceededException: Tick resource limit exceeded
        
        Invariants Enforced:
        - INV-I2-08: Pipeline execution within tick boundaries
        - INV-I2-09: Pipeline failure escalation
        """
        # Implementation obligations:
        # 1. Invoke semantic projection stage
        # 2. Invoke compilation stage
        # 3. Invoke validation stage
        # 4. Invoke externalization stage (if applicable)
        # 5. Monitor resource usage within tick limits
        # 6. Return PipelineResult
        # 7. Escalate pipeline failures to Logos Agent
        pass
    
    def handle_pipeline_failure(
        self,
        failure: "PipelineFailure"
    ) -> "FailureResponse":
        """
        Handle MTP pipeline failure.
        
        Failure handling:
        - Log failure event
        - Escalate to Logos Agent
        - Return failure response
        
        Args:
            failure: PipelineFailure details
        
        Returns:
            FailureResponse for Logos Agent
        
        Invariants Enforced:
        - INV-I2-09: Pipeline failure escalation
        """
        # Implementation obligations:
        # 1. Log pipeline failure event
        # 2. Create FailureResponse
        # 3. Return for Logos Agent escalation
        pass
```

---

## 6. TICK LIFECYCLE MANAGER IMPLEMENTATION

### 6.1 Class Definition: `TickLifecycleManager`

**Location**: `I2/tick_lifecycle/tick_manager.py`

**Responsibilities** (per Design Spec §4.4):
- Manage tick lifecycle (start, processing, end)
- Coordinate with MTP Nexus for continuity state
- Enforce tick resource limits

**Class Signature**:
```python
from typing import Optional
from uuid import UUID
from ..types.tick_types import TickContext, TickResult
from ..types.decomposition_types import Subtask
from ..types.error_types import TickException, ResourceExceededException
from ..integration.mtp_nexus_interface import MTPNexusInterface
from .resource_monitor import ResourceMonitor

class TickLifecycleManager:
    """
    Manages tick lifecycle for multi-tick task execution.
    
    Tick lifecycle phases (per Design Spec §6.2):
    1. Tick Start: Initialize context, load continuity from MTP Nexus
    2. Tick Processing: Execute subtask(s) within tick
    3. Tick End: Save continuity to MTP Nexus, dispose context
    
    Constraints:
    - Tick context MUST be initialized before processing (INV-I2-11)
    - Tick resource limits MUST be enforced (INV-I2-12)
    - Continuity MUST be saved at tick end (INV-I2-13)
    - Tick context MUST be disposed (INV-I2-14)
    """
    
    def __init__(
        self,
        mtp_nexus_interface: MTPNexusInterface,
        resource_monitor: ResourceMonitor,
        tick_resource_limits: "ResourceConstraints"
    ):
        """
        Initialize Tick Lifecycle Manager.
        
        Args:
            mtp_nexus_interface: MTP Nexus integration interface
            resource_monitor: Tick resource monitoring component
            tick_resource_limits: Resource constraints per tick
        """
        # Assignment
        pass
    
    def start_tick(self, task_id: UUID) -> TickContext:
        """
        Start new tick for task.
        
        Tick start operations:
        1. Initialize tick context
        2. Load continuity state from MTP Nexus (if not first tick)
        3. Allocate tick resources
        
        Args:
            task_id: UUID of task being processed
        
        Returns:
            TickContext initialized for tick processing
        
        Raises:
            MTPNexusUnavailableException: Continuity load failure (fail-closed)
        
        Invariants Enforced:
        - INV-I2-11: Tick context initialization
        - INV-I2-20: Continuity state load from MTP Nexus
        """
        # Implementation obligations:
        # 1. Create TickContext
        # 2. Load continuity state from MTP Nexus (if not first tick)
        # 3. Initialize resource monitoring
        # 4. Return TickContext
        pass
    
    def process_tick(
        self,
        tick_context: TickContext,
        subtask: Subtask
    ) -> TickResult:
        """
        Execute subtask within tick.
        
        Args:
            tick_context: Initialized tick context
            subtask: Subtask to execute in this tick
        
        Returns:
            TickResult with subtask outcome
        
        Raises:
            ResourceExceededException: Tick resource limit exceeded (INV-I2-12)
            TickException: Tick processing failure
        
        Invariants Enforced:
        - INV-I2-12: Tick resource limit enforcement
        """
        # Implementation obligations:
        # 1. Monitor resource usage via resource_monitor
        # 2. Execute subtask (via MTP pipeline or direct execution)
        # 3. Check resource usage against limits
        # 4. Generate TickResult
        # 5. Abort if resource limit exceeded
        pass
    
    def end_tick(
        self,
        tick_context: TickContext,
        tick_result: TickResult
    ) -> None:
        """
        End tick and save continuity state.
        
        Tick end operations:
        1. Save continuity state to MTP Nexus
        2. Log tick event
        3. Dispose tick context
        
        Args:
            tick_context: Tick context to finalize
            tick_result: Result from tick processing
        
        Raises:
            MTPNexusUnavailableException: Continuity save failure (fail-closed)
        
        Invariants Enforced:
        - INV-I2-13: Continuity state save to MTP Nexus
        - INV-I2-14: Tick context disposal
        - INV-I2-24: Tick event logging
        """
        # Implementation obligations:
        # 1. Extract continuity state from tick_context + tick_result
        # 2. Save continuity state to MTP Nexus
        # 3. Log tick end event
        # 4. Dispose tick_context
        pass
```

### 6.2 Class Definition: `ResourceMonitor`

**Location**: `I2/tick_lifecycle/resource_monitor.py`

**Responsibilities**:
- Monitor tick resource usage in real-time
- Enforce tick resource limits

**Class Signature**:
```python
from ..types.tick_types import ResourceUsage, ResourceConstraints
from ..types.error_types import ResourceExceededException

class ResourceMonitor:
    """
    Monitors resource usage within tick boundaries.
    
    Monitored resources (per Design Spec §6.2):
    - Computation time (wall-clock)
    - Memory allocation (heap usage)
    - MTP operations (pipeline invocation count)
    """
    
    def start_monitoring(self, limits: ResourceConstraints) -> None:
        """
        Start resource monitoring for tick.
        
        Args:
            limits: Resource limits to enforce
        """
        # Implementation: Initialize monitoring + set limits
        pass
    
    def check_limits(self) -> None:
        """
        Check current resource usage against limits.
        
        Raises:
            ResourceExceededException: Resource limit exceeded
        
        Invariants Enforced:
        - INV-I2-12: Real-time resource limit enforcement
        """
        # Implementation: Compare current usage against limits
        pass
    
    def get_usage(self) -> ResourceUsage:
        """
        Get current resource usage snapshot.
        
        Returns:
            ResourceUsage with current consumption metrics
        """
        # Implementation: Snapshot current usage
        pass
    
    def stop_monitoring(self) -> ResourceUsage:
        """
        Stop monitoring and return final usage.
        
        Returns:
            ResourceUsage for tick
        """
        # Implementation: Finalize + return usage
        pass
```

---

## 7. EA CONTEXT HANDLER IMPLEMENTATION

### 7.1 Class Definition: `EAContextHandler`

**Location**: `I2/ea_context/context_handler.py`

**Responsibilities** (per Design Spec §4.5):
- Fetch EA context from UWM
- Transform EA structure into I2-compatible format
- Dispose EA context after task completion

**Class Signature**:
```python
from typing import List
from ..types.task_types import EAReference
from ..types.error_types import EAFetchException, UWMUnavailableException
from ..integration.uwm_interface import UWMInterface

class EAContextHandler:
    """
    Manages EA context lifecycle for I2 tasks.
    
    EA context operations:
    1. Fetch EA content from UWM
    2. Transform EA → I2Context
    3. Provide context to task processing
    4. Dispose context after task completion
    
    Constraints:
    - EA access MUST be read-only (INV-I2-15)
    - NO caching across tasks (INV-I2-16)
    - Disposal MUST be unconditional (INV-I2-17)
    """
    
    def __init__(self, uwm_interface: UWMInterface):
        """
        Initialize EA Context Handler.
        
        Args:
            uwm_interface: UWM integration interface
        """
        # Assignment
        pass
    
    def fetch_ea_context(
        self,
        ea_refs: List[EAReference]
    ) -> "EAContext":
        """
        Fetch EA context from UWM for task processing.
        
        Args:
            ea_refs: List of EA references from TaskAssignment
        
        Returns:
            EAContext ready for I2 consumption
        
        Raises:
            EAFetchException: EA fetch failure (permissions, not found)
            UWMUnavailableException: UWM unreachable (triggers degraded mode)
        
        Invariants Enforced:
        - INV-I2-15: Read-only EA access
        - INV-I2-16: No caching (fresh fetch per task)
        """
        # Implementation obligations:
        # 1. Fetch EA content from UWM via uwm_interface
        # 2. Validate EA read permissions
        # 3. Transform EA → EAContext
        # 4. Return EAContext
        # 5. Handle UWM unavailability (degraded mode)
        pass
    
    def transform_ea(
        self,
        ea: "EpistemicArtifact"
    ) -> "I2ContextFragment":
        """
        Transform EA structure to I2-compatible format.
        
        Args:
            ea: EpistemicArtifact from UWM
        
        Returns:
            I2ContextFragment suitable for I2 processing
        """
        # Implementation: EA → I2ContextFragment transformation
        pass
    
    def dispose_ea_context(
        self,
        context: "EAContext"
    ) -> None:
        """
        Dispose EA context after task completion.
        
        Disposal is unconditional - occurs regardless of task success/failure.
        
        Args:
            context: EAContext to dispose
        
        Invariants Enforced:
        - INV-I2-17: Context disposal requirement
        - INV-I2-16: No context persistence
        """
        # Implementation obligations:
        # 1. Clear all EA references
        # 2. Release held resources
        # 3. Ensure no context leakage
        pass
```

---

## 8. INTEGRATION POINT IMPLEMENTATIONS

### 8.1 Logos Agent Interface

**Location**: `I2/integration/logos_interface.py`

**Purpose**: Protocol adapter for Logos Agent communication (per Design Spec §5.1)

**Class Signature**:
```python
from ..types.task_types import TaskAssignment, TaskResult
from ..types.decomposition_types import DecompositionProposal
from ..types.error_types import InvalidTaskException

class LogosInterface:
    """
    Integration adapter for Logos Agent communication.
    
    Protocol: Synchronous task assignment + proposal review
    Authority: Logos Agent is I2's ONLY task authority (INV-I2-01)
    """
    
    def receive_task_assignment(
        self,
        raw_assignment: dict
    ) -> TaskAssignment:
        """
        Parse task assignment from Logos Agent.
        
        Args:
            raw_assignment: Raw task data from Logos Agent
        
        Returns:
            Parsed TaskAssignment object
        
        Raises:
            InvalidTaskException: Assignment parsing failure
        """
        # Implementation: Deserialize + validate schema
        pass
    
    def validate_logos_signature(self, signature: str) -> bool:
        """
        Validate Logos Agent authority signature.
        
        Args:
            signature: Cryptographic signature from Logos Agent
        
        Returns:
            True if signature is valid and non-expired, False otherwise
        
        Invariants Enforced:
        - INV-I2-01: Logos Agent signature requirement
        """
        # Implementation: Cryptographic signature verification
        pass
    
    def submit_decomposition_proposal(
        self,
        proposal: DecompositionProposal
    ) -> bool:
        """
        Submit decomposition proposal to Logos Agent for approval.
        
        Args:
            proposal: DecompositionProposal to submit
        
        Returns:
            True if approved, False if rejected
        
        Invariants Enforced:
        - INV-I2-02: Proposal submission requirement
        """
        # Implementation: Serialize + transmit + await response
        pass
    
    def send_task_result(self, result: TaskResult) -> None:
        """
        Send task result to Logos Agent.
        
        Args:
            result: TaskResult to transmit
        
        Invariants Enforced:
        - INV-I2-19: Result delivery to Logos Agent only
        """
        # Implementation: Serialize + transmit
        pass
```

### 8.2 MTP Nexus Interface

**Location**: `I2/integration/mtp_nexus_interface.py`

**Purpose**: Continuity state management interface to MTP Nexus (per Design Spec §5.2)

**Class Signature**:
```python
from uuid import UUID
from typing import Optional
from ..types.error_types import MTPNexusUnavailableException

class MTPNexusInterface:
    """
    Integration adapter for MTP Nexus continuity management.
    
    Protocol: Continuity state persistence and retrieval
    Authority: I2 has read + write authority for assigned tasks
    """
    
    def load_continuity_state(
        self,
        task_id: UUID
    ) -> Optional["ContinuityState"]:
        """
        Load continuity state from MTP Nexus for task.
        
        Args:
            task_id: UUID of task
        
        Returns:
            ContinuityState if available, None if first tick
        
        Raises:
            MTPNexusUnavailableException: MTP Nexus unreachable (fail-closed)
        
        Invariants Enforced:
        - INV-I2-20: Continuity load at tick start
        - INV-I2-22: Fail-closed on MTP Nexus unavailability
        """
        # Implementation: MTP Nexus query + deserialization
        pass
    
    def save_continuity_state(
        self,
        task_id: UUID,
        state: "ContinuityState"
    ) -> None:
        """
        Save continuity state to MTP Nexus for task.
        
        Args:
            task_id: UUID of task
            state: ContinuityState to persist
        
        Raises:
            MTPNexusUnavailableException: MTP Nexus unreachable (fail-closed)
        
        Invariants Enforced:
        - INV-I2-13: Continuity save at tick end
        - INV-I2-21: Session-scoped continuity (V1)
        - INV-I2-22: Fail-closed on MTP Nexus unavailability
        """
        # Implementation: Serialize + MTP Nexus write
        pass
```

### 8.3 UWM Interface

**Location**: `I2/integration/uwm_interface.py`

**Purpose**: EA fetch interface to UWM (per Design Spec §5.3)

**Class Signature**:
```python
from typing import List
from ..types.task_types import EAReference
from ..types.error_types import EAFetchException, UWMUnavailableException

class UWMInterface:
    """
    Integration adapter for UWM EA fetching.
    
    Protocol: EA context retrieval
    Authority: Read-only (INV-I2-15)
    """
    
    def fetch_ea(self, ref: EAReference) -> "EpistemicArtifact":
        """
        Fetch EA content from UWM.
        
        Args:
            ref: EAReference identifying EA to fetch
        
        Returns:
            EpistemicArtifact content
        
        Raises:
            EAFetchException: Fetch failure (permissions, not found)
            UWMUnavailableException: UWM unreachable (triggers degraded mode)
        
        Invariants Enforced:
        - INV-I2-15: Read-only EA access
        - INV-I2-23: UWM unavailability triggers degraded mode
        """
        # Implementation: UWM fetch + permission validation
        pass
    
    def fetch_batch(
        self,
        refs: List[EAReference]
    ) -> List["EpistemicArtifact"]:
        """
        Batch fetch multiple EAs from UWM.
        
        Args:
            refs: List of EAReferences to fetch
        
        Returns:
            List of EpistemicArtifacts (order preserved)
        """
        # Implementation: Batch fetch optimization
        pass
```

### 8.4 Operational Logger Interface

**Location**: `I2/integration/logger_interface.py`

**Purpose**: Event logging interface to Operational Logger (per Design Spec §5.4)

**Class Signature**:
```python
from ..types.task_types import Task, TaskResult
from ..types.tick_types import TickContext, TickResult

class OperationalLoggerInterface:
    """
    Integration adapter for Operational Logger.
    
    Protocol: Event log submission
    Authority: Write-only
    """
    
    def log_task_event(
        self,
        event_type: str,
        task: Task,
        details: dict
    ) -> None:
        """
        Log task lifecycle event.
        
        Event types: "task_start", "task_completion", "task_failure"
        
        Args:
            event_type: Type of event
            task: Task being logged
            details: Additional event details
        
        Invariants Enforced:
        - INV-I2-04: Task lifecycle event logging
        - INV-I2-25: Logger unavailability does not block operations
        """
        # Implementation: Serialize + log submission (with stderr fallback)
        pass
    
    def log_tick_event(
        self,
        event_type: str,
        tick_context: TickContext,
        tick_result: TickResult
    ) -> None:
        """
        Log tick lifecycle event.
        
        Event types: "tick_start", "tick_processing", "tick_end"
        
        Args:
            event_type: Type of event
            tick_context: Tick context
            tick_result: Tick result
        
        Invariants Enforced:
        - INV-I2-24: Tick transition logging
        """
        # Implementation: Serialize + log submission
        pass
```

---

## 9. ERROR HANDLING PROTOCOLS

### 9.1 Exception Hierarchy

**Location**: `I2/types/error_types.py`

**Structure**:
```python
class I2Exception(Exception):
    """Base exception for all I2 errors."""
    pass

# Task assignment errors (E1 per Design Spec §9.1)
class InvalidTaskException(I2Exception):
    """Logos Agent signature invalid, schema malformed, or resource constraints invalid."""
    pass

# Task analysis errors (E2)
class EAFetchException(I2Exception):
    """EA fetch failure (permissions denied, EA not found)."""
    pass

class UWMUnavailableException(I2Exception):
    """UWM unreachable - triggers degraded mode (INV-I2-23)."""
    pass

class DecompositionException(I2Exception):
    """Task decomposition failure (analysis, proposal generation)."""
    pass

# Tick execution errors (E3)
class MTPNexusUnavailableException(I2Exception):
    """MTP Nexus unreachable - fail-closed (INV-I2-22)."""
    pass

class PipelineException(I2Exception):
    """MTP pipeline execution failure."""
    pass

class ResourceExceededException(I2Exception):
    """Tick resource limit exceeded."""
    pass

class TickException(I2Exception):
    """Tick processing failure."""
    pass

# Task completion errors (E4)
class TaskExecutionException(I2Exception):
    """Task execution failure (general)."""
    pass

# System errors (E5)
class I2InternalException(I2Exception):
    """I2 internal error."""
    pass
```

### 9.2 Error Handling Pattern

**Fail-Closed Default** (per Design Spec §9.2):
```python
def accept_task(self, assignment: TaskAssignment) -> TaskResult:
    ea_context = None
    task_context = None
    
    try:
        # 1. Validate Logos Agent authority
        if not self.logos_interface.validate_logos_signature(assignment.logos_signature):
            raise InvalidTaskException("Invalid Logos Agent signature")
        
        # 2. Log task start
        self.logger_interface.log_task_event("task_start", assignment.task, {})
        
        # 3. Fetch EA context
        ea_context = self.ea_handler.fetch_ea_context(assignment.ea_context_refs)
        
        # 4. Analyze task complexity
        profile = self.decomposition_engine.analyze_complexity(assignment.task)
        
        # 5. Decompose if needed
        if self.decomposition_engine.requires_decomposition(profile):
            proposal = self.decomposition_engine.generate_proposal(assignment.task)
            approved = self.logos_interface.submit_decomposition_proposal(proposal)
            
            if not approved:
                return TaskResult(
                    task_id=assignment.task_id,
                    status="REJECTED",
                    error_details={"message": "Decomposition proposal rejected by Logos Agent"}
                )
            
            # Multi-tick execution
            result = self._execute_multi_tick_task(assignment.task, proposal, ea_context)
        else:
            # Single-tick execution
            result = self._execute_single_tick_task(assignment.task, ea_context)
        
        # 6. Log task completion
        self.logger_interface.log_task_event("task_completion", assignment.task, {"result": result})
        
        return result
    
    except InvalidTaskException as e:
        # Task validation failure
        return self._create_error_result(assignment.task_id, "INVALID_TASK", e)
    
    except MTPNexusUnavailableException as e:
        # MTP Nexus unavailable - fail-closed
        return self._create_error_result(assignment.task_id, "CRITICAL_DEGRADATION", e)
    
    except UWMUnavailableException as e:
        # UWM unavailable - degraded mode
        return self._handle_degraded_mode("UWM", assignment)
    
    except I2Exception as e:
        # Other I2 errors - fail-closed
        return self._create_error_result(assignment.task_id, "TASK_FAILURE", e)
    
    finally:
        # ALWAYS dispose EA context (INV-I2-17)
        if ea_context is not None:
            self.ea_handler.dispose_ea_context(ea_context)
        
        # ALWAYS dispose task context (INV-I2-30)
        if task_context is not None:
            self._dispose_task_context(task_context)
```

---

## 10. TESTING REQUIREMENTS

### 10.1 Unit Test Obligations

**Test File Structure**:
```
LOGOS_SYSTEM/
└── RUNTIME_CORES/
    └── RUNTIME_EXECUTION_CORE/
        └── Logos_Core/
            └── Logos_Protocol/
                └── LP_Core/
                    └── Agent_Integration/
                        └── I2/
                            └── Tests/
                                ├── test_i2_agent.py
                                ├── test_task_decomposition.py
                                ├── test_mtp_pipeline_coordinator.py
                                ├── test_tick_lifecycle_manager.py
                                ├── test_ea_context_handler.py
                                └── test_invariants.py  # Dedicated invariant tests
```

**Required Test Cases** (per Design Spec §10.1):

**I2 Agent Tests** (`test_i2_agent.py`):
- `test_accept_task_valid`: Happy path task execution
- `test_accept_task_invalid_signature`: Reject invalid Logos signature (INV-I2-01)
- `test_accept_task_requires_decomposition`: Decomposition proposal flow
- `test_accept_task_single_tick`: Single-tick execution
- `test_accept_task_multi_tick`: Multi-tick execution
- `test_accept_task_mtp_nexus_unavailable`: Fail-closed on MTP Nexus unavailability (INV-I2-22)

**Task Decomposition Tests** (`test_task_decomposition.py`):
- `test_analyze_complexity`: Complexity analysis correctness
- `test_requires_decomposition_true`: Detect decomposition need
- `test_requires_decomposition_false`: Simple task (no decomposition)
- `test_generate_proposal_tick_bounded`: Subtasks are tick-bounded (INV-I2-05)
- `test_generate_proposal_resource_estimates`: Proposals include estimates (INV-I2-06)
- `test_identify_boundaries`: Boundary detection correctness
- `test_generate_subtasks_dependency_order`: Subtask dependency ordering (INV-I2-33)

**MTP Pipeline Coordinator Tests** (`test_mtp_pipeline_coordinator.py`):
- `test_invoke_pipeline_success`: Happy path pipeline execution
- `test_invoke_pipeline_failure`: Pipeline failure handling (INV-I2-09)
- `test_invoke_pipeline_within_tick`: Pipeline execution within tick boundaries (INV-I2-08)

**Tick Lifecycle Manager Tests** (`test_tick_lifecycle_manager.py`):
- `test_start_tick`: Tick context initialization (INV-I2-11)
- `test_start_tick_load_continuity`: Continuity load from MTP Nexus (INV-I2-20)
- `test_process_tick_resource_enforcement`: Tick resource limit enforcement (INV-I2-12)
- `test_end_tick_save_continuity`: Continuity save to MTP Nexus (INV-I2-13)
- `test_end_tick_context_disposal`: Tick context disposal (INV-I2-14)
- `test_mtp_nexus_unavailable`: Fail-closed on MTP Nexus unavailability (INV-I2-22)

**EA Context Handler Tests** (`test_ea_context_handler.py`):
- `test_fetch_ea_context_success`: Successful EA fetch
- `test_fetch_ea_context_read_only`: Verify read-only access (INV-I2-15)
- `test_fetch_ea_context_uwm_unavailable`: Degraded mode on UWM unavailability (INV-I2-23)
- `test_dispose_ea_context_unconditional`: Context disposal always occurs (INV-I2-17)
- `test_no_ea_caching`: Verify no caching across tasks (INV-I2-16)

### 10.2 Integration Test Obligations

**Integration Test Scope** (per Design Spec §10.2):

**Logos Agent Integration** (`test_logos_integration.py`):
- End-to-end task assignment and result return
- Decomposition proposal approval/rejection flow
- Multiple concurrent task assignments

**MTP Nexus Integration** (`test_mtp_nexus_integration.py`):
- Continuity state save/load correctness
- Multi-tick continuity preservation
- MTP Nexus unavailability handling (fail-closed)

**UWM Integration** (`test_uwm_integration.py`):
- EA fetch correctness
- EA read permission validation
- UWM unavailability handling (degraded mode)

**Operational Logger Integration** (`test_logger_integration.py`):
- Event log submission correctness
- Operational Logger unavailability (stderr fallback)

### 10.3 Invariant Test Obligations

**Dedicated Invariant Test File** (`test_invariants.py`):

Each invariant INV-I2-01 through INV-I2-35 MUST have dedicated test case(s):

```python
def test_INV_I2_01_logos_authority_validation():
    """INV-I2-01: I2 MUST validate Logos Agent signature on all task assignments."""
    # Test: Task without valid signature → InvalidTaskException
    pass

def test_INV_I2_03_tick_transitions_via_mtp_nexus():
    """INV-I2-03: I2 MUST coordinate all tick transitions via MTP Nexus."""
    # Test: Verify continuity load/save at each tick transition
    pass

def test_INV_I2_15_read_only_ea_access():
    """INV-I2-15: EA access MUST be read-only. I2 MUST NOT write to UWM."""
    # Test: Attempt EA write → Exception or rejection
    pass

# ... (32 more invariant tests)

def test_INV_I2_35_deterministic_operations():
    """INV-I2-35: All I2 operations MUST be deterministic. Identical inputs → identical outputs."""
    # Test: Same task + context executed twice → identical results
    pass
```

**Invariant Test Execution**:
- Pre-commit: Subset of critical invariants (INV-I2-01, 03, 15, 17, 22)
- CI/CD: Full invariant test suite (all 35 invariants)
- Nightly: Extended stress tests for invariant compliance

---

## 11. DEPLOYMENT AND CONFIGURATION

### 11.1 Configuration Schema

**Location**: `I2/config.json`

```json
{
    "i2_configuration": {
        "tick_resource_limits": {
            "computation_time_seconds": 30,
            "memory_mb": 256,
            "mtp_operations_per_tick": 10
        },
        "decomposition_policy": {
            "enable_auto_decomposition": true,
            "complexity_threshold": 0.7,
            "min_subtask_size": 0.1
        },
        "degradation_policy": {
            "uwm_unavailable_mode": "DEGRADED_LEVEL_1",
            "mtp_nexus_unavailable_mode": "FAIL_CLOSED",
            "logger_unavailable_mode": "STDERR_FALLBACK"
        },
        "logging": {
            "enabled": true,
            "log_level": "INFO",
            "include_tick_details": true
        }
    }
}
```

### 11.2 Initialization Protocol

**Initialization Sequence**:
1. Load configuration from `config.json`
2. Initialize integration interfaces (Logos, MTP Nexus, UWM, Logger)
3. Initialize I2 components (decomposition engine, pipeline coordinator, tick manager, EA handler)
4. Initialize I2Agent with all dependencies
5. Run invariant smoke tests (critical invariants)
6. Mark I2 as operational

**Bootstrap Code** (conceptual):
```python
def initialize_i2() -> I2Agent:
    """Initialize I2 sub-agent with all dependencies."""
    
    # 1. Load config
    config = load_config("config.json")
    
    # 2. Initialize interfaces
    logos_interface = LogosInterface()
    mtp_nexus_interface = MTPNexusInterface()
    uwm_interface = UWMInterface()
    logger_interface = OperationalLoggerInterface()
    
    # 3. Initialize components
    decomposition_engine = TaskDecompositionEngine(
        tick_resource_limits=config["tick_resource_limits"]
    )
    pipeline_coordinator = MTPPipelineCoordinator(
        pipeline_runner=PipelineRunner()
    )
    tick_manager = TickLifecycleManager(
        mtp_nexus_interface=mtp_nexus_interface,
        resource_monitor=ResourceMonitor(),
        tick_resource_limits=config["tick_resource_limits"]
    )
    ea_handler = EAContextHandler(uwm_interface=uwm_interface)
    
    # 4. Initialize I2 Agent
    i2_agent = I2Agent(
        decomposition_engine=decomposition_engine,
        pipeline_coordinator=pipeline_coordinator,
        tick_manager=tick_manager,
        ea_handler=ea_handler,
        logos_interface=logos_interface,
        mtp_nexus_interface=mtp_nexus_interface,
        logger_interface=logger_interface
    )
    
    # 5. Run smoke tests
    run_invariant_smoke_tests(i2_agent)
    
    return i2_agent
```

---

## 12. AMBIGUITY ESCALATION LOG

### 12.1 Resolved Ambiguities

**None**: All implementation obligations are clearly entailed by the design specification.

### 12.2 Unresolved Ambiguities Requiring Governance Decision

**A1: Decomposition Proposal Timeout Handling**  
**Context**: Design Spec §5.1 requires I2 to submit decomposition proposals to Logos Agent for approval, but does not specify timeout behavior if Logos Agent does not respond.

**Question**: How long should I2 wait for Logos Agent approval before timing out?
- Option 1: Fixed timeout (e.g., 60 seconds)
- Option 2: Configuration-based timeout
- Option 3: Indefinite wait (blocking)

**Recommendation**: Option 2 (configuration-based timeout) with graceful escalation (log timeout, return error result to Logos Agent if reachable).

**Escalation Required**: Yes (governance decision on timeout policy)

---

**A2: MTP Pipeline Stage Invocation Details**  
**Context**: Design Spec §4.3 requires MTP Pipeline Coordinator to invoke MTP pipeline stages, but does not specify exact invocation protocol or stage interface contracts.

**Question**: What is the canonical interface for MTP pipeline stages?
- Requires MTP Design Specification or interface contracts

**Recommendation**: Consult MTP Design Specification for stage invocation protocol.

**Escalation Required**: Yes (technical specification dependency)

---

**A3: Degraded Mode Result Acceptance by Logos Agent**  
**Context**: Design Spec §9.3 defines degraded modes (UWM unavailability triggers Level 1 degradation), but does not specify whether Logos Agent should accept degraded results or reject them.

**Question**: Should Logos Agent accept degraded task results, or require full-fidelity results?

**Recommendation**: Degraded results are valid but explicitly flagged. Logos Agent decides acceptance based on degradation level and task criticality.

**Escalation Required**: Yes (Logos Agent specification dependency)

---

**A4: Subtask Parallelization Support**  
**Context**: Design Spec §6.3 mentions "parallel" subtasks for independent operations, but does not specify parallel execution mechanism in V1.

**Question**: Does V1 support parallel subtask execution, or is all execution sequential?

**Recommendation**: V1 executes all subtasks sequentially (one subtask per tick). Parallel execution deferred to V2.

**Escalation Required**: No (clarification confirms sequential execution for V1)

---

**A5: Continuity State Schema Definition**  
**Context**: Design Spec §5.2 defines continuity state schema conceptually, but does not provide exact field definitions or serialization format.

**Question**: What is the canonical schema and serialization format for continuity state?

**Recommendation**: Define continuity state schema in coordination with MTP Nexus specification (JSON serialization).

**Escalation Required**: Yes (technical specification dependency - MTP Nexus schema)

---

### 12.3 Escalation Protocol

**For Unresolved Ambiguities**:
1. Document ambiguity in this log
2. Provide options + recommendation
3. Flag for governance review
4. Block implementation until resolution
5. Update this guide after resolution

---

**END OF IMPLEMENTATION GUIDE**

**Prepared By**: LOGOS Development Assistant (Claude)  
**Effective Date**: [Approval Date Placeholder]  
**Next Review**: [Review Date Placeholder]
