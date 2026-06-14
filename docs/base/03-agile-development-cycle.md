# Agile Development Cycle (Phases)

## Automated Sprint Mechanics for AI-Native Teams

**Document Classification:** Operational Playbook  
**Target Audience:** CTO, Scrum Masters (Transitioning), AI Operations Leads  
**Prerequisite Reading:** Document 02 — Organizational Structure & AI Agent Roles

---

## 1. Cycle Overview

The AI-native Agile cycle preserves the **ceremonial structure of Scrum** (backlog refinement, sprint planning, execution, review, retrospective, deployment) but automates the **mechanical and cognitive labor** within each phase. Human executives (CEO, CTO) provide **direction and governance**; AI agents perform **execution and validation**.

A standard sprint duration is **5 business days** (one calendar week), compared to 2 weeks for traditional human teams. The compression is possible because:

- Agents work **continuously** without context-switching overhead
- Testing happens **in parallel** with development, not after
- Code review is **instantaneous** (no queueing for reviewer availability)
- Deployment is **fully automated** with rollback capability

| Phase | Duration | Human Touchpoints | Automated Activities |
|---|---|---|---|
| Backlog & Refinement | 2–4 hrs (Day 0) | CEO presents problem; CTO validates | Product Agent decomposes; generates PRD |
| Sprint Planning | 1–2 hrs (Day 0) | CTO approves plan | Planner Agent allocates tasks; builds dependency graph |
| Execution | 3.5 days (Days 1–4) | CTO resolves escalations only | Coder, Tester, Reviewer agents work in parallel |
| Review & Retrospective | 2–3 hrs (Day 5) | CEO accepts/rejects; CTO reviews metrics | Auto-demo generation; lesson capture |
| Deployment | 1–2 hrs (Day 5) | CTO approves production push | DevOps Agent deploys; monitoring activates |

---

## 2. Phase 1: Backlog & Refinement

### 2.1 Objective

Transform the CEO's high-level business problem into a **machine-executable product backlog** with clearly defined user stories, acceptance criteria, and technical constraints.

### 2.2 Process Flow

```
CEO (Problem Statement)
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 1: Structured Interview           │
│  Product Agent asks 8–12 clarifying     │
│  questions from standard template       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 2: PRD Generation                 │
│  Product Agent produces markdown PRD    │
│  with: problem, users, features, NFRs,  │
│  constraints, success metrics           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 3: CTO Validation                 │
│  CTO reviews for technical feasibility, │
│  scope realism, and alignment with      │
│  architectural standards                │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 4: Story Decomposition            │
│  Product Agent breaks PRD into user     │
│  stories with Gherkin-style acceptance  │
│  criteria (Given/When/Then)             │
└─────────────────────────────────────────┘
    │
    ▼
BACKLOG (Ready for Sprint Planning)
```

### 2.3 Key Artifacts

| Artifact | Owner | Format | Validation Rule |
|---|---|---|---|
| **Product Requirements Document (PRD)** | Product Agent | Markdown | CTO approval required |
| **User Story Map** | Product Agent | Jira/Linear issues + Mermaid diagram | Each story has ≤8 story points equivalent |
| **Acceptance Criteria** | Product Agent | Gherkin syntax (Given/When/Then) | Must be machine-testable (automatable) |
| **Definition of Done** | Product Agent | Checklist | Includes code, tests, docs, review |
| **Risk Register** | Product Agent | Markdown table | Identifies technical and business risks |

### 2.4 Acceptance Criteria Template

All acceptance criteria must follow **Gherkin syntax** to enable automated test generation:

```gherkin
Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given a registered user with email "user@example.com" and password "SecurePass123"
    When the user submits the login form
    Then the response status code should be 200
    And the response should contain a valid JWT token
    And the token should expire in 24 hours

  Scenario: Failed login with invalid password
    Given a registered user with email "user@example.com" and password "WrongPass"
    When the user submits the login form
    Then the response status code should be 401
    And the response should contain error message "Invalid credentials"
```

The Tester Agent can parse these scenarios directly and generate corresponding test code.

---

## 3. Phase 2: Sprint Planning

### 3.1 Objective

Create an **optimized execution plan** that allocates tasks to agent instances, maps dependencies, identifies critical paths, and establishes delivery milestones.

### 3.2 Process Flow

```
Backlog (Approved Stories)
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 1: Story Analysis                 │
│  Planner Agent analyzes each story for: │
│  • Complexity (agent-hours estimate)    │
│  • Dependencies (what must finish first)│
│  • Resource needs (which agent types)   │
│  • Risk level (novelty, integration)    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 2: Constraint Modeling            │
│  Planner builds optimization model:     │
│  • Variables: task-agent assignments    │
│  • Constraints: dependencies, capacity  │
│  • Objective: minimize makespan         │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 3: Plan Generation                │
│  Output: Gantt chart, task list per     │
│  agent, dependency graph, risk mitigations
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 4: CTO Approval                   │
│  CTO reviews for realism, critical path │
│  risks, and resource overallocation     │
└─────────────────────────────────────────┘
    │
    ▼
SPRINT PLAN (Ready for Execution)
```

### 3.3 Key Artifacts

| Artifact | Owner | Format | Contents |
|---|---|---|---|
| **Sprint Plan** | Planner Agent | JSON + Gantt visualization | Task assignments, start/end times, dependencies |
| **Dependency Graph** | Planner Agent | Mermaid/Graphviz diagram | Visual representation of task interdependencies |
| **Risk Mitigation Plan** | Planner Agent | Markdown table | Identified risks + contingency actions |
| **Resource Allocation Map** | Planner Agent | Table | Agent instance → task mapping |

### 3.4 Dynamic Replanning

The Planner Agent **continuously monitors** execution progress and triggers replanning when:

- An agent completes a task **early** (reassigns next task from critical path)
- An agent is **blocked** >15 minutes (reassigns dependent tasks, escalates blocker)
- A task **fails review** (inserts rework task, adjusts downstream schedule)
- A **new story** is added mid-sprint (evaluates impact, proposes scope adjustment)

---

## 4. Phase 3: Execution

### 4.1 Objective

Agents execute their assigned tasks in **parallel streams** with continuous integration, testing, and review. This is the core value-delivery phase.

### 4.2 Parallel Execution Streams

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXECUTION PHASE (Days 1–4)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Stream A: Architecture  Stream B: Development    Stream C: Quality    │
│  ──────────────────────  ────────────────────     ─────────────────    │
│                                                                         │
│  Architect Agent         Coder Agent 1            Tester Agent          │
│  ├── Design API          ├── Story A (auth)       ├── Gen tests A      │
│  ├── Design DB schema    ├── Unit tests A         ├── Run tests A      │
│  └── Write ADRs          └── Submit PR            ├── Gen tests B      │
│                         Coder Agent 2             ├── Run tests B      │
│  Stream D: Review         ├── Story B (payments)  └── Coverage report  │
│  ────────────────         ├── Unit tests B                            │
│                           └── Submit PR         Stream E: DevOps      │
│  Reviewer Agent                                        ─────────────   │
│  ├── Review PR A (auto)                              DevOps Agent     │
│  ├── Review PR B (auto)                              ├── Setup env    │
│  └── Security scan                                   ├── Configure CI │
│                                                      └── Prep deploy   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Coder Agent Execution Loop

Each Coder Agent follows a **strict TDD loop** with built-in quality gates:

```python
execution_loop:
    while task_not_complete:
        # Step 1: Understand
        read_user_story()
        read_acceptance_criteria()
        read_api_spec()
        query_codebase_rag()  # Find similar patterns
        
        # Step 2: Test First
        write_failing_tests()
        run_tests()  # Confirm they fail
        
        # Step 3: Implement
        write_implementation_code()
        
        # Step 4: Validate
        run_tests()
        if all_tests_pass:
            run_linter()
            run_type_checker()
            confidence_score = self_assess()
            submit_for_review(confidence_score)
            break
        else:
            attempt += 1
            if attempt > 3:
                escalate_to_cto("test_failure_cascade")
                break
            debug_and_fix()
```

### 4.4 Reviewer Agent Quality Gate

Every submitted pull request must pass the **three-pass review**:

| Pass | Tools | Gate Criteria | Auto-Action on Failure |
|---|---|---|---|
| **Static Analysis** | Semgrep, Bandit, ESLint, Pylint | Zero critical/high findings; ≤3 minor issues | Reject with findings report |
| **Semantic Review** | LLM-based logic analysis | No logic errors; matches specification; no race conditions | Request changes with explanation |
| **Architectural Compliance** | Custom rules engine | Follows approved ADRs; uses authorized dependencies; no anti-patterns | Reject with architectural violation notice |

A PR must achieve **"Approve"** from all three passes to proceed to deployment.

### 4.5 Escalation During Execution

The following conditions trigger **automatic escalation** to the CTO:

```yaml
escalation_triggers:
  time_based:
    - agent_stalled: "No output > 30 minutes"
    - retry_exhausted: "Same task failed > 3 times"
    
  quality_based:
    - test_coverage_drop: "Coverage decreased > 10% from baseline"
    - security_finding: "Critical or high severity vulnerability detected"
    - performance_regression: "Latency increased > 20% from benchmark"
    
  dependency_based:
    - circular_dependency: "Agents waiting on each other"
    - external_service_down: "Third-party API unavailable > 15 minutes"
    
  business_based:
    - scope_ambiguity: "Implementation contradicts specification"
    - requirement_conflict: "Two stories have mutually exclusive implementations"
```

---

## 5. Phase 4: Review & Retrospective

### 5.1 Objective

Validate delivered increments against acceptance criteria, capture organizational learning, and feed improvements into the next sprint.

### 5.2 Sprint Review (Demo)

| Activity | Owner | Duration | Output |
|---|---|---|---|
| **Demo Generation** | DevOps Agent | Automated | Running application in staging environment |
| **Feature Walkthrough** | Product Agent | 15 min | Guided demo script with screen captures |
| **CEO Evaluation** | CEO | 15 min | Accept/reject per story; change requests |
| **CTO Technical Review** | CTO | 15 min | Code quality assessment; security posture |
| **Metrics Presentation** | All Agents | 15 min | Velocity, coverage, bug count, cost report |

### 5.3 Automated Retrospective

Unlike human retrospectives (which rely on subjective recall), the AI retrospective is **data-driven and automated**:

| Metric | Source | Insight Generated |
|---|---|---|
| **Velocity Trend** | Planner Agent | Stories completed vs. planned; trend analysis |
| **Quality Metrics** | Reviewer + Tester Agents | Bug density, review rejection rate, coverage trend |
| **Efficiency Metrics** | System logs | Agent utilization %, idle time, handoff delays |
| **Cost Metrics** | DevOps Agent | Token consumption per story, compute cost per feature |
| **Escalation Analysis** | CTO logs | Escalation frequency by type; resolution time |

The retrospective output is a **structured improvement plan** with specific actions for the next sprint:

```json
{
  "sprint_id": "Sprint-42",
  "summary": {
    "stories_planned": 8,
    "stories_completed": 7,
    "stories_rejected": 1,
    "escalations": 2,
    "total_cost_usd": 127.50
  },
  "improvements": [
    {
      "category": "prompt_engineering",
      "issue": "Coder Agent struggled with API integration patterns",
      "action": "Add 3 few-shot examples for REST API consumption to Coder prompt",
      "owner": "CTO"
    },
    {
      "category": "tooling",
      "issue": "Security scan flagged 2 false positives",
      "action": "Update Semgrep rules to exclude internal utility functions",
      "owner": "CTO"
    }
  ]
}
```

---

## 6. Phase 5: Deployment

### 6.1 Objective

Deliver the approved increment to production with **zero-downtime deployment**, comprehensive monitoring, and instant rollback capability.

### 6.2 Deployment Pipeline

```
Approved Code
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 1: Build                          │
│  • Build container image                │
│  • Run unit + integration tests         │
│  • Generate SBOM (Software Bill of Mat.)│
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 2: Staging Deployment             │
│  • Deploy to staging environment        │
│  • Run smoke tests                      │
│  • Run performance benchmark            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 3: CTO Approval Gate              │
│  CTO reviews staging results            │
│  Approves/rejects production push       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 4: Production Deployment          │
│  • Blue/green deployment                │
│  • Gradual traffic shift (10% → 50% → 100%)
│  • Health checks at each stage          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 5: Monitoring Activation          │
│  • Error rate alerts (>0.1% triggers page)
│  • Latency alerts (p99 > 200ms triggers page)
│  • Throughput baselines established     │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 6: Rollback Readiness             │
│  • Previous version kept warm           │
│  • One-command rollback prepared        │
│  • Rollback tested in staging           │
└─────────────────────────────────────────┘
```

### 6.3 Deployment Artifacts

| Artifact | Owner | Purpose |
|---|---|---|
| **Container Image** | DevOps Agent | Immutable deployment artifact |
| **SBOM** | DevOps Agent | Security audit trail; dependency vulnerability tracking |
| **Deployment Manifest** | DevOps Agent | Kubernetes/Docker Compose configuration |
| **Monitoring Dashboard** | DevOps Agent | Real-time visibility into production health |
| **Runbook** | DevOps Agent | Incident response procedures; rollback commands |
| **Cost Report** | DevOps Agent | Infrastructure cost for this deployment |

---

## 7. Governance Layer: Cross-Cutting Rules

Across all phases, a **Governance Layer** enforces rules that no agent can override:

| Rule Category | Examples | Enforcement |
|---|---|---|
| **Security** | No hardcoded secrets; all APIs use OAuth2; SQL injection prevention patterns | SAST tools + Reviewer Agent |
| **Compliance** | GDPR data handling; SOC2 logging requirements; HIPAA encryption | Automated compliance checks |
| **Code Quality** | 80% minimum test coverage; max cyclomatic complexity of 10; consistent formatting | CI pipeline gates |
| **Cost Control** | Token budget per sprint; compute cost cap per deployment | DevOps Agent monitoring + alerts |
| **Documentation** | All public APIs documented; ADRs for major decisions; README updates | Reviewer Agent checklist |

---

## 8. Sprint Timeline: Visual Summary

```
Day 0 (Monday)          Day 1–2 (Tue–Wed)       Day 3–4 (Thu–Fri)       Day 5 (Friday)
─────────────────       ─────────────────       ─────────────────       ───────────────
                                                                                
┌───────────────┐       ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ 09:00 CEO     │       │               │       │               │       │ 09:00 Auto    │
│     Problem   │       │  Architect    │       │  Coder Agents │       │     Demo Gen  │
│     Presentation      │  designs system       │  implement    │       │               │
│               │       │               │       │               │       │ 10:00 Sprint  │
│ 10:00 Product │       │  Coder Agents │       │  Tester Agent │       │     Review    │
│     Agent     │       │  begin coding │       │  tests        │       │     (CEO/CTO) │
│     Interview │       │               │       │               │       │               │
│               │       │  Tester Agent │       │  Reviewer     │       │ 11:00 Retro-  │
│ 12:00 PRD     │       │  generates    │       │  reviews code │       │     spective  │
│     Generated │       │  tests        │       │               │       │               │
│               │       │               │       │               │       │ 14:00 Deploy- │
│ 14:00 CTO     │       │               │       │               │       │     ment      │
│     Validates │       │               │       │               │       │     (CTO      │
│               │       │               │       │               │       │     approval) │
│ 15:00 Planner │       │               │       │               │       │               │
│     Creates   │       │               │       │               │       │ 16:00 Sprint  │
│     Sprint Plan       │               │       │               │       │     Complete  │
│               │       │               │       │               │       │               │
│ 16:00 CTO     │       │               │       │               │       │               │
│     Approves  │       │               │       │               │       │               │
│     Plan      │       │               │       │               │       │               │
└───────────────┘       └───────────────┘       └───────────────┘       └───────────────┘
   BACKLOG &               EXECUTION (Early)      EXECUTION (Late)      REVIEW & DEPLOY
   PLANNING                                                                
```

---

## 9. Continuous Improvement

After each sprint, the framework itself is improved through:

1. **Prompt Evolution:** CTO refines agent prompts based on failure patterns
2. **Tool Updates:** New versions of orchestration frameworks, SAST tools, and base models are evaluated
3. **Governance Tuning:** Rules are tightened or relaxed based on quality metrics
4. **Knowledge Base Growth:** Project memory (vector database) expands with each completed story
5. **Benchmarking:** Performance metrics are compared against previous sprints and industry baselines

This **meta-learning loop** ensures that the AI team becomes more effective over time — unlike human teams, where knowledge walks out the door when people leave.
