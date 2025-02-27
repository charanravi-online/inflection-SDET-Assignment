# Exit on any error
$ErrorActionPreference = "Stop"

# Function to check if a command exists
function Check-Command($cmd) {
    try {
        $null = Get-Command $cmd -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Check prerequisites
Write-Host "Checking prerequisites..."
if (-not (Check-Command "docker-compose")) {
    Write-Error "Docker Compose is not installed or not in PATH. Please install Docker Desktop and ensure docker-compose is available."
    exit 1
}
if (-not (Check-Command "python")) {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.11.1 or later."
    exit 1
}

# Create and activate virtual environment
$venvDir = "venv"
if (-not (Test-Path $venvDir)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvDir
} else {
    Write-Host "Virtual environment already exists, skipping creation..."
}

Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1  # Use Activate.ps1 for PowerShell

# Install requirements
Write-Host "Installing dependencies from requirements.txt..."
python -m pip install --no-cache-dir -r requirements.txt

# Start Docker Compose E2E services
Write-Host "Starting Docker Compose E2E services..."
docker-compose -f docker-compose-e2e.yml up -d
Start-Sleep -Seconds 120  # Wait for services to start

Write-Host "Setup completed successfully! Run '.\run.ps1' to execute tests."
Write-Host "Note: Docker services are running in the background. Stop them with 'docker-compose -f docker-compose-e2e.yml down' when done."
Write-Host "PLEASE WAIT TILL THE DOCKER CONTAINERS ARE UP AND RUNNING BEFORE RUNNING THE TESTS."
