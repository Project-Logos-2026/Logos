
class ReasoningBudgetExceeded(Exception): pass

class EMP_Meta_Reasoner:
    def __init__(self, budget):
        self.budget = budget
        self.steps = 0

    def _use(self, n=1):
        self.steps += n
        if self.steps > self.budget:
            raise ReasoningBudgetExceeded()

    def analyze(self, artifact):
        self._use()
        # Return a new dict to avoid mutating the caller's artifact.
        # Mutation of shared state violates the immutability governance invariant.
        result = dict(artifact)
        if result.get("proof_state") == "complete":
            result["epistemic_state"] = "canonical_candidate"
        else:
            result["epistemic_state"] = "provisional"
        result["reasoning_steps_used"] = self.steps
        return result
