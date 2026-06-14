# How to Use This Project

**Document Classification:** User Guide  
**Target Audience:** CTO, Lead Engineers, DevOps, Operations Managers  
**Version:** 1.0  
**Effective Date:** June 2026  
**Prerequisite Reading:** Documents 01–15 in `docs/`

---

## 1. What This Project Is

This repository is a **reference implementation** of the Agile AI-Driven Software Development Framework. It provides:

- A governed, multi-agent AI development team architecture
- Pi agent harness configuration (skills, prompts, governance rules)
- Agent orchestration code with LangGraph-style state machines
- A 5-stage automated quality fortress
- Cost tracking, KPI dashboards, and monitoring scaffolding
- Governance documents and compliance templates
- Infrastructure-as-code for local development
- A sample pilot project

It is designed to be cloned, configured, and extended for your organization.

---

## 2. Quick Start

### 2.1 Prerequisites

Before you begin, ensure you have:

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.11+ | Required for orchestration code |
| Git | Latest | For version control |
| Docker + Docker Compose | Latest | For local infrastructure |
| LLM API accounts | — | Anthropic, OpenAI, and/or Moonshot (Kimi) |
| Cloud account | — | AWS, GCP, or Azure for production |

### 2.2 Clone and Set Up

```bash
# Clone the repository
git clone <repository-url>
cd agile_ai_framework

# Run the setup script
./scripts/setup.sh
```

The setup script will:

1. Create a Python virtual environment (`.venv`)
2. Install production and development dependencies
3. Create required directories (`data/`, `audit/`, `logs/`, `pilots/`)
4. Copy `.env.example` to `.env`
5. Install pre-commit hooks (if available)
6. Run smoke tests

### 2.3 Configure Environment

Edit `.env` with your actual API keys and settings:

```bash
# Required: at least one LLM provider
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
KIMI_API_KEY=your_kimi_key

# Framework settings
DEFAULT_PROVIDER_STRATEGY=hybrid
SPRINT_BUDGET_USD=100
MIN_TEST_COVERAGE=80
```

> **Security note:** Never commit `.env` to version control. It is already in `.gitignore`.

---

## 3. Validate the Framework

### 3.1 Run the Sprint Simulation

The simulation executes a full AI-native sprint using simulated agent outputs:

```bash
python -m src.simulations.sprint_simulation
```

You should see:

- PRD generation
- Sprint planning
- Architecture design
- Coder/Test/Review cycles for each story
- Deployment preparation
- Cost summary and KPI dashboard

### 3.2 Run the Test Suite

```bash
# Smoke and unit tests
python -m pytest tests/smoke tests/unit -v

# With coverage
python -m pytest tests/unit --cov=src --cov-report=term
```

### 3.3 Start the API

```bash
uvicorn src.api.main:app --reload
```

Then open:

- `http://localhost:8000/health` — health check
- `http://localhost:8000/dashboard` — KPI dashboard

---

## 4. Start a Local Infrastructure Stack

```bash
cd infrastructure
docker-compose up -d
```

This starts:

| Service | URL | Purpose |
|---|---|---|
| Framework API | `http://localhost:8000` | Framework services |
| ChromaDB | `http://localhost:8001` | Vector database for RAG |
| LangGraph | `http://localhost:8123` | Orchestration platform |
| Grafana | `http://localhost:3000` | Monitoring dashboards |

To stop:

```bash
docker-compose down
```

---

## 5. Create a New Project

### 5.1 Using the Project Template

```bash
# Copy the template
cp -r templates/project-template pilots/my-new-project

# Edit the README
cd pilots/my-new-project
```

Update:

- Project name and ID
- Client name
- Tech stack
- Data sensitivity level
- AI disclosure level

### 5.2 Define the Business Problem

Document the problem in the project's `README.md` or `docs/prd.md`.

### 5.3 Score the Project

Use the pilot scoring matrix from `docs/14-master-execution-plan.md`:

| Criteria | Weight | Score (1–5) | Weighted |
|---|---|---|---|
| Scope clarity | 20% | | |
| Tech stack familiarity | 15% | | |
| Client risk tolerance | 15% | | |
| Timeline flexibility | 15% | | |
| Data sensitivity | 10% | | |
| Integration complexity | 10% | | |
| UI complexity | 10% | | |
| Strategic learning value | 5% | | |

**Rule:** Only proceed if scope clarity and tech stack familiarity score ≥4.

---

## 6. Run an AI-Native Sprint

### 6.1 Day 0: Backlog Refinement

Use Pi with the `/interview` prompt template to conduct a structured CEO interview:

```bash
pi /interview
```

Then generate the PRD:

```bash
pi /prd
```

The Product Agent will output `docs/prd.md` with user stories and acceptance criteria.

### 6.2 CTO Validates PRD

Review `docs/prd.md` and approve or request changes.

### 6.3 Day 0: Sprint Planning

Use the `/plan` prompt template:

```bash
pi /plan
```

The Planner Agent outputs:

- `sprint-plan.json`
- `gantt.mmd`
- Dependency graph
- Resource allocation

### 6.4 Days 1–4: Execution

Run the orchestration graph:

```bash
python -m src.graph.sprint_graph --project my-new-project
```

This executes:

1. Architect Agent designs system
2. Coder Agents implement stories in parallel
3. Tester Agents generate and run tests
4. Reviewer Agents perform code review

### 6.5 Day 5: Review and Deployment

1. DevOps Agent deploys to staging
2. CEO reviews demo
3. CTO approves production deployment
4. DevOps Agent executes blue/green deployment
5. Automated retrospective is captured

---

## 7. Customize Agent Behavior

### 7.1 Change Provider Strategy

Edit `.pi/agent/AGENTS.md` and `src/config/providers.yaml`:

| Strategy | Use Case |
|---|---|
| `default` | Claude 4 / GPT-4o for all coding |
| `kimi` | Kimi for all coding |
| `hybrid` | Kimi for coding, Claude/o3 for reasoning |

### 7.2 Modify Agent Skills

Edit files in `.pi/agent/skills/` to:

- Add new escalation rules
- Change output formats
- Add tool integrations
- Update operational protocols

### 7.3 Add Prompt Templates

Create new files in `.pi/prompts/` and reference them with `/template-name` in Pi.

### 7.4 Add Real LLM Integration

Current agent implementations in `src/agents/*.py` use simulated outputs. To connect to real LLMs, update each agent's `execute()` method to call the provider API:

```python
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# Example for Coder Agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
response = await llm.ainvoke([SystemMessage(content=skill_prompt), HumanMessage(content=task_prompt)])
```

> A future update will add a `src/llm/` provider abstraction layer.

---

## 8. Governance Workflow

### 8.1 Establish the Committee

1. Review and sign `governance/charter.md`
2. Add approved signatures
3. Schedule monthly governance meetings

### 8.2 Client Disclosure

For each client project:

1. Choose disclosure level (full / partial / minimal)
2. Add the appropriate clause from `governance/client-disclosure.md` to the SOW
3. Obtain client signature

### 8.3 Human Approval Gates

Before proceeding at each gate, ensure the designated approver signs off:

| Gate | Approver | Artifact |
|---|---|---|
| Project kickoff | CEO | Signed SOW + AI disclosure |
| Architecture approval | CTO | Approved ADR |
| Production deployment | CTO | Security scan report + change log |
| Client acceptance | CEO | Demo recording + acceptance criteria |
| Budget override | CEO | Cost overrun justification |

### 8.4 Escalations

When an agent escalates:

1. Review the escalation in the queue
2. Apply the appropriate playbook from `governance/escalation-runbook.md`
3. Document resolution in `audit/sprints/{sprint_id}/`
4. Update agent prompts if recurrence is likely

---

## 9. Monitor Costs and KPIs

### 9.1 Cost Tracking

Costs are tracked automatically in `src/monitoring/cost_tracker.py`. View summary:

```python
from src.monitoring.cost_tracker import CostTracker
tracker = CostTracker()
print(tracker.get_summary())
```

### 9.2 KPI Dashboard

Use the API endpoint:

```bash
curl http://localhost:8000/dashboard
```

Or programmatically:

```python
from src.monitoring.kpi_tracker import KPITracker, SprintKPIs
tracker = KPITracker()
print(tracker.dashboard_summary())
```

### 9.3 Set Alerts

Cost alerts are configured via `.env`:

```env
SPRINT_BUDGET_USD=100
COST_ALERT_THRESHOLDS=0.5,0.75,0.9,1.0
```

When a threshold is crossed, logs are written and can be routed to PagerDuty/Opsgenie.

---

## 10. Add Real LLM Providers

### 10.1 Anthropic (Claude)

1. Create account at https://console.anthropic.com
2. Generate API key
3. Add to `.env`: `ANTHROPIC_API_KEY=...`

### 10.2 OpenAI

1. Create account at https://platform.openai.com
2. Generate API key
3. Add to `.env`: `OPENAI_API_KEY=...`

### 10.3 Moonshot AI (Kimi)

1. Create account at https://platform.moonshot.cn
2. Generate API key
3. Add to `.env`:

```env
KIMI_API_KEY=...
KIMI_BASE_URL=https://api.moonshot.cn/v1
```

### 10.4 Verify Provider Connection

```python
from src.config.providers import load_provider_config
config = load_provider_config()
print(config)
```

---

## 11. Common Workflows

### 11.1 Add a New Agent Skill

1. Create `.pi/agent/skills/my-skill.md`
2. Define role, inputs, outputs, tools, protocol
3. Reference it in `AGENTS.md` or agent assignments
4. Test with Pi using `/my-skill`

### 11.2 Add a New Prompt Template

1. Create `.pi/prompts/my-template.md`
2. Add instructions and output format
3. Use `/my-template` in Pi

### 11.3 Run a Pilot Project

1. Copy `templates/project-template/` to `pilots/{pilot-name}/`
2. Define problem and PRD
3. Score the project
4. Run simulation or real sprint
5. Measure KPIs
6. Convene governance committee for Go/No-Go

### 11.4 Scale to Multiple Projects

1. Confirm pilot KPIs meet targets
2. Clone agent templates for additional instances
3. Increase `capacity` in sprint plans
4. Add Escalation Triage Agent
5. Train secondary technical lead

---

## 12. Run the Self-Learning Loop

After a sprint completes, the self-learning loop can analyze outcomes and propose improvements.

### 12.1 Run After Simulation

```bash
python -m src.simulations.sprint_simulation --learning
```

### 12.2 Run Directly

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
    result = await loop.run_full_pipeline(
        context={"problem_statement": "..."},
        cto_approver="cto@company.com",
    )
    print(result)

asyncio.run(main())
```

### 12.3 Review Proposals

```bash
curl http://localhost:8000/learning/proposals
curl http://localhost:8000/learning/impact
```

### 12.4 Approve or Reject Proposals

```bash
# Approve
curl -X POST http://localhost:8000/learning/proposals/PROP-001/approve \
  -H "Content-Type: application/json" \
  -d '{"approver": "cto@company.com"}'

# Reject
curl -X POST http://localhost:8000/learning/proposals/PROP-001/reject
```

### 12.5 Inspect Audit Trail

```bash
ls audit/learning/
cat audit/learning/applied.yaml
cat audit/learning/validations.yaml
```

See `docs/18-self-learning-loop-implementation.md` for full details.

## 13. Troubleshooting

| Problem | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| Pi cannot find skills | Wrong directory structure | Ensure `.pi/agent/skills/` exists |
| Simulation fails | Missing `.env` | Copy `.env.example` to `.env` |
| Docker ports conflict | Services already running | Change ports in `docker-compose.yml` or stop conflicting services |
| Tests fail | Framework files missing | Re-run `./scripts/setup.sh` |
| Cost exceeds budget | Token-heavy prompts | Enable caching, use smaller models for simple tasks |
| Agent escalates frequently | Ambiguous requirements | Improve PRD and acceptance criteria |

---

## 13. Project File Reference

| Path | Purpose |
|---|---|
| `.pi/agent/AGENTS.md` | Governance charter |
| `.pi/agent/SYSTEM.md` | Universal agent instructions |
| `.pi/agent/skills/` | Agent skill definitions |
| `.pi/prompts/` | Reusable prompt templates |
| `src/agents/` | Agent orchestration code |
| `src/core/` | Core state, messages, feedback models |
| `src/graph/sprint_graph.py` | Sprint state machine |
| `src/learning/` | Self-learning loop |
| `src/memory/vector_store.py` | RAG memory |
| `src/monitoring/` | Cost and KPI tracking |
| `src/simulations/` | Sprint simulations |
| `src/api/main.py` | FastAPI service |
| `.github/workflows/ci.yml` | CI/CD pipeline |
| `infrastructure/` | Docker/Terraform configs |
| `governance/` | Governance documents |
| `pilots/` | Pilot project workspace |
| `templates/` | Project templates |
| `tests/` | Test suites |
| `docs/` | Framework documentation |

---

## 14. Next Steps After Setup

1. ✅ Run simulation: `python -m src.simulations.sprint_simulation`
2. ✅ Run simulation with learning: `python -m src.simulations.sprint_simulation --learning`
3. ✅ Run tests: `python -m pytest tests/smoke tests/unit tests/learning -v`
4. ✅ Configure API keys in `.env`
5. ✅ Start local infrastructure: `cd infrastructure && docker-compose up -d`
6. ✅ Select or create a pilot project in `pilots/`
7. ✅ Run first real sprint
8. ✅ Run self-learning loop after sprint
9. ✅ Review KPIs and governance committee Go/No-Go

---

## 15. Getting Help

- Review `docs/14-master-execution-plan.md` for detailed operational procedures
- Review `docs/15-implementation-report.md` for what was built
- Review `docs/18-self-learning-loop-implementation.md` for self-learning loop details
- Check `governance/escalation-runbook.md` for incident response
- Open an issue in the repository for bugs or questions

---

**End of How-To Guide**
