# ARP Overhaul Package

## Overview

This package contains the complete ARP (Advanced Reasoning Protocol) overhaul implementation. It transforms ARP from stub-based execution into a multi-stage reasoning pipeline with 12 base engines, 5 taxonomical aggregators, and integration with PXL/IEL/Math meta-reasoning.

## Architecture

```
AACED Packet (from I3 Agent)
    ↓
Stage 1: Base Reasoning (12 engines)
    ↓
Stage 2: Taxonomical Aggregation (5 taxonomies)
    ↓
Stage 3+4: PXL/IEL/Math Triune + Synthesis
    ↓
Stage 5: Unified Reasoning Binder
    ↓
I3AA Artifact (to SMP)
```

## Directory Structure

```
ARP_Core/
├── compiler/
│   └── arp_compiler_core.py          # Main orchestrator
├── engines/
│   ├── base_reasoning_registry.py    # 12-engine orchestrator
│   ├── taxonomy_aggregator.py        # 5-taxonomy aggregator
│   ├── integration_bridge.py         # Meta engine bridge
│   └── unified_binder.py             # I3AA assembly

ARP_Tools/reasoning_engines/
├── logical/
│   ├── deductive_engine.py
│   ├── abductive_engine.py
│   └── inductive_engine.py
├── probabilistic/
│   ├── bayesian_engine.py
│   └── causal_engine.py
├── relational_structural/
│   ├── topological_engine.py
│   ├── graph_engine.py
│   └── relational_engine.py
├── semantic/
│   ├── analogical_engine.py
│   └── metaphorical_engine.py
└── constraint/
    ├── consistency_engine.py
    └── invariant_engine.py
```

## Installation

1. Extract this package to your LOGOS repository
2. Overlay files in the appropriate locations:
   ```
   cp -r ARP_Core/* LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Core/
   cp -r ARP_Tools/* LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Tools/
   ```
3. Verify imports resolve correctly
4. Run validation tests

## Compute Modes

- **Lightweight**: 4 engines, fast path (~0.5-1s per AACED)
- **Balanced** (default): 12 engines, full pipeline (~3-5s per AACED)
- **High-Rigor**: All engines + full IEL/Math domains (~15-25s per AACED)

## Integration Points

- **I3 Agent**: Invokes `ARPCompilerCore.compile(aaced_packet, context)`
- **Meta_Reasoning_Engine**: Integration via `integration_bridge.py`
- **ARP_Nexus**: Receives compiled I3AA artifacts (no changes required)

## Key Features

1. **Fail-Closed**: Degraded outputs preferred over hallucination
2. **Provenance Tracking**: Complete audit trail from AACED → I3AA
3. **Contradiction Detection**: Multi-layer consistency checking
4. **Confidence Calibration**: Fused probabilistic + formal verification
5. **Governance Compliant**: I3AA conforms to SMP_Agent_AA_Schemas.md

## Testing

See VALIDATION_CHECKLIST.md for complete testing procedure.

Quick smoke test:
```python
from ARP_Core.compiler.arp_compiler_core import ARPCompilerCore

compiler = ARPCompilerCore()
aaced = {"task": "test task", "concepts": ["logic", "proof"]}
i3aa = compiler.compile(aaced)
print(i3aa["status"])  # Should be "compiled" or "degraded"
```

## Documentation

- AUDIT_REPORT.md: Pre-overhaul audit findings
- OVERHAUL_SPEC.md: Complete architectural specification
- CHANGESET_PLAN.md: File-by-file change documentation
- VALIDATION_CHECKLIST.md: Testing and validation steps

## Support

For questions or issues, reference the full audit and spec documents included in this package.
