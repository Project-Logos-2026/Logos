
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
        if artifact.get("proof_state") == "complete":
            artifact["epistemic_state"] = "canonical_candidate"
        else:
            artifact["epistemic_state"] = "provisional"
        artifact["reasoning_steps_used"] = self.steps
        return artifact
