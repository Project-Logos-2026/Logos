# GitHub Copilot instructions for the LOGOS repository ✅

Purpose: give AI coding agents the exact, actionable facts needed to be productive and safe in this repo.

## High-level architecture & why it matters 🔧
- LOGOS is a **design-first, governance-driven** analytical framework. Governance artifacts are authoritative; many files are intentionally "design-only" (non-executable). See `Repo_Documents/GOVERNANCE_MODEL.txt` and `Repo_Documents/REPO_GUIDE.txt` for background.
- Major components: Governance (constraints & lifecycle), Protocols (reasoning interfaces), Frameworks (PXL/IEL), Simulations (descriptive runbooks), and System_Stack (agents & runtime plumbing). Changes must respect these boundaries — do not convert design-only docs into executable behavior.

## Critical workflows & canonical commands ⚙️
- Canonical Coq/proof gate (kernel build + LEM check):
  - `python3 test_lem_discharge.py` — this script invokes `coq_makefile` → `make -f CoqMakefile ...` and then runs a `Print Assumptions` check on `pxl_excluded_middle`.
  - The script output is parsed by downstream dashboards and tooling. **Preserve stdout markers** such as `Overall status: PASS`, `<none>`, and `Current status: ALIGNED` (do not rename or remove them).
  - Equivalent low-level steps: `coq_makefile -f _CoqProject -o CoqMakefile && make -f CoqMakefile clean && make -f CoqMakefile -j$(nproc)`
- Tests:
  - Default `pytest` is scoped by `pytest.ini` to run governance and agent tests (see `pytest.ini` testpaths). To run a broader set of tests, invoke `pytest <path>` directly (e.g., `pytest Logos_System/...`). Use `-k` or `-m` to target markers like `integration`.
- Docker / runtime stack:
  - Deployment helpers live under System_Stack and utilities like `deploy_full_stack.py`. Compose files include `docker-compose.yml` / `docker-compose.v7.yml`. Use the deploy scripts rather than modifying compose files blindly.

## Project-specific conventions & patterns 📐
- Governance-first: default posture is DENY / FAIL-CLOSED. Any code that implies autonomous action, real-world authority, or intent is a governance violation.
- Many scripts explicitly detect missing external tools (e.g., `coq_makefile`, `docker`, `docker-compose`) and skip/abort gracefully — keep those checks intact.
- Tests and smoke suites often live in `_Dev_Resources` and `DEV_RESOURCES/Dev_Scripts/smoke_tests/`; many are intentionally environment-sensitive and may `skip` when dependencies aren't available.
- Pages and files named `PHASE_*` or `Phase_*` capture lifecycle / policy states — consult these before changing high-impact behavior.

## Integration points & external dependencies 🔗
- External tools: Coq (rocq/coq_makefile), Docker & Docker Compose, RabbitMQ, Redis, system Python packages in `requirements.txt` (numpy, pandas, pydantic, pytest, ...).
- Service contracts: deployment and health checks are implemented in `System_Stack/.../deploy` and `Utilities/validate_production.py`. When adding runtime integrations, add matching health checks and governance assertions.

## Editing rules for AI agents (must follow) ✍️
- Preserve governance semantics: do NOT introduce any code that grants autonomy, authority, or external effect without explicit governance-approved artifacts.
- Preserve output markers or fingerprints used by other tools (examples above). If you must change a marker, leave the old marker and add a new one temporarily, and request human review.
- Keep changes minimal and reversible: prefer small, well-documented commits and add tests (where applicable) under the same governance/test scopes.
- When adding runtime behavior, add a corresponding governance artifact describing the allowed action and authorization path (`/Governance/`).

## Quick map: files & directories to check first 📂
- `README.md` — project purpose
- `Repo_Documents/REPO_GUIDE.txt` & `Repo_Documents/GOVERNANCE_MODEL.txt` — rules of the road
- `pytest.ini` — test discovery defaults
- `requirements.txt` — Python dependencies
- `STARTUP/PXL_Gate/coq/*` and `System_Entry_Point/*` — Coq build and proof gate scripts
- `System_Stack/.../deploy_full_stack.py`, `Utilities/validate_production.py` — deployment and runtime validation

---
If anything in these instructions is unclear or missing (e.g., a missing canonical script, a new runtime service, or a governance exception), ask a human reviewer before making changes. Please share a short PR description that references which governance artifact you updated or why the change is safe. 💬

---
Would you like me to iterate on any sections (build steps, tests, or governance rules) or add repository-specific examples taken from a particular file? 🔍
