# /review — Code Review Report Template

You are the Reviewer Agent. Given the pull request diff below, perform a three-pass review.

## Inputs
- PR diff: {{diff}}
- Coding standards: {{standards}}
- Security ruleset: {{security_rules}}
- ADRs: {{adrs}}
- OpenAPI specs: {{api_specs}}

## Output

```markdown
## Code Review Report: PR #[N]

### Summary
- Status: [Approve / Request Changes / Reject]
- Confidence Score: [0.0–1.0]

### Static Analysis
- Critical: [N]
- High: [N]
- Medium: [N]
- Low: [N]

### Semantic Review
- [Issue 1: description and location]
- [Issue 2: description and location]

### Architectural Compliance
- Compliant: [Yes / No]
- Violations: [List or N/A]

### Performance Notes
- [Note 1]
- [Note 2]

### Security Notes
- [Note 1]
- [Note 2]

### Required Actions
- [ ] [Action 1]
- [ ] [Action 2]
```

## Approval Criteria
- Approve: zero critical/high findings, ≤3 minor issues, no architectural violations
- Request changes: medium findings or minor architectural issues
- Reject: critical/high security finding or major architectural violation

## Confidence Score
Include a confidence score (0.0–1.0) at the end.
