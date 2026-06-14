"""Unit tests for validation runner."""

import pytest

from src.learning.improvement_proposer import ImprovementProposer
from src.core.feedback import FeedbackCategory, GapPattern, ImprovementProposal
from src.learning.validation_runner import ValidationRunner


@pytest.mark.asyncio
async def test_validate_proposal():
    """Test validating a proposal."""
    runner = ValidationRunner()
    proposal = ImprovementProposal(
        target_file=".pi/agent/skills/coder-agent.md",
        category=FeedbackCategory.SKILL,
        rationale="Test",
        current_state="...",
        proposed_change="...",
        confidence=0.9,
    )
    baseline = {
        "delivery": {
            "story_completion_rate": 75,
            "first_build_success_rate": 65,
            "test_pass_rate": 80,
            "coverage_percent": 80,
        },
        "economic": {"cost_per_story": 10},
    }
    result = await runner.validate(proposal, baseline)
    assert result.proposal_id == proposal.proposal_id
    assert "after_kpis" in result.model_dump()
