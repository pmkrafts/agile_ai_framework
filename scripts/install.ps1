# AI-Native Framework — Unified installer for Windows
# Supports:
#   Remote:  iex (irm https://raw.githubusercontent.com/pmkrafts/agile_ai_framework/main/scripts/install.ps1)
#   Local:   .\scripts\install.ps1

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/pmkrafts/agile_ai_framework.git"
$RepoName = "agile_ai_framework"

function Test-InsideRepo {
    return (Test-Path "scripts\setup.sh") -and (Test-Path "pyproject.toml") -and (Test-Path ".env.example")
}

function Get-PythonCommand {
    # Prefer 'python', fallback to 'python3'
    $cmds = @("python", "python3")
    foreach ($cmd in $cmds) {
        if (Get-Command $cmd -ErrorAction SilentlyContinue) {
            return $cmd
        }
    }
    return $null
}

function Test-PythonVersion {
    param([string]$PythonCmd)
    try {
        $verStr = & $PythonCmd --version 2>$null
        $ver = [System.Version]($verStr -replace "Python ", "")
        return ($ver.Major -eq 3 -and $ver.Minor -ge 11) -or ($ver.Major -gt 3)
    }
    catch {
        return $false
    }
}

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "AI-Native Framework Installer" -ForegroundColor Cyan
Write-Host "Detected OS: Windows" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# --- Execution policy check --------------------------------------------------

$policy = Get-ExecutionPolicy
if ($policy -eq "Restricted") {
    Write-Host "ℹ️  Your PowerShell execution policy is 'Restricted'. This installer avoids running local .ps1 files, so it should still work." -ForegroundColor DarkYellow
    Write-Host "   If you later want to run local scripts, use:" -ForegroundColor DarkYellow
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor DarkYellow
}
elseif ($policy -eq "AllSigned") {
    Write-Host "⚠️  Your PowerShell execution policy is 'AllSigned'. You may need to run:" -ForegroundColor Yellow
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
}

# --- Prerequisites -----------------------------------------------------------

Write-Host "Checking prerequisites..."

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is required but not installed. Please install Git and try again." -ForegroundColor Red
    exit 1
}

$pythonCmd = Get-PythonCommand
if (-not $pythonCmd) {
    Write-Host "❌ Python 3.11+ is required but neither 'python' nor 'python3' was found." -ForegroundColor Red
    exit 1
}

if (-not (Test-PythonVersion -PythonCmd $pythonCmd)) {
    $verStr = & $pythonCmd --version 2>$null
    Write-Host "❌ Python 3.11 or higher is required. Found $verStr" -ForegroundColor Red
    exit 1
}

# Check Docker availability (optional)
$dockerAvailable = (Get-Command docker -ErrorAction SilentlyContinue) -and (Get-Command docker-compose -ErrorAction SilentlyContinue)
if (-not $dockerAvailable) {
    Write-Host "⚠️  Docker and/or docker-compose not found. Local infrastructure will not be started." -ForegroundColor Yellow
    Write-Host "   You can start it later by running: cd infrastructure; docker-compose up -d" -ForegroundColor Yellow
}

# --- Clone or reuse repository -----------------------------------------------

if (Test-InsideRepo) {
    Write-Host "Repository already present at $(Get-Location). Skipping clone."
}
else {
    $installDir = Join-Path $env:USERPROFILE $RepoName
    if (Test-Path (Join-Path $installDir ".git")) {
        Write-Host "Directory $installDir already exists. Pulling latest changes..."
        Set-Location $installDir
        git pull
    }
    else {
        Write-Host "Cloning repository into $installDir..."
        git clone $RepoUrl $installDir
        Set-Location $installDir
    }
}

# Guard: ensure we are now in the repo root
if (-not (Test-InsideRepo)) {
    Write-Host "❌ Failed to locate repository root. Expected scripts\setup.sh, pyproject.toml, and .env.example." -ForegroundColor Red
    exit 1
}

# --- Local environment setup -------------------------------------------------

$venvPython = ".venv\Scripts\python.exe"
$venvPip = ".venv\Scripts\pip.exe"

Write-Host "Creating virtual environment..."
& $pythonCmd -m venv .venv

Write-Host "Upgrading pip in virtual environment..."
& $venvPython -m pip install --upgrade pip

Write-Host "Installing production dependencies..."
& $venvPip install -r requirements.txt

Write-Host "Installing development dependencies..."
& $venvPip install -r requirements-dev.txt

Write-Host "Creating project directories..."
New-Item -ItemType Directory -Force -Path "data\chroma" | Out-Null
New-Item -ItemType Directory -Force -Path "audit\sprints" | Out-Null
New-Item -ItemType Directory -Force -Path "pilots" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from template..."
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env with your actual API keys before running agents." -ForegroundColor Yellow
}

if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    Write-Host "Installing pre-commit hooks..."
    pre-commit install
}
elseif (Test-Path ".venv\Scripts\pre-commit.exe") {
    Write-Host "Installing pre-commit hooks..."
    & .venv\Scripts\pre-commit.exe install
}

# --- Smoke tests -------------------------------------------------------------

Write-Host "Running smoke tests..."
try {
    & $venvPython -m pytest tests\smoke -v
}
catch {
    Write-Host "⚠️  Smoke tests reported failures. The framework may still be usable." -ForegroundColor Yellow
}

# --- Start local infrastructure ----------------------------------------------

if ($dockerAvailable) {
    Write-Host ""
    Write-Host "Starting local infrastructure with Docker Compose..."
    Set-Location infrastructure
    docker-compose up -d
    Set-Location ..
    Write-Host ""
    Write-Host "Infrastructure services:"
    Write-Host "  Framework API: http://localhost:8000"
    Write-Host "  ChromaDB:      http://localhost:8001"
    Write-Host "  LangGraph:     http://localhost:8123"
    Write-Host "  Grafana:       http://localhost:3000"
}

# --- Completion --------------------------------------------------------------

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "1. Edit .env with your actual API keys"
Write-Host "2. Run: python -m src.simulations.sprint_simulation"
Write-Host "3. Review docs\14-master-execution-plan.md for the full operational playbook"
