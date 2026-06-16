#!/bin/bash
set -e

# AI-Native Framework — Unified installer
# Supports:
#   Remote:  curl -fsSL https://raw.githubusercontent.com/pmkrafts/agile_ai_framework/main/scripts/install.sh | bash
#   Local:   ./scripts/install.sh

REPO_URL="https://github.com/pmkrafts/agile_ai_framework.git"
REPO_NAME="agile_ai_framework"

# Determine if we are inside the repo or need to clone it
is_inside_repo() {
    if [ -f "scripts/setup.sh" ] && [ -f "pyproject.toml" ] && [ -f ".env.example" ]; then
        return 0
    fi
    return 1
}

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux";;
        Darwin*)    echo "macOS";;
        CYGWIN*|MINGW*|MSYS*) echo "Windows";;
        *)          echo "Unknown";;
    esac
}

OS=$(detect_os)
echo "=================================="
echo "AI-Native Framework Installer"
echo "Detected OS: $OS"
echo "=================================="

# --- Prerequisites -----------------------------------------------------------

echo "Checking prerequisites..."

command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed. Please install Git and try again."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3.11+ is required but 'python3' was not found."; exit 1; }
command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1 || { echo "❌ pip is required but not found."; exit 1; }

# Check Docker availability (optional — infrastructure is started if present)
if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1; then
    DOCKER_AVAILABLE=true
else
    DOCKER_AVAILABLE=false
    echo "⚠️  Docker and/or docker-compose not found. Local infrastructure will not be started."
    echo "   You can start it later by running: cd infrastructure && docker-compose up -d"
fi

# --- Clone or reuse repository -----------------------------------------------

if is_inside_repo; then
    echo "Repository already present at $(pwd). Skipping clone."
else
    INSTALL_DIR="$HOME/$REPO_NAME"
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo "Directory $INSTALL_DIR already exists. Pulling latest changes..."
        cd "$INSTALL_DIR"
        git pull
    else
        echo "Cloning repository into $INSTALL_DIR..."
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
fi

# Guard: ensure we are now in the repo root
if ! is_inside_repo; then
    echo "❌ Failed to locate repository root. Expected scripts/setup.sh, pyproject.toml, and .env.example."
    exit 1
fi

# --- Local environment setup -------------------------------------------------

echo "Running local environment setup..."
./scripts/setup.sh

# --- Start local infrastructure ----------------------------------------------

if [ "$DOCKER_AVAILABLE" = true ]; then
    echo ""
    echo "Starting local infrastructure with Docker Compose..."
    cd infrastructure
    docker-compose up -d
    cd ..
    echo ""
    echo "Infrastructure services:"
    echo "  Framework API: http://localhost:8000"
    echo "  ChromaDB:      http://localhost:8001"
    echo "  LangGraph:     http://localhost:8123"
    echo "  Grafana:       http://localhost:3000"
fi

# --- Completion --------------------------------------------------------------

echo ""
echo "=================================="
echo "Installation complete!"
echo "=================================="
echo "Next steps:"
echo "1. Edit .env with your actual API keys"
echo "2. Run: python -m src.simulations.sprint_simulation"
echo "3. Review docs/14-master-execution-plan.md for the full operational playbook"
