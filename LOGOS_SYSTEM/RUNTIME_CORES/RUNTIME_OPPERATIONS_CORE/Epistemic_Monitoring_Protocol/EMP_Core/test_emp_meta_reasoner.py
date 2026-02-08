"""Tests for EMP_Meta_Reasoner immutability and budget enforcement."""

import sys
from pathlib import Path

import pytest

# Ensure the module is importable regardless of working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from EMP_Meta_Reasoner import EMP_Meta_Reasoner, ReasoningBudgetExceeded


class TestAnalyzeDoesNotMutateInput:
    """analyze() must return a new dict, leaving the original untouched."""

    def test_original_artifact_unchanged(self):
        reasoner = EMP_Meta_Reasoner(budget=10)
        artifact = {"proof_state": "complete", "data": "preserved"}
        result = reasoner.analyze(artifact)

        # The returned dict should carry the enrichment fields.
        assert result["epistemic_state"] == "canonical_candidate"
        assert "reasoning_steps_used" in result

        # The original must NOT have been mutated.
        assert "epistemic_state" not in artifact
        assert "reasoning_steps_used" not in artifact
        # Pre-existing keys must survive in the copy.
        assert result["data"] == "preserved"

    def test_provisional_state_for_incomplete_proof(self):
        reasoner = EMP_Meta_Reasoner(budget=10)
        artifact = {"proof_state": "incomplete"}
        result = reasoner.analyze(artifact)

        assert result["epistemic_state"] == "provisional"
        assert "epistemic_state" not in artifact

    def test_missing_proof_state_defaults_to_provisional(self):
        reasoner = EMP_Meta_Reasoner(budget=10)
        artifact = {"some_key": "value"}
        result = reasoner.analyze(artifact)

        assert result["epistemic_state"] == "provisional"


class TestReasoningBudget:
    """Budget enforcement must halt analysis when exceeded."""

    def test_budget_exceeded_raises(self):
        reasoner = EMP_Meta_Reasoner(budget=2)
        reasoner.analyze({"proof_state": "incomplete"})
        reasoner.analyze({"proof_state": "incomplete"})
        with pytest.raises(ReasoningBudgetExceeded):
            reasoner.analyze({"proof_state": "incomplete"})

    def test_steps_tracked_correctly(self):
        reasoner = EMP_Meta_Reasoner(budget=5)
        result = reasoner.analyze({"proof_state": "complete"})
        assert result["reasoning_steps_used"] == 1
        result2 = reasoner.analyze({"proof_state": "complete"})
        assert result2["reasoning_steps_used"] == 2
