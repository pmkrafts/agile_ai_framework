"""Integration tests for self-learning loop."""

import pytest

from src.learning.models import LearningLoopConfig
from src.learning.self_learning_loop import SelfLearningLoop


@pytest.mark.asyncio
async def test_self_learning_loop_runs():
    """Test that the self-learning loop runs end-to-end."""
    loop = SelfLearningLoop(
        config=LearningLoopConfig(
            max_iterations=2,
            budget_usd=5.0,
            auto_approve_low_risk=True,
        )
    )

    context = {
        "problem_statement": "Build a simple task management API",
        "interview_answers": {"Target user": "Internal teams"},
        "capacity": {"coder_agent": 2, "tester_agent": 1, "reviewer_agent": 1},
        "target": "staging",
        "code_reference": "test",
    }

    result = await loop.run_full_pipeline(context, cto_approver="cto@company.com")
    assert result["status"] == "complete"
    assert "iterations" in result
    assert "applied_proposals" in result
    assert "rolled_back_proposals" in result
