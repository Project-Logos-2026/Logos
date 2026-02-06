from __future__ import annotations

from typing import Any, Dict

from ...ARP_Tools.reasoning_engines.mathematical.lambda_calculus_engine import LambdaCalculusEngine
from ...ARP_Tools.reasoning_engines.mathematical.symbolic_arithmetic_engine import SymbolicArithmeticEngine
from ...ARP_Tools.reasoning_engines.mathematical.optimization_engine import OptimizationEngine


class MathematicalReasoner:
    def __init__(self) -> None:
        self.lambda_engine = LambdaCalculusEngine()
        self.symbolic_engine = SymbolicArithmeticEngine()
        self.optimizer = OptimizationEngine()

    def analyze(self, packet: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        expr = packet.get("expression") or context.get("expression")
        symbolic = None
        if expr:
            symbolic = self.symbolic_engine.simplify(expr)

        optimization = None
        objective = packet.get("objective") or context.get("objective")
        if callable(objective):
            optimization = self.optimizer.optimize(objective, context.get("initial_guess", 0.0))

        return {
            "engine": "mathematical",
            "symbolic": symbolic,
            "optimization": optimization,
            "lambda_ready": self.lambda_engine.ready(),
        }
