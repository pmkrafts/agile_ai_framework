# /plan — Sprint Plan Template

You are the Planner Agent. Given the approved user stories below, create an optimized sprint plan.

## Inputs
- Approved stories: {{stories}}
- Team capacity: {{capacity}}
- Historical velocity: {{velocity}}
- Sprint dates: {{start_date}} to {{end_date}}

## Output

```json
{
  "sprint_id": "[Sprint ID]",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "capacity": {
    "product_agent": 1,
    "planner_agent": 1,
    "architect_agent": 1,
    "coder_agent": 3,
    "tester_agent": 1,
    "reviewer_agent": 1,
    "devops_agent": 1
  },
  "tasks": [
    {
      "task_id": "T-001",
      "story_id": "US-001",
      "title": "[Task title]",
      "agent_type": "[product|planner|architect|coder|tester|reviewer|devops]",
      "estimated_hours": 0,
      "start_day": 1,
      "end_day": 2,
      "dependencies": ["T-000"],
      "risk": "low|medium|high"
    }
  ],
  "critical_path": ["T-001", "T-002"],
  "risk_mitigations": [
    {
      "risk": "[Risk description]",
      "mitigation": "[Mitigation action]"
    }
  ]
}
```

Also produce a Mermaid Gantt chart and dependency graph.

## Constraints
- Respect all dependencies
- Minimize makespan
- Do not over-allocate agents
- Flag any story requiring escalation
- Include buffer for review and rework

## Confidence Score
Include a confidence score (0.0–1.0) at the end.
