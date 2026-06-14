"""Unit tests for feedback collector."""

from src.core.feedback import FeedbackEventType
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, SprintState, TaskStatus
from src.learning.feedback_collector import FeedbackCollector


def test_collect_from_task_failure():
    """Test collecting feedback from a failed task."""
    collector = FeedbackCollector(storage_dir="data/test_feedback")
    task = AgentTask(
        task_id="T-001",
        story_id="US-001",
        title="Test task",
        agent_type="coder_agent",
        status=TaskStatus.FAILED,
        blockers=["API unavailable"],
    )
    events = collector._collect_from_task(task, "S-001")
    assert len(events) == 1
    assert events[0].event_type == FeedbackEventType.FAILURE
    assert events[0].agent_type == "coder_agent"


def test_collect_from_agent_message_escalation():
    """Test collecting feedback from an escalation message."""
    collector = FeedbackCollector(storage_dir="data/test_feedback")
    msg = AgentMessage(
        from_agent="coder_agent:001",
        to_agent="cto",
        message_type=MessageType.ESCALATION,
        payload={
            "task_id": "T-001",
            "content": "Stuck on API integration",
            "blockers": ["API returns 500"],
            "confidence": 0.5,
        },
    )
    events = collector.collect_from_agent_message(msg, "S-001")
    assert len(events) == 2  # escalation + low confidence
    assert events[0].event_type == FeedbackEventType.ESCALATION


def test_collect_from_sprint():
    """Test collecting feedback from a sprint state."""
    collector = FeedbackCollector(storage_dir="data/test_feedback")
    state = SprintState(sprint_id="S-001", project_id="P-001")
    state.tasks.append(
        AgentTask(
            task_id="T-001",
            story_id="US-001",
            title="Test",
            agent_type="coder_agent",
            status=TaskStatus.COMPLETE,
            confidence=0.75,
        )
    )

    cost_data = {"total_cost_usd": 50, "budget_usd": 100, "utilization": 0.5}
    kpi_data = {"latest": {"delivery": {"story_completion_rate": 80, "test_pass_rate": 85}}}

    events = collector.collect_from_sprint(state, cost_data, kpi_data)
    assert len(events) >= 1
    assert events[0].sprint_id == "S-001"
