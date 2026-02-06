# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
PXL Reasoning Engine - Core Substrate
=====================================

Baseline reasoning engine that provides the Philosophically Extended Logic (PXL)
substrate for all higher-order reasoning operations. Imports and coordinates
IEL domains and Mathematical categories as reasoning lenses.

Integration Architecture:
- PXL Schema: Foundational logic structures
- Relation Mapper: Trinity-grounded relation discovery
- IEL Domains: Philosophical reasoning domains
- Math Categories: Formal mathematical frameworks

Author: LOGOS AGI Development Team
Version: 1.0.0
Date: 2026-01-24
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum

# PXL Core Components
from Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.pxl_schema import (
    PXLRelationType,
    PXLRelation,
    TrinityVector,
    ModalProperties,
    PXLAnalysisConfig,
    ValidationResult,
    ValidationSeverity
)

from Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.relation_mapper import (
    PXLRelationMapper,
    RelationMappingResult,
    TrinityRelationAnalyzer
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReasoningMode(Enum):
    """PXL reasoning execution modes"""
    ANALYTICAL = "analytical"  # Pure logical analysis
    SYNTHETIC = "synthetic"  # Cross-domain synthesis
    EXPLORATORY = "exploratory"  # Discovery-oriented
    VALIDATING = "validating"  # Consistency checking


@dataclass
class PXLReasoningContext:
    """Context for PXL reasoning operations"""
    mode: ReasoningMode
    trinity_vector: TrinityVector
    modal_properties: ModalProperties
    active_domains: Set[str] = field(default_factory=set)
    active_categories: Set[str] = field(default_factory=set)
    timestamp: float = field(default_factory=time.time)


@dataclass
class PXLReasoningResult:
    """Result of PXL reasoning operation"""
    success: bool
    relations_discovered: List[PXLRelation]
    trinity_coherence: float
    modal_consistency: bool
    validation_result: ValidationResult
    context: PXLReasoningContext
    processing_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class PXLReasoningEngine:
    """
    Core PXL Reasoning Engine
    
    Provides the foundational substrate for philosophical reasoning by:
    1. Managing PXL schema and relation structures
    2. Coordinating Trinity-grounded analysis
    3. Providing integration points for IEL and Math lenses
    4. Maintaining reasoning coherence and validation
    """
    
    def __init__(self, config: Optional[PXLAnalysisConfig] = None):
        """Initialize PXL reasoning engine"""
        self.config = config or PXLAnalysisConfig()
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.relation_mapper = PXLRelationMapper()
        self.trinity_analyzer = TrinityRelationAnalyzer()
        
        # Reasoning state
        self.concept_registry: Dict[str, Dict[str, Any]] = {}
        self.relation_cache: Dict[str, List[PXLRelation]] = {}
        self.trinity_vectors: Dict[str, TrinityVector] = {}
        
        # Available lenses (populated by IEL and Math engines)
        self.available_iel_domains: Set[str] = set()
        self.available_math_categories: Set[str] = set()
        
        # Statistics
        self.reasoning_operations = 0
        self.cache_hits = 0
        
        self.logger.info("PXL Reasoning Engine initialized")
    
    def register_concept(
        self,
        concept_name: str,
        trinity_vector: Optional[TrinityVector] = None,
        definition: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Register a concept in the PXL substrate"""
        try:
            if trinity_vector is None:
                # Default to balanced Trinity vector
                trinity_vector = TrinityVector(
                    essence=0.5,
                    generation=0.5,
                    temporal=0.5
                )
            
            self.concept_registry[concept_name] = {
                "definition": definition or "",
                "properties": properties or {},
                "registered_at": time.time()
            }
            
            self.trinity_vectors[concept_name] = trinity_vector
            
            self.logger.debug(f"Registered concept: {concept_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register concept {concept_name}: {e}")
            return False
    
    def reason(
        self,
        concepts: List[str],
        context: Optional[PXLReasoningContext] = None,
        use_cache: bool = True
    ) -> PXLReasoningResult:
        """
        Execute PXL reasoning over concepts
        
        Args:
            concepts: List of concept names to reason about
            context: Reasoning context (created if None)
            use_cache: Whether to use cached relations
            
        Returns:
            PXLReasoningResult with discovered relations and analysis
        """
        start_time = time.time()
        self.reasoning_operations += 1
        
        try:
            # Create default context if needed
            if context is None:
                context = PXLReasoningContext(
                    mode=ReasoningMode.ANALYTICAL,
                    trinity_vector=TrinityVector(0.5, 0.5, 0.5),
                    modal_properties=ModalProperties()
                )
            
            # Ensure all concepts are registered
            for concept in concepts:
                if concept not in self.concept_registry:
                    self.register_concept(concept)
            
            # Check cache
            cache_key = self._generate_cache_key(concepts, context)
            if use_cache and cache_key in self.relation_cache:
                self.cache_hits += 1
                cached_relations = self.relation_cache[cache_key]
                
                return PXLReasoningResult(
                    success=True,
                    relations_discovered=cached_relations,
                    trinity_coherence=self._calculate_trinity_coherence(cached_relations),
                    modal_consistency=True,
                    validation_result=ValidationResult(valid=True),
                    context=context,
                    processing_time=time.time() - start_time,
                    metadata={"cached": True}
                )
            
            # Extract Trinity vectors for concepts
            trinity_vectors = {
                c: self.trinity_vectors.get(c, TrinityVector(0.5, 0.5, 0.5))
                for c in concepts
            }
            
            # Extract definitions if available
            concept_definitions = {
                c: self.concept_registry[c].get("definition", "")
                for c in concepts if c in self.concept_registry
            }
            
            # Map relations using PXL relation mapper
            mapping_result = self.relation_mapper.map_concept_relations(
                concepts={c: self.concept_registry.get(c, {}) for c in concepts},
                trinity_vectors=trinity_vectors,
                concept_definitions=concept_definitions
            )
            
            # Extract relations
            relations = self._extract_relations_from_mapping(mapping_result)
            
            # Filter by context mode
            filtered_relations = self._filter_relations_by_mode(relations, context.mode)
            
            # Validate relations
            validation_result = self._validate_relations(filtered_relations, context)
            
            # Calculate Trinity coherence
            trinity_coherence = self._calculate_trinity_coherence(filtered_relations)
            
            # Check modal consistency
            modal_consistency = self._check_modal_consistency(
                filtered_relations,
                context.modal_properties
            )
            
            # Cache results
            if use_cache and validation_result.valid:
                self.relation_cache[cache_key] = filtered_relations
            
            # Create result
            result = PXLReasoningResult(
                success=validation_result.valid,
                relations_discovered=filtered_relations,
                trinity_coherence=trinity_coherence,
                modal_consistency=modal_consistency,
                validation_result=validation_result,
                context=context,
                processing_time=time.time() - start_time,
                metadata={
                    "mapping_result": {
                        "total_relations": mapping_result.total_relations,
                        "clusters": len(mapping_result.relation_clusters),
                        "global_coherence": mapping_result.global_coherence_score
                    }
                }
            )
            
            self.logger.info(
                f"PXL reasoning completed: {len(filtered_relations)} relations, "
                f"coherence={trinity_coherence:.3f}"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"PXL reasoning failed: {e}")
            return PXLReasoningResult(
                success=False,
                relations_discovered=[],
                trinity_coherence=0.0,
                modal_consistency=False,
                validation_result=ValidationResult(
                    valid=False,
                    issues=[ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=str(e)
                    )]
                ),
                context=context,
                processing_time=time.time() - start_time,
                metadata={"error": str(e)}
            )
    
    def _extract_relations_from_mapping(
        self,
        mapping_result: RelationMappingResult
    ) -> List[PXLRelation]:
        """Extract PXL relations from mapping result"""
        relations = []
        
        # Convert from internal relation format to PXL format
        for relation in mapping_result.strongest_relations:
            pxl_relation = PXLRelation(
                source_concept=relation.source_concept,
                target_concept=relation.target_concept,
                relation_type=self._map_relation_type(relation.relation_type),
                strength=relation.strength,
                confidence=relation.confidence,
                trinity_coherence=relation.metadata.get("trinity_coherence"),
                metadata=relation.metadata
            )
            relations.append(pxl_relation)
        
        return relations
    
    def _map_relation_type(self, internal_type) -> PXLRelationType:
        """Map internal relation type to PXL relation type"""
        mapping = {
            "logical_implication": PXLRelationType.LOGICAL_IMPLICATION,
            "trinity_coherence": PXLRelationType.TRINITY_COHERENCE,
            "semantic_similarity": PXLRelationType.SEMANTIC_SIMILARITY,
            "necessity_relation": PXLRelationType.NECESSITY_RELATION,
        }
        
        type_str = str(internal_type).lower()
        for key, value in mapping.items():
            if key in type_str:
                return value
        
        return PXLRelationType.SEMANTIC_SIMILARITY  # Default
    
    def _filter_relations_by_mode(
        self,
        relations: List[PXLRelation],
        mode: ReasoningMode
    ) -> List[PXLRelation]:
        """Filter relations based on reasoning mode"""
        if mode == ReasoningMode.ANALYTICAL:
            # Focus on logical and definitional relations
            return [r for r in relations if r.relation_type in [
                PXLRelationType.LOGICAL_IMPLICATION,
                PXLRelationType.LOGICAL_EQUIVALENCE,
                PXLRelationType.DEFINITIONAL_RELATION
            ]]
        
        elif mode == ReasoningMode.SYNTHETIC:
            # Include cross-domain relations
            return [r for r in relations if r.relation_type in [
                PXLRelationType.TRINITY_COHERENCE,
                PXLRelationType.TRINITY_COMPLEMENTARITY,
                PXLRelationType.SEMANTIC_SIMILARITY
            ]]
        
        elif mode == ReasoningMode.EXPLORATORY:
            # Include all strong relations
            return [r for r in relations if r.strength > 0.5]
        
        else:  # VALIDATING
            # Focus on consistency-checking relations
            return relations
    
    def _validate_relations(
        self,
        relations: List[PXLRelation],
        context: PXLReasoningContext
    ) -> ValidationResult:
        """Validate discovered relations"""
        result = ValidationResult(valid=True)
        
        for i, relation in enumerate(relations):
            # Validate individual relation
            rel_validation = relation.validate()
            if not rel_validation.valid:
                for issue in rel_validation.issues:
                    result.add_issue(
                        issue.severity,
                        f"Relation {i}: {issue.message}",
                        field_name=f"relations[{i}]"
                    )
        
        return result
    
    def _calculate_trinity_coherence(self, relations: List[PXLRelation]) -> float:
        """Calculate overall Trinity coherence of relations"""
        if not relations:
            return 0.0
        
        coherence_values = [
            r.trinity_coherence for r in relations
            if r.trinity_coherence is not None
        ]
        
        if not coherence_values:
            return 0.0
        
        return sum(coherence_values) / len(coherence_values)
    
    def _check_modal_consistency(
        self,
        relations: List[PXLRelation],
        modal_properties: ModalProperties
    ) -> bool:
        """Check modal consistency of relations"""
        # Simplified modal consistency check
        # In full implementation, would check modal logic constraints
        
        for relation in relations:
            if relation.relation_type == PXLRelationType.NECESSITY_RELATION:
                if not modal_properties.necessary:
                    return False
            
            if relation.relation_type == PXLRelationType.POSSIBILITY_RELATION:
                if not modal_properties.possible:
                    return False
        
        return True
    
    def _generate_cache_key(
        self,
        concepts: List[str],
        context: PXLReasoningContext
    ) -> str:
        """Generate cache key for reasoning operation"""
        import hashlib
        
        key_data = {
            "concepts": sorted(concepts),
            "mode": context.mode.value,
            "trinity": context.trinity_vector.to_tuple()
        }
        
        key_string = str(key_data)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def register_iel_domain(self, domain_name: str):
        """Register available IEL domain lens"""
        self.available_iel_domains.add(domain_name)
        self.logger.info(f"Registered IEL domain: {domain_name}")
    
    def register_math_category(self, category_name: str):
        """Register available Math category lens"""
        self.available_math_categories.add(category_name)
        self.logger.info(f"Registered Math category: {category_name}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get PXL engine statistics"""
        return {
            "reasoning_operations": self.reasoning_operations,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": self.cache_hits / max(self.reasoning_operations, 1),
            "registered_concepts": len(self.concept_registry),
            "cached_relations": len(self.relation_cache),
            "available_iel_domains": list(self.available_iel_domains),
            "available_math_categories": list(self.available_math_categories)
        }


# Global PXL engine instance
_pxl_engine = None

def get_pxl_engine(config: Optional[PXLAnalysisConfig] = None) -> PXLReasoningEngine:
    """Get or create global PXL engine instance"""
    global _pxl_engine
    if _pxl_engine is None:
        _pxl_engine = PXLReasoningEngine(config)
    return _pxl_engine


__all__ = [
    "PXLReasoningEngine",
    "PXLReasoningContext",
    "PXLReasoningResult",
    "ReasoningMode",
    "get_pxl_engine"
]
