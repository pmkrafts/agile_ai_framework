"""Core state models for the framework."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SprintPhase(str, Enum):
    """Phases of a compressed AI-native sprint."""

    BACKLOG = "backlog"
    PLANNING = "planning"
    EXECUTION = "execution"
    REVIEW = "review"
    DEPLOYMENT = "deployment"
    COMPLETE = "complete"


class StoryStatus(str, Enum):
    """Status of a user story."""

    BACKLOG = "backlog"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class TaskStatus(str, Enum):
    """Status of an agent task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"
    ESCALATED = "escalated"


class UserStory(BaseModel):
    """A user story with acceptance criteria."""

    story_id: str
    title: str
    description: str
    acceptance_criteria: list[str] = Field(default_factory=list)
    status: StoryStatus = StoryStatus.BACKLOG
    assigned_to: str | None = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentTask(BaseModel):
    """A task assigned to an agent."""

    task_id: str
    story_id: str
    title: str
    agent_type: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: list[str] = Field(default_factory=list)
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    confidence: float = 0.0
    output: str = ""
    artifacts: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)


class SprintState(BaseModel):
    """State of an AI-native sprint."""

    sprint_id: str
    project_id: str
    phase: SprintPhase = SprintPhase.BACKLOG
    stories: list[UserStory] = Field(default_factory=list)
    tasks: list[AgentTask] = Field(default_factory=list)
    prd: str = ""
    architecture: str = ""
    sprint_plan: dict[str, Any] = Field(default_factory=dict)
    deployments: list[dict[str, Any]] = Field(default_factory=list)
    escalations: list[dict[str, Any]] = Field(default_factory=list)
    retrospective: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
