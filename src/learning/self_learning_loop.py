"""Self-learning loop orchestrator."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

import structlog

from src.core.feedback import GapPattern, ImprovementProposal, ValidationResult
from src.learning.models import LearningLoopConfig
from src.core.state import SprintState
from src.graph.sprint_graph import SprintGraph
from src.learning.baseline_tracker import BaselineTracker
from src.learning.change_manager import ChangeManager
from src.learning.feedback_collector import FeedbackCollector
from src.learning.gap_analyzer import GapAnalyzer
from src.learning.improvement_proposer import ImprovementProposer
from src.learning.validation_runner import ValidationRunner
from src.monitoring.cost_tracker import CostTracker, TokenUsage
from src.monitoring.kpi_tracker import KPITracker, SprintKPIs
from src.monitoring.cost_tracker import CostTracker, TokenUsage
from src.monitoring.kpi_tracker import KPITracker, SprintKPIs

logger = structlog.get_logger()


class SelfLearningLoop:
    """Orchestrates the self-learning loop."""

    def __init__(
        self,
        config: LearningLoopConfig | None = None,
        feedback_collector: FeedbackCollector | None = None,
        gap_analyzer: GapAnalyzer | None = None,
        proposer: ImprovementProposer | None = None,
        change_manager: ChangeManager | None = None,
        validation_runner: ValidationRunner | None = None,
        baseline_tracker: BaselineTracker | None = None,
    ):
        self.config = config or LearningLoopConfig()
        self.feedback_collector = feedback_collector or FeedbackCollector()
        self.gap_analyzer = gap_analyzer or GapAnalyzer()
        self.proposer = proposer or ImprovementProposer()
        self.change_manager = change_manager or ChangeManager()
        self.validation_runner = validation_runner or ValidationRunner()
        self.baseline_tracker = baseline_tracker or BaselineTracker()
        self.kpi_tracker = KPITracker()
        self.total_learning_cost = 0.0

    async def run(
        self,
        sprint_state: SprintState,
        cost_data: dict[str, Any],
        kpi_data: dict[str, Any],
        cto_approver: str | None = None,
    ) -> dict[str, Any]:
        """Run the self-learning loop after a sprint."""
        logger.info(
            "self_learning_loop_started",
            sprint_id=sprint_state.sprint_id,
            max_iterations=self.config.max_iterations,
            budget=self.config.budget_usd,
        )

        # Record baseline
        latest_kpis = kpi_data.get("latest", {})
        self.baseline_tracker.record_baseline(SprintKPIs.from_dict(latest_kpis))

        iteration = 0
        applied_proposals: list[ImprovementProposal] = []
        rolled_back_proposals: list[ImprovementProposal] = []
        rejected_proposals: list[ImprovementProposal] = []

        while iteration < self.config.max_iterations:
            iteration += 1
            logger.info("learning_iteration", iteration=iteration)

            # Check budget
            if self._budget_exceeded():
                logger.warning("learning_budget_exceeded", total_cost=self.total_learning_cost)
                break

            # Collect feedback
            events = self.feedback_collector.collect_from_sprint(
                sprint_state, cost_data, kpi_data
            )
            if not events:
                logger.info("no_feedback_events", iteration=iteration)
                break

            # Analyze gaps
            baseline = self.baseline_tracker.get_latest_baseline()
            current_kpis = latest_kpis.get("delivery", {})
            baseline_kpis = baseline.get("delivery", {})
            gap_patterns = self.gap_analyzer.analyze(events)
            baseline_gaps = self.gap_analyzer.compare_to_baseline(
                current_kpis,
                baseline_kpis,
            )
            all_gaps = gap_patterns + baseline_gaps

            if not all_gaps:
                logger.info("no_gaps_identified", iteration=iteration)
                break

            # Generate proposals
            proposals = self.proposer.generate_proposals(
                all_gaps,
                max_proposals=self.config.max_proposals_per_iteration,
            )
            if not proposals:
                logger.info("no_proposals_generated", iteration=iteration)
                break

            # Process proposals
            for proposal in proposals:
                if proposal.confidence < self.config.min_proposal_confidence:
                    logger.info(
                        "proposal_below_confidence_threshold",
                        proposal_id=proposal.proposal_id,
                        confidence=proposal.confidence,
                    )
                    rejected_proposals.append(proposal)
                    continue

                # Determine approval path
                auto_approve = (
                    self.config.auto_approve_low_risk
                    and proposal.category.value in self.config.low_risk_categories
                    and proposal.confidence >= 0.8
                )

                if not auto_approve:
                    # In a real system, this would notify the CTO and await approval
                    # For now, we simulate approval if cto_approver is provided
                    if not cto_approver:
                        logger.info(
                            "proposal_requires_cto_approval",
                            proposal_id=proposal.proposal_id,
                        )
                        rejected_proposals.append(proposal)
                        continue

                proposal.approved_by = cto_approver or "auto-approved"
                proposal.approved_at = datetime.now(timezone.utc).isoformat()

                # Apply change
                applied = self.change_manager.apply_change(proposal)
                if not applied:
                    rejected_proposals.append(proposal)
                    continue

                # Validate change
                validation = await self.validation_runner.validate(
                    proposal,
                    baseline,
                )
                self.change_manager.record_validation(validation)

                # Track learning cost
                self._track_learning_cost()

                if validation.regression_detected and self.config.stop_on_critical_regression:
                    logger.warning(
                        "critical_regression_detected",
                        proposal_id=proposal.proposal_id,
                    )
                    self.change_manager.rollback_change(proposal)
                    rolled_back_proposals.append(proposal)
                    break

                if validation.improved:
                    applied_proposals.append(proposal)
                    self.baseline_tracker.record_baseline(
                        SprintKPIs.from_dict(validation.after_kpis)
                    )
                else:
                    self.change_manager.rollback_change(proposal)
                    rolled_back_proposals.append(proposal)

        result = {
            "sprint_id": sprint_state.sprint_id,
            "iterations": iteration,
            "total_learning_cost": round(self.total_learning_cost, 4),
            "applied_proposals": len(applied_proposals),
            "rolled_back_proposals": len(rolled_back_proposals),
            "rejected_proposals": len(rejected_proposals),
            "proposal_ids": [p.proposal_id for p in applied_proposals],
            "status": "complete",
        }

        logger.info("self_learning_loop_complete", **result)
        return result

    def _budget_exceeded(self) -> bool:
        """Check if learning budget is exceeded."""
        if not self.config.stop_on_budget_exceeded:
            return False
        return self.total_learning_cost >= self.config.budget_usd

    def _track_learning_cost(self) -> None:
        """Track cost of running validation."""
        # Simplified: each validation costs ~$0.02
        self.total_learning_cost += 0.02

    async def run_full_pipeline(
        self,
        simulation_context: dict[str, Any],
        cto_approver: str | None = None,
    ) -> dict[str, Any]:
        """Run a full sprint followed by the learning loop."""
        # Run sprint
        state = SprintState(sprint_id="SL-001", project_id="SelfLearning")
        graph = SprintGraph(state)
        final_state = await graph.run_full_sprint(simulation_context)

        # Calculate KPIs
        cost_tracker = CostTracker(sprint_budget_usd=100.0)
        cost_tracker.record_usage(TokenUsage("kimi", "kimi-k2-6-latest", 10000, 5000, 0.075))
        cost_tracker.record_usage(TokenUsage("openai", "o3-2025-01-31", 5000, 2000, 0.035))

        kpis = SprintKPIs(
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
        kpi_data = {"latest": kpis.to_dict()}

        # Run learning loop
        return await self.run(
            final_state,
            cost_tracker.get_summary(),
            kpi_data,
            cto_approver,
        )


async def main() -> None:
    """Example usage of the self-learning loop."""
    loop = SelfLearningLoop(
        config=LearningLoopConfig(
            max_iterations=3,
            budget_usd=5.0,
            auto_approve_low_risk=True,
        )
    )

    context = {
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
        "code_reference": "self-learning-run",
    }

    result = await loop.run_full_pipeline(context, cto_approver="cto@company.com")
    print("Self-Learning Loop Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
