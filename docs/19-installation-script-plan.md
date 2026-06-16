# Installation Script Plan

## Goals

- Reduce AI-Native Framework setup friction to a single command for Linux, macOS, and Windows.
- Provide a Hermes-agent-style remote install experience:
  - Linux/macOS: `curl -fsSL https://raw.githubusercontent.com/pmkrafts/agile_ai_framework/main/scripts/install.sh | bash`
  - Windows: `iex (irm https://raw.githubusercontent.com/pmkrafts/agile_ai_framework/main/scripts/install.ps1)`
- Preserve the existing `scripts/setup.sh` logic by delegating local environment setup to it.
- Support both remote (clone + setup) and local (setup only) execution modes.
- Start local Docker Compose infrastructure automatically when Docker is available.
- Document the design, rollout steps, and risks in this plan.

## Scope

### In scope

- Cross-platform installer scripts (`scripts/install.sh` and `scripts/install.ps1`).
- Prerequisite checks (Git, Python 3.11+, pip, Docker).
- Repository cloning or reuse.
- Python virtual environment creation and dependency installation.
- Project directory creation (`data/chroma`, `audit/sprints`, `pilots`, `logs`).
- `.env` initialization from `.env.example`.
- Smoke test execution.
- Optional Docker Compose startup.
- README and runbook updates to surface the new install commands.

### Out of scope

- Cloud provisioning.
- API key acquisition for LLM providers.
- CI/CD pipeline changes.
- Packaging as a standalone binary.

## Design Decisions

| Decision | Rationale |
|---|---|
| Separate Bash and PowerShell scripts | Matches the Hermes agent pattern and handles platform differences cleanly (paths, venv activation, execution policy). |
| `install.sh` delegates to `scripts/setup.sh` | Avoids duplicating environment setup logic. `setup.sh` is hardened to run from any directory. |
| Auto-start Docker Compose | User requested automatic startup; graceful fallback when Docker is unavailable. |
| Silent `.env` copy with a loud warning | Interactive prompts inside `curl \| bash` are fragile; copying the template and warning the user is safer. |
| Smoke tests warn but do not abort | The framework may still be usable even if some smoke checks fail during initial setup. |
| Remote install clones to `~/agile_ai_framework` (or `%USERPROFILE%\agile_ai_framework`) | Provides a predictable, easy-to-find installation location. |

## File Layout

### New files

- `scripts/install.sh` — Bash installer (remote + local modes).
- `scripts/install.ps1` — PowerShell installer (remote + local modes).
- `docs/19-installation-script-plan.md` — This plan document.

### Modified files

- `scripts/setup.sh` — Fixed `2>&1` typo, added Python 3.11+ check, changed to repo root relative to script location.
- `README.md` — Updated Quick Start with one-liner install commands.
- `docs/runbook.html` — Added a new "Install" section and renumbered subsequent sections.

## Script Behavior

### Bash installer (`scripts/install.sh`)

1. Detect OS (Linux/macOS/Windows-bash/WSL).
2. Check prerequisites: Git, Python 3.11+, pip.
3. Check Docker availability (optional).
4. If not already inside the repo, clone `https://github.com/pmkrafts/agile_ai_framework.git` into `~/agile_ai_framework`.
5. Change to repo root and run `./scripts/setup.sh`.
6. If Docker is available, run `docker-compose up -d` in `infrastructure/`.
7. Print service URLs and next steps.

### PowerShell installer (`scripts/install.ps1`)

1. Detect Windows and check PowerShell execution policy.
2. Check prerequisites: Git, Python 3.11+ (probing `python` then `python3`), pip.
3. Check Docker availability (optional).
4. If not already inside the repo, clone into `%USERPROFILE%\agile_ai_framework`.
5. Create `.venv`, activate it, upgrade pip, install `requirements.txt` and `requirements-dev.txt`.
6. Create project directories and copy `.env.example` → `.env`.
7. Install pre-commit hooks if available.
8. Run smoke tests.
9. If Docker is available, run `docker-compose up -d` in `infrastructure/`.
10. Print service URLs and next steps.

## Distribution URLs

### Remote install

```bash
# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/pmkrafts/agile_ai_framework/main/scripts/install.sh | bash
```

```powershell
# Windows (PowerShell)
iex (irm https://raw.githubusercontent.com/pmkrafts/agile_ai_framework/main/scripts/install.ps1)
```

### Local install

```bash
# Linux / macOS
git clone https://github.com/pmkrafts/agile_ai_framework.git
cd agile_ai_framework
./scripts/install.sh
```

```powershell
# Windows
git clone https://github.com/pmkrafts/agile_ai_framework.git
cd agile_ai_framework
.\scripts\install.ps1
```

## Rollout Steps

1. Implement `scripts/install.sh` and `scripts/install.ps1`.
2. Harden `scripts/setup.sh` and add Python version check.
3. Create `docs/19-installation-script-plan.md`.
4. Update `README.md` Quick Start section.
5. Update `docs/runbook.html` with a new Install section.
6. Test scripts on Linux/macOS and Windows (local mode at minimum).
7. Merge to `main`.
8. Verify raw GitHub URLs serve the scripts correctly.

## Verification Matrix

| Scenario | Expected Result |
|---|---|
| Linux/macOS local install | Repo stays in place, `.venv` created, deps installed, `.env` copied, smoke tests run, Docker started. |
| Windows local install | Same as above with PowerShell-specific paths. |
| Remote install simulation | Script clones to `~/agile_ai_framework` or `%USERPROFILE%\agile_ai_framework` and completes setup. |
| Docker unavailable | Setup continues; warning printed; Docker step skipped. |
| Python 3.10 installed | Clear error message; installer exits. |
| `.env` already exists | Existing file preserved; no overwrite. |

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| `curl \| bash` security concerns | Document local/manual install alternative; use HTTPS raw GitHub URLs. |
| PowerShell execution policy blocks `.ps1` | Detect policy at runtime and print remediation guidance. |
| Python version mismatch | Explicit version check with clear failure message. |
| Docker not running | Graceful fallback with instructions for manual startup. |
| Remote script has stale logic post-merge | Raw GitHub URL reflects `main` branch; release tags can be used later for stability. |

## Notes

- The installers are intentionally lightweight wrappers. Heavy lifting remains in `scripts/setup.sh` (Linux/macOS local setup) or inline in `install.ps1` (Windows local setup).
- Future iterations may add command-line flags for install directory, Python interpreter path, or `--skip-docker`.
