"""
Radial_Genesis_Engine - Hysteresis_Governor (Phase 5)
Implements deterministic, fail-closed hysteresis gating for configuration selection.
Conforms to Phase_5_Hysteresis_Formalization.md.

No mutation of Runtime_Spine. No identity rebinding. Deterministic only.
"""

from typing import Optional

class Hysteresis_Governor:
    def __init__(self, theta: float = 0.0, tau_min: int = 1):
        self.theta = theta
        self.tau_min = tau_min
        self.omega_prev: Optional[str] = None
        self.t_last: Optional[int] = None

    def evaluate(
        self,
        candidate_id: str,
        candidate_score: float,
        prev_id: Optional[str],
        prev_score: Optional[float],
        tick: int,
        A_t: bool,
        override_type: Optional[str]
    ) -> str:
        trace = []
        epsilon_tie = 1e-9
        # 0. Override
        if override_type is not None:
            trace.append(f"Override active: {override_type} → {candidate_id}")
            self.omega_prev = candidate_id
            self.t_last = tick
            print("; ".join(trace))
            return candidate_id
        # 1. Mode Authorization
        if not A_t:
            trace.append("Mode not authorized → fail closed")
            print("; ".join(trace))
            return prev_id if prev_id is not None else candidate_id
        # 2. Cold Start
        if prev_id is None or prev_score is None or self.omega_prev is None or self.t_last is None:
            trace.append("Cold start → select candidate")
            self.omega_prev = candidate_id
            self.t_last = tick
            print("; ".join(trace))
            return candidate_id
        # 3. Tie Stickiness
        score_diff = abs(candidate_score - prev_score)
        if score_diff < epsilon_tie:
            chosen = min(candidate_id, prev_id)
            trace.append(f"Tie detected (|Δ|={score_diff}) → lex min: {chosen}")
            self.omega_prev = chosen
            self.t_last = tick if chosen != prev_id else self.t_last
            print("; ".join(trace))
            return chosen
        # 4. Minimum Dwell
        dwell = tick - self.t_last
        if dwell < self.tau_min:
            trace.append(f"Dwell {dwell} < τ_min {self.tau_min} → stick prev: {prev_id}")
            print("; ".join(trace))
            return prev_id
        # 5. Improvement Threshold
        if candidate_score < prev_score - self.theta:
            trace.append(f"Improvement {prev_score-candidate_score} > θ {self.theta} → select candidate: {candidate_id}")
            self.omega_prev = candidate_id
            self.t_last = tick
            print("; ".join(trace))
            return candidate_id
        trace.append(f"No gate passed → stick prev: {prev_id}")
        print("; ".join(trace))
        return prev_id
