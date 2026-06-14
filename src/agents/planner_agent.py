"""Planner Agent implementation."""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, TaskStatus


class PlannerAgent(BaseAgent):
    """Creates optimized sprint plans with dependencies and resource allocation."""

    def __init__(self, instance_id: str | None = None):
        super().__init__("planner_agent", instance_id)

    async def execute(self, task: AgentTask, context: dict[str, Any]) -> AgentMessage:
        """Generate sprint plan from approved stories."""
        self.log_task_start(task)

        stories = context.get("stories", [])
        capacity = context.get("capacity", {})

        plan = self._generate_plan(stories, capacity)
        confidence = 0.90 if stories else 0.60

        self.mark_task_status(task, TaskStatus.COMPLETE)
        self.log_task_complete(task, confidence)

        return AgentMessage(
            from_agent=self.name,
            to_agent="cto",
            message_type=MessageType.STATUS_UPDATE,
            priority="normal" if confidence >= 0.8 else "high",
            payload={
                "task_id": task.task_id,
                "content": "Sprint plan generated",
                "artifacts": ["sprint-plan.json", "gantt.mmd"],
                "confidence": confidence,
                "metadata": {"plan": plan},
            },
        )

    def _generate_plan(self, stories: list[dict[str, Any]], capacity: dict[str, Any]) -> dict[str, Any]:
        """Generate a sprint plan (simulated)."""
        tasks = []
        for i, story in enumerate(stories):
            tasks.append(
                {
                    "task_id": f"T-{i+1:03d}",
                    "story_id": story.get("story_id", f"US-{i+1:03d}"),
                    "title": f"Implement {story.get('title', 'feature')}",
                    "agent_type": "coder_agent",
                    "estimated_hours": 4.0,
                    "dependencies": [],
                    "start_day": 1,
                    "end_day": 2,
                    "risk": "low",
                }
            )

        return {
            "sprint_id": "Sprint-001",
            "start_date": "2026-06-15",
            "end_date": "2026-06-19",
            "capacity": capacity,
            "tasks": tasks,
            "critical_path": [t["task_id"] for t in tasks],
            "risk_mitigations": [
                {"risk": "Integration unknowns", "mitigation": "Allocate tester time early"}
            ],
        }
