"""
Meta_Reasoning_Engine
---------------------
Exports for the Meta Reasoning Engine layer of the ARP stack.

PCCRE is positioned ABOVE the 5-stage ARPCompilerCore pipeline.
It validates a ConceptPacket against PXL operators, DRAC axioms,
5 reasoning lenses, a formal proof engine, and a MESH fixed-point
attractor before the concept is admitted to execution envelope assembly.

Amplification is available via IterativeReasoningAmplifier or the
Amplify_Concept_To_Artifact convenience entry point.

Phase F (FBC Combination Engine) extends PCCRE with full optional-
composable axiom coverage via DRAC_Function_Block_Core_Engine:
  - 8 new reasoning lenses (EvidenceChain, ExistenceProof, Temporal,
    TrinitarianLogic, BijectionClosure, TripartiteDistinction,
    HypostaticIdentity, InputSanitizer)
  - 5 power FBC configurations (POWER-A..E) scored and ranked
  - Context embedding injection: each optional axiom is paired with
    the optimal SCX context embedding (SCX-001..005)
"""

from .Proof_Carrying_Context_Reasoning_Engine import (
    # Primary engine
    ProofCarryingContextReasoningEngine,
    # Artifact type
    ProofCarryingArtifact,
    # Input type
    ConceptPacket,
    # Construction helpers
    Build_Concept_Packet,
    # Single-pass entry point
    Reason_Concept_To_Artifact,
    # Iterative amplification entry point
    Amplify_Concept_To_Artifact,
    # Amplifier class (for advanced use)
    IterativeReasoningAmplifier,
    AmplificationResult,
    # Sub-components (for composition)
    PXLKernel,
    DRACAxiomRegistry,
    OntologicalProofEngine,
    MeshFixedPointAttractor,
    ContextCompiler,
    # Lens classes
    DeductiveLens,
    InductiveLens,
    AbductiveLens,
    AnalogicalLens,
    TopologicalLens,
    # Exceptions
    ReasoningViolation,
    InvariantViolation,
    CapabilityViolation,
    CoherenceViolation,
    ProofViolation,
    ConvergenceViolation,
)

__all__ = [
    "ProofCarryingContextReasoningEngine",
    "ProofCarryingArtifact",
    "ConceptPacket",
    "Build_Concept_Packet",
    "Reason_Concept_To_Artifact",
    "Amplify_Concept_To_Artifact",
    "IterativeReasoningAmplifier",
    "AmplificationResult",
    "PXLKernel",
    "DRACAxiomRegistry",
    "OntologicalProofEngine",
    "MeshFixedPointAttractor",
    "ContextCompiler",
    "DeductiveLens",
    "InductiveLens",
    "AbductiveLens",
    "AnalogicalLens",
    "TopologicalLens",
    "ReasoningViolation",
    "InvariantViolation",
    "CapabilityViolation",
    "CoherenceViolation",
    "ProofViolation",
    "ConvergenceViolation",
]

# ── DRAC Function Block Core Engine ─────────────────────────────────────────
try:
    from .DRAC_Function_Block_Core_Engine import (
        # Engine
        FBCCombinationEngine,
        Build_FBC_Engine,
        Run_FBC_Phase,
        # Configurations
        FunctionBlockCore,
        FBCScore,
        FBCEvaluationResult,
        PowerClass,
        # Context embeddings
        ContextEmbedding as FBCContextEmbedding,
        # Catalog helpers
        ranked_configurations,
        get_fbc_configuration,
        # Lenses
        EvidenceChainLens,
        ExistenceProofLens,
        TemporalSupersessionLens,
        TrinitarianLogicLens,
        BijectionClosureLens,
        TripartiteDistinctionLens,
        HypostaticIdentityLens,
        InputSanitizerLens,
        # Exceptions
        SanitizerViolation,
    )
    _FBC_ENGINE_EXPORTED = True
except ImportError:
    _FBC_ENGINE_EXPORTED = False

if _FBC_ENGINE_EXPORTED:
    __all__ += [
        "FBCCombinationEngine",
        "Build_FBC_Engine",
        "Run_FBC_Phase",
        "FunctionBlockCore",
        "FBCScore",
        "FBCEvaluationResult",
        "PowerClass",
        "FBCContextEmbedding",
        "ranked_configurations",
        "get_fbc_configuration",
        "EvidenceChainLens",
        "ExistenceProofLens",
        "TemporalSupersessionLens",
        "TrinitarianLogicLens",
        "BijectionClosureLens",
        "TripartiteDistinctionLens",
        "HypostaticIdentityLens",
        "InputSanitizerLens",
        "SanitizerViolation",
    ]
