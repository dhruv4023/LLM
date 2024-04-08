# Set the project directory and Virtual Environment name
$venvName = ".venv"

# Check if the Virtual Environment folder exists
$venvExists = Test-Path $venvName

if (-not $venvExists) {
    # Create Virtual Environment if it doesn't exist
    Write-Host "Creating Virtual Environment..."
    python -m venv $venvName
}

Write-Host "+--------------------------------------------------------------------------------------+"
Write-Host "Activating Virtual Environment..."

& .\.venv\Scripts\Activate.ps1

Write-Host "+--------------------------------------------------------------------------------------+"
Write-Host "Virtual Environment activated"
Write-Host "Installing dependencies..."
Write-Host "+--------------------------------------------------------------------------------------+"

try {
    python -m pip install -r "requirements.txt"
    Write-Host "+--------------------------------------------------------------------------------------+"
    Write-Host "All modules installed successfully"
    Write-Host "+--------------------------------------------------------------------------------------+"
} catch {
    Write-Host "An error occurred while installing modules: $_"
    Write-Host "Some modules might not be installed correctly."
    Write-Host "+--------------------------------------------------------------------------------------+"
}
