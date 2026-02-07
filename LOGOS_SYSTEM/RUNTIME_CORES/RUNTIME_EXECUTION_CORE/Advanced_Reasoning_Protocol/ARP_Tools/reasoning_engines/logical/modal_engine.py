# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: modal_engine
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Tools/reasoning_engines/logical/modal_engine.py.
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Advanced_Reasoning_Protocol/ARP_Tools/reasoning_engines/logical/modal_engine.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class ModalOperator(Enum):
    NECESSITY = "NECESSITY"
    POSSIBILITY = "POSSIBILITY"
    KNOWLEDGE = "KNOWLEDGE"
    BELIEF = "BELIEF"
    OBLIGATION = "OBLIGATION"
    PERMISSION = "PERMISSION"
    TEMPORAL_ALWAYS = "TEMPORAL_ALWAYS"
    TEMPORAL_EVENTUALLY = "TEMPORAL_EVENTUALLY"


class LogicalConnective(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    IMPLIES = "IMPLIES"
    BICONDITIONAL = "BICONDITIONAL"


@dataclass
class World:
    world_id: str
    propositions: Set[str] = field(default_factory=set)

    def satisfies(self, proposition: str) -> bool:
        return proposition in self.propositions


@dataclass
class ModalFormula:
    operator: Optional[ModalOperator]
    content: Union[str, "ModalFormula", List["ModalFormula"]]
    connective: Optional[LogicalConnective] = None


@dataclass
class KripkeModel:
    worlds: Dict[str, World]
    accessibility: Dict[Tuple[str, str], bool]
    current_world: str

    def is_accessible(self, from_world: str, to_world: str) -> bool:
        return self.accessibility.get((from_world, to_world), False)

    def accessible_worlds(self, from_world: str) -> List[str]:
        return [w for w in self.worlds if self.is_accessible(from_world, w)]


@dataclass
class ModalValidationResult:
    is_valid: bool
    truth_value: bool
    satisfaction_worlds: List[str]
    countermodel_worlds: List[str]
    reasoning_trace: List[str]
    confidence: float


class ModalLogicEngine:
    def __init__(self) -> None:
        self.default_model = self._create_default_model()

    def validate_modal_formula(
        self,
        formula: Union[str, ModalFormula],
        model: Optional[KripkeModel] = None,
        world: Optional[str] = None,
    ) -> ModalValidationResult:
        model = model or self.default_model
        world = world or model.current_world
        if isinstance(formula, str):
            formula = self._parse_formula(formula)

        trace: List[str] = []
        truth_value, satisfaction_worlds = self._evaluate_formula(formula, model, world, trace)
        countermodel_worlds = [w for w in model.worlds if w not in satisfaction_worlds]
        confidence = 0.6 if truth_value else 0.4
        return ModalValidationResult(
            is_valid=True,
            truth_value=truth_value,
            satisfaction_worlds=satisfaction_worlds,
            countermodel_worlds=countermodel_worlds,
            reasoning_trace=trace,
            confidence=confidence,
        )

    def _create_default_model(self) -> KripkeModel:
        worlds = {
            "w0": World("w0", {"actual", "existent"}),
            "w1": World("w1", {"possible"}),
            "w2": World("w2", {"possible", "alternative"}),
        }
        accessibility = {(w1, w2): True for w1 in worlds for w2 in worlds}
        return KripkeModel(worlds=worlds, accessibility=accessibility, current_world="w0")

    def _parse_formula(self, formula_str: str) -> ModalFormula:
        text = formula_str.strip()

        if text.startswith("[]"):
            return ModalFormula(ModalOperator.NECESSITY, text[2:].strip())
        if text.startswith("<>"):
            return ModalFormula(ModalOperator.POSSIBILITY, text[2:].strip())
        if text.startswith("K:"):
            return ModalFormula(ModalOperator.KNOWLEDGE, text[2:].strip())
        if text.startswith("B:"):
            return ModalFormula(ModalOperator.BELIEF, text[2:].strip())
        if text.startswith("O:"):
            return ModalFormula(ModalOperator.OBLIGATION, text[2:].strip())
        if text.startswith("P:"):
            return ModalFormula(ModalOperator.PERMISSION, text[2:].strip())
        if text.startswith("G:"):
            return ModalFormula(ModalOperator.TEMPORAL_ALWAYS, text[2:].strip())
        if text.startswith("F:"):
            return ModalFormula(ModalOperator.TEMPORAL_EVENTUALLY, text[2:].strip())

        if "<->" in text:
            left, right = [part.strip() for part in text.split("<->", 1)]
            return ModalFormula(None, [self._parse_formula(left), self._parse_formula(right)], LogicalConnective.BICONDITIONAL)
        if "->" in text:
            left, right = [part.strip() for part in text.split("->", 1)]
            return ModalFormula(None, [self._parse_formula(left), self._parse_formula(right)], LogicalConnective.IMPLIES)
        if " and " in text:
            left, right = [part.strip() for part in text.split(" and ", 1)]
            return ModalFormula(None, [self._parse_formula(left), self._parse_formula(right)], LogicalConnective.AND)
        if " or " in text:
            left, right = [part.strip() for part in text.split(" or ", 1)]
            return ModalFormula(None, [self._parse_formula(left), self._parse_formula(right)], LogicalConnective.OR)
        if text.startswith("not "):
            return ModalFormula(None, self._parse_formula(text[4:].strip()), LogicalConnective.NOT)

        return ModalFormula(None, text)

    def _evaluate_formula(
        self,
        formula: ModalFormula,
        model: KripkeModel,
        world: str,
        trace: List[str],
    ) -> Tuple[bool, List[str]]:
        if formula.connective == LogicalConnective.NOT:
            inner = formula.content if isinstance(formula.content, ModalFormula) else ModalFormula(None, formula.content)
            value, worlds = self._evaluate_formula(inner, model, world, trace)
            return (not value), [w for w in model.worlds if w not in worlds]

        if formula.connective == LogicalConnective.AND:
            left, right = formula.content
            left_value, left_worlds = self._evaluate_formula(left, model, world, trace)
            right_value, right_worlds = self._evaluate_formula(right, model, world, trace)
            return left_value and right_value, list(set(left_worlds).intersection(right_worlds))

        if formula.connective == LogicalConnective.OR:
            left, right = formula.content
            left_value, left_worlds = self._evaluate_formula(left, model, world, trace)
            right_value, right_worlds = self._evaluate_formula(right, model, world, trace)
            return left_value or right_value, list(set(left_worlds).union(right_worlds))

        if formula.connective == LogicalConnective.IMPLIES:
            left, right = formula.content
            left_value, _ = self._evaluate_formula(left, model, world, trace)
            right_value, right_worlds = self._evaluate_formula(right, model, world, trace)
            return (not left_value) or right_value, right_worlds

        if formula.connective == LogicalConnective.BICONDITIONAL:
            left, right = formula.content
            left_value, left_worlds = self._evaluate_formula(left, model, world, trace)
            right_value, right_worlds = self._evaluate_formula(right, model, world, trace)
            value = (left_value and right_value) or (not left_value and not right_value)
            return value, list(set(left_worlds).intersection(right_worlds))

        if formula.operator is None:
            proposition = str(formula.content)
            satisfied = [w for w, obj in model.worlds.items() if obj.satisfies(proposition)]
            trace.append(f"Proposition '{proposition}' satisfied in {satisfied}")
            return (world in satisfied), satisfied

        accessible = model.accessible_worlds(world)
        if formula.operator in {ModalOperator.NECESSITY, ModalOperator.KNOWLEDGE, ModalOperator.OBLIGATION, ModalOperator.TEMPORAL_ALWAYS}:
            satisfied = []
            for w in accessible:
                value, _ = self._evaluate_formula(ModalFormula(None, formula.content), model, w, trace)
                if value:
                    satisfied.append(w)
            return (len(satisfied) == len(accessible)), satisfied

        if formula.operator in {ModalOperator.POSSIBILITY, ModalOperator.BELIEF, ModalOperator.PERMISSION, ModalOperator.TEMPORAL_EVENTUALLY}:
            satisfied = []
            for w in accessible:
                value, _ = self._evaluate_formula(ModalFormula(None, formula.content), model, w, trace)
                if value:
                    satisfied.append(w)
            return (len(satisfied) > 0), satisfied

        return False, []


class ModalEngine:
    def __init__(self) -> None:
        self.engine = ModalLogicEngine()

    def analyze(self, statement: str, operator: str = "possible") -> Dict[str, Any]:
        operator_map = {
            "necessary": "[]",
            "possible": "<>",
            "knowledge": "K:",
            "belief": "B:",
            "obligation": "O:",
            "permission": "P:",
            "always": "G:",
            "eventually": "F:",
        }
        prefix = operator_map.get(operator.lower().strip(), "<>")
        formula = f"{prefix}{statement}"
        result = self.engine.validate_modal_formula(formula)
        return {
            "engine": "modal",
            "statement": statement,
            "operator": operator,
            "valid": result.is_valid,
            "truth_value": result.truth_value,
            "confidence": result.confidence,
        }
