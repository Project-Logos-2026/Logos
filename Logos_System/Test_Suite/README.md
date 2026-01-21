# Test Suite

## Phase-G Deployment Tests (Pytest)

Additional Phase-G deployment checks live under:

Logos_System/System_Stack/Logos_Agents/Logos_Agent/tests/test_runtime_deployment.py

These tests validate:
- deny without attestation
- conservative governance defaults
- attested execution → UWM commit path

They are **not executed** by run_all_tests.py by design.
Run explicitly with:

pytest Logos_System/System_Stack/Logos_Agents/Logos_Agent/tests/test_runtime_deployment.py

## Phase-H Multi-Tick Specification Tests (Pytest)

Phase-H introduces **test-first specification scaffolds** for future multi-tick
agent execution. These tests define required safety and governance properties
but **do not enable multi-tick execution**.

Location:
Logos_System/System_Stack/Logos_Agents/Logos_Agent/tests/test_multi_tick_execution.py

Properties specified:
- Multi-tick execution denied by default
- Explicit policy + attestation required
- Bounded tick budgets
- Fail-closed halt on budget exhaustion
- Append-only UWM commits per tick

These tests are **pytest-only** and are not executed by run_all_tests.py.

Run explicitly with:
pytest Logos_System/System_Stack/Logos_Agents/Logos_Agent/tests/test_multi_tick_execution.py
