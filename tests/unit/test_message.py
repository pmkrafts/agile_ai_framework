"""Unit tests for message protocol."""

import json

import pytest

from src.core.message import AgentMessage, MessageType, Priority, create_escalation


def test_agent_message_creation():
    """Test creating an agent message."""
    msg = AgentMessage(
        from_agent="coder_agent:001",
        to_agent="reviewer_agent:001",
        message_type=MessageType.STATUS_UPDATE,
        payload={
            "task_id": "T-001",
            "content": "Implementation complete",
            "confidence": 0.92,
        },
    )
    assert msg.from_agent == "coder_agent:001"
    assert msg.to_agent == "reviewer_agent:001"
    assert msg.message_type == MessageType.STATUS_UPDATE
    assert msg.payload.confidence == 0.92


def test_message_serialization():
    """Test message JSON serialization."""
    msg = AgentMessage(
        from_agent="product_agent:001",
        to_agent="cto",
        message_type=MessageType.STATUS_UPDATE,
        payload={"task_id": "T-PRD-001", "content": "PRD generated", "confidence": 0.95},
    )
    json_str = msg.to_json()
    data = json.loads(json_str)
    assert data["from_agent"] == "product_agent:001"
    assert data["message_type"] == "status_update"


def test_create_escalation():
    """Test escalation message creation."""
    escalation = create_escalation(
        from_agent="coder_agent:001",
        reason="Stuck on API integration",
        details="External API returns 500 errors",
        priority=Priority.HIGH,
        task_id="T-001",
    )
    assert escalation.to_agent == "cto"
    assert escalation.message_type == MessageType.ESCALATION
    assert escalation.priority == Priority.HIGH
    assert "Stuck on API integration" in escalation.payload.content
