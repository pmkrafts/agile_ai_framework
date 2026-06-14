"""Unit tests for change manager."""

from pathlib import Path

from src.core.feedback import FeedbackCategory, GapPattern, ImprovementProposal
from src.learning.change_manager import ChangeManager
from src.learning.improvement_proposer import ImprovementProposer


def test_apply_and_rollback(tmp_path):
    """Test applying and rolling back a change."""
    target_file = tmp_path / "test_skill.md"
    target_file.write_text("# Original content\n")

    change_manager = ChangeManager(audit_dir=str(tmp_path / "audit"))
    proposal = ImprovementProposal(
        target_file=str(target_file),
        category=FeedbackCategory.SKILL,
        rationale="Test change",
        current_state="# Original content",
        proposed_change="\n\n# Added content\n",
        confidence=0.9,
    )

    applied = change_manager.apply_change(proposal)
    assert applied is True
    assert "# Added content" in target_file.read_text()

    rolled_back = change_manager.rollback_change(proposal)
    assert rolled_back is True
    assert "# Added content" not in target_file.read_text()
