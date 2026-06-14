"""Cost tracking for AI-native operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import structlog

logger = structlog.get_logger()


@dataclass
class TokenUsage:
    """Token usage for a single operation."""

    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class CostTracker:
    """Tracks LLM API costs across agents and sprints."""

    def __init__(self, sprint_budget_usd: float = 100.0):
        self.sprint_budget_usd = sprint_budget_usd
        self.usages: list[TokenUsage] = []
        self.total_cost = 0.0

    def record_usage(self, usage: TokenUsage) -> None:
        """Record token usage."""
        self.usages.append(usage)
        self.total_cost += usage.cost_usd
        self._check_budget()

    def _check_budget(self) -> None:
        """Check if budget thresholds are exceeded."""
        ratio = self.total_cost / self.sprint_budget_usd
        thresholds = [0.5, 0.75, 0.9, 1.0]
        for threshold in thresholds:
            if ratio >= threshold:
                logger.warning(
                    "budget_threshold_reached",
                    threshold=threshold,
                    total_cost=self.total_cost,
                    budget=self.sprint_budget_usd,
                )
        if ratio >= 1.0:
            logger.error("budget_exceeded", total_cost=self.total_cost, budget=self.sprint_budget_usd)

    def get_summary(self) -> dict[str, Any]:
        """Get cost summary by provider and model."""
        summary: dict[str, dict[str, Any]] = {}
        for usage in self.usages:
            key = f"{usage.provider}/{usage.model}"
            if key not in summary:
                summary[key] = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0.0,
                    "calls": 0,
                }
            summary[key]["input_tokens"] += usage.input_tokens
            summary[key]["output_tokens"] += usage.output_tokens
            summary[key]["cost_usd"] += usage.cost_usd
            summary[key]["calls"] += 1

        return {
            "total_cost_usd": round(self.total_cost, 4),
            "budget_usd": self.sprint_budget_usd,
            "utilization": round(self.total_cost / self.sprint_budget_usd, 4),
            "by_provider": summary,
            "usage_count": len(self.usages),
        }

    def estimate_cost(self, provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a hypothetical operation."""
        # Simplified pricing; in production, load from providers.yaml
        pricing = {
            "anthropic/claude-4-sonnet-20250514": (0.003, 0.015),
            "openai/gpt-4o-2024-05-13": (0.005, 0.015),
            "kimi/kimi-k2-6-latest": (0.005, 0.015),
            "kimi/kimi-k2-5-latest": (0.003, 0.009),
        }
        input_price, output_price = pricing.get(f"{provider}/{model}", (0.005, 0.015))
        return (input_tokens / 1000 * input_price) + (output_tokens / 1000 * output_price)
