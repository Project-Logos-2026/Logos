from __future__ import annotations

from typing import Any, Dict, Optional

from .aggregator import aggregate_results
from .bayesian_dispatcher import run_bayesian_dispatch
from .external_analysis import run_external_analysis


class ARNOrchestrator:
    def run(self, payload: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        bayes = run_bayesian_dispatch(payload, context)
        external = run_external_analysis(payload, context)
        return aggregate_results(bayes, external)
