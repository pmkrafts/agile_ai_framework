# Plan: Self-Learning Loop for AI-Native Development Framework

**Document Classification:** Implementation Plan  
**Target Audience:** CTO, Lead Engineers, AI Operations Leads  
**Version:** 1.0  
**Effective Date:** June 2026  
**Prerequisite Reading:** Documents 01–16 in `docs/`

---

## 1. Executive Summary

This plan defines the architecture, components, and implementation steps for adding an **automated self-learning loop** to the Agile AI-Driven Software Development Framework.

The self-learning loop continuously analyzes sprint outcomes, identifies failure patterns, proposes improvements to agent prompts/skills/governance rules, applies the changes in a controlled manner, and validates whether the changes improved performance. The loop runs until:

- All KPIs meet their targets, **or**
- No further improvements can be generated, **or**
- A maximum iteration/cost budget is reached, **or**
- Human escalation is required

This capability transforms the framework from a static configuration into an **adaptive system** that improves with every sprint.

---

## 2. Problem Statement

Currently, the framework has:

- ✅ Agent skills and prompts
- ✅ Sprint execution orchestration
- ✅ Cost and KPI monitoring
- ✅ Retrospective templates

But it lacks:

- ❌ Automated analysis of failure patterns across sprints
- ❌ Systematic generation of prompt/skill improvements
- ❌ Controlled application and rollback of changes
- ❌ Re-run validation to confirm improvements
- ❌ A closed feedback loop from outcome → learning → change → validation

Without a self-learning loop, the CTO must manually inspect every retrospective, infer patterns, and update prompts. This creates a bottleneck and slows continuous improvement.

---

## 3. Objectives

| Objective | Target |
|---|---|
| Reduce manual prompt tuning effort | 70% reduction in CTO prompt-review time |
| Improve story completion rate over time | +10 percentage points per quarter |
| Reduce escalation rate over time | -5 percentage points per quarter |
| Reduce cost per story over time | -15% per quarter |
| Increase first-build success rate | +10 percentage points per quarter |
| Maintain human oversight | 100% of proposed changes require CTO approval before application |

---

## 4. Self-Learning Loop Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SELF-LEARNING LOOP                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │   OBSERVE    │────▶│   ANALYZE    │────▶│   PROPOSE    │            │
│  │              │     │              │     │              │            │
│  │ Collect KPIs │     │ Find failure │     │ Generate     │            │
│  │ Agent logs   │     │ patterns     │     │ improvements │            │
│  │ Test results │     │ Root causes  │     │ Prompt edits │            │
│  │ Escalations  │     │ Cost spikes  │     │ Skill edits  │            │
│  └──────────────┘     └──────────────┘     └──────────────┘            │
│         ▲                                           │                   │
│         │                                           ▼                   │
│         │                                    ┌──────────────┐           │
│         │                                    │   APPROVE    │           │
│         │                                    │              │           │
│         │                                    │ CTO review   │           │
│         │                                    │ Accept/      │           │
│         │                                    │ reject/      │           │
│         │                                    │ modify       │           │
│         │                                    └──────────────┘           │
│         │                                           │                   │
│         │                                           ▼                   │
│         │                                    ┌──────────────┐           │
│         │                                    │    APPLY     │           │
│         │                                    │              │           │
│         │                                    │ Update skill │           │
│         │                                    │ Update prompt│           │
│         │                                    │ Update rule  │           │
│         │                                    └──────────────┘           │
│         │                                           │                   │
│         │                                           ▼                   │
│         │                                    ┌──────────────┐           │
│         │                                    │   VALIDATE   │           │
│         │                                    │              │           │
│         │                                    │ Re-run tests │           │
│         │                                    │ Re-run sim   │           │
│         │                                    │ Compare KPIs │           │
│         │                                    └──────────────┘           │
│         │                                           │                   │
│         └───────────────────────────────────────────┘                   │
│                      Keep improvements, rollback failures               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Components to Build

### 5.1 Feedback Collector

**File:** `src/learning/feedback_collector.py`

**Purpose:** Collect structured feedback from every sprint execution.

**Inputs:**
- Sprint state
- Agent messages
- Escalation records
- Test reports
- Review reports
- Cost tracker output
- KPI tracker output

**Outputs:**
- Normalized feedback events
- Per-agent performance scores
- Per-task failure records

**Data Schema:**

```python
class FeedbackEvent:
    event_id: str
    sprint_id: str
    agent_type: str
    task_id: str
    event_type: str  # success, failure, escalation, retry, rejection
    category: str    # prompt, skill, tool, spec, governance
    severity: str    # low, medium, high, critical
    description: str
    context: dict
    timestamp: str
```

### 5.2 Gap Analyzer

**File:** `src/learning/gap_analyzer.py`

**Purpose:** Analyze feedback events to identify recurring patterns and root causes.

**Capabilities:**
- Cluster failures by agent, task type, error message, and context
- Detect recurring escalation reasons
- Identify prompt/skill gaps (e.g., "Coder Agent fails on auth patterns")
- Correlate failures with cost spikes
- Compare current sprint vs. historical baseline

**Outputs:**
- Pattern report
- Root cause hypotheses
- Recommended improvement categories
- Priority-ranked gap list

### 5.3 Improvement Proposer

**File:** `src/learning/improvement_proposer.py`

**Purpose:** Generate concrete improvement proposals for prompts, skills, and governance rules.

**Capabilities:**
- Generate new few-shot examples
- Add negative examples for common anti-patterns
- Suggest prompt clarifications
- Propose new escalation rules
- Recommend tool additions

**Output Format:**

```json
{
  "proposal_id": "PROP-001",
  "target": ".pi/agent/skills/coder-agent.md",
  "category": "few_shot_examples",
  "rationale": "Coder Agent fails on JWT auth patterns 4 times",
  "current_state": "...",
  "proposed_change": "...",
  "expected_impact": {
    "first_build_success_rate": "+10%",
    "escalation_rate": "-5%"
  },
  "confidence": 0.85
}
```

### 5.4 Change Manager

**File:** `src/learning/change_manager.py`

**Purpose:** Safely apply, version, and rollback changes.

**Capabilities:**
- Create a backup of target files
- Apply proposed changes as a patch
- Record change metadata
- Roll back changes if validation fails
- Integrate with git for version control

**Rules:**
- No autonomous changes without CTO approval
- All changes logged in `audit/learning/`
- Rollback must be possible within 1 command

### 5.5 Validation Runner

**File:** `src/learning/validation_runner.py`

**Purpose:** Re-run affected tasks or simulations to validate improvements.

**Capabilities:**
- Run targeted unit tests
- Re-run sprint simulation
- Re-run specific agent tasks with updated prompts
- Compare before/after KPIs
- Detect regressions

**Outputs:**
- Validation report
- KPI comparison
- Pass/fail verdict

### 5.6 Self-Learning Orchestrator

**File:** `src/learning/self_learning_loop.py`

**Purpose:** Coordinate the entire loop.

**Algorithm:**

```python
while not stop_condition_met():
    feedback = collect_feedback(latest_sprint)
    gaps = analyze_gaps(feedback, historical_data)
    proposals = generate_improvements(gaps)
    
    for proposal in proposals:
        if proposal.confidence < threshold:
            escalate_to_cto(proposal)
            continue
            
        approval = request_cto_approval(proposal)
        if approval == "accept":
            apply_change(proposal)
            validation = run_validation(proposal)
            if validation.improved:
                keep_change(proposal)
                update_baseline()
            else:
                rollback_change(proposal)
                log_failure(proposal, validation)
        elif approval == "modify":
            proposal = modify_proposal(proposal)
            retry
        else:
            reject_change(proposal)
```

**Stop Conditions:**

- All KPIs meet targets
- No new gaps identified
- Max iterations reached (default: 10)
- Learning budget exceeded (default: 20% of sprint budget)
- CTO manually stops the loop
- Critical failure requiring governance review

### 5.7 Learning Dashboard

**File:** `src/api/main.py` (extended)

**Purpose:** Surface learning loop activity to CTO.

**Endpoints:**
- `GET /learning/status` — current loop status
- `GET /learning/proposals` — pending and historical proposals
- `POST /learning/proposals/{id}/approve` — approve a proposal
- `POST /learning/proposals/{id}/reject` — reject a proposal
- `GET /learning/impact` — before/after KPI comparisons

---

## 6. Data Stores

### 6.1 Feedback Store

**Location:** `data/feedback/`

Stores raw feedback events per sprint in JSONL format.

### 6.2 Pattern Store

**Location:** `data/patterns/`

Stores aggregated patterns and root cause analyses.

### 6.3 Proposal Store

**Location:** `data/proposals/`

Stores improvement proposals with status (pending/approved/applied/rejected/rolled-back).

### 6.4 Audit Store

**Location:** `audit/learning/`

Stores change logs, approvals, rollbacks, and validation results.

---

## 7. Files to Create and Modify

### New Files

| File | Purpose |
|---|---|
| `src/learning/__init__.py` | Package init |
| `src/learning/feedback_collector.py` | Collect sprint feedback |
| `src/learning/gap_analyzer.py` | Analyze failure patterns |
| `src/learning/improvement_proposer.py` | Generate improvements |
| `src/learning/change_manager.py` | Apply/rollback changes |
| `src/learning/validation_runner.py` | Validate changes |
| `src/learning/self_learning_loop.py` | Orchestrate the loop |
| `src/learning/baseline_tracker.py` | Track before/after baselines |
| `tests/learning/test_feedback_collector.py` | Unit tests |
| `tests/learning/test_gap_analyzer.py` | Unit tests |
| `tests/learning/test_improvement_proposer.py` | Unit tests |
| `tests/learning/test_change_manager.py` | Unit tests |
| `tests/learning/test_validation_runner.py` | Unit tests |
| `tests/learning/test_self_learning_loop.py` | Integration tests |
| `.pi/agent/skills/learning-agent.md` | Skill for the learning agent |
| `docs/18-self-learning-loop-implementation.md` | Implementation guide |

### Modified Files

| File | Change |
|---|---|
| `src/graph/sprint_graph.py` | Emit structured feedback after each sprint |
| `src/agents/base.py` | Add feedback emission helpers |
| `src/monitoring/kpi_tracker.py` | Expose historical trends |
| `src/api/main.py` | Add learning dashboard endpoints |
| `requirements.txt` | Add clustering/analysis libraries (scikit-learn, numpy) |
| `README.md` | Document self-learning loop usage |
| `docs/16-how-to-use-this-project.md` | Add self-learning section |

---

## 8. Implementation Phases

### Phase 1: Foundation (Week 1)

- Create `src/learning/` package structure
- Implement `FeedbackCollector`
- Implement `BaselineTracker`
- Add feedback emission to `SprintGraph`
- Add tests

**Deliverable:** Feedback collection operational after each sprint.

### Phase 2: Analysis (Week 2)

- Implement `GapAnalyzer`
- Implement pattern clustering
- Add root cause hypothesis generation
- Connect to feedback store
- Add tests

**Deliverable:** Automated gap analysis report after each sprint.

### Phase 3: Proposal Generation (Week 3)

- Implement `ImprovementProposer`
- Add prompt/skill diff generation
- Implement confidence scoring
- Add CTO approval workflow
- Add tests

**Deliverable:** System generates ranked improvement proposals.

### Phase 4: Change Management (Week 4)

- Implement `ChangeManager`
- Add backup/apply/rollback logic
- Integrate with git
- Add audit logging
- Add tests

**Deliverable:** Safe, reversible change application.

### Phase 5: Validation (Week 5)

- Implement `ValidationRunner`
- Add before/after KPI comparison
- Add regression detection
- Add tests

**Deliverable:** Automated validation of proposed improvements.

### Phase 6: Orchestration (Week 6)

- Implement `SelfLearningLoop`
- Add stop conditions and budgets
- Add dashboard endpoints
- End-to-end integration test

**Deliverable:** Fully operational self-learning loop.

---

## 9. Governance and Safety

### 9.1 Human Approval Requirements

- All prompt/skill changes require CTO approval
- Governance rule changes require committee approval
- Auto-apply is prohibited for production-facing changes
- Rollback must be possible within 1 command

### 9.2 Budget Controls

- Learning loop has its own budget cap (default 20% of sprint budget)
- Validation runs are metered
- Cost spikes trigger automatic pause

### 9.3 Audit Trail

Every learning loop action is logged:

- Feedback collected
- Gap identified
- Proposal generated
- Approval/rejection
- Change applied
- Validation result
- Rollback action

### 9.4 Stop Conditions

The loop must stop when:

- KPIs meet targets
- No improvements generated
- Budget exhausted
- Max iterations reached
- Human override
- Critical regression detected

---

## 10. Success Criteria

| Metric | Baseline | Target (Month 3) |
|---|---|---|
| Manual prompt tuning time | 100% | 30% |
| Story completion rate | 75% | 85% |
| Escalation rate | 10% | 5% |
| Cost per story | $10 | $8 |
| First-build success rate | 65% | 80% |
| Proposals requiring no modification | — | ≥60% |
| Rollback rate | — | ≤10% |

---

## 11. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Loop proposes harmful changes | High | Human approval gate; automated rollback; validation before keep |
| Loop runs forever | Medium | Max iterations and budget caps |
| Loop consumes too much budget | High | Separate learning budget; cost monitoring |
| Loop generates low-quality proposals | Medium | Confidence threshold; escalation to CTO |
| Changes cause regression | High | Before/after validation; rollback on failure |
| Loop optimizes wrong metrics | Medium | Align KPIs with business outcomes; governance review |

---

## 12. Example Usage

### 12.1 Run After a Sprint

```bash
python -m src.learning.self_learning_loop \
  --sprint-id Sprint-001 \
  --max-iterations 5 \
  --budget-usd 20.0 \
  --auto-approve-low-risk false
```

### 12.2 Review Proposals

```bash
curl http://localhost:8000/learning/proposals
```

### 12.3 Approve a Proposal

```bash
curl -X POST http://localhost:8000/learning/proposals/PROP-001/approve \
  -H "Content-Type: application/json" \
  -d '{"approver": "cto@company.com"}'
```

### 12.4 View Learning Impact

```bash
curl http://localhost:8000/learning/impact
```

---

## 13. Next Steps

1. **Approve this plan** with the governance committee.
2. **Create the `src/learning/` package** and Phase 1 components.
3. **Wire feedback collection** into `SprintGraph`.
4. **Implement one agent skill** improvement end-to-end as a proof of concept.
5. **Run the loop** against simulated sprints.
6. **Measure impact** and iterate on the loop design.

---

**End of Plan**
