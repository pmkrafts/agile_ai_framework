# Kimi-Powered Execution Plan: AI-Native Development Framework

**Document Classification:** Provider-Specific Execution Playbook  
**Target Audience:** CEO, CTO, Program Managers, Lead Engineers  
**Version:** 1.0  
**Effective Date:** June 2026  
**Prerequisite Reading:** Documents 01–10 in `docs/base/` and `docs/11-summary-execution-plan.md`

---

## 1. Purpose of This Plan

This document adapts the **Agile AI-Driven Software Development Framework** execution plan for deployments where **Kimi** (Moonshot AI) is the primary coding LLM provider. It preserves the same CEO → CTO → AI Agent governance model, sprint mechanics, and risk architecture from the base framework, but retools the agent-to-model assignments, cost model, context-window strategy, and Pi configuration specifically for Kimi.

> **Core Thesis:** Use Kimi's competitive token economics and long-context capabilities as the workhorse coding engine, while retaining high-reasoning models for planning, architecture, and review where appropriate. This preserves the framework's 70–80% cost reduction target and can further improve it given Kimi's pricing advantage for long-context coding workloads.

---

## 2. Why Kimi for Coding

**Kimi** is Moonshot AI's family of large language models. As of 2026, Kimi is recognized for:

- **Very long context windows** (200K+ tokens, with effective use across the full length)
- **Strong code generation and refactoring** performance across multiple languages
- **Competitive per-token pricing**, especially for long-context tasks
- **Good instruction following** for structured outputs (JSON, Gherkin, OpenAPI specs)
- **OpenAI-compatible API**, making it easy to plug into Pi, LangGraph, and other orchestrators

### 2.1 Where Kimi Excels in the Framework

| Agent Role | Why Kimi Fits | Caveat |
|---|---|---|
| **Coder Agent** | Strong code generation; long context helps with large files and multi-file edits | Validate against latest benchmark for target language |
| **Tester Agent** | Good at generating test cases from specs and code | May need few-shot examples for domain-specific test patterns |
| **Reviewer Agent** | Long context enables reviewing large diffs in one pass | Pair with SAST tools for security-critical findings |
| **Architect Agent** | Can ingest large codebases and produce coherent designs | Validate ADRs with a second reasoning pass |
| **DevOps Agent** | Good at generating config, scripts, and deployment manifests | Test generated infrastructure code in sandbox first |
| **Product Agent** | Capable for PRDs and structured stories | Consider Claude/GPT for highly nuanced product reasoning |
| **Planner Agent** | Works for dependency mapping and sprint plans | Use a dedicated reasoning model for complex optimization |

### 2.2 Recommended Model Mix

| Agent | Primary Model | Fallback / Secondary |
|---|---|---|
| **Product Agent** | Kimi k2.5 (large) or Claude 4 | GPT-4o |
| **Planner Agent** | Claude 4 / o3 (reasoning) | Kimi k2.5 (large) |
| **Architect Agent** | Kimi k2.5 (large) | Claude 4 |
| **Coder Agent(s)** | **Kimi k2.6 / k2.5** | Claude 4 Sonnet |
| **Tester Agent** | Kimi k2.5 | Claude 4 |
| **Reviewer Agent** | Kimi k2.5 (large) + SAST tools | Claude 4 (security pass) |
| **DevOps Agent** | Kimi k2.5 | GPT-4o |

> **Note:** Model names and versions should be pinned and updated as Moonshot AI releases new Kimi versions. Always benchmark Kimi against the target tech stack before committing to a model version.

---

## 3. Strategic Objectives (Kimi-Adjusted)

| Objective | Target | Measurement |
|---|---|---|
| Reduce delivery cost vs. traditional team | **75–85%** | `ROI-T = (Traditional Cost − AI Cost) / Traditional Cost × 100` |
| Compress delivery timeline | 40–60% | Time-to-Delivery (TTD) per project |
| Maintain quality parity or better | ≤0.15 production defects per story | Defect Escape Rate (DER) |
| Keep governance sustainable | ≤10 hrs/week per project for CTO | CTO Cost per Project (CCP) |
| Maximize long-context utilization | ≥80% of coding tasks use full-file or multi-file context | Token/usage analytics |
| Scale without linear hiring | 8–12 concurrent projects per CTO | Concurrent project count |
| Preserve human accountability | 100% compliance | Governance Compliance Rate (GCR) |

---

## 4. Pi Configuration for Kimi

Pi supports multiple providers. Kimi can be integrated via its **OpenAI-compatible API endpoint** or through a custom Pi extension if needed.

### 4.1 Pi Provider Configuration

Add the following to Pi's configuration (e.g., `~/.pi/config.yaml` or project-level settings):

```yaml
providers:
  kimi:
    base_url: https://api.moonshot.cn/v1
    api_key: ${KIMI_API_KEY}
    default_model: kimi-k2-6-latest
    models:
      - id: kimi-k2-6-latest
        context_window: 256000
        cost_per_1k_input: 0.005
        cost_per_1k_output: 0.015
      - id: kimi-k2-5-latest
        context_window: 256000
        cost_per_1k_input: 0.003
        cost_per_1k_output: 0.009
```

> **Pricing above is illustrative.** Verify current Kimi pricing at https://platform.moonshot.cn/ and pin exact model snapshots for reproducibility.

### 4.2 Agent-to-Provider Mapping in `AGENTS.md`

```markdown
# AI-Native Development Team — Kimi Provider Mapping

## Default Provider
- Coding tasks: **kimi**
- Reasoning/planning tasks: **anthropic** or **openai**

## Agent Provider Assignments
| Agent | Primary Provider | Model | Notes |
|---|---|---|---|
| Product Agent | anthropic | claude-4-sonnet | Nuanced product reasoning |
| Planner Agent | openai | o3 | Constraint optimization |
| Architect Agent | kimi | kimi-k2-6-latest | Large codebase context |
| Coder Agent | **kimi** | **kimi-k2-6-latest** | Primary coding engine |
| Tester Agent | kimi | kimi-k2-5-latest | Test generation |
| Reviewer Agent | kimi | kimi-k2-6-latest | Large diff review |
| DevOps Agent | kimi | kimi-k2-5-latest | Config/script generation |

## Context Window Rules
- Prefer sending full files to Kimi rather than chunked snippets when within context budget.
- Use Kimi's long context for cross-file refactoring and architecture tasks.
- For tasks exceeding 200K tokens, use RAG + hierarchical memory as described in Document 07.
```

### 4.3 Project File Structure

```
agile_ai_framework/
├── .pi/
│   ├── agent/
│   │   ├── AGENTS.md              # Global governance + Kimi provider map
│   │   ├── SYSTEM.md              # System-wide instructions
│   │   └── skills/
│   │       ├── product-agent.md
│   │       ├── planner-agent.md
│   │       ├── architect-agent.md
│   │       ├── coder-agent-kimi.md    # Kimi-specific coding skill
│   │       ├── tester-agent-kimi.md
│   │       ├── reviewer-agent-kimi.md
│   │       └── devops-agent-kimi.md
│   └── prompts/
│       ├── prd-template.md
│       ├── sprint-plan-template.md
│       ├── review-report-template.md
│       ├── deployment-report-template.md
│       └── kimi-context-prompt.md     # Long-context instructions
├── TODO.md
└── docs/
    ├── 11-summary-execution-plan.md
    └── 12-kimi-execution-plan.md        # This document
```

---

## 5. Cost Model Adjustment for Kimi

Kimi's pricing is generally more favorable than Claude 4 / GPT-4o for long-context coding workloads. The framework cost model should be updated accordingly.

### 5.1 Revised 6-Month Project Cost (Kimi-Powered)

| Cost Component | Calculation | Amount (USD) |
|---|---|---|
| **CTO Oversight (0.25 FTE)** | 0.25 × $200K × 0.5 year | $25,000 |
| **CEO Time (minimal)** | 2 hrs/week × 26 weeks × $500/hr | $26,000 |
| **LLM API Costs (Kimi primary)** | ~$120/week × 26 weeks | $3,120 |
| **Secondary LLM Costs (Claude/o3)** | ~$40/week × 26 weeks | $1,040 |
| **Orchestration Platform** | LangGraph Cloud / CrewAI Enterprise | $2,400 |
| **Vector Database** | Pinecone/Weaviate production tier | $1,800 |
| **Monitoring Tools** | LangSmith, Helicone | $1,200 |
| **CI/CD & Sandbox Infrastructure** | GitHub Actions + cloud compute | $8,000 |
| **Security Scanning Tools** | Semgrep, Snyk, CodeQL | $3,600 |
| **Cloud Infrastructure (Production)** | Same as baseline | $15,000 |
| **Contingency (20%)** | Higher buffer for AI-specific risks | $17,692 |
| **TOTAL 6-MONTH PROJECT COST** | | **$105,852** |

**Net savings vs. traditional ($469K): 77.4%**  
**Net savings vs. hybrid ($387K): 72.7%**  
**Additional savings vs. all-Claude/OpenAI mix: ~$2–4K per project** (varies by workload)

### 5.2 Token Economics (Kimi)

| Operation | Input Tokens | Output Tokens | Estimated Cost (Kimi k2.6) |
|---|---|---|---|
| **Product Agent: PRD Generation** | 2,000 | 3,000 | ~$0.030 |
| **Planner Agent: Sprint Planning** | 5,000 | 2,000 | ~$0.023 |
| **Architect Agent: API Design** | 3,000 | 2,500 | ~$0.023 |
| **Coder Agent: Feature Implementation** | 10,000 | 5,000 | ~$0.075 |
| **Tester Agent: Test Generation** | 4,000 | 3,000 | ~$0.038 |
| **Reviewer Agent: Code Review** | 8,000 | 2,000 | ~$0.040 |
| **DevOps Agent: Deployment** | 2,000 | 1,000 | ~$0.010 |
| **TOTAL PER STORY** | ~34,000 | ~18,500 | **~$0.24** |

At 8 stories per sprint: **~$1.92 per sprint in LLM costs** (Kimi portion only; excluding Claude/o3 for planning/reasoning).

### 5.3 Cost Optimization Strategies Specific to Kimi

| Strategy | Implementation | Expected Savings |
|---|---|---|
| **Full-file context** | Send complete files to Kimi instead of snippets; reduce RAG overhead | 10–20% |
| **Long-context batching** | Group related files in a single prompt; reduce API call count | 15–25% |
| **Model tiering** | Use Kimi k2.5 for simpler tasks; reserve k2.6 for complex coding | 20–30% |
| **Prompt caching** | Cache repeated prompts via Pi / Helicone | 20–30% |
| **Output token compression** | Request concise outputs; post-process for formatting | 15–25% |
| **Temperature=0** | Greedy decoding for deterministic coding outputs | Reduces rework costs |

---

## 6. Execution Roadmap (Kimi-Adjusted)

The four-phase roadmap remains structurally identical to the base plan, but Week 2 agent configuration is tailored for Kimi.

### 6.1 Phase 1: Foundation (Weeks 1–4)

#### Week 1 — Infrastructure & Tooling

| Day | Action | Owner | Deliverable |
|---|---|---|---|
| 1 | Create cloud account; provision compute | CTO | Cloud environment live |
| 2 | **Create Moonshot AI account; obtain Kimi API key** | CTO | API key secured in vault |
| 3 | Deploy Pi; configure Kimi as provider; test connection | CTO | Kimi responds to test prompt |
| 4 | Deploy LangGraph + vector database | CTO | Orchestration + RAG ready |
| 5 | Configure GitHub repo + Actions + security scans | CTO | CI/CD skeleton operational |

#### Week 2 — Kimi Agent Configuration

| Day | Action | Owner | Deliverable |
|---|---|---|---|
| 1 | Write `AGENTS.md` with Kimi provider map | CTO | Governance charter loaded |
| 2 | Create Kimi-specific skills for Coder, Tester, Reviewer, DevOps | CTO | Skills tested in isolation |
| 3 | Engineer prompt templates; include long-context instructions | CTO | `/prd`, `/plan`, `/review`, `/deploy` commands |
| 4 | Configure agent tools: Jira, GitHub, SAST, sandbox | CTO | Agents can call required tools |
| 5 | Run benchmark: Kimi vs. Claude on sample coding task | CTO | Model selection validated |

#### Week 3 — Quality, Security & Monitoring

| Day | Action | Owner | Deliverable |
|---|---|---|---|
| 1 | Integrate Semgrep, Bandit, Snyk, GitLeaks into CI | CTO | 5-stage quality pipeline |
| 2 | Configure test automation + coverage reporting | CTO | Coverage reporting active |
| 3 | Deploy LangSmith + Helicone; add Kimi provider tracking | CTO | Cost dashboard per provider |
| 4 | Set up Grafana/Datadog agent health dashboard | CTO | Real-time agent status visible |
| 5 | Configure cost alerts (50%, 75%, 90%, 100%) with Kimi-specific thresholds | CTO | Alerts tested |

#### Week 4 — Governance & Validation

Same as base plan: establish governance committee, draft AI disclosure, define escalation procedures, run end-to-end simulation, and select 2 pilot projects.

**Kimi-Specific Simulation Add-on:**
- Test a cross-file refactoring task using Kimi's long context.
- Validate that Kimi-generated code passes the 5-stage quality fortress.
- Measure first-build success rate and compare against Claude baseline.

### 6.2 Phase 2: Pilot Projects (Weeks 5–8)

Same pilot criteria and sprint structure as base plan. Additional Kimi focus:

- **Coder Agent** uses Kimi for all feature implementation.
- **Reviewer Agent** uses Kimi for large-diff semantic review; SAST tools handle security.
- **Architect Agent** uses Kimi to ingest existing codebase context for design tasks.
- Track Kimi-specific metrics: token efficiency, cost per story, context-window utilization.

### 6.3 Phase 3: Expansion (Weeks 9–12)

Same as base plan, with added emphasis on:

- **Kimi model tiering:** Route simple tasks to k2.5, complex tasks to k2.6.
- **Long-context optimization:** Standardize full-file prompts where beneficial.
- **Fallback testing:** Ensure Claude fallback is configured for tasks where Kimi underperforms.

### 6.4 Phase 4: Scale (Weeks 13–20)

Same as base plan. With Kimi's cost advantage, pricing power may be even stronger.

---

## 7. Kimi-Powered Sprint Mechanics

### 7.1 Backlog & Refinement (Day 0)

```
CEO (natural language problem)
    │
    ▼
Pi Product Agent (Claude 4 recommended)
├── Runs structured CEO interview
├── Generates PRD using `/prd` template
├── Submits PRD to CTO for validation
└── Upon approval, decomposes into Gherkin stories
```

### 7.2 Sprint Planning (Day 0)

```
Approved Stories
    │
    ▼
Pi Planner Agent (o3 / Claude 4)
├── Builds dependency graph
├── Optimizes for minimum makespan
├── Outputs sprint plan JSON + Gantt
└── Submits to CTO for approval
```

### 7.3 Execution (Days 1–4)

```
Parallel Streams:

Stream A: Architecture      Stream B: Development        Stream C: Quality
──────────────────          ───────────────────          ────────────────
Pi Architect Agent          Pi Coder Agent (Kimi)         Pi Tester Agent (Kimi)
├── Design API              ├── Implement story           ├── Generate tests
├── Design DB schema        ├── Write unit tests          ├── Run tests
└── Write ADRs              └── Submit PR                 └── Coverage report

Stream D: Review            Stream E: DevOps
──────────────              ─────────────────
Pi Reviewer Agent (Kimi)    Pi DevOps Agent (Kimi)
├── Static analysis         ├── Setup environment
├── Semantic review         ├── Configure CI
└── Security scan           └── Prep deployment
```

### 7.4 Review & Deployment (Day 5)

Same as base plan. DevOps Agent awaits CTO approval before production deployment.

---

## 8. Governance Gates (Unchanged)

Governance gates remain identical to the base framework. Kimi does not change accountability:

| Gate | Approver | Kimi-Specific Note |
|---|---|---|
| Project kickoff | CEO | Disclose Kimi as AI provider in contracts |
| Architecture approval | CTO | Validate Kimi-generated ADRs with reasoning model if needed |
| Production deployment | CTO | Human signature mandatory |
| Client acceptance | CEO | Demo against acceptance criteria |
| Budget override | CEO | Kimi cost caps configured per sprint |

---

## 9. Technical Considerations for Kimi

### 9.1 Long Context Advantage

Kimi's large context window should be exploited for:

- **Cross-file refactoring:** Pass entire modules or packages in one prompt.
- **Codebase onboarding:** Let Architect Agent ingest large existing codebases.
- **Large diff review:** Reviewer Agent can analyze substantial PRs holistically.
- **Traceability:** Include requirement-to-code traceability in a single prompt.

### 9.2 Context Window Management

| Model | Theoretical Context | Effective Working Context | Practical Codebase Size |
|---|---|---|---|
| Kimi k2.6 | 256K tokens | ~180K tokens | ~150K lines of code |
| Kimi k2.5 | 256K tokens | ~180K tokens | ~150K lines of code |
| Claude 4 Sonnet | 200K tokens | ~100K tokens | ~75K lines of code |
| Claude 4 Opus | 1M tokens | ~400K tokens | ~300K lines of code |
| GPT-4o | 128K tokens | ~64K tokens | ~48K lines of code |

> **Strategy:** Use Kimi for medium-to-large codebase tasks where Claude Sonnet would require chunking, but switch to Claude Opus for extremely large codebases (>200K lines).

### 9.3 Determinism

Same deterministic execution protocol as base plan:

```yaml
deterministic_execution:
  model_configuration:
    temperature: 0
    top_p: 1.0
    seed: 42
    model_version: "kimi-k2-6-2025xx"  # Pin exact snapshot
```

### 9.4 Hallucination and Security

Kimi is not immune to hallucination or security anti-patterns. The same 3-layer hallucination detection and security hardening pipeline apply:

1. **Syntactic validation:** Build must pass; imports must resolve.
2. **Semantic validation:** RAG grounding + test execution + Reviewer Agent.
3. **Business validation:** CEO demo + CTO review.

### 9.5 Data Residency and Compliance

| Consideration | Action |
|---|---|
| **Data residency** | Verify Moonshot AI data processing region matches client/regulatory requirements |
| **Training opt-out** | Confirm Kimi API does not use client code for model training |
| **Enterprise agreement** | Negotiate BAA / enterprise terms for regulated industries |
| **Audit logging** | Export Pi sessions and Kimi API logs to immutable storage |

---

## 10. Risk Mitigation (Kimi-Specific Additions)

| Risk | Mitigation | Pi Implementation |
|---|---|---|
| Kimi API availability issues | Maintain Claude fallback for critical coding tasks | Provider fallback config in `AGENTS.md` |
| Kimi underperforms on specific language/framework | A/B test Kimi vs. Claude on pilot tasks | Benchmark skill in Pi |
| Context window mismanagement | Monitor prompt token counts; enforce limits | Helicone cost/token alerts |
| Data residency concerns | Use enterprise tier; verify region | Compliance check in governance skill |
| Vendor lock-in to Moonshot | Keep prompts provider-agnostic; test Claude fallback quarterly | Multi-provider skill templates |
| Long-context cost surprises | Set per-prompt token caps; prefer RAG for very large inputs | Token budget skill |

---

## 11. KPIs & Measurement Dashboard

### 11.1 Essential KPIs (Same as Base)

| Category | KPI | Month 3 Target | Month 6 Target |
|---|---|---|---|
| Delivery | Story Completion Rate | ≥75% | ≥85% |
| Delivery | First-Build Success Rate | ≥65% | ≥80% |
| Delivery | Defect Escape Rate | ≤0.25 | ≤0.15 |
| Economic | Cost per Story | <$12 | <$8 |
| Economic | Margin per Project | ≥60% | ≥70% |
| Operational | Escalation Rate | ≤10% | ≤5% |
| Operational | Governance Compliance Rate | 100% | 100% |
| Strategic | Client Satisfaction Score | ≥7 | ≥8 |

### 11.2 Kimi-Specific Metrics

| Metric | Definition | Target | Why It Matters |
|---|---|---|---|
| **Kimi Utilization Rate** | % of coding tasks routed to Kimi | ≥80% | Cost optimization |
| **Kimi Fallback Rate** | % of Kimi tasks escalated to Claude fallback | <10% | Model fit validation |
| **Long-Context Task Rate** | % of tasks using >50K context | ≥30% | Exploiting Kimi's strength |
| **Kimi Cost per Story** | Kimi API cost / stories delivered | <$2 | Economic efficiency |
| **Kimi First-Build Success** | Kimi-generated builds passing first attempt | ≥70% | Quality benchmark |

---

## 12. Tool Stack Recommendation (Kimi-Adjusted)

| Layer | Recommended Tool | Role |
|---|---|---|
| **Agent Harness** | **Pi (pi.dev)** | Primary interface |
| **Orchestration** | **LangGraph** | Deterministic workflows |
| **Primary Coding LLM** | **Kimi k2.6 / k2.5 (Moonshot AI)** | Coder, Tester, Reviewer, DevOps Agents |
| **Reasoning / Planning LLM** | **Claude 4 / o3** | Planner, high-stakes architecture |
| **Fallback Coding LLM** | **Claude 4 Sonnet** | Fallback when Kimi underperforms |
| **Vector DB** | **Pinecone / Weaviate** | Project memory and RAG |
| **CI/CD** | **GitHub Actions** | Automated quality fortress |
| **SAST** | **Semgrep + Bandit** | Static security analysis |
| **Dependency Scan** | **Snyk** | Vulnerability management |
| **Secret Detection** | **GitLeaks** | Pre-commit secret scanning |
| **Observability** | **LangSmith + Helicone** | Tracing and cost monitoring |
| **Deployment** | **Docker + Kubernetes** | Container orchestration |

---

## 13. 30-Day Launch Checklist (Kimi-Adjusted)

| # | Action | Owner | Verification |
|---|---|---|---|
| 1 | Read base framework documents | CEO, CTO | Discussion meeting |
| 2 | **Create Moonshot AI account; secure Kimi API key** | CTO | API key in vault |
| 3 | Install and configure Pi with Kimi provider | CTO | Kimi test prompt succeeds |
| 4 | Write `AGENTS.md`, `SYSTEM.md`, and Kimi-specific skills | CTO | Pi loads project instructions |
| 5 | Create prompt templates (include long-context guidance) | CTO | Templates expand correctly |
| 6 | Provision LangGraph + vector database | CTO | Health checks pass |
| 7 | Set up GitHub repo + Actions + security scans | CTO | Test repo passes all gates |
| 8 | Deploy LangSmith + Helicone with Kimi provider tracking | CTO | Dashboards active |
| 9 | Configure cost alerts and budget caps | CTO | Alert test successful |
| 10 | **Benchmark Kimi vs. Claude on sample coding task** | CTO | Model selection validated |
| 11 | Establish governance committee | CEO | Charter signed |
| 12 | Select first pilot project | CEO | Scored ≥4 on clarity and stack |
| 13 | Review client contracts for Kimi AI disclosure | Legal | Disclosure approved |
| 14 | Confirm E&O + cyber insurance | CEO | Certificates verified |
| 15 | Run tabletop escalation exercise | CTO | Response procedures validated |
| 16 | Execute first end-to-end sprint simulation with Kimi | CTO | PRD → code → review → deploy |
| 17 | Define pilot success criteria | CEO + CTO | KPI targets documented |

---

## 14. Immediate Next Steps

1. **CEO + CTO review** this Kimi-specific plan alongside the base framework.
2. **CTO creates a Moonshot AI account**, obtains API key, and verifies Kimi availability in your region.
3. **Install Pi** and configure Kimi as the primary coding provider using the OpenAI-compatible endpoint.
4. **Create Kimi-specific skills** in `.pi/agent/skills/` for Coder, Tester, Reviewer, and DevOps Agents.
5. **Benchmark Kimi** against Claude on 2–3 representative coding tasks from your stack.
6. **Select the first pilot project** and update client contracts with Kimi disclosure language.
7. **Run a simulation sprint** before any client-facing deployment.

---

## 15. Key Takeaway

> Using **Kimi as the primary coding provider** preserves the framework's governance, quality gates, and human accountability while potentially lowering costs further through Kimi's competitive long-context pricing. The key success factors are: (1) rigorous benchmarking before commitment, (2) maintaining a Claude/o3 fallback for reasoning-heavy tasks, and (3) exploiting Kimi's long-context capability for cross-file coding and review workloads. Execute the 30-day launch checklist, validate through pilots, and scale only when KPIs are met.

---

## Appendix A: Kimi Coder Agent Skill

```markdown
# Coder Agent Skill — Kimi Variant

## Role
Implement features according to specifications using Kimi as the coding engine.

## Provider
- **Primary:** kimi / kimi-k2-6-latest
- **Fallback:** anthropic / claude-4-sonnet

## Inputs
- Assigned user story
- API specification
- Architecture diagram
- Codebase context (prefer full files when within context budget)

## Outputs
- Commit-ready code
- Unit tests
- Implementation notes
- Confidence score (0.0–1.0)

## Tools
- GitHub/GitLab API
- Sandbox execution environment
- Linter/formatter
- RAG query tool

## Execution Loop
1. Read story and acceptance criteria
2. Query codebase memory for similar patterns
3. Write failing unit tests
4. Implement code using Kimi
5. Run tests; debug up to 3 attempts
6. Run linter/formatter
7. Self-assess confidence
8. Submit for review (escalate if confidence < 0.8)

## Long-Context Instructions
- When the task spans multiple files, include the full content of relevant files in the prompt.
- Do not artificially chunk files unless the combined context exceeds 200K tokens.
- After generating code, verify cross-file references match actual signatures.

## Escalation Rules
- Escalate if blocked >30 minutes
- Escalate after 3 failed debug attempts
- Escalate if specification contradiction found
- Escalate if confidence score < 0.8
```

## Appendix B: Kimi Reviewer Agent Skill

```markdown
# Reviewer Agent Skill — Kimi Variant

## Role
Perform code review, security scan coordination, and architectural compliance checks.

## Provider
- **Primary:** kimi / kimi-k2-6-latest
- **Security deep-dive fallback:** anthropic / claude-4-sonnet

## Inputs
- Pull request diff
- Coding standards
- Security ruleset
- Architecture Decision Records

## Outputs
- Review report (approve / request changes / reject)
- Security findings
- Performance notes
- Style violations

## Three-Pass Analysis
1. **Static Analysis Pass:** Run Semgrep, Bandit, ESLint, Pylint
2. **Semantic Review Pass:** Use Kimi's long context to analyze full diff logic
3. **Architectural Compliance Pass:** Verify ADR adherence and authorized dependencies

## Approval Criteria
- Zero critical/high findings
- No more than 3 minor issues
- No architectural violations
- Confidence score ≥ 0.85

## Escalation Rules
- Escalate critical security findings to CTO immediately
- Escalate performance regression >20%
- Escalate architectural violations
```

## Appendix C: Pi Config Snippet — Kimi Provider

```yaml
# ~/.pi/config.yaml or project-level pi config

providers:
  kimi:
    base_url: https://api.moonshot.cn/v1
    api_key: ${KIMI_API_KEY}
    default_model: kimi-k2-6-latest
    request_timeout: 120
    models:
      - id: kimi-k2-6-latest
        name: Kimi k2.6
        context_window: 256000
      - id: kimi-k2-5-latest
        name: Kimi k2.5
        context_window: 256000

  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    default_model: claude-4-sonnet-20250514

  openai:
    api_key: ${OPENAI_API_KEY}
    default_model: o3

agent_defaults:
  coder:
    provider: kimi
    model: kimi-k2-6-latest
    temperature: 0
  tester:
    provider: kimi
    model: kimi-k2-5-latest
    temperature: 0
  reviewer:
    provider: kimi
    model: kimi-k2-6-latest
    temperature: 0
  devops:
    provider: kimi
    model: kimi-k2-5-latest
    temperature: 0
  planner:
    provider: openai
    model: o3
    temperature: 0
  product:
    provider: anthropic
    model: claude-4-sonnet-20250514
    temperature: 0
  architect:
    provider: kimi
    model: kimi-k2-6-latest
    temperature: 0
```

---

**End of Document**
