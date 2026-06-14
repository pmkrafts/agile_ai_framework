# Self-Learning Loop Implementation Guide

**Document Classification:** Implementation Guide  
**Target Audience:** CTO, Lead Engineers, AI Operations Leads  
**Version:** 1.0  
**Effective Date:** June 2026  
**Prerequisite Reading:** `docs/17-self-learning-loop-plan.md`

---

## 1. What Was Implemented

The self-learning loop is now operational as part of the AI-Native Development Framework. It adds a closed feedback cycle that:

1. **Observes** sprint outcomes and agent behavior
2. **Analyzes** feedback for recurring patterns and KPI gaps
3. **Proposes** improvements to agent skills, prompts, and governance rules
4. **Approves** changes via CTO (or auto-approves low-risk changes if configured)
5. **Applies** changes safely with backups and audit logging
6. **Validates** changes by re-running simulations and comparing KPIs
7. **Rolls back** changes that cause regression

---

## 2. Components Implemented

### 2.1 Core Feedback Models (`src/core/feedback.py`)

Shared data models used by agents and the learning loop:

- `FeedbackEvent` — individual success/failure/escalation events
- `FeedbackEventType` — event type enum
- `FeedbackCategory` — category enum (prompt, skill, tool, governance, architecture)
- `FeedbackSeverity` — severity enum
- `GapPattern` — recurring pattern identified by analysis
- `ImprovementProposal` — proposed change to a file
- `ValidationResult` — before/after KPI comparison

### 2.2 Feedback Collector (`src/learning/feedback_collector.py`)

Collects structured feedback from:

- Sprint state (task statuses, confidence scores, blockers)
- Agent messages (escalations, low-confidence outputs)
- Cost data (budget exceeded)
- KPI data (below-target metrics)

Feedback is persisted to `data/feedback/{sprint_id}.jsonl`.

### 2.3 Gap Analyzer (`src/learning/gap_analyzer.py`)

Identifies recurring patterns by:

- Grouping events by category and agent type
- Counting occurrences
- Inferring severity and root cause hypotheses
- Comparing current KPIs to baseline thresholds

### 2.4 Improvement Proposer (`src/learning/improvement_proposer.py`)

Generates concrete proposals:

- **Skill proposals:** Adds few-shot examples and escalation rules to `.pi/agent/skills/{agent}.md`
- **Prompt proposals:** Adds clarifications to `.pi/prompts/*.md`
- **Governance proposals:** Adds escalation triggers to `.pi/agent/AGENTS.md`
- **Architecture proposals:** Suggests pattern additions to organizational memory
- **Tool proposals:** Suggests provider/retries configuration changes

### 2.5 Change Manager (`src/learning/change_manager.py`)

Safely applies and rolls back changes:

- Creates backups before changes
- Appends proposed changes to target files
- Logs all actions to `audit/learning/`
- Restores from backup on rollback

### 2.6 Validation Runner (`src/learning/validation_runner.py`)

Validates proposals by:

- Re-running the sprint simulation
- Comparing before/after KPIs
- Detecting regressions
- Returning a pass/fail verdict

### 2.7 Self-Learning Orchestrator (`src/learning/self_learning_loop.py`)

Coordinates the full loop with:

- Configurable max iterations and budget
- Human approval workflow
- Auto-approval for low-risk changes
- Stop conditions (KPI targets, budget, max iterations, regression)

### 2.8 Baseline Tracker (`src/learning/baseline_tracker.py`)

Records and retrieves baseline KPIs for comparison.

### 2.9 Learning Agent Skill (`.pi/agent/skills/learning-agent.md`)

Pi skill documenting the learning agent role and operational protocol.

### 2.10 API Endpoints (`src/api/main.py`)

New endpoints:

- `GET /learning/status`
- `GET /learning/proposals`
- `POST /learning/proposals/{id}/approve`
- `POST /learning/proposals/{id}/reject`
- `GET /learning/impact`

---

## 3. How to Run

### 3.1 Run Sprint Simulation with Learning Loop

```bash
python -m src.simulations.sprint_simulation --learning
```

### 3.2 Run Self-Learning Loop Directly

```python
import asyncio
from src.learning.self_learning_loop import SelfLearningLoop
from src.learning.models import LearningLoopConfig

async def main():
    loop = SelfLearningLoop(
        config=LearningLoopConfig(
            max_iterations=5,
            budget_usd=10.0,
            auto_approve_low_risk=True,
        )
    )
    context = {
        "problem_statement": "Build a simple task management API",
        "capacity": {"coder_agent": 2, "tester_agent": 1, "reviewer_agent": 1},
        "target": "staging",
        "code_reference": "learning-run",
    }
    result = await loop.run_full_pipeline(context, cto_approver="cto@company.com")
    print(result)

asyncio.run(main())
```

### 3.3 Run Tests

```bash
python -m pytest tests/learning tests/unit -v
```

---

## 4. Configuration

Edit `LearningLoopConfig` or pass it to `SelfLearningLoop`:

| Setting | Default | Description |
|---|---|---|
| `max_iterations` | 10 | Max learning iterations per run |
| `budget_usd` | 20.0 | Max learning budget |
| `min_proposal_confidence` | 0.6 | Minimum confidence to propose |
| `auto_approve_low_risk` | False | Auto-approve prompt/skill changes |
| `low_risk_categories` | `["prompt", "skill"]` | Categories eligible for auto-approval |
| `max_proposals_per_iteration` | 3 | Max proposals per iteration |
| `stop_on_budget_exceeded` | True | Stop if learning budget exceeded |
| `stop_on_critical_regression` | True | Stop if regression detected |

---

## 5. Observing the Loop

### 5.1 Feedback Events

```bash
ls data/feedback/
cat data/feedback/SIM-001.jsonl
```

### 5.2 Proposals

Proposals are stored in memory and via API. To view:

```bash
curl http://localhost:8000/learning/proposals
```

### 5.3 Audit Trail

```bash
ls audit/learning/
cat audit/learning/applied.yaml
cat audit/learning/validations.yaml
```

### 5.4 Baselines

```bash
cat data/baselines.json
```

---

## 6. Current Limitations

1. **Simulated agents:** The built-in agent implementations use simulated outputs and do not yet emit rich feedback automatically. Real LLM integration will generate more actionable feedback.
2. **Auto-approval:** Governance rule changes still require CTO approval; auto-approval is limited to prompt/skill changes.
3. **Validation:** Re-runs the same simulation scenario. In production, validation should run against historical test suites or A/B sprints.
4. **Proposal quality:** Generated examples are templates. Real LLM-based proposal generation will produce higher-quality, context-specific improvements.
5. **No email/Slack notifications:** CTO approval requests are logged; real notification channels should be added.

---

## 7. Next Enhancements

1. Add real LLM-based proposal generation
2. Implement CTO notification/approval UI
3. Add A/B testing framework for proposals
4. Integrate with Pi to auto-apply approved prompt/skill changes
5. Add learning loop metrics to Grafana dashboard
6. Implement proposal ranking using cost/benefit analysis

---

## 8. Safety Notes

- All changes are backed up before application
- Rollback is one command away
- Governance rule changes require explicit approval
- Budget caps prevent runaway costs
- Regression detection stops the loop automatically

---

**End of Implementation Guide**
