"""Base agent class and utilities."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any

import structlog
from dotenv import load_dotenv

from src.core.feedback import FeedbackCategory, FeedbackEvent, FeedbackEventType, FeedbackSeverity
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, TaskStatus

load_dotenv()
logger = structlog.get_logger()


class BaseAgent(ABC):
    """Base class for all AI development team agents."""

    def __init__(self, agent_type: str, instance_id: str | None = None):
        self.agent_type = agent_type
        self.instance_id = instance_id or "001"
        self.name = f"{agent_type}:{self.instance_id}"
        self.logger = logger.bind(agent=self.name)
        self.feedback_callbacks: list = []

    @abstractmethod
    async def execute(self, task: AgentTask, context: dict[str, Any]) -> AgentMessage:
        """Execute the assigned task and return a message."""
        pass

    def register_feedback_callback(self, callback) -> None:
        """Register a callback for feedback events."""
        self.feedback_callbacks.append(callback)

    def emit_feedback(
        self,
        sprint_id: str,
        task: AgentTask,
        event_type: FeedbackEventType,
        severity: FeedbackSeverity,
        description: str,
        category: FeedbackCategory | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Emit a feedback event to registered callbacks."""
        event = FeedbackEvent(
            sprint_id=sprint_id,
            agent_type=self.agent_type,
            task_id=task.task_id,
            event_type=event_type,
            category=category or self._infer_category(),
            severity=severity,
            description=description,
            context=context or {},
        )
        for callback in self.feedback_callbacks:
            callback(event)

    def _infer_category(self) -> FeedbackCategory:
        """Infer feedback category from agent type."""
        category_map = {
            "product_agent": FeedbackCategory.PROMPT,
            "planner_agent": FeedbackCategory.PROMPT,
            "architect_agent": FeedbackCategory.ARCHITECTURE,
            "coder_agent": FeedbackCategory.SKILL,
            "tester_agent": FeedbackCategory.SKILL,
            "reviewer_agent": FeedbackCategory.SKILL,
            "devops_agent": FeedbackCategory.TOOL,
            "learning_agent": FeedbackCategory.GOVERNANCE,
        }
        return category_map.get(self.agent_type, FeedbackCategory.UNKNOWN)

    def log_task_start(self, task: AgentTask) -> None:
        """Log task start."""
        self.logger.info(
            "task_started",
            task_id=task.task_id,
            title=task.title,
            story_id=task.story_id,
        )

    def log_task_complete(self, task: AgentTask, confidence: float) -> None:
        """Log task completion."""
        self.logger.info(
            "task_completed",
            task_id=task.task_id,
            confidence=confidence,
            status=task.status,
        )

    def create_status_update(
        self,
        to_agent: str,
        task: AgentTask,
        content: str,
        confidence: float,
        artifacts: list[str] | None = None,
    ) -> AgentMessage:
        """Create a status update message."""
        return AgentMessage(
            from_agent=self.name,
            to_agent=to_agent,
            message_type=MessageType.STATUS_UPDATE,
            payload={
                "task_id": task.task_id,
                "content": content,
                "artifacts": artifacts or [],
                "confidence": confidence,
                "blockers": task.blockers,
            },
        )

    def mark_task_status(self, task: AgentTask, status: TaskStatus) -> None:
        """Update task status."""
        task.status = status

    def get_env(self, key: str, default: str | None = None) -> str | None:
        """Get environment variable."""
        return os.getenv(key, default)
