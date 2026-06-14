"""Smoke tests for framework initialization."""

import os

import pytest


def test_environment_template_exists():
    """Ensure .env.example exists."""
    assert os.path.exists(".env.example")


def test_pi_config_exists():
    """Ensure Pi configuration files exist."""
    assert os.path.exists(".pi/agent/AGENTS.md")
    assert os.path.exists(".pi/agent/SYSTEM.md")


def test_agent_skills_exist():
    """Ensure all agent skills exist."""
    agents = [
        "product-agent",
        "planner-agent",
        "architect-agent",
        "coder-agent",
        "tester-agent",
        "reviewer-agent",
        "devops-agent",
        "learning-agent",
    ]
    for agent in agents:
        assert os.path.exists(f".pi/agent/skills/{agent}.md")


def test_ci_workflow_exists():
    """Ensure CI/CD workflow exists."""
    assert os.path.exists(".github/workflows/ci.yml")


def test_governance_documents_exist():
    """Ensure governance documents exist."""
    assert os.path.exists("governance/charter.md")
    assert os.path.exists("governance/client-disclosure.md")
    assert os.path.exists("governance/escalation-runbook.md")


def test_learning_package_exists():
    """Ensure self-learning loop package exists."""
    assert os.path.exists("src/learning/__init__.py")
    assert os.path.exists("src/learning/self_learning_loop.py")
    assert os.path.exists("src/learning/feedback_collector.py")
    assert os.path.exists("src/learning/gap_analyzer.py")
    assert os.path.exists("src/learning/improvement_proposer.py")
    assert os.path.exists("src/learning/change_manager.py")
    assert os.path.exists("src/learning/validation_runner.py")
    assert os.path.exists("src/learning/baseline_tracker.py")
