"""Feedback collector for the self-learning loop."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import structlog

from src.core.feedback import FeedbackCategory, FeedbackEvent, FeedbackEventType, FeedbackSeverity
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, SprintState, TaskStatus

logger = structlog.get_logger()


class FeedbackCollector:
    """Collects structured feedback from sprint executions."""

    def __init__(self, storage_dir: str = "data/feedback"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.events: list[FeedbackEvent] = []

    def collect_from_sprint(
        self,
        state: SprintState,
        cost_data: dict[str, Any],
        kpi_data: dict[str, Any],
    ) -> list[FeedbackEvent]:
        """Collect feedback from a completed sprint."""
        events: list[FeedbackEvent] = []

        # Collect task-level feedback
        for task in state.tasks:
            events.extend(self._collect_from_task(task, state.sprint_id))

        # Collect escalation feedback
        for escalation in state.escalations:
            events.append(
                FeedbackEvent(
                    sprint_id=state.sprint_id,
                    agent_type=escalation.get("from_agent", "unknown"),
                    task_id=escalation.get("task_id", "unknown"),
                    event_type=FeedbackEventType.ESCALATION,
                    category=FeedbackCategory.GOVERNANCE,
                    severity=FeedbackSeverity.HIGH,
                    description=escalation.get("reason", "Escalation occurred"),
                    context=escalation,
                )
            )

        # Collect cost feedback
        if cost_data.get("utilization", 0) > 1.0:
            events.append(
                FeedbackEvent(
                    sprint_id=state.sprint_id,
                    agent_type="system",
                    task_id="budget",
                    event_type=FeedbackEventType.COST_SPIKE,
                    category=FeedbackCategory.GOVERNANCE,
                    severity=FeedbackSeverity.HIGH,
                    description=f"Budget exceeded: ${cost_data.get('total_cost_usd', 0)} / ${cost_data.get('budget_usd', 0)}",
                    context=cost_data,
                )
            )

        # Collect KPI feedback
        delivery = kpi_data.get("latest", {}).get("delivery", {})
        if delivery.get("story_completion_rate", 100) < 75:
            events.append(
                FeedbackEvent(
                    sprint_id=state.sprint_id,
                    agent_type="system",
                    task_id="kpi",
                    event_type=FeedbackEventType.FAILURE,
                    category=FeedbackCategory.GOVERNANCE,
                    severity=FeedbackSeverity.MEDIUM,
                    description=f"Story completion rate below target: {delivery.get('story_completion_rate')}%",
                    context=delivery,
                )
            )

        if delivery.get("test_pass_rate", 100) < 80:
            events.append(
                FeedbackEvent(
                    sprint_id=state.sprint_id,
                    agent_type="tester_agent",
                    task_id="kpi",
                    event_type=FeedbackEventType.FAILURE,
                    category=FeedbackCategory.SKILL,
                    severity=FeedbackSeverity.MEDIUM,
                    description=f"Test pass rate below target: {delivery.get('test_pass_rate')}%",
                    context=delivery,
                )
            )

        self.events.extend(events)
        self._persist_events(events, state.sprint_id)
        logger.info("feedback_collected", sprint_id=state.sprint_id, event_count=len(events))
        return events

    def _collect_from_task(self, task: AgentTask, sprint_id: str) -> list[FeedbackEvent]:
        """Collect feedback from a single task."""
        events: list[FeedbackEvent] = []

        if task.status == TaskStatus.FAILED:
            events.append(
                FeedbackEvent(
                    sprint_id=sprint_id,
                    agent_type=task.agent_type,
                    task_id=task.task_id,
                    event_type=FeedbackEventType.FAILURE,
                    category=self._infer_category(task),
                    severity=FeedbackSeverity.HIGH,
                    description=f"Task {task.task_id} failed",
                    context={"blockers": task.blockers, "confidence": task.confidence},
                )
            )

        if task.status == TaskStatus.ESCALATED:
            events.append(
                FeedbackEvent(
                    sprint_id=sprint_id,
                    agent_type=task.agent_type,
                    task_id=task.task_id,
                    event_type=FeedbackEventType.ESCALATION,
                    category=self._infer_category(task),
                    severity=FeedbackSeverity.HIGH,
                    description=f"Task {task.task_id} escalated",
                    context={"blockers": task.blockers, "confidence": task.confidence},
                )
            )

        if task.confidence > 0 and task.confidence < 0.8:
            events.append(
                FeedbackEvent(
                    sprint_id=sprint_id,
                    agent_type=task.agent_type,
                    task_id=task.task_id,
                    event_type=FeedbackEventType.RETRY,
                    category=self._infer_category(task),
                    severity=FeedbackSeverity.MEDIUM,
                    description=f"Low confidence output: {task.confidence}",
                    context={"confidence": task.confidence},
                )
            )

        return events

    def _infer_category(self, task: AgentTask) -> FeedbackCategory:
        """Infer feedback category from task type."""
        category_map = {
            "coder_agent": FeedbackCategory.SKILL,
            "tester_agent": FeedbackCategory.SKILL,
            "reviewer_agent": FeedbackCategory.SKILL,
            "architect_agent": FeedbackCategory.ARCHITECTURE,
            "planner_agent": FeedbackCategory.PROMPT,
            "product_agent": FeedbackCategory.PROMPT,
            "devops_agent": FeedbackCategory.TOOL,
        }
        return category_map.get(task.agent_type, FeedbackCategory.UNKNOWN)

    def _persist_events(self, events: list[FeedbackEvent], sprint_id: str) -> None:
        """Persist events to disk."""
        file_path = self.storage_dir / f"{sprint_id}.jsonl"
        with open(file_path, "a", encoding="utf-8") as f:
            for event in events:
                f.write(event.model_dump_json() + "\n")

    def load_events(self, sprint_id: str | None = None) -> list[FeedbackEvent]:
        """Load feedback events from disk."""
        if sprint_id:
            file_path = self.storage_dir / f"{sprint_id}.jsonl"
            if not file_path.exists():
                return []
            with open(file_path, "r", encoding="utf-8") as f:
                return [FeedbackEvent.model_validate_json(line) for line in f if line.strip()]

        events = []
        for file_path in self.storage_dir.glob("*.jsonl"):
            with open(file_path, "r", encoding="utf-8") as f:
                events.extend(
                    FeedbackEvent.model_validate_json(line)
                    for line in f
                    if line.strip()
                )
        return events

    def collect_from_agent_message(
        self,
        message: AgentMessage,
        sprint_id: str,
    ) -> list[FeedbackEvent]:
        """Collect feedback from an agent message."""
        events: list[FeedbackEvent] = []

        if message.message_type == MessageType.ESCALATION:
            events.append(
                FeedbackEvent(
                    sprint_id=sprint_id,
                    agent_type=message.from_agent,
                    task_id=message.payload.task_id or "unknown",
                    event_type=FeedbackEventType.ESCALATION,
                    category=FeedbackCategory.GOVERNANCE,
                    severity=FeedbackSeverity.HIGH,
                    description=message.payload.content,
                    context={"blockers": message.payload.blockers},
                )
            )

        if message.payload.confidence > 0 and message.payload.confidence < 0.8:
            events.append(
                FeedbackEvent(
                    sprint_id=sprint_id,
                    agent_type=message.from_agent,
                    task_id=message.payload.task_id or "unknown",
                    event_type=FeedbackEventType.RETRY,
                    category=FeedbackCategory.PROMPT,
                    severity=FeedbackSeverity.MEDIUM,
                    description=f"Low confidence: {message.payload.confidence}",
                    context={"confidence": message.payload.confidence},
                )
            )

        self.events.extend(events)
        return events
