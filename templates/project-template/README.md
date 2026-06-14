# Project Template: {{project_name}}

**Project ID:** {{project_id}}  
**Start Date:** {{start_date}}  
**Sprint Cycle:** 1 week

---

## 1. Project Metadata

| Field | Value |
|---|---|
| Client | [Client Name] |
| CEO Owner | [CEO Name] |
| CTO Owner | [CTO Name] |
| Tech Stack | [Stack] |
| Data Sensitivity | [Low/Medium/High] |
| AI Disclosure Level | [Full/Partial/Minimal] |

## 2. Directory Structure

```
{{project_id}}/
├── docs/
│   ├── prd.md
│   ├── architecture/
│   └── decisions/
├── src/
├── tests/
├── infrastructure/
└── README.md
```

## 3. Workflow

1. Product Agent generates `docs/prd.md`
2. CTO validates PRD
3. Architect Agent generates `docs/architecture/`
4. Planner Agent creates sprint plan
5. Coder/Test/Review agents execute in parallel
6. DevOps Agent prepares deployment
7. CTO approves production deployment
8. CEO accepts deliverable

## 4. Governance

All human approval gates must be documented in `governance/approvals/`.

## 5. Getting Started

```bash
# Initialize project
./scripts/init-project.sh {{project_id}}

# Start first sprint
python -m src.graph.sprint_graph --project {{project_id}}
```
