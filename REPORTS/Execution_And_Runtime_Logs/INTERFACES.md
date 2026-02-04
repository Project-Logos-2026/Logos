# ARP Application Functions — Interfaces (Design-Only)

## Constraints
- Interfaces only; no implementation
- No new axioms or IEL domains
- No runtime wiring or execution
- Enforceable by Runtime_Control

## Interfaces

### AF-PXL-VALIDATE
Inputs: relation_spec, context, options
Outputs: heuristic_validation (labeled), proof_refs (optional)

### AF-PXL-CACHE-POLICY
Inputs: cache_key, ttl, proof_refs
Outputs: cache_decision (allow/deny/downgrade)

### AF-IEL-DOMAIN-SELECT
Inputs: problem_spec
Outputs: selected_domains (explicit)

### AF-IEL-SYNTHESIZE
Inputs: domain_outputs
Outputs: synthesized_heuristic (labeled)

### AF-MATH-SIMILARITY
Inputs: structures
Outputs: similarity_scores (heuristic)

### AF-UNIFIED-AGGREGATE
Inputs: pxl_out, iel_out, math_out
Outputs: aggregated_heuristic (weakest-epistemic)

### AF-EPISTEMIC-DOWNGRADE
Inputs: aggregated_heuristic
Outputs: downgraded_output (labels enforced)

## Status
Design-only. Implementation not authorized.
