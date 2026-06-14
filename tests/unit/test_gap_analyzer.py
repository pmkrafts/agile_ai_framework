"""Unit tests for gap analyzer."""

from src.core.feedback import FeedbackCategory, FeedbackEvent, FeedbackEventType, FeedbackSeverity
from src.learning.gap_analyzer import GapAnalyzer


def test_analyze_recurring_pattern():
    """Test gap analyzer identifies recurring patterns."""
    analyzer = GapAnalyzer(min_occurrences=1)
    events = [
        FeedbackEvent(
            sprint_id="S-001",
            agent_type="coder_agent",
            task_id="T-001",
            event_type=FeedbackEventType.FAILURE,
            category=FeedbackCategory.SKILL,
            severity=FeedbackSeverity.HIGH,
            description="Auth pattern fails",
        ),
        FeedbackEvent(
            sprint_id="S-001",
            agent_type="coder_agent",
            task_id="T-002",
            event_type=FeedbackEventType.FAILURE,
            category=FeedbackCategory.SKILL,
            severity=FeedbackSeverity.HIGH,
            description="Auth pattern fails again",
        ),
    ]
    patterns = analyzer.analyze(events)
    assert len(patterns) == 1
    assert patterns[0].agent_type == "coder_agent"
    assert patterns[0].occurrence_count == 2


def test_compare_to_baseline():
    """Test comparing current KPIs to baseline."""
    analyzer = GapAnalyzer()
    current = {"story_completion_rate": 60, "test_pass_rate": 75}
    baseline = {"story_completion_rate": 75, "test_pass_rate": 80}
    gaps = analyzer.compare_to_baseline(current, baseline)
    assert len(gaps) == 2
    assert any("story_completion_rate" in gap.description for gap in gaps)
