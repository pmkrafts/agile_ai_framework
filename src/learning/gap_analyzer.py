"""Gap analyzer for the self-learning loop."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

import structlog

from src.core.feedback import FeedbackCategory, FeedbackEvent, FeedbackSeverity, GapPattern

logger = structlog.get_logger()


class GapAnalyzer:
    """Analyzes feedback events to identify recurring patterns and root causes."""

    def __init__(self, min_occurrences: int = 1):
        self.min_occurrences = min_occurrences

    def analyze(self, events: list[FeedbackEvent]) -> list[GapPattern]:
        """Analyze feedback events and return gap patterns."""
        if not events:
            logger.info("no_events_to_analyze")
            return []

        patterns: list[GapPattern] = []

        # Group by category + agent_type
        grouped = defaultdict(list)
        for event in events:
            key = (event.category, event.agent_type)
            grouped[key].append(event)

        for (category, agent_type), group_events in grouped.items():
            if len(group_events) < self.min_occurrences:
                continue

            severity = self._aggregate_severity(group_events)
            description = self._generate_description(category, agent_type, group_events)
            root_cause = self._infer_root_cause(category, agent_type, group_events)

            patterns.append(
                GapPattern(
                    category=category,
                    agent_type=agent_type,
                    description=description,
                    occurrence_count=len(group_events),
                    affected_sprints=list(set(e.sprint_id for e in group_events)),
                    severity=severity,
                    root_cause_hypothesis=root_cause,
                    example_events=[e.event_id for e in group_events[:3]],
                )
            )

        # Sort by severity and occurrence count
        severity_order = {
            FeedbackSeverity.CRITICAL: 0,
            FeedbackSeverity.HIGH: 1,
            FeedbackSeverity.MEDIUM: 2,
            FeedbackSeverity.LOW: 3,
        }
        patterns.sort(key=lambda p: (severity_order[p.severity], -p.occurrence_count))

        logger.info("gap_analysis_complete", pattern_count=len(patterns))
        return patterns

    def _aggregate_severity(self, events: list[FeedbackEvent]) -> FeedbackSeverity:
        """Aggregate severity from a group of events."""
        severity_order = {
            FeedbackSeverity.CRITICAL: 4,
            FeedbackSeverity.HIGH: 3,
            FeedbackSeverity.MEDIUM: 2,
            FeedbackSeverity.LOW: 1,
        }
        max_score = max(severity_order[e.severity] for e in events)
        for sev, score in severity_order.items():
            if score == max_score:
                return sev
        return FeedbackSeverity.LOW

    def _generate_description(
        self,
        category: FeedbackCategory,
        agent_type: str,
        events: list[FeedbackEvent],
    ) -> str:
        """Generate a human-readable pattern description."""
        event_types = Counter(e.event_type for e in events)
        top_type = event_types.most_common(1)[0][0]

        if category == FeedbackCategory.SKILL and agent_type:
            return f"{agent_type} shows recurring {top_type} events ({len(events)} occurrences)"
        elif category == FeedbackCategory.PROMPT:
            return f"Prompt-related {top_type} events ({len(events)} occurrences)"
        elif category == FeedbackCategory.GOVERNANCE:
            return f"Governance escalations or budget issues ({len(events)} occurrences)"
        elif category == FeedbackCategory.ARCHITECTURE:
            return f"Architecture-related issues ({len(events)} occurrences)"
        elif category == FeedbackCategory.TOOL:
            return f"Tool/integration failures ({len(events)} occurrences)"
        else:
            return f"Recurring {top_type} events ({len(events)} occurrences)"

    def _infer_root_cause(
        self,
        category: FeedbackCategory,
        agent_type: str,
        events: list[FeedbackEvent],
    ) -> str:
        """Infer a root cause hypothesis."""
        sample_descriptions = [e.description for e in events[:3]]
        sample_text = "; ".join(sample_descriptions)

        cause_map = {
            FeedbackCategory.PROMPT: "Prompt lacks clarity or sufficient examples for this task type",
            FeedbackCategory.SKILL: f"{agent_type} skill missing patterns or negative examples for common failures",
            FeedbackCategory.TOOL: "Tool configuration or integration is unreliable",
            FeedbackCategory.ARCHITECTURE: "Architecture patterns insufficiently defined or communicated",
            FeedbackCategory.GOVERNANCE: "Governance rules or escalation thresholds need tuning",
            FeedbackCategory.UNKNOWN: "Root cause unclear; requires manual investigation",
        }

        base_cause = cause_map.get(category, "Unknown root cause")
        return f"{base_cause}. Examples: {sample_text}"

    def compare_to_baseline(
        self,
        current_kpis: dict[str, Any],
        baseline_kpis: dict[str, Any],
    ) -> list[GapPattern]:
        """Compare current KPIs to baseline and generate gap patterns."""
        gaps = []

        comparisons = [
            ("story_completion_rate", 75.0, FeedbackCategory.GOVERNANCE),
            ("first_build_success_rate", 65.0, FeedbackCategory.SKILL),
            ("test_pass_rate", 80.0, FeedbackCategory.SKILL),
            ("coverage_percent", 80.0, FeedbackCategory.SKILL),
        ]

        for metric, threshold, category in comparisons:
            current = current_kpis.get(metric)
            if current is None:
                continue
            if current < threshold:
                gaps.append(
                    GapPattern(
                        category=category,
                        description=f"{metric} below target: {current}% < {threshold}%",
                        occurrence_count=1,
                        severity=FeedbackSeverity.HIGH if current < threshold * 0.8 else FeedbackSeverity.MEDIUM,
                        root_cause_hypothesis=f"{metric} indicates skill or prompt quality issue",
                    )
                )

        return gaps
