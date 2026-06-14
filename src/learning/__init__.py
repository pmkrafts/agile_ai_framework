"""Self-learning loop package.

Note: Import submodules directly to avoid circular imports.
For example:
    from src.learning.self_learning_loop import SelfLearningLoop
    from src.learning.feedback_collector import FeedbackCollector
"""

from src.learning.baseline_tracker import BaselineTracker
from src.learning.feedback_collector import FeedbackCollector
from src.learning.gap_analyzer import GapAnalyzer
from src.learning.improvement_proposer import ImprovementProposer
from src.learning.models import LearningLoopConfig

__all__ = [
    "BaselineTracker",
    "FeedbackCollector",
    "GapAnalyzer",
    "ImprovementProposer",
    "LearningLoopConfig",
]
