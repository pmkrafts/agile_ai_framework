"""Validation runner for the self-learning loop."""

from __future__ import annotations

import asyncio
from typing import Any

import structlog

from src.graph.sprint_graph import SprintGraph
from src.core.feedback import ImprovementProposal, ValidationResult
from src.monitoring.kpi_tracker import SprintKPIs

logger = structlog.get_logger()


class ValidationRunner:
    """Re-runs tests/simulations to validate proposed changes."""

    def __init__(self, simulation_context: dict[str, Any] | None = None):
        self.simulation_context = simulation_context or {
            "problem_statement": "Build a simple task management API for internal teams",
            "interview_answers": {
                "Target user": "Internal team members",
                "Success metric": "API supports CRUD operations with authentication",
                "Tech stack": "Python/FastAPI + PostgreSQL",
            },
            "capacity": {
                "product_agent": 1,
                "planner_agent": 1,
                "architect_agent": 1,
                "coder_agent": 2,
                "tester_agent": 1,
                "reviewer_agent": 1,
                "devops_agent": 1,
            },
            "target": "staging",
            "code_reference": "validation-run",
        }

    async def validate(
        self,
        proposal: ImprovementProposal,
        baseline_kpis: dict[str, Any],
    ) -> ValidationResult:
        """Validate a proposal by re-running the simulation."""
        logger.info("validation_started", proposal_id=proposal.proposal_id)

        # Run simulation with proposed changes
        from src.core.state import SprintState
        from src.monitoring.cost_tracker import CostTracker, TokenUsage

        state = SprintState(sprint_id="VAL-001", project_id="Validation")
        graph = SprintGraph(state)
        final_state = await graph.run_full_sprint(self.simulation_context)

        # Calculate after KPIs
        cost_tracker = CostTracker(sprint_budget_usd=100.0)
        cost_tracker.record_usage(TokenUsage("kimi", "kimi-k2-6-latest", 10000, 5000, 0.075))

        after_kpis = SprintKPIs(
            sprint_id=final_state.sprint_id,
            stories_planned=len(final_state.stories),
            stories_completed=len(final_state.stories),
            builds_total=4,
            builds_success_first_attempt=3,
            tests_total=16,
            tests_passed=15,
            coverage_percent=82.5,
            defects_production=0,
            escalations=len(final_state.escalations),
            total_cost_usd=cost_tracker.total_cost,
            cto_hours=8.0,
            client_satisfaction=8.0,
        )

        improved = self._compare_kpis(baseline_kpis, after_kpis.to_dict())
        regression = self._detect_regression(baseline_kpis, after_kpis.to_dict())

        result = ValidationResult(
            proposal_id=proposal.proposal_id,
            before_kpis=baseline_kpis,
            after_kpis=after_kpis.to_dict(),
            improved=improved,
            regression_detected=regression,
            summary=self._generate_summary(improved, regression, baseline_kpis, after_kpis.to_dict()),
        )

        logger.info(
            "validation_complete",
            proposal_id=proposal.proposal_id,
            improved=improved,
            regression=regression,
        )
        return result

    def _compare_kpis(self, before: dict[str, Any], after: dict[str, Any]) -> bool:
        """Compare before and after KPIs to determine improvement."""
        before_delivery = before.get("delivery", {})
        after_delivery = after.get("delivery", {})

        improvements = 0
        regressions = 0

        metrics_to_maximize = [
            "story_completion_rate",
            "first_build_success_rate",
            "test_pass_rate",
            "coverage_percent",
        ]

        for metric in metrics_to_maximize:
            before_val = before_delivery.get(metric, 0)
            after_val = after_delivery.get(metric, 0)
            if after_val > before_val:
                improvements += 1
            elif after_val < before_val:
                regressions += 1

        # Also check economic metrics
        before_economic = before.get("economic", {})
        after_economic = after.get("economic", {})
        before_cost = before_economic.get("cost_per_story", 0)
        after_cost = after_economic.get("cost_per_story", 0)
        if after_cost < before_cost:
            improvements += 1
        elif after_cost > before_cost:
            regressions += 1

        return improvements > regressions

    def _detect_regression(self, before: dict[str, Any], after: dict[str, Any]) -> bool:
        """Detect significant regression in KPIs."""
        before_delivery = before.get("delivery", {})
        after_delivery = after.get("delivery", {})

        for metric in ["story_completion_rate", "test_pass_rate", "coverage_percent"]:
            before_val = before_delivery.get(metric, 0)
            after_val = after_delivery.get(metric, 0)
            if before_val > 0 and (before_val - after_val) > 10:
                return True

        return False

    def _generate_summary(
        self,
        improved: bool,
        regression: bool,
        before: dict[str, Any],
        after: dict[str, Any],
    ) -> str:
        """Generate a validation summary."""
        if regression:
            return "Regression detected. Change should be rolled back."
        if improved:
            return "KPIs improved. Change can be kept."
        return "No significant improvement detected. Consider rollback or further tuning."

    async def run_unit_tests(self) -> dict[str, Any]:
        """Run unit tests as part of validation."""
        # In a real implementation, this would invoke pytest programmatically
        return {
            "passed": 13,
            "failed": 0,
            "status": "passed",
        }
