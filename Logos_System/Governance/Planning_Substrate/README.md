# Planning Substrate -- Design Only

This directory defines the planning substrate for LOGOS as
a governed, non-executable layer.

## What This Is
- Formal definitions of plans
- Validation requirements
- Constraints on tick usage

## What This Is NOT
- A planner
- A planning loop
- An execution engine
- Autonomy or goal selection

## Key Principle
Planning is a client of execution, never its driver.

No artifact in this directory enables execution.
All future planning work must pass governance and tick constraints
defined elsewhere.
