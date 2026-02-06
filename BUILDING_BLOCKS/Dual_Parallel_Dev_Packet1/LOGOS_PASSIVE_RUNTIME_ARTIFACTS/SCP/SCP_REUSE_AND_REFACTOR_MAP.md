# SCP_REUSE_AND_REFACTOR_MAP.md

## Purpose
This document classifies **existing SCP (Synthetic Cognition Protocol) assets** for reuse, refactor, extension, or deprecation under LOGOS V1.

SCP is assumed to be the **most mature and internally coherent protocol** in the stack; this audit focuses on normalization, not redesign.

---

## REUSE AS-IS (High Confidence)

These components are already aligned with SCP’s intended role and architecture.

- Modal Vector Space (MVS) core implementation
- 3D / fractal analysis space and traversal logic
- Baanock Data Node (BDN) system
- Parent–child decomposition and recomposition logic
- Retro-linking and chain reconstruction
- Fractal and orbital analysis toolkits
- Cross-domain inference engines embedded in SCP tools

Action:
- Preserve implementations
- Normalize interfaces and headers
- Enforce protocol directory conventions

---

## REFACTOR / NORMALIZE

These elements are correct in substance but require structural alignment.

- Module placement relative to Core / Tools separation
- Naming normalization per canonical repo standards
- Input/output normalization to SMP-AA / AA schemas
- Tool invocation interfaces (make SMP-first)

Action:
- No logic redesign
- Structural and interface cleanup only

---

## EXTEND (NEW, LIMITED SCOPE)

- SCP append-artifact emission (SMP-AA compatibility)
- Passive runtime hooks for I₁ collaboration
- Promotion-condition tagging (signal insufficiency, constraint failure, instability)
- I1AA artifact class (promotion-request artifact)

---

## DEPRECATE / ISOLATE

- Any SCP module assuming global orchestration authority
- Any SCP logic that mutates canonical state directly

---

END DOCUMENT
