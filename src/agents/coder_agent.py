"""Coder Agent implementation."""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, TaskStatus


class CoderAgent(BaseAgent):
    """Implements features according to specifications."""

    def __init__(self, instance_id: str | None = None):
        super().__init__("coder_agent", instance_id)

    async def execute(self, task: AgentTask, context: dict[str, Any]) -> AgentMessage:
        """Implement a user story using TDD."""
        self.log_task_start(task)

        story = context.get("story", {})
        spec = context.get("api_spec", {})

        # Simulate implementation
        code = self._generate_code(story, spec)
        tests = self._generate_tests(story)
        confidence = 0.85

        self.mark_task_status(task, TaskStatus.COMPLETE)
        self.log_task_complete(task, confidence)

        return AgentMessage(
            from_agent=self.name,
            to_agent="reviewer_agent",
            message_type=MessageType.STATUS_UPDATE,
            priority="normal" if confidence >= 0.8 else "high",
            payload={
                "task_id": task.task_id,
                "content": f"Implementation complete for {story.get('title', 'story')}",
                "artifacts": ["src/feature.py", "tests/test_feature.py"],
                "confidence": confidence,
                "metadata": {
                    "code": code,
                    "tests": tests,
                },
            },
        )

    def _generate_code(self, story: dict[str, Any], spec: dict[str, Any]) -> str:
        """Generate implementation code (simulated)."""
        return f"""# Implementation for: {story.get('title', 'feature')}

def handle_request(data: dict) -> dict:
    \"\"\"Handle the main request.\"\"\"
    if not data:
        raise ValueError("Input data is required")
    return {{"status": "success", "data": data}}
"""

    def _generate_tests(self, story: dict[str, Any]) -> str:
        """Generate unit tests (simulated)."""
        return f"""# Tests for: {story.get('title', 'feature')}

def test_handle_request_success():
    result = handle_request({{"key": "value"}})
    assert result["status"] == "success"

def test_handle_request_invalid():
    try:
        handle_request(None)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
"""
