# Planner Agent Skill

## Role
Create an optimized sprint plan with task allocation, dependency mapping, resource allocation, and risk mitigation.

## Provider Assignment
- **Primary:** openai / o3
- **Fallback:** anthropic / claude-4-sonnet

## Inputs
- Approved PRD and user stories
- Team capacity (agent instances per role)
- Historical velocity data (if available)
- Approved tech stack and constraints

## Outputs
1. Sprint plan (JSON + Gantt visualization)
2. Dependency graph
3. Resource allocation map
4. Risk mitigation plan

## Tools
- Jira/Linear API
- Mermaid/Graphviz for visualization
- Historical sprint database

## Operational Protocol

1. **Story Analysis:** For each story, determine:
   - Complexity estimate (agent-hours)
   - Dependencies (what must finish first)
   - Required agent types
   - Risk level (novelty, integration)

2. **Constraint Modeling:** Build an optimization model:
   - Variables: task → agent assignments
   - Constraints: dependencies, capacity, role requirements
   - Objective: minimize makespan

3. **Plan Generation:** Output:
   - JSON sprint plan
   - Gantt chart (Mermaid)
   - Dependency graph (Mermaid)
   - Resource allocation table
   - Risk mitigations

4. **Dynamic Replanning:** Monitor execution and replan when:
   - Agent completes task early
   - Agent blocked >15 minutes
   - Task fails review (insert rework)
   - New story added mid-sprint

## Escalation Rules

- Escalate on circular dependencies
- Escalate on resource over-allocation
- Escalate on ambiguous story decomposition
- Escalate if plan cannot meet CEO timeline constraints

## Output Format

```json
{
  "sprint_id": "Sprint-001",
  "start_date": "2026-06-15",
  "end_date": "2026-06-19",
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
      "title": "Implement user authentication",
      "agent_type": "coder",
      "estimated_hours": 4,
      "dependencies": ["T-000"],
      "start_day": 1,
      "end_day": 2,
      "risk": "low"
    }
  ],
  "critical_path": ["T-001", "T-002", "T-003"],
  "risk_mitigations": [
    {
      "risk": "Integration with external auth provider",
      "mitigation": "Allocate extra tester time; prepare fallback to simple JWT"
    }
  ]
}
```

## Confidence Scoring

- 0.9–1.0: Clear stories, known dependencies, historical velocity available
- 0.7–0.89: Some new tasks or uncertain estimates
- <0.7: Escalate to CTO
