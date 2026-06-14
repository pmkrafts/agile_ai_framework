"""Core message protocol for inter-agent communication."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    REVIEW_RESULT = "review_result"
    ESCALATION = "escalation"
    APPROVAL = "approval"
    REJECTION = "rejection"


class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class AgentMessagePayload(BaseModel):
    """Payload for agent messages."""

    task_id: str | None = None
    content: str = ""
    artifacts: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    blockers: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentMessage(BaseModel):
    """Structured message protocol for inter-agent communication."""

    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    from_agent: str
    to_agent: str
    message_type: MessageType
    payload: AgentMessagePayload
    requires_response: bool = True
    priority: Priority = Priority.NORMAL

    def to_json(self) -> str:
        """Serialize message to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> AgentMessage:
        """Deserialize message from JSON string."""
        return cls.model_validate_json(json_str)


def create_escalation(
    from_agent: str,
    reason: str,
    details: str = "",
    priority: Priority = Priority.HIGH,
    task_id: str | None = None,
) -> AgentMessage:
    """Create an escalation message to the CTO."""
    return AgentMessage(
        from_agent=from_agent,
        to_agent="cto",
        message_type=MessageType.ESCALATION,
        priority=priority,
        payload=AgentMessagePayload(
            task_id=task_id,
            content=f"ESCALATION: {reason}",
            blockers=[details] if details else [],
        ),
    )
