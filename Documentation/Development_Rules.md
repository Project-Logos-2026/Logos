# Development Rules

## Canonical Family Routing Rule

When a function family is declared canonical, VS Code must:

1. Write a governance contract to `_Governance/Canonical_Contracts/<Canonical_Name>_Contract.json`
2. Backfill `semantic_capability_map_v0.json` with spine binding and admission status
3. Create a callable monolith module `Monolith/<Canonical_Name>.py`
4. Register execution in `Monolith/Monolith_Runtime.py`
5. Append a plain-language entry to `docs/Canonical_Contracts_Index.md`

This rule is mandatory and enforced fail-closed.
