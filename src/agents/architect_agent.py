"""Architect Agent implementation."""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.core.message import AgentMessage, MessageType
from src.core.state import AgentTask, TaskStatus


class ArchitectAgent(BaseAgent):
    """Designs system architecture, APIs, and database schemas."""

    def __init__(self, instance_id: str | None = None):
        super().__init__("architect_agent", instance_id)

    async def execute(self, task: AgentTask, context: dict[str, Any]) -> AgentMessage:
        """Generate architecture design and ADRs."""
        self.log_task_start(task)

        prd = context.get("prd", "")
        tech_stack = context.get("tech_stack", "Python/FastAPI + PostgreSQL")

        design = self._generate_design(prd, tech_stack)
        confidence = 0.88

        self.mark_task_status(task, TaskStatus.COMPLETE)
        self.log_task_complete(task, confidence)

        return AgentMessage(
            from_agent=self.name,
            to_agent="cto",
            message_type=MessageType.STATUS_UPDATE,
            priority="normal" if confidence >= 0.8 else "high",
            payload={
                "task_id": task.task_id,
                "content": "Architecture design and ADRs generated",
                "artifacts": ["architecture.md", "adr-001.md", "openapi.yaml"],
                "confidence": confidence,
                "metadata": {"design": design},
            },
        )

    def _generate_design(self, prd: str, tech_stack: str) -> dict[str, Any]:
        """Generate architecture design (simulated)."""
        return {
            "tech_stack": tech_stack,
            "components": [
                {"name": "API Layer", "type": "FastAPI", "responsibility": "HTTP endpoints"},
                {"name": "Service Layer", "type": "Business Logic", "responsibility": "Domain logic"},
                {"name": "Data Layer", "type": "PostgreSQL", "responsibility": "Persistence"},
            ],
            "api_spec": {
                "openapi": "3.0.0",
                "paths": {
                    "/auth/login": {"post": {"summary": "User login"}},
                    "/resources": {"post": {"summary": "Create resource"}},
                },
            },
            "database_schema": {
                "users": {"id": "UUID PK", "email": "VARCHAR UNIQUE", "password_hash": "VARCHAR"},
                "resources": {"id": "UUID PK", "owner_id": "UUID FK", "data": "JSONB"},
            },
            "adrs": [
                {
                    "id": "ADR-001",
                    "title": "Use FastAPI for API layer",
                    "decision": "FastAPI provides async support and automatic OpenAPI docs",
                    "consequences": "Positive: high performance, type safety. Negative: team must learn async patterns.",
                }
            ],
        }
