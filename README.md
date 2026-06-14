# AI-Native Development Framework

This repository implements the **Agile AI-Driven Software Development Framework** described in `docs/`.

## Overview

The framework replaces traditional human-engineered delivery teams with a governed team of specialized AI agents:

- **CEO:** Strategic vision and final acceptance
- **CTO:** Technical governance and escalation resolution
- **AI Development Team:** 7 specialized agents executing a compressed Agile cycle

## Repository Structure

```
.
├── .pi/                          # Pi agent harness configuration
│   ├── agent/
│   │   ├── AGENTS.md             # Governance charter
│   │   ├── SYSTEM.md             # Universal system instructions
│   │   └── skills/               # Agent skill definitions
│   └── prompts/                  # Reusable prompt templates
├── .github/workflows/            # CI/CD quality fortress
├── docs/                         # Framework documentation
├── governance/                   # Governance documents
├── infrastructure/               # Docker / Terraform configs
├── pilots/                       # Pilot project workspace
├── scripts/                      # Setup and utility scripts
├── src/                          # Agent orchestration code
│   ├── agents/                   # Agent implementations
│   ├── core/                     # Core state, messages, feedback models
│   ├── graph/                    # LangGraph state machines
│   ├── learning/                 # Self-learning loop
│   ├── memory/                   # Vector DB / RAG
│   ├── monitoring/               # Cost and KPI tracking
│   └── tools/                    # Tool integrations
├── templates/                    # Project templates
├── tests/                        # Test suites
├── README.md                     # This file
├── requirements.txt              # Production dependencies
└── requirements-dev.txt          # Development dependencies
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run setup script:**
   ```bash
   ./scripts/setup.sh
   ```

4. **Run a simulation sprint:**
   ```bash
   python -m src.simulations.sprint_simulation
   ```

5. **Run a simulation with self-learning loop:**
   ```bash
   python -m src.simulations.sprint_simulation --learning
   ```

## Provider Strategy

This implementation uses a **hybrid provider strategy**:

- **Kimi (Moonshot AI):** Primary coding engine for Coder, Tester, Reviewer, DevOps, and Architect agents
- **Claude 4 / o3:** Planning, reasoning, and product tasks

You can switch providers by updating `.pi/agent/AGENTS.md` and `src/config/providers.yaml`.

## Self-Learning Loop

The framework includes an automated self-learning loop that continuously improves agent prompts and skills based on sprint outcomes:

- **Observe:** Collects feedback from sprint execution
- **Analyze:** Identifies recurring failure patterns and KPI gaps
- **Propose:** Generates improvement proposals
- **Approve:** CTO approval workflow (with optional auto-approval for low-risk changes)
- **Apply:** Safely applies changes with backups
- **Validate:** Re-runs simulation and compares KPIs
- **Rollback:** Reverts changes that cause regression

See `docs/17-self-learning-loop-plan.md` and `docs/18-self-learning-loop-implementation.md` for details.

## Governance

All production deployments require human (CTO) approval. See `governance/charter.md` and `.pi/agent/AGENTS.md`.

## Documentation

See `docs/` for the complete framework documentation, including:

- `docs/13-master-plan.md`
- `docs/14-master-execution-plan.md`

## License

[Organization License]
