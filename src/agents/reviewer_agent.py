"""Reviewer Agent implementation."""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, TaskStatus


class ReviewerAgent(BaseAgent):
    """Performs code review, security analysis, and architectural compliance."""

    def __init__(self, instance_id: str | None = None):
        super().__init__("reviewer_agent", instance_id)

    async def execute(self, task: AgentTask, context: dict[str, Any]) -> AgentMessage:
        """Review code submission."""
        self.log_task_start(task)

        code = context.get("code", "")
        adrs = context.get("adrs", [])

        # Simulate review
        critical = 0
        high = 0
        medium = 1
        low = 2
        confidence = 0.92 if critical == 0 and high == 0 else 0.55
        status = "approve" if confidence >= 0.85 else "request_changes"

        self.mark_task_status(task, TaskStatus.COMPLETE)
        self.log_task_complete(task, confidence)

        return AgentMessage(
            from_agent=self.name,
            to_agent="devops_agent" if status == "approve" else "coder_agent",
            message_type=MessageType.REVIEW_RESULT,
            priority="normal" if status == "approve" else "high",
            payload={
                "task_id": task.task_id,
                "content": f"Review status: {status}",
                "artifacts": ["review-report.md"],
                "confidence": confidence,
                "metadata": {
                    "status": status,
                    "findings": {
                        "critical": critical,
                        "high": high,
                        "medium": medium,
                        "low": low,
                    },
                },
            },
        )
