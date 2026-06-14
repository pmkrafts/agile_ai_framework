"""Baseline tracker for the self-learning loop."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.monitoring.kpi_tracker import SprintKPIs


class BaselineTracker:
    """Tracks baseline KPIs for before/after comparisons."""

    def __init__(self, storage_path: str = "data/baselines.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.baselines: list[dict[str, Any]] = []
        self._load()

    def record_baseline(self, kpis: SprintKPIs) -> None:
        """Record a new baseline."""
        self.baselines.append(kpis.to_dict())
        self._save()

    def get_latest_baseline(self) -> dict[str, Any]:
        """Get the most recent baseline."""
        if not self.baselines:
            return {}
        return self.baselines[-1]

    def get_baseline_for_sprint(self, sprint_id: str) -> dict[str, Any] | None:
        """Get baseline for a specific sprint."""
        for baseline in self.baselines:
            if baseline.get("sprint_id") == sprint_id:
                return baseline
        return None

    def _load(self) -> None:
        """Load baselines from disk."""
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self.baselines = json.load(f)

    def _save(self) -> None:
        """Save baselines to disk."""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.baselines, f, indent=2)

    def get_trend(self, metric_path: str, n_sprints: int = 5) -> list[Any]:
        """Get trend for a metric over last N sprints."""
        values = []
        for baseline in self.baselines[-n_sprints:]:
            value = baseline
            for key in metric_path.split("."):
                value = value.get(key, {}) if isinstance(value, dict) else None
                if value is None:
                    break
            values.append(value)
        return values
