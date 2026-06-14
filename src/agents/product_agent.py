"""Product Agent implementation."""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, TaskStatus


class ProductAgent(BaseAgent):
    """Translates CEO problem statements into PRDs and user stories."""

    def __init__(self, instance_id: str | None = None):
        super().__init__("product_agent", instance_id)

    async def execute(self, task: AgentTask, context: dict[str, Any]) -> AgentMessage:
        """Generate PRD and user stories from problem statement."""
        self.log_task_start(task)

        problem_statement = context.get("problem_statement", "")
        interview_answers = context.get("interview_answers", {})

        # Simulate PRD generation
        prd = self._generate_prd(problem_statement, interview_answers)
        stories = self._generate_stories(prd)

        confidence = 0.92 if interview_answers else 0.75

        self.mark_task_status(task, TaskStatus.COMPLETE)
        self.log_task_complete(task, confidence)

        return AgentMessage(
            from_agent=self.name,
            to_agent="cto",
            message_type=MessageType.STATUS_UPDATE,
            priority="normal" if confidence >= 0.8 else "high",
            payload={
                "task_id": task.task_id,
                "content": "PRD and user stories generated",
                "artifacts": ["prd.md", "stories.json"],
                "confidence": confidence,
                "metadata": {
                    "prd": prd,
                    "stories": stories,
                    "story_count": len(stories),
                },
            },
        )

    def _generate_prd(self, problem: str, answers: dict[str, Any]) -> str:
        """Generate a PRD (simulated)."""
        return f"""# PRD: {problem[:50]}

## Problem Statement
{problem}

## Goals
- Deliver working software that solves the stated problem
- Meet all acceptance criteria
- Pass quality fortress gates

## Target Users
- {answers.get('Target user', 'End users')}

## Functional Requirements
1. Core feature implementation
2. Input validation
3. Error handling

## Non-Functional Requirements
- Performance: p99 latency < 200ms
- Security: OAuth2, input sanitization
- Scalability: 10K concurrent users

## Definition of Done
- [ ] Code implemented
- [ ] Tests pass with ≥80% coverage
- [ ] Security scan clean
- [ ] CTO architecture approval
- [ ] CEO acceptance
"""

    def _generate_stories(self, prd: str) -> list[dict[str, Any]]:
        """Generate user stories (simulated)."""
        return [
            {
                "story_id": "US-001",
                "title": "As a user, I want to authenticate so that I can access the system",
                "acceptance_criteria": [
                    "Given valid credentials, When I login, Then I receive a JWT token",
                    "Given invalid credentials, When I login, Then I receive a 401 error",
                ],
            },
            {
                "story_id": "US-002",
                "title": "As a user, I want to create a resource so that I can store data",
                "acceptance_criteria": [
                    "Given valid input, When I POST to /resources, Then it returns 201",
                    "Given invalid input, When I POST to /resources, Then it returns 400",
                ],
            },
        ]
