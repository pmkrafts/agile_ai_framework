"""Change manager for the self-learning loop."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import structlog
import yaml

from src.core.feedback import ImprovementProposal, ValidationResult

logger = structlog.get_logger()


class ChangeManager:
    """Safely applies, versions, and rolls back improvements."""

    def __init__(self, audit_dir: str = "audit/learning"):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir = self.audit_dir / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def apply_change(self, proposal: ImprovementProposal) -> bool:
        """Apply a proposed change to the target file."""
        target_path = Path(proposal.target_file)
        if not target_path.exists():
            logger.warning("target_file_not_found", target=proposal.target_file)
            return False

        # Create backup
        backup_path = self._create_backup(target_path, proposal.proposal_id)

        try:
            with open(target_path, "a", encoding="utf-8") as f:
                f.write(f"\n\n{proposal.proposed_change}\n")

            proposal.status = "applied"
            self._log_change(proposal, backup_path, "applied")
            logger.info("change_applied", proposal_id=proposal.proposal_id, target=proposal.target_file)
            return True
        except Exception as e:
            logger.error("change_application_failed", proposal_id=proposal.proposal_id, error=str(e))
            self.rollback_change(proposal)
            return False

    def rollback_change(self, proposal: ImprovementProposal) -> bool:
        """Rollback a previously applied change."""
        target_path = Path(proposal.target_file)
        backup_path = self.backup_dir / f"{target_path.name}.{proposal.proposal_id}.bak"

        if not backup_path.exists():
            logger.warning("backup_not_found", proposal_id=proposal.proposal_id)
            return False

        try:
            shutil.copy2(backup_path, target_path)
            proposal.status = "rolled_back"
            self._log_change(proposal, backup_path, "rolled_back")
            logger.info("change_rolled_back", proposal_id=proposal.proposal_id)
            return True
        except Exception as e:
            logger.error("rollback_failed", proposal_id=proposal.proposal_id, error=str(e))
            return False

    def _create_backup(self, target_path: Path, proposal_id: str) -> Path:
        """Create a backup of the target file."""
        backup_path = self.backup_dir / f"{target_path.name}.{proposal_id}.bak"
        shutil.copy2(target_path, backup_path)
        return backup_path

    def _log_change(
        self,
        proposal: ImprovementProposal,
        backup_path: Path,
        action: str,
    ) -> None:
        """Log change action to audit store."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "proposal_id": proposal.proposal_id,
            "action": action,
            "target_file": proposal.target_file,
            "backup_path": str(backup_path),
            "approved_by": proposal.approved_by,
        }

        log_file = self.audit_dir / f"{action}.yaml"
        existing = []
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                existing = yaml.safe_load(f) or []

        existing.append(log_entry)
        with open(log_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(existing, f)

    def record_validation(self, validation: ValidationResult) -> None:
        """Record validation result in audit store."""
        log_file = self.audit_dir / "validations.yaml"
        existing = []
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                existing = yaml.safe_load(f) or []

        existing.append(validation.model_dump())
        with open(log_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(existing, f)
