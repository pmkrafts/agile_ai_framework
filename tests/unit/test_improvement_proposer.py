"""Unit tests for improvement proposer."""

from src.learning.gap_analyzer import GapAnalyzer
from src.core.feedback import FeedbackCategory, FeedbackEvent, FeedbackEventType, FeedbackSeverity
from src.learning.improvement_proposer import ImprovementProposer


def test_generate_skill_proposal():
    """Test generating a skill improvement proposal."""
    proposer = ImprovementProposer()
    gap = GapAnalyzer(min_occurrences=1).analyze([
        FeedbackEvent(
            sprint_id="S-001",
            agent_type="coder_agent",
            task_id="T-001",
            event_type=FeedbackEventType.FAILURE,
            category=FeedbackCategory.SKILL,
            severity=FeedbackSeverity.HIGH,
            description="Auth pattern fails",
        ),
    ])[0]

    proposal = proposer._generate_for_gap(gap)
    assert proposal is not None
    assert proposal.category == FeedbackCategory.SKILL
    assert "coder" in proposal.target_file
    assert proposal.confidence > 0


def test_generate_proposals():
    """Test generating multiple proposals."""
    proposer = ImprovementProposer()
    gaps = [
        GapAnalyzer(min_occurrences=1).analyze([
            FeedbackEvent(
                sprint_id="S-001",
                agent_type="coder_agent",
                task_id="T-001",
                event_type=FeedbackEventType.FAILURE,
                category=FeedbackCategory.SKILL,
                severity=FeedbackSeverity.HIGH,
                description="Auth pattern fails",
            ),
        ])[0]
    ]
    proposals = proposer.generate_proposals(gaps, max_proposals=1)
    assert len(proposals) == 1
