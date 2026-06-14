"""Sprint simulation for validating the framework implementation."""

from __future__ import annotations

import asyncio
import json

from src.graph.sprint_graph import SprintGraph
from src.learning.models import LearningLoopConfig
from src.learning.self_learning_loop import SelfLearningLoop
from src.monitoring.cost_tracker import CostTracker, TokenUsage
from src.monitoring.kpi_tracker import KPITracker, SprintKPIs
from src.core.state import SprintState


async def run_simulation(run_learning_loop: bool = False) -> dict:
    """Run a simulated AI-native sprint end-to-end."""
    print("=" * 60)
    print("AI-NATIVE SPRINT SIMULATION")
    print("=" * 60)

    state = SprintState(sprint_id="SIM-001", project_id="Pilot-Alpha")
    graph = SprintGraph(state)

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
        "code_reference": "sim-abc123",
    }

    # Run full sprint
    final_state = await graph.run_full_sprint(context)

    # Simulate cost tracking
    cost_tracker = CostTracker(sprint_budget_usd=100.0)
    cost_tracker.record_usage(TokenUsage("kimi", "kimi-k2-6-latest", 10000, 5000, 0.075))
    cost_tracker.record_usage(TokenUsage("openai", "o3-2025-01-31", 5000, 2000, 0.035))

    # Simulate KPI tracking
    kpi_tracker = KPITracker()
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
    kpi_tracker.record_sprint(kpis)

    result = {
        "sprint_id": final_state.sprint_id,
        "final_phase": final_state.phase,
        "story_count": len(final_state.stories),
        "feedback_events_collected": len(graph.feedback_collector.events),
        "cost_summary": cost_tracker.get_summary(),
        "kpis": kpi_tracker.dashboard_summary(),
    }

    if run_learning_loop:
        print("\nStarting self-learning loop...")
        loop = SelfLearningLoop(
            config=LearningLoopConfig(
                max_iterations=2,
                budget_usd=2.0,
                auto_approve_low_risk=True,
            )
        )
        learning_result = await loop.run(
            final_state,
            cost_tracker.get_summary(),
            {"latest": kpis.to_dict()},
            cto_approver="cto@company.com",
        )
        result["learning_loop"] = learning_result

    print("\nSimulation Results:")
    print(json.dumps(result, indent=2))
    print("=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)

    return result


if __name__ == "__main__":
    import sys
    run_loop = "--learning" in sys.argv
    asyncio.run(run_simulation(run_learning_loop=run_loop))
