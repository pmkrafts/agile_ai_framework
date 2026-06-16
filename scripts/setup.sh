#!/bin/bash
set -e

# Move to repository root regardless of where the script is invoked
cd "$(dirname "$0")/.."

echo "=================================="
echo "AI-Native Framework Setup"
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Enforce Python 3.11+
python_major=$(echo "$python_version" | cut -d. -f1)
python_minor=$(echo "$python_version" | cut -d. -f2)
if [ "$python_major" -lt 3 ] || { [ "$python_major" -eq 3 ] && [ "$python_minor" -lt 11 ]; }; then
    echo "❌ Python 3.11 or higher is required. Found $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing production dependencies..."
pip install -r requirements.txt

echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/chroma
mkdir -p audit/sprints
mkdir -p pilots
mkdir -p logs

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your actual API keys before running agents."
fi

# Run pre-commit install if available
if command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit hooks..."
    pre-commit install
fi

# Run smoke tests
echo "Running smoke tests..."
python -m pytest tests/smoke -v || true

echo ""
echo "=================================="
echo "Setup complete!"
echo "=================================="
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run: python -m src.simulations.sprint_simulation"
echo "3. Review docs/14-master-execution-plan.md for next steps"
