# ============================================================
# setup.ps1 — ClaimSense Development Environment Bootstrap
# Run this ONCE after cloning the repository.
# Usage:  .\setup.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$ProjectName = "ClaimSense"

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  $ProjectName — Environment Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check Python version ──────────────────────────────────
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow
$pyVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed. Please install Python 3.11+ from https://python.org" -ForegroundColor Red
    exit 1
}
Write-Host "  Found: $pyVersion" -ForegroundColor Green

# ── 2. Create virtual environment ────────────────────────────
Write-Host "[2/6] Creating virtual environment (.venv)..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "  .venv already exists. Skipping creation." -ForegroundColor Gray
} else {
    python -m venv .venv
    Write-Host "  Virtual environment created." -ForegroundColor Green
}

# ── 3. Activate and upgrade pip ──────────────────────────────
Write-Host "[3/6] Activating environment and upgrading pip..." -ForegroundColor Yellow
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip --quiet
Write-Host "  pip upgraded." -ForegroundColor Green

# ── 4. Install dependencies ───────────────────────────────────
Write-Host "[4/6] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "  All packages installed." -ForegroundColor Green

# ── 5. Set up .env ────────────────────────────────────────────
Write-Host "[5/6] Setting up environment file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "  .env created from .env.example. Please fill in your actual values!" -ForegroundColor Yellow
} else {
    Write-Host "  .env already exists. Skipping." -ForegroundColor Gray
}

# ── 6. Verify key packages ────────────────────────────────────
Write-Host "[6/6] Verifying key package installations..." -ForegroundColor Yellow
$packages = @("langchain", "fastapi", "streamlit", "mlflow", "sklearn", "xgboost", "faiss")
foreach ($pkg in $packages) {
    $result = python -c "import $pkg; print('  OK: $pkg')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host $result -ForegroundColor Green
    } else {
        Write-Host "  WARN: $pkg import failed" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Edit .env with your Azure OpenAI keys and DB credentials"
Write-Host "  2. Open claimsense.code-workspace in VS Code"
Write-Host "  3. Run: python src/data/generate_synthetic_data.py"
Write-Host "  4. Run: python src/rag/build_knowledge_base.py"
Write-Host "  5. Run: python src/ml/train_classifier.py"
Write-Host "  6. Run: uvicorn src.api.main:app --reload  (API on :8080)"
Write-Host "  7. Run: streamlit run src/dashboard/app.py  (UI on :8501)"
Write-Host ""
