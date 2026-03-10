from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PromotionEvaluation:
    eligible: bool
    current_state: Optional[str]
    target_state: str
    missing_requirements: List[str]
    aa_summary: Dict[str, int]
    conflicts: List[str]
    emp_proof_available: bool

class PromotionEvaluator:
    def __init__(self, uwm_read):
        self.uwm_read = uwm_read

    def evaluate_for_provisional(self, smp_id: str) -> PromotionEvaluation:
        smp = self.uwm_read.get_smp(smp_id, requester_role="logos_agent")
        missing = []
        aa_summary = {}
        conflicts = []
        if not smp:
            return PromotionEvaluation(False, None, "provisional", ["SMP not found"], {}, [], False)
        if smp.header.classification_state != "conditional":
            missing.append("Not conditional state")
        aas = self.uwm_read.get_aas_for_smp(smp_id, requester_role="logos_agent")
        if not aas or len(aas) == 0:
            missing.append("No AA present")
        for aa in aas:
            aa_summary[aa.aa_type] = aa_summary.get(aa.aa_type, 0) + 1
            if aa.aa_type == "ConflictAA":
                conflicts.append(aa.aa_id)
        eligible = len(missing) == 0 and len(conflicts) == 0
        return PromotionEvaluation(eligible, smp.header.classification_state, "provisional", missing, aa_summary, conflicts, False)

    def evaluate_for_canonical(self, smp_id: str) -> PromotionEvaluation:
        from logos.imports.protocols import validate_promotion_boundary
        smp = self.uwm_read.get_smp(smp_id, requester_role="logos_agent")
        missing = []
        aa_summary = {}
        conflicts = []
        if not smp:
            return PromotionEvaluation(False, None, "canonical", ["SMP not found"], {}, [], False)
        validate_promotion_boundary(smp.header.classification_state, "canonical")
        if smp.header.classification_state != "provisional":
            missing.append("Not provisional state")
        aas = self.uwm_read.get_aas_for_smp(smp_id, requester_role="logos_agent")
        types_needed = ["I1AA", "I2AA", "I3AA"]
        for t in types_needed:
            if not any(aa.aa_type == t for aa in aas):
                missing.append(f"Missing {t}")
        for aa in aas:
            aa_summary[aa.aa_type] = aa_summary.get(aa.aa_type, 0) + 1
            if aa.aa_type == "ConflictAA":
                conflicts.append(aa.aa_id)
        eligible = len(missing) == 0 and len(conflicts) == 0
        return PromotionEvaluation(eligible, smp.header.classification_state, "canonical", missing, aa_summary, conflicts, False)
