"""KPI tracking and dashboards."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SprintKPIs:
    """KPIs for a single sprint."""

    sprint_id: str
    stories_planned: int = 0
    stories_completed: int = 0
    stories_rejected: int = 0
    builds_total: int = 0
    builds_success_first_attempt: int = 0
    tests_total: int = 0
    tests_passed: int = 0
    coverage_percent: float = 0.0
    defects_production: int = 0
    escalations: int = 0
    total_cost_usd: float = 0.0
    cto_hours: float = 0.0
    client_satisfaction: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def story_completion_rate(self) -> float:
        if self.stories_planned == 0:
            return 0.0
        return self.stories_completed / self.stories_planned * 100

    @property
    def first_build_success_rate(self) -> float:
        if self.builds_total == 0:
            return 0.0
        return self.builds_success_first_attempt / self.builds_total * 100

    @property
    def test_pass_rate(self) -> float:
        if self.tests_total == 0:
            return 0.0
        return self.tests_passed / self.tests_total * 100

    @property
    def defect_escape_rate(self) -> float:
        if self.stories_completed == 0:
            return 0.0
        return self.defects_production / self.stories_completed

    @property
    def cost_per_story(self) -> float:
        if self.stories_completed == 0:
            return 0.0
        return self.total_cost_usd / self.stories_completed

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SprintKPIs:
        """Create SprintKPIs from a dictionary."""
        return cls(
            sprint_id=data.get("sprint_id", "unknown"),
            timestamp=data.get("timestamp"),
            stories_planned=data.get("stories_planned", 0),
            stories_completed=data.get("stories_completed", 0),
            stories_rejected=data.get("stories_rejected", 0),
            builds_total=data.get("builds_total", 0),
            builds_success_first_attempt=data.get("builds_success_first_attempt", 0),
            tests_total=data.get("tests_total", 0),
            tests_passed=data.get("tests_passed", 0),
            coverage_percent=data.get("coverage_percent", 0),
            defects_production=data.get("defects_production", 0),
            escalations=data.get("escalations", 0),
            total_cost_usd=data.get("total_cost_usd", 0),
            cto_hours=data.get("cto_hours", 0),
            client_satisfaction=data.get("client_satisfaction", 0),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "sprint_id": self.sprint_id,
            "timestamp": self.timestamp,
            "stories_planned": self.stories_planned,
            "stories_completed": self.stories_completed,
            "stories_rejected": self.stories_rejected,
            "builds_total": self.builds_total,
            "builds_success_first_attempt": self.builds_success_first_attempt,
            "tests_total": self.tests_total,
            "tests_passed": self.tests_passed,
            "coverage_percent": self.coverage_percent,
            "defects_production": self.defects_production,
            "escalations": self.escalations,
            "total_cost_usd": round(self.total_cost_usd, 2),
            "cto_hours": self.cto_hours,
            "client_satisfaction": self.client_satisfaction,
            "delivery": {
                "story_completion_rate": round(self.story_completion_rate, 2),
                "first_build_success_rate": round(self.first_build_success_rate, 2),
                "test_pass_rate": round(self.test_pass_rate, 2),
                "coverage_percent": round(self.coverage_percent, 2),
                "defect_escape_rate": round(self.defect_escape_rate, 4),
            },
            "economic": {
                "cost_per_story": round(self.cost_per_story, 2),
            },
            "operational": {
                "cto_hours": self.cto_hours,
            },
            "strategic": {
                "client_satisfaction": self.client_satisfaction,
            },
        }


class KPITracker:
    """Tracks KPIs across sprints."""

    def __init__(self):
        self.sprints: list[SprintKPIs] = []

    def record_sprint(self, kpis: SprintKPIs) -> None:
        """Record sprint KPIs."""
        self.sprints.append(kpis)

    def get_latest(self) -> SprintKPIs | None:
        """Get the latest sprint KPIs."""
        if not self.sprints:
            return None
        return self.sprints[-1]

    def get_trends(self) -> dict[str, Any]:
        """Get KPI trends over time."""
        if len(self.sprints) < 2:
            return {}

        latest = self.sprints[-1]
        previous = self.sprints[-2]

        return {
            "story_completion_rate_change": round(
                latest.story_completion_rate - previous.story_completion_rate, 2
            ),
            "first_build_success_rate_change": round(
                latest.first_build_success_rate - previous.first_build_success_rate, 2
            ),
            "test_pass_rate_change": round(
                latest.test_pass_rate - previous.test_pass_rate, 2
            ),
            "coverage_percent_change": round(
                latest.coverage_percent - previous.coverage_percent, 2
            ),
            "cost_per_story_change": round(latest.cost_per_story - previous.cost_per_story, 2),
            "defect_escape_rate_change": round(
                latest.defect_escape_rate - previous.defect_escape_rate, 4
            ),
        }

    def get_historical_trends(self, metric_path: str, n_sprints: int = 5) -> list[Any]:
        """Get historical values for a specific metric."""
        values = []
        for sprint in self.sprints[-n_sprints:]:
            value = sprint.to_dict()
            for key in metric_path.split("."):
                value = value.get(key, {}) if isinstance(value, dict) else None
                if value is None:
                    break
            values.append({"sprint_id": sprint.sprint_id, "value": value})
        return values

    def dashboard_summary(self) -> dict[str, Any]:
        """Generate dashboard summary."""
        latest = self.get_latest()
        if latest is None:
            return {"error": "No sprint data available"}

        return {
            "latest": latest.to_dict(),
            "trends": self.get_trends(),
            "historical": {
                "story_completion_rate": self.get_historical_trends("delivery.story_completion_rate"),
                "cost_per_story": self.get_historical_trends("economic.cost_per_story"),
            },
            "sprint_count": len(self.sprints),
        }
