"""Learning loop configuration models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

# Re-export shared feedback models from core for backward compatibility
from src.core.feedback import (  # noqa: F401
    FeedbackCategory,
    FeedbackEvent,
    FeedbackEventType,
    FeedbackSeverity,
    GapPattern,
    ImprovementProposal,
    ValidationResult,
)


class LearningLoopConfig(BaseModel):
    """Configuration for the self-learning loop."""

    max_iterations: int = 10
    budget_usd: float = 20.0
    min_proposal_confidence: float = 0.6
    auto_approve_low_risk: bool = False
    low_risk_categories: list[str] = Field(default_factory=lambda: ["prompt", "skill"])
    max_proposals_per_iteration: int = 3
    stop_on_budget_exceeded: bool = True
    stop_on_critical_regression: bool = True
