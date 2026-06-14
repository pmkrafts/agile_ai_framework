"""Unit tests for cost tracker."""

from src.monitoring.cost_tracker import CostTracker, TokenUsage


def test_cost_tracker_records_usage():
    """Test that cost tracker records usage."""
    tracker = CostTracker(sprint_budget_usd=100.0)
    tracker.record_usage(TokenUsage("kimi", "kimi-k2-6-latest", 1000, 500, 0.01))
    assert tracker.total_cost == 0.01


def test_cost_tracker_summary():
    """Test cost tracker summary."""
    tracker = CostTracker(sprint_budget_usd=100.0)
    tracker.record_usage(TokenUsage("kimi", "kimi-k2-6-latest", 10000, 5000, 0.075))
    summary = tracker.get_summary()
    assert summary["total_cost_usd"] == 0.075
    assert summary["budget_usd"] == 100.0
    assert "kimi/kimi-k2-6-latest" in summary["by_provider"]


def test_cost_tracker_budget_exceeded():
    """Test budget exceeded detection."""
    tracker = CostTracker(sprint_budget_usd=1.0)
    tracker.record_usage(TokenUsage("kimi", "kimi-k2-6-latest", 1000, 1000, 1.5))
    assert tracker.total_cost > tracker.sprint_budget_usd
