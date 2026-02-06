from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class LambdaVar:
    name: str
    var_type: str

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "var", "name": self.name, "var_type": self.var_type}


@dataclass
class LambdaValue:
    value: str
    value_type: str

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "value", "value": self.value, "value_type": self.value_type}


@dataclass
class LambdaAbstraction:
    var: LambdaVar
    body: Any

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "lambda", "var": self.var.to_dict(), "body": _to_dict(self.body)}


@dataclass
class LambdaApplication:
    func: Any
    arg: Any

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "app", "func": _to_dict(self.func), "arg": _to_dict(self.arg)}


@dataclass
class SufficientReason:
    source_type: str
    target_type: str
    value: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "sr",
            "source_type": self.source_type,
            "target_type": self.target_type,
            "value": self.value,
        }


def _to_dict(expr: Any) -> Dict[str, Any]:
    if hasattr(expr, "to_dict"):
        return expr.to_dict()
    return {"type": "raw", "value": str(expr)}


class LambdaCalculusEngine:
    def __init__(self) -> None:
        self.env: Dict[str, Any] = {}

    def ready(self) -> bool:
        return True

    def create_variable(self, name: str, var_type: str) -> LambdaVar:
        return LambdaVar(name=name, var_type=var_type)

    def create_value(self, value: str, value_type: str) -> LambdaValue:
        return LambdaValue(value=value, value_type=value_type)

    def create_lambda(self, var: LambdaVar, body: Any) -> LambdaAbstraction:
        return LambdaAbstraction(var=var, body=body)

    def create_application(self, func: Any, arg: Any) -> LambdaApplication:
        return LambdaApplication(func=func, arg=arg)

    def create_sufficient_reason(self, source_type: str, target_type: str, value: int) -> SufficientReason:
        return SufficientReason(source_type=source_type, target_type=target_type, value=value)

    def evaluate(self, expr: Any) -> Any:
        if isinstance(expr, LambdaApplication) and isinstance(expr.func, LambdaAbstraction):
            return self._substitute(expr.func.body, expr.func.var.name, expr.arg)
        return expr

    def _substitute(self, expr: Any, var_name: str, value: Any) -> Any:
        if isinstance(expr, LambdaVar) and expr.name == var_name:
            return value
        if isinstance(expr, LambdaApplication):
            return LambdaApplication(
                func=self._substitute(expr.func, var_name, value),
                arg=self._substitute(expr.arg, var_name, value),
            )
        if isinstance(expr, LambdaAbstraction):
            if expr.var.name == var_name:
                return expr
            return LambdaAbstraction(expr.var, self._substitute(expr.body, var_name, value))
        return expr
