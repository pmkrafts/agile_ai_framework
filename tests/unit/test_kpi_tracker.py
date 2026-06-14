"""Unit tests for KPI tracker."""

from src.monitoring.kpi_tracker import KPITracker, SprintKPIs


def test_kpi_tracker_records_sprint():
    """Test recording sprint KPIs."""
    tracker = KPITracker()
    kpis = SprintKPIs(
        sprint_id="S-001",
        stories_planned=8,
        stories_completed=7,
        tests_total=20,
        tests_passed=19,
        total_cost_usd=50.0,
    )
    tracker.record_sprint(kpis)
    assert tracker.get_latest().sprint_id == "S-001"


def test_kpi_dashboard_summary():
    """Test dashboard summary generation."""
    tracker = KPITracker()
    kpis = SprintKPIs(
        sprint_id="S-001",
        stories_planned=8,
        stories_completed=7,
        tests_total=20,
        tests_passed=19,
        total_cost_usd=50.0,
    )
    tracker.record_sprint(kpis)
    summary = tracker.dashboard_summary()
    assert summary["sprint_count"] == 1
    assert summary["latest"]["sprint_id"] == "S-001"
