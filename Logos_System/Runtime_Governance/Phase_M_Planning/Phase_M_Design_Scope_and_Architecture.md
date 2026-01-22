# Phase-M Design Scope & Architecture (Planning Runtime, Design-Only)

There is **no direct path** from Planning -> Execution.

---

## 3. Core Responsibilities (Design Scope)

The planning runtime is responsible for:

- Constructing candidate **Plan objects**
- Ensuring plans are **PXL-admissible by construction**
- Annotating:
  - intent
  - domain references
  - estimated tick budgets
- Producing **reviewable, serializable plan artifacts**

The planning runtime is **not** responsible for:

- Executing actions
- Selecting goals autonomously
- Approving plans
- Invoking agents
- Expanding authority or scope

---

## 4. Planner Runtime Components (Conceptual)

### 4.1 Plan Constructor
- Accepts inputs: intent, constraints, domain context
- Produces a Plan object
- Enforces structural validity

### 4.2 PXL Constraint Filter
- Applies PXL admissibility gates
- Rejects non-coherent or out-of-scope plans

### 4.3 Plan Serializer
- Produces inspectable, auditable representations
- Enables governance review

No component may:
- mutate authority,
- assume approval,
- trigger execution.

---

## 5. Governance Interface (Design-Only)

The planning runtime exposes plans **only** to governance.

Governance may:
- approve plans,
- reject plans,
- request modification.

Governance approval:
- does not execute plans,
- does not schedule execution,
- does not guarantee execution.

---

## 6. Execution Separation Guarantee

Execution systems:

- do not import the planner,
- do not depend on planner state,
- do not accept plans directly.

Execution occurs **only** via:
- explicit policy,
- tick governance,
- executor invocation.

---

## 7. Safety & Non-Autonomy Invariants

Phase-M inherits and enforces:

- No autonomy
- No goal selection
- No self-authorization
- No implicit execution
- No unbounded planning

Violation of any invariant invalidates the design.

---

## 8. Out of Scope (Explicit)

The following are **out of scope** for Phase-M design:

- Runtime scheduling
- Optimization loops
- Learning or adaptation
- Self-directed reasoning
- Cross-plan chaining

These require future phase authorization.

---

## 9. Phase-M Completion Criteria (Design)

Phase-M design is complete when:

- Architecture is documented and reviewed
- Interfaces are frozen
- Governance hooks are defined
- Safety invariants are reaffirmed
- A Phase-M Audit Checklist is satisfied

No code may be written before that point.

---

## 10. Final Statement

> Planning is permitted only because authority is already proven.
> Planning is constrained so that authority can never drift.

This document defines the **only acceptable shape**
of a LOGOS planning runtime.
