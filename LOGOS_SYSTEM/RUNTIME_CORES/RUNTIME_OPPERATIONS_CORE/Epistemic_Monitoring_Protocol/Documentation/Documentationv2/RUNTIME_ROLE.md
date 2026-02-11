# EMP Runtime Role

EMP provides Coq-backed epistemic classification via the Meta Reasoner and a
Standard Nexus with explicit pre/post gates. It verifies proof artifacts
mechanically through Coq subprocess compilation and assigns six-tier monotonic
classification states (UNVERIFIED through CANONICAL_CANDIDATE) based on
verification results, axiom footprint analysis, and MSPC coherence witness
confirmation.

The Nexus enforces mesh validation and deterministic routing. The enhanced
PostProcessGate applies Coq-verified proof tagging when the Meta Reasoner
is available, falling back to keyword-based provisional tagging otherwise.

Secondary capabilities:
- Proof indexing and search (EMP_Proof_Index)
- Template extraction and validation (EMP_Template_Engine)
- Structural abstraction and pattern mining (EMP_Abstraction_Engine)
- MSPC coherence witness integration (EMP_MSPC_Witness)

Supported invariants:
- Reasoning budget enforcement
- Deterministic tick ordering and mesh enforcement
- Fail-closed on invalid packets
- Fail-closed on Coq verification errors
- Fail-closed on MSPC unavailability (halts at VERIFIED_PXL, never false-promotes)
- Six-tier monotonic classification (no level skipping)
- All outputs are non-authoritative ProtocolAAs

Removal impact analysis:
- Epistemic tagging and EMP routing would be unavailable to downstream systems.
- Proof verification capability would be lost.
- CANONICAL_CANDIDATE classification would be impossible.
- SMP canonicalization would be blocked (EMP proof artifacts required per AA Schema).

Prohibited extensions:
- No autonomous inference or goal selection
- No authority escalation or SOP mutation
- No external IO beyond Coq subprocess and Logos Agent relay
- No persistent state across sessions
