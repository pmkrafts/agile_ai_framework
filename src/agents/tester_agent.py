"""Tester Agent implementation."""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, TaskStatus


class TesterAgent(BaseAgent):
    """Generates and executes test suites."""

    def __init__(self, instance_id: str | None = None):
        super().__init__("tester_agent", instance_id)

    async def execute(self, task: AgentTask, context: dict[str, Any]) -> AgentMessage:
        """Generate and run tests for a story."""
        self.log_task_start(task)

        story = context.get("story", {})
        code = context.get("code", "")

        # Simulate test generation and execution
        test_count = 8
        passed = 7
        coverage = 82.5
        confidence = 0.87 if coverage >= 80 else 0.65

        self.mark_task_status(task, TaskStatus.COMPLETE)
        self.log_task_complete(task, confidence)

        return AgentMessage(
            from_agent=self.name,
            to_agent="reviewer_agent",
            message_type=MessageType.STATUS_UPDATE,
            priority="normal" if confidence >= 0.8 else "high",
            payload={
                "task_id": task.task_id,
                "content": f"Test execution complete: {passed}/{test_count} passed, {coverage}% coverage",
                "artifacts": ["test-report.md", "coverage.xml"],
                "confidence": confidence,
                "metadata": {
                    "test_count": test_count,
                    "passed": passed,
                    "failed": test_count - passed,
                    "coverage": coverage,
                },
            },
        )
