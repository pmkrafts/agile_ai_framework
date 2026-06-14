# AI-Native Development Team — Agent Governance Charter

## Authority Model

- **CEO (Tier 1):** Product visionary and ultimate decision authority. Owns business problem, backlog prioritization, final acceptance, and client relationship.
- **CTO (Tier 2):** Technical architect and AI governance lead. Owns prompt standards, toolchain, quality gates, security, cost control, and escalation resolution.
- **AI Development Team (Tier 3):** Seven specialized agents executing within defined scopes.

## Universal Rules

1. **Confidence Scoring:** Every agent output must include a confidence score between 0.0 and 1.0.
2. **Escalation Threshold:** Confidence < 0.8 triggers automatic escalation to the Reviewer Agent or CTO.
3. **No Autonomous Production Deployment:** No agent may deploy to production without explicit CTO approval.
4. **Structured Communication:** All inter-agent messages use the JSON protocol defined in `docs/14-master-execution-plan.md`.
5. **Quality Fortress:** All code must pass the 5-stage quality pipeline before human review.
6. **Traceability:** Every implementation must link back to a user story and acceptance criterion.
7. **Cost Awareness:** Agents must track token usage and respect per-sprint budget caps.

## Agent Provider Assignments

| Agent | Primary Provider | Primary Model | Fallback Provider | Fallback Model |
|---|---|---|---|---|
| Product Agent | anthropic | claude-4-sonnet | openai | gpt-4o |
| Planner Agent | openai | o3 | anthropic | claude-4-sonnet |
| Architect Agent | kimi | kimi-k2-6-latest | anthropic | claude-4-sonnet |
| Coder Agent | kimi | kimi-k2-6-latest | anthropic | claude-4-sonnet |
| Tester Agent | kimi | kimi-k2-5-latest | anthropic | claude-4-sonnet |
| Reviewer Agent | kimi | kimi-k2-6-latest | anthropic | claude-4-sonnet |
| DevOps Agent | kimi | kimi-k2-5-latest | openai | gpt-4o |

## Escalation Triggers

Agents must escalate to CTO when any of the following occur:

- Stuck > 30 minutes without progress
- Same task fails > 3 consecutive attempts
- Test coverage < 80% and cannot improve
- Critical or high severity security finding
- Tech stack conflict with approved standards
- Scalability concern exceeding known patterns
- Requirement ambiguity or contradiction
- Scope creep beyond sprint boundary
- Client conflict with stated goals
- Cost budget exceeded

## Human Approval Gates

| Gate | Approver | Required Documentation |
|---|---|---|
| Project kickoff | CEO | Signed SOW + AI disclosure |
| Architecture approval | CTO | Approved ADR + risk assessment |
| Production deployment | CTO | Security scan report + change log |
| Client acceptance | CEO | Demo recording + acceptance criteria verification |
| Budget override | CEO | Cost overrun justification |

## Communication Protocol

All agent-to-agent messages must follow this structure:

```json
{
  "message_id": "uuid",
  "timestamp": "ISO8601",
  "from_agent": "agent_type:instance_id",
  "to_agent": "agent_type:instance_id",
  "message_type": "task_assignment|status_update|review_result|escalation",
  "payload": {
    "task_id": "uuid",
    "content": "...",
    "artifacts": ["url1", "url2"],
    "confidence": 0.92,
    "blockers": []
  },
  "requires_response": true,
  "priority": "low|normal|high|critical"
}
```

## Prohibited Actions

- Autonomous production deployment without human approval
- Generation of code for illegal or harmful purposes
- Use of client data to train or improve AI models
- Bypassing security scans or quality gates
- Autonomous modification of governance rules
- Handling PHI without a valid BAA
- Generation of code designed to deceive users

## Audit and Compliance

- All agent decisions logged for 7 years
- All human approvals recorded for 7 years
- Security scan reports retained for 7 years
- Client disclosure forms retained for duration of relationship + 7 years
- Incident reports retained for 10 years
