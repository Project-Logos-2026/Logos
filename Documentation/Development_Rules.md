# Development Rules

## Canonical Family Routing Rule

When a function family is declared canonical, VS Code must:

1. Write a governance contract to `_Governance/Canonical_Contracts/<Canonical_Name>_Contract.json`
2. Backfill `semantic_capability_map_v0.json` with spine binding and admission status
3. Create a callable monolith module `Monolith/<Canonical_Name>.py`
4. Register execution in `Monolith/Monolith_Runtime.py`
5. Append a plain-language entry to `docs/Canonical_Contracts_Index.md`

This rule is mandatory and enforced fail-closed.
# Development Rules — Contextual Embedding (Semantic Contexts Synthesis)

**Phase ID:** PHASE_CONTEXTUAL_EMBEDDING
**Status:** ACTIVE
**Established:** 2026-01-16T17:45:31.334985Z

## Purpose
Synthesize unprocessed family deltas into governed semantic context modules without modifying axioms or application logic.

## Inputs
- `FAMILY_DELTAS/UNPROCESSED_FAMILIES/*.json`

## Outputs
- `PYTHON_MODULES/SEMANTIC_CONTEXTS/*.py`
- `SEMANTIC_CONTEXTS/SEMANTIC_CONTEXTS_CATALOG.json`

## Layer Rules
- **SEMANTIC_AXIOMS**: READ_ONLY
- **SEMANTIC_CONTEXTS**: WRITE_ALLOWED
- **APPLICATION_FUNCTIONS**: DEFERRED

## Classification Outcomes
- EMBEDDED
- DEFERRED
- RETIRED

## Embedding Constraints
**Allowed Imports:**
- PYTHON_MODULES/SEMANTIC_AXIOMS
- python_standard_library

**Forbidden Imports:**
- APPLICATION_FUNCTIONS
- legacy_scripts
- external_libraries
- direct_UWM_mutation

**Side Effects:** PROHIBITED

## Context Module Rules
- **one_context_per_family**: True
- **file_naming**: Title_Case_With_Underscores.py
- **public_entrypoint**: run(context: dict) -> dict
- **classes_optional**: True

## Catalog Requirements
- family_id
- family_delta_file
- status
- context_module
- semantic_tags
- control_role
- data_role
- spine_binding
- axiom_dependencies
- contracts_implicated
- notes

## Governance Interaction
- **runtime_spine**: READ_ONLY
- **semantic_capability_map**: READ_ONLY
- **new_capabilities**: NOT_PERMITTED_IN_THIS_PHASE

## Documentation Policy
- **headers**: DEFERRED
- **authoritative_metadata**: SEMANTIC_CONTEXTS_CATALOG.json

## Completion Criteria
- all_unprocessed_families_classified
- all_embedded_families_have_context_modules
- catalog_complete
- no_axiom_changes

---

