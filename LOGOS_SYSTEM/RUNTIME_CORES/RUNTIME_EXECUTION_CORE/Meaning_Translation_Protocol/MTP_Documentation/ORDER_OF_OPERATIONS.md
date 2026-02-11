# MTP Egress Enhancement — Order of Operations

## Entry Point

MTPNexus.process(smp_payload, discourse_mode=None, render_config=None)

## Pipeline Flow

### Stage 1: Projection

ProjectionEngine.project(smp_payload) -> ProjectionResult
- Extracts semantic primitives (SP-01 through SP-12) from SMP payload
- Builds Semantic Content Graph with typed nodes and inferred edges
- Topological ordering computed for downstream linearization
- Fail: empty graph -> pipeline FAILED

### Stage 2: Linearization (AF-LANG-001)

SemanticLinearizer.linearize(graph, discourse_mode) -> LinearizationPlan
- Computes canonical order: scope/grounding first, uncertainty/unknown last
- Assigns discourse roles per mode (technical/declarative/explanatory)
- Produces ordered LinearUnit sequence
- Fail: no units -> pipeline FAILED

### Stage 3: Fractal Evaluation (AF-LANG-002)

FractalEvaluator.evaluate(plan) -> StabilityReport
- Computes primitive distribution and detects structural patterns
- Calculates triadic resonance (sign/bridge/mind axis balance)
- Produces stability score and structural warnings
- Advisory only: evaluation failure does not halt pipeline

### Stage 4: Rendering (AF-LANG-003)

OutputRenderer.render(plan, config, stability_report) -> RenderedOutput
- Selects sentence templates per primitive type and tone level
- Produces L1 (natural language surface), L2 (arithmetic shadow), L3 (PXL refs)
- L1/L2 synchronization check enforced if L2 populated
- Fail: L1/L2 divergence -> render FAILED

### Stage 5: Validation

ValidationGate.validate(rendered, plan) -> ValidationResult
- Check 1: Structural Coverage (bijective unit-to-sentence mapping)
- Check 2: Arithmetic Shadow Consistency (L2 matches L1 numeric claims)
- Check 3: Semantic Predicate Alignment (sentences trace to source templates)
- PASS -> proceed to Stage 6
- REJECT + retries remain -> retry with alternate tone
- REJECT + retries exhausted -> pipeline HALTED

### Stage 6: I2 Critique

I2EgressCritique.critique(rendered, plan, graph, smp_payload) -> CritiqueResult
- Check 1: Translatability (NL reverse-maps to source units)
- Check 2: Privation Surface (NL preserves source privation states)
- Check 3: Grounding Audit (grounding claims trace to SMP evidence)
- PASS -> proceed to emission
- ABSTAIN -> proceed to emission (advisory)
- FAIL + retries remain -> retry with alternate tone
- FAIL + retries exhausted -> emit with critique warning attached

### Stage 7: Emission

Pipeline returns EgressPipelineResult with status EMITTED.
emitted_text() returns final L1 paragraph.

## Retry Mechanics

Tone rotation on retry: neutral -> formal -> accessible
Maximum retries: 2 (configurable via MTPNexus constructor)
I2 FAIL on final retry: emit anyway (I2 is non-authoritative per governance)

## Explicit Non-Operations

- No agent reasoning or autonomous decision-making
- No semantic mutation at any pipeline stage
- No SMP payload modification
- No authority escalation
- No external IO
- No session persistence
