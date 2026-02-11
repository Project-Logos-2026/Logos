# EMP Stack Position

Runtime domain: Operations

## Upstream Dependencies (Imports/Callers)

Standard library imports:
- typing, dataclasses, time, hashlib, subprocess, tempfile, pathlib, re, collections

External infrastructure:
- PXL_Gate Coq baseline (STARTUP/PXL_Gate/coq/)
  - _CoqProject loadpath configuration
  - 60 .v source files
  - coqc binary (system PATH) or jsCoq WebAssembly
- MSPC Protocol (LOGOS_SYSTEM/Runtime_Protocols/MSPC/)
  - Coherence witness integration via Logos Agent routing

Callers:
- Logos Agent (via DRAC session reconstruction)
- PostProcessGate (internal, Nexus tick cycle)

## Downstream Consumers (Targets/Emit Paths)

- Registered Nexus participants implementing NexusParticipant
- SOP or other consumers of epistemic_state tagging (via ProtocolAA)
- CSP for CANONICAL_CANDIDATE SMPs (via Logos Agent promotion decision)
- MTP Core for non-canonical SMPs and AAs

## Runtime Bridge Interaction

- No direct runtime bridge interaction.
- MSPC communication routed exclusively via Logos Agent.
- Coq subprocess is fire-and-forget with timeout enforcement.

## Session Lifecycle

- EMP_Proof_Index rebuilt on each session via DRAC reconstruction.
- EMP_Template_Engine catalog is session-scoped.
- No persistent state survives session boundary.
