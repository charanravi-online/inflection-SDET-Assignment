# Exit on any error
$ErrorActionPreference = "Stop"

# Function to check if a Python package is installed
function Check-PythonPackage($package) {
    try {
        $output = python -c "import $package" 2>$null
        return $true
    } catch {
        return $false
    }
}

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
if (-not (Check-Command "pytest")) {
    Write-Error "pytest is not installed or not in PATH. Please run '.\setup.ps1' first to set up the environment."
    exit 1
}

# Check if pytest-html is installed as a Python package
if (-not (Check-PythonPackage "pytest_html")) {
    Write-Error "pytest-html is not installed. Please run '.\setup.ps1' or install it with 'pip install pytest-html' in the virtual environment."
    exit 1
}

# Ensure Docker services are running (assuming docker-compose-e2e.yml is running from setup.ps1)
Write-Host "Verifying Docker services are running..."
$containers = docker ps --format "{{.Names}}" | Select-String "demo-campaign-scheduling|demo-email-templates|demo-recipient|mongodb"
if ($containers -eq $null) {
    Write-Error "Docker services are not running. Please run '.\setup.ps1' first to start them."
    exit 1
}

# Run E2E tests with xdist and generate report
Write-Host "Running End-to-End tests with pytest-xdist..."
try {
    pytest tests\e2e\test_e2e.py -n auto --html=test_report_e2e.html --self-contained-html
} catch {
    Write-Error "Failed to run E2E tests: $_"
    exit 1
}

# Run Integration tests with xdist and generate report
Write-Host "Running Integration tests with pytest-xdist..."
try {
    pytest tests\integration\test_integration.py -n auto --html=test_report_integration.html --self-contained-html
} catch {
    Write-Error "Failed to run Integration tests: $_"
    exit 1
}

Write-Host "Tests completed! Reports are saved as test_report_e2e.html and test_report_integration.html in the root directory."