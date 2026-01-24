#!/usr/bin/env python3
"""
Unified Reasoning Engine - Demonstration
========================================

Demonstrates the complete PXL+IEL+Math reasoning system with
cross-domain synthesis and Trinity-grounded analysis.

Author: LOGOS AGI Development Team
Version: 1.0.0
Date: 2026-01-24
"""

from unified_reasoning import (
    get_unified_engine,
    IEL_MATH_MAPPING,
    MATH_IEL_MAPPING
)

from pxl_engine import PXLReasoningContext, ReasoningMode
from iel_engine import IELDomain
from math_engine import MathCategory

from Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.pxl_schema import (
    TrinityVector,
    ModalProperties
)


def print_separator(title: str = ""):
    """Print formatted separator"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def demonstrate_pxl_substrate():
    """Demonstrate PXL substrate reasoning"""
    print_separator("LAYER 1: PXL SUBSTRATE REASONING")
    
    engine = get_unified_engine()
    
    # Define philosophical concepts
    concepts = ["truth", "knowledge", "belief"]
    
    # Create Trinity-balanced context
    context = PXLReasoningContext(
        mode=ReasoningMode.ANALYTICAL,
        trinity_vector=TrinityVector(0.8, 0.7, 0.9),  # High truth focus
        modal_properties=ModalProperties(necessary=True, possible=True)
    )
    
    # Execute PXL reasoning
    pxl_result = engine.pxl_engine.reason(concepts, context)
    
    print(f"Concepts analyzed: {concepts}")
    print(f"Relations discovered: {len(pxl_result.relations_discovered)}")
    print(f"Trinity coherence: {pxl_result.trinity_coherence:.3f}")
    print(f"Modal consistency: {pxl_result.modal_consistency}")
    
    # Show sample relations
    if pxl_result.relations_discovered:
        print("\nSample PXL Relations:")
        for i, rel in enumerate(pxl_result.relations_discovered[:3], 1):
            print(f"  {i}. {rel.source_concept} → {rel.target_concept}")
            print(f"     Type: {rel.relation_type.value}, Strength: {rel.strength:.2f}")


def demonstrate_iel_domains():
    """Demonstrate IEL domain reasoning"""
    print_separator("LAYER 2: IEL DOMAIN REASONING")
    
    engine = get_unified_engine()
    
    concepts = ["axiom", "proof", "theorem"]
    
    # Apply specific IEL domains
    active_domains = {IELDomain.AXIOPRAXIS, IELDomain.GNOSIPRAXIS}
    
    iel_result = engine.iel_engine.reason(concepts, active_domains)
    
    print(f"Concepts analyzed: {concepts}")
    print(f"Domains applied: {[d.value for d in active_domains]}")
    print(f"Overall coherence: {iel_result.overall_coherence:.3f}")
    
    # Show domain analyses
    print("\nDomain Analyses:")
    for analysis in iel_result.domain_analyses:
        print(f"\n  [{analysis.domain.value}]")
        print(f"  Confidence: {analysis.confidence:.2f}")
        print(f"  Trinity: E={analysis.trinity_alignment.essence:.2f}, "
              f"G={analysis.trinity_alignment.generation:.2f}, "
              f"T={analysis.trinity_alignment.temporal:.2f}")
        print(f"  Insights:")
        for insight in analysis.insights[:2]:
            print(f"    - {insight}")


def demonstrate_math_categories():
    """Demonstrate Math category reasoning"""
    print_separator("LAYER 3: MATHEMATICAL CATEGORY REASONING")
    
    engine = get_unified_engine()
    
    concepts = ["number", "set", "relation"]
    
    # Apply specific math categories
    active_categories = {MathCategory.CORE, MathCategory.BOOLEAN_LOGIC}
    
    math_result = engine.math_engine.reason(concepts, active_categories)
    
    print(f"Concepts analyzed: {concepts}")
    print(f"Categories applied: {[c.value for c in active_categories]}")
    print(f"Mathematical coherence: {math_result.mathematical_coherence:.3f}")
    
    # Show category analyses
    print("\nCategory Analyses:")
    for analysis in math_result.category_analyses:
        print(f"\n  [{analysis.category.value}]")
        print(f"  Confidence: {analysis.confidence:.2f}")
        print(f"  Theorems applied: {len(analysis.theorems_applied)}")
        if analysis.theorems_applied:
            for theorem in analysis.theorems_applied[:2]:
                print(f"    - {theorem}")
    
    # Show formal verification
    print("\nFormal Verification:")
    for prop, verified in math_result.formal_verification.items():
        status = "✓" if verified else "✗"
        print(f"  {status} {prop}: {verified}")


def demonstrate_unified_synthesis():
    """Demonstrate complete unified reasoning with synthesis"""
    print_separator("UNIFIED SYNTHESIS: PXL + IEL + MATH")
    
    engine = get_unified_engine()
    
    # Complex philosophical-mathematical concepts
    concepts = ["consistency", "completeness", "truth"]
    
    # Create context
    context = PXLReasoningContext(
        mode=ReasoningMode.SYNTHETIC,  # Synthesis mode
        trinity_vector=TrinityVector(0.8, 0.8, 0.9),
        modal_properties=ModalProperties(necessary=True)
    )
    
    # Execute unified reasoning with full synthesis
    result = engine.reason(
        concepts=concepts,
        context=context,
        enable_synthesis=True
    )
    
    print(f"Concepts analyzed: {concepts}")
    print(f"Overall confidence: {result.overall_confidence:.3f}")
    print(f"Trinity coherence: E={result.trinity_coherence.essence:.2f}, "
          f"G={result.trinity_coherence.generation:.2f}, "
          f"T={result.trinity_coherence.temporal:.2f}")
    
    # Show cross-domain syntheses
    print(f"\n{len(result.cross_domain_syntheses)} Cross-Domain Syntheses:")
    for i, synthesis in enumerate(result.cross_domain_syntheses[:3], 1):
        print(f"\n  Synthesis {i}:")
        print(f"  IEL Domain: {synthesis.iel_domain.value}")
        print(f"  Math Category: {synthesis.math_category.value}")
        print(f"  Synergy Score: {synthesis.synergy_score:.3f}")
        print(f"  Amplified Insights:")
        for insight in synthesis.amplified_insights[:2]:
            print(f"    - {insight}")
    
    # Show key insights
    print(f"\nKey Insights ({len(result.key_insights)}):")
    for insight in result.key_insights[:5]:
        print(f"  • {insight}")
    
    # Show recommendations
    print(f"\nRecommended Actions:")
    for action in result.recommended_actions[:3]:
        print(f"  → {action}")


def demonstrate_iel_math_mapping():
    """Demonstrate IEL-Math category mapping"""
    print_separator("IEL-MATH CATEGORY MAPPING")
    
    print("IEL Domain → Math Categories:")
    print("-" * 70)
    for iel, maths in IEL_MATH_MAPPING.items():
        print(f"\n{iel.value}:")
        for math in maths:
            print(f"  → {math.value}")
    
    print("\n")
    print("Math Category → IEL Domains:")
    print("-" * 70)
    for math, iels in MATH_IEL_MAPPING.items():
        if iels:  # Only show if mapped
            print(f"\n{math.value}:")
            for iel in iels:
                print(f"  ← {iel.value}")


def demonstrate_statistics():
    """Show engine statistics"""
    print_separator("ENGINE STATISTICS")
    
    engine = get_unified_engine()
    stats = engine.get_statistics()
    
    print("Unified Engine:")
    print(f"  Total operations: {stats['unified_operations']}")
    print(f"  Synthesis operations: {stats['synthesis_operations']}")
    
    print("\nPXL Engine:")
    pxl_stats = stats['pxl_stats']
    print(f"  Reasoning operations: {pxl_stats['reasoning_operations']}")
    print(f"  Cache hit rate: {pxl_stats['cache_hit_rate']:.2%}")
    print(f"  Registered concepts: {pxl_stats['registered_concepts']}")
    
    print("\nIEL Engine:")
    print(f"  Available domains: {stats['available_iel_domains']}")
    
    print("\nMath Engine:")
    print(f"  Available categories: {stats['available_math_categories']}")


def main():
    """Main demonstration"""
    print("\n" + "=" * 70)
    print("  LOGOS UNIFIED REASONING ENGINE - DEMONSTRATION")
    print("  PXL Substrate + IEL Domains + Math Categories")
    print("=" * 70)
    
    # Run demonstrations
    demonstrate_pxl_substrate()
    demonstrate_iel_domains()
    demonstrate_math_categories()
    demonstrate_unified_synthesis()
    demonstrate_iel_math_mapping()
    demonstrate_statistics()
    
    print_separator("DEMONSTRATION COMPLETE")
    print("The unified reasoning engine successfully integrates:")
    print("  1. PXL substrate for foundational logic")
    print("  2. IEL domains for philosophical reasoning")
    print("  3. Math categories for formal verification")
    print("  4. Cross-domain synthesis for amplified insights")
    print("\nAll components are Trinity-grounded and coherence-validated.")
    print()


if __name__ == "__main__":
    main()
