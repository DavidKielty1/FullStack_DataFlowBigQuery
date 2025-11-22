# PowerShell script to check Docker status on Windows

Write-Host "Checking Docker installation..." -ForegroundColor Cyan

# Check if Docker is installed
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not found"
    }
    Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker daemon is running
try {
    docker info | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker daemon not running"
    }
    Write-Host "✅ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker daemon is not running" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please start Docker Desktop:" -ForegroundColor Yellow
    Write-Host "  - Look for Docker Desktop icon in system tray" -ForegroundColor Yellow
    Write-Host "  - Or launch Docker Desktop from Start Menu" -ForegroundColor Yellow
    Write-Host "  - Wait for Docker to fully start (whale icon should be steady)" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Docker Compose version:" -ForegroundColor Cyan
docker-compose --version

Write-Host ""
Write-Host "✅ Ready to run: docker-compose up --build" -ForegroundColor Green

