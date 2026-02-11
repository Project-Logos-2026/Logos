# EMP Order Of Operations

## Entry Points

- EMP_Meta_Reasoner.analyze(artifact)
- EMP_Coq_Bridge.verify(coq_source)
- EMP_Coq_Bridge.compile_file(file_path)
- EMP_Coq_Bridge.check_theorem(theorem_name, file_path)
- EMP_Proof_Index.index_file(file_path, verification_result)
- EMP_Proof_Index.index_directory(directory)
- EMP_Proof_Index.search(query)
- EMP_Template_Engine.extract_templates(proof_entries)
- EMP_Template_Engine.instantiate(template, params)
- EMP_Abstraction_Engine.generalize(proof_entry)
- EMP_Abstraction_Engine.mine_patterns(proof_entries)
- EMP_MSPC_Witness.request_coherence_check(derivation)
- EMP_Nexus.PreProcessGate.apply(packet)
- EMP_Nexus.PostProcessGate.apply(packet)
- EMP_Nexus.StandardNexus.register_participant(participant)
- EMP_Nexus.StandardNexus.ingest(packet)
- EMP_Nexus.StandardNexus.tick(causal_intent=None)
- EMP_Nexus.NexusHandle.emit(payload, causal_intent=None)

## Meta Reasoner Flow (Coq-Backed)

1. analyze receives artifact dict.
2. Budget check via _use(). Raises ReasoningBudgetExceeded on overflow.
3. Extract coq_source or proof_content from artifact.
4. If no proof content or no Coq bridge: classify as UNVERIFIED.
5. Budget check. Submit to EMP_Coq_Bridge.verify().
6. If verification fails: classify as PROVISIONAL.
7. If admits_count > 0: classify as PARTIAL.
8. If axioms exceed PXL kernel: classify as VERIFIED_AXIOMATIC.
9. If all axioms within PXL kernel: classify as VERIFIED_PXL.
10. If MSPC witness available: request coherence check.
11. If MSPC returns coherent=true: promote to CANONICAL_CANDIDATE.
12. Attach EMP_PROOF_RESULT AA to artifact.
13. Record reasoning_steps_used.

## Coq Bridge Flow

1. Detect Coq environment (coqc on PATH).
2. Configure loadpath from _CoqProject.
3. Write source to temp .v file.
4. Invoke coqc with loadpath args and timeout.
5. Parse output: admits count, axiom dependencies, proof steps.
6. Hash .vo artifact if produced.
7. Return CoqVerificationResult.
8. Clean up temp files.

## Nexus Flow (Enhanced PostProcessGate)

1. PreProcessGate validates structural admissibility.
2. Inbound packets are ingested and mesh-validated.
3. Tick routes inbound packets to participants.
4. MRE pre-check gates each participant tick.
5. Participants execute deterministically (sorted by id).
6. MRE post-check completes the tick.
7. PostProcessGate:
   a. If payload contains coq_source/proof_content AND meta_reasoner available:
      route to Coq-backed tagging via _apply_coq_proof_tagging.
   b. Otherwise: apply keyword-based provisional tagging (backward-compatible).
8. Participant projections are routed downstream.

## MSPC Witness Flow

1. EMP requests coherence check via EMP_MSPC_Witness.
2. Witness constructs request payload.
3. Request routed: EMP -> Logos Agent -> MSPC.
4. MSPC evaluates four-modality expressibility.
5. Response routed: MSPC -> Logos Agent -> EMP.
6. Witness parses response into CoherenceResult.
7. Result returned to Meta Reasoner for classification gating.

## Explicit Non-Operations

- No agent reasoning or goal selection.
- No governance authority mutation.
- No autonomous external IO or network calls.
- No direct protocol-to-protocol communication.
- No persistent state across sessions.
