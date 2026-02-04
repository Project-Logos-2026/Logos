# DRAC_CROSS_STAGE_BINDING_MAP.md

**Status:** CANONICAL | DESIGN-ONLY  

| DRAC Stage | Governing Invariants | Boundary |
|-----------|---------------------|----------|
| session_init | G1, G7 | — |
| profile_loader | G2 | — |
| baseline_assembler | G1–G4 | Boundary A |
| artifact_overlay | G1, G7 | Boundary B |
| reuse_decision | G7 | Boundary B |
| compilation | G3, G6 | Boundary B |
| artifact_cataloger | G5, G6, G8 | Boundary C |
