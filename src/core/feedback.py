"""Core feedback models used by agents and learning loop."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class FeedbackEventType(str, Enum):
    """Types of feedback events."""

    SUCCESS = "success"
    FAILURE = "failure"
    ESCALATION = "escalation"
    RETRY = "retry"
    REJECTION = "rejection"
    COST_SPIKE = "cost_spike"
    TIMEOUT = "timeout"


class FeedbackCategory(str, Enum):
    """Categories of feedback."""

    PROMPT = "prompt"
    SKILL = "skill"
    TOOL = "tool"
    SPEC = "spec"
    GOVERNANCE = "governance"
    ARCHITECTURE = "architecture"
    UNKNOWN = "unknown"


class FeedbackSeverity(str, Enum):
    """Severity levels for feedback."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FeedbackEvent(BaseModel):
    """A single feedback event from a sprint execution."""

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sprint_id: str
    agent_type: str
    task_id: str
    event_type: FeedbackEventType
    category: FeedbackCategory
    severity: FeedbackSeverity
    description: str
    context: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GapPattern(BaseModel):
    """A recurring pattern identified by the gap analyzer."""

    pattern_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: FeedbackCategory
    agent_type: str | None = None
    task_type: str | None = None
    description: str
    occurrence_count: int = 0
    affected_sprints: list[str] = Field(default_factory=list)
    severity: FeedbackSeverity
    root_cause_hypothesis: str = ""
    example_events: list[str] = Field(default_factory=list)


class ImprovementProposal(BaseModel):
    """A proposed improvement to prompts, skills, or governance."""

    proposal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    target_file: str
    category: FeedbackCategory
    rationale: str
    current_state: str
    proposed_change: str
    expected_impact: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0)
    status: str = "pending"  # pending, approved, applied, rejected, rolled_back
    related_gaps: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    approved_by: str | None = None
    approved_at: str | None = None


class ValidationResult(BaseModel):
    """Result of validating a proposed change."""

    proposal_id: str
    before_kpis: dict[str, Any] = Field(default_factory=dict)
    after_kpis: dict[str, Any] = Field(default_factory=dict)
    improved: bool = False
    regression_detected: bool = False
    summary: str = ""
    validation_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
