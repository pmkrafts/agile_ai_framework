"""Improvement proposer for the self-learning loop."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import structlog

from src.core.feedback import FeedbackCategory, GapPattern, ImprovementProposal

logger = structlog.get_logger()


class ImprovementProposer:
    """Generates improvement proposals from gap patterns."""

    def __init__(self, pi_dir: str = ".pi"):
        self.pi_dir = Path(pi_dir)
        self.skill_dir = self.pi_dir / "agent" / "skills"
        self.prompt_dir = self.pi_dir / "prompts"

    def generate_proposals(self, gaps: list[GapPattern], max_proposals: int = 5) -> list[ImprovementProposal]:
        """Generate improvement proposals from gap patterns."""
        proposals: list[ImprovementProposal] = []

        for gap in gaps[:max_proposals]:
            proposal = self._generate_for_gap(gap)
            if proposal:
                proposals.append(proposal)

        logger.info("proposals_generated", count=len(proposals))
        return proposals

    def _generate_for_gap(self, gap: GapPattern) -> ImprovementProposal | None:
        """Generate a proposal for a single gap."""
        if gap.category == FeedbackCategory.SKILL and gap.agent_type:
            return self._generate_skill_proposal(gap)
        elif gap.category == FeedbackCategory.PROMPT:
            return self._generate_prompt_proposal(gap)
        elif gap.category == FeedbackCategory.GOVERNANCE:
            return self._generate_governance_proposal(gap)
        elif gap.category == FeedbackCategory.ARCHITECTURE:
            return self._generate_architecture_proposal(gap)
        elif gap.category == FeedbackCategory.TOOL:
            return self._generate_tool_proposal(gap)
        return None

    def _generate_skill_proposal(self, gap: GapPattern) -> ImprovementProposal | None:
        """Generate a skill improvement proposal."""
        agent_type = gap.agent_type
        if not agent_type:
            return None

        # Skill files use hyphens (e.g., coder-agent.md)
        skill_file_name = agent_type.replace("_", "-")
        skill_file = self.skill_dir / f"{skill_file_name}.md"
        if not skill_file.exists():
            return None

        current_content = skill_file.read_text(encoding="utf-8")

        # Generate a few-shot example based on the gap description
        example = self._generate_few_shot_example(gap)

        proposed_change = f"""
## Additional Few-Shot Example (Auto-generated)

{example}

## Additional Escalation Rule (Auto-generated)
- Escalate if the same failure pattern occurs more than once: {gap.description}
"""

        return ImprovementProposal(
            target_file=str(skill_file),
            category=FeedbackCategory.SKILL,
            rationale=f"Recurring failures in {agent_type}: {gap.description}",
            current_state=current_content[-500:] if len(current_content) > 500 else current_content,
            proposed_change=proposed_change,
            expected_impact={
                "escalation_rate": "-5%",
                "first_build_success_rate": "+5%",
            },
            confidence=self._calculate_confidence(gap),
            related_gaps=[gap.pattern_id],
        )

    def _generate_prompt_proposal(self, gap: GapPattern) -> ImprovementProposal | None:
        """Generate a prompt improvement proposal."""
        prompt_file = self.prompt_dir / "prd-template.md"
        if not prompt_file.exists():
            return None

        current_content = prompt_file.read_text(encoding="utf-8")
        proposed_change = """
## Additional Rule
- All acceptance criteria must explicitly state the error response for invalid input.
- Include at least one negative scenario per feature.
"""

        return ImprovementProposal(
            target_file=str(prompt_file),
            category=FeedbackCategory.PROMPT,
            rationale=f"Prompt-related gaps: {gap.description}",
            current_state=current_content[-500:] if len(current_content) > 500 else current_content,
            proposed_change=proposed_change,
            expected_impact={
                "story_completion_rate": "+5%",
                "escalation_rate": "-3%",
            },
            confidence=self._calculate_confidence(gap),
            related_gaps=[gap.pattern_id],
        )

    def _generate_governance_proposal(self, gap: GapPattern) -> ImprovementProposal | None:
        """Generate a governance improvement proposal."""
        target = ".pi/agent/AGENTS.md"
        target_path = Path(target)
        if not target_path.exists():
            return None

        current_content = target_path.read_text(encoding="utf-8")
        proposed_change = f"""
## Additional Escalation Trigger (Auto-generated)
- {gap.description}
"""

        return ImprovementProposal(
            target_file=target,
            category=FeedbackCategory.GOVERNANCE,
            rationale=f"Governance gap: {gap.description}",
            current_state=current_content[-500:] if len(current_content) > 500 else current_content,
            proposed_change=proposed_change,
            expected_impact={
                "escalation_rate": "-5%",
                "governance_compliance": "+2%",
            },
            confidence=self._calculate_confidence(gap),
            related_gaps=[gap.pattern_id],
        )

    def _generate_architecture_proposal(self, gap: GapPattern) -> ImprovementProposal | None:
        """Generate an architecture improvement proposal."""
        return ImprovementProposal(
            target_file="docs/architecture-patterns.md",
            category=FeedbackCategory.ARCHITECTURE,
            rationale=f"Architecture gap: {gap.description}",
            current_state="Architecture patterns are defined in Architect Agent skill and ADRs",
            proposed_change="Add explicit architecture pattern examples for common integration scenarios to organizational memory.",
            expected_impact={
                "first_build_success_rate": "+5%",
            },
            confidence=self._calculate_confidence(gap) * 0.8,
            related_gaps=[gap.pattern_id],
        )

    def _generate_tool_proposal(self, gap: GapPattern) -> ImprovementProposal | None:
        """Generate a tool improvement proposal."""
        return ImprovementProposal(
            target_file="src/config/providers.yaml",
            category=FeedbackCategory.TOOL,
            rationale=f"Tool gap: {gap.description}",
            current_state="Provider configuration includes retry logic defaults",
            proposed_change="Increase retry attempts and add exponential backoff for external API calls.",
            expected_impact={
                "escalation_rate": "-3%",
            },
            confidence=self._calculate_confidence(gap) * 0.8,
            related_gaps=[gap.pattern_id],
        )

    def _generate_few_shot_example(self, gap: GapPattern) -> str:
        """Generate a few-shot example based on gap description."""
        return f"""### Example: Handling {gap.description[:50]}

**Input:** [Typical input that triggers this gap]

**Incorrect Output:**
```
[Example of failure described in gap]
```

**Correct Output:**
```
[Example of successful handling]
```

**Key points:**
- Validate input before processing
- Escalate if pattern repeats
- Log context for retrospective
"""

    def _calculate_confidence(self, gap: GapPattern) -> float:
        """Calculate confidence score for a proposal."""
        base = 0.7
        if gap.occurrence_count >= 3:
            base += 0.15
        elif gap.occurrence_count >= 2:
            base += 0.05

        if gap.severity.value == "critical":
            base += 0.05
        elif gap.severity.value == "low":
            base -= 0.1

        return min(0.95, base)
