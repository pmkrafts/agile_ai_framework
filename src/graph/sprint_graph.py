"""LangGraph-based sprint orchestration."""

from __future__ import annotations

import asyncio
from typing import Any

from src.agents import (
    ArchitectAgent,
    CoderAgent,
    DevOpsAgent,
    PlannerAgent,
    ProductAgent,
    ReviewerAgent,
    TesterAgent,
)
from src.core.state import AgentTask, SprintPhase, SprintState, TaskStatus
from src.learning.feedback_collector import FeedbackCollector


class SprintGraph:
    """Deterministic state machine for executing an AI-native sprint."""

    def __init__(self, state: SprintState, feedback_collector: FeedbackCollector | None = None):
        self.state = state
        self.feedback_collector = feedback_collector or FeedbackCollector()
        self.agents = {
            "product_agent": ProductAgent(),
            "planner_agent": PlannerAgent(),
            "architect_agent": ArchitectAgent(),
            "coder_agent": CoderAgent(),
            "tester_agent": TesterAgent(),
            "reviewer_agent": ReviewerAgent(),
            "devops_agent": DevOpsAgent(),
        }
        self._register_feedback_callbacks()

    def _register_feedback_callbacks(self) -> None:
        """Register feedback collection callbacks on all agents."""
        def on_feedback(event):
            self.feedback_collector.events.append(event)

        for agent in self.agents.values():
            agent.register_feedback_callback(on_feedback)

    async def run_phase(self, phase: SprintPhase, context: dict[str, Any]) -> None:
        """Run a single sprint phase."""
        self.state.phase = phase
        if phase == SprintPhase.BACKLOG:
            await self._run_backlog(context)
        elif phase == SprintPhase.PLANNING:
            await self._run_planning(context)
        elif phase == SprintPhase.EXECUTION:
            await self._run_execution(context)
        elif phase == SprintPhase.REVIEW:
            await self._run_review(context)
        elif phase == SprintPhase.DEPLOYMENT:
            await self._run_deployment(context)

    async def _run_backlog(self, context: dict[str, Any]) -> None:
        """Run backlog refinement phase."""
        task = AgentTask(
            task_id="T-PRD-001",
            story_id="PRD",
            title="Generate PRD and user stories",
            agent_type="product_agent",
        )
        msg = await self.agents["product_agent"].execute(task, context)
        self.state.prd = msg.payload.metadata.get("prd", "")
        self.state.stories = [
            {
                "story_id": s["story_id"],
                "title": s["title"],
                "acceptance_criteria": s.get("acceptance_criteria", []),
            }
            for s in msg.payload.metadata.get("stories", [])
        ]

    async def _run_planning(self, context: dict[str, Any]) -> None:
        """Run sprint planning phase."""
        task = AgentTask(
            task_id="T-PLAN-001",
            story_id="PLAN",
            title="Create sprint plan",
            agent_type="planner_agent",
        )
        plan_context = {
            "stories": self.state.stories,
            "capacity": context.get("capacity", {}),
        }
        msg = await self.agents["planner_agent"].execute(task, plan_context)
        self.state.sprint_plan = msg.payload.metadata.get("plan", {})

    async def _run_execution(self, context: dict[str, Any]) -> None:
        """Run execution phase in parallel streams."""
        # Architecture stream
        arch_task = AgentTask(
            task_id="T-ARCH-001",
            story_id="ARCH",
            title="Design system architecture",
            agent_type="architect_agent",
        )
        arch_msg = await self.agents["architect_agent"].execute(
            arch_task, {"prd": self.state.prd}
        )
        self.state.architecture = str(arch_msg.payload.metadata.get("design", ""))

        # Development + quality + review streams for each story
        for story in self.state.stories:
            story_context = {
                "story": story,
                "api_spec": self.state.architecture,
            }

            coder_task = AgentTask(
                task_id=f"T-CODE-{story['story_id']}",
                story_id=story["story_id"],
                title=f"Implement {story['title']}",
                agent_type="coder_agent",
            )
            code_msg = await self.agents["coder_agent"].execute(coder_task, story_context)

            tester_task = AgentTask(
                task_id=f"T-TEST-{story['story_id']}",
                story_id=story["story_id"],
                title=f"Test {story['title']}",
                agent_type="tester_agent",
            )
            test_context = {
                "story": story,
                "code": code_msg.payload.metadata.get("code", ""),
            }
            await self.agents["tester_agent"].execute(tester_task, test_context)

            reviewer_task = AgentTask(
                task_id=f"T-REVIEW-{story['story_id']}",
                story_id=story["story_id"],
                title=f"Review {story['title']}",
                agent_type="reviewer_agent",
            )
            review_context = {
                "code": code_msg.payload.metadata.get("code", ""),
                "adrs": self.state.architecture,
            }
            await self.agents["reviewer_agent"].execute(reviewer_task, review_context)

    async def _run_review(self, context: dict[str, Any]) -> None:
        """Run sprint review phase (CEO demo and retrospective)."""
        # In a real implementation, this would coordinate demos and acceptance
        self.state.retrospective = {
            "stories_planned": len(self.state.stories),
            "stories_completed": len(self.state.stories),
            "escalations": len(self.state.escalations),
            "improvements": [],
        }

    async def _run_deployment(self, context: dict[str, Any]) -> None:
        """Run deployment phase."""
        task = AgentTask(
            task_id="T-DEPLOY-001",
            story_id="DEPLOY",
            title="Prepare deployment",
            agent_type="devops_agent",
        )
        deploy_context = {
            "target": context.get("target", "staging"),
            "code_reference": context.get("code_reference", "latest"),
        }
        await self.agents["devops_agent"].execute(task, deploy_context)
        self.state.phase = SprintPhase.COMPLETE

    async def run_full_sprint(self, context: dict[str, Any]) -> SprintState:
        """Run all phases of a sprint."""
        phases = [
            SprintPhase.BACKLOG,
            SprintPhase.PLANNING,
            SprintPhase.EXECUTION,
            SprintPhase.REVIEW,
            SprintPhase.DEPLOYMENT,
        ]
        for phase in phases:
            await self.run_phase(phase, context)
        return self.state


async def main() -> None:
    """Example usage of SprintGraph."""
    state = SprintState(sprint_id="Sprint-001", project_id="Project-Alpha")
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
        "code_reference": "abc123",
    }

    final_state = await graph.run_full_sprint(context)
    print(f"Sprint completed: {final_state.sprint_id}")
    print(f"Final phase: {final_state.phase}")
    print(f"Stories: {len(final_state.stories)}")


if __name__ == "__main__":
    asyncio.run(main())
