# PowerShell script to build Synology DSM package
# This script creates a .spk file from the package directory

param(
    [string]$OutputName = "photo-organizer.spk"
)

Write-Host "Building Synology DSM package..." -ForegroundColor Green

# Check if package directory exists
if (-not (Test-Path "package")) {
    Write-Host "Error: package directory not found!" -ForegroundColor Red
    exit 1
}

# Create temporary build directory
$BuildDir = "build"
if (Test-Path $BuildDir) {
    Remove-Item -Recurse -Force $BuildDir
}
New-Item -ItemType Directory -Path $BuildDir | Out-Null

Write-Host "Copying package files..." -ForegroundColor Yellow

# Copy package structure
Copy-Item -Recurse "package\*" "$BuildDir\"

# Make scripts executable (for Linux compatibility)
Write-Host "Setting script permissions..." -ForegroundColor Yellow
$scripts = Get-ChildItem -Path "$BuildDir\scripts" -File
foreach ($script in $scripts) {
    # Note: On Windows, we can't set Unix permissions, but this will be handled on Synology
    Write-Host "  - $($script.Name)"
}

# Create SPK file using tar (if available) or zip
Write-Host "Creating package archive..." -ForegroundColor Yellow

if (Get-Command tar -ErrorAction SilentlyContinue) {
    # Use tar for proper .spk format
    Set-Location $BuildDir
    tar -czf "../$OutputName" *
    Set-Location ..
    Write-Host "Package created: $OutputName" -ForegroundColor Green
} else {
    # Fallback to zip (may need to be renamed to .spk)
    $ZipName = $OutputName -replace '\.spk$', '.zip'
    Compress-Archive -Path "$BuildDir\*" -DestinationPath $ZipName -Force
    Write-Host "Package created as ZIP: $ZipName" -ForegroundColor Yellow
    Write-Host "Note: Rename to .spk if needed, or use tar to create proper .spk format" -ForegroundColor Yellow
}

# Cleanup
Remove-Item -Recurse -Force $BuildDir

Write-Host "`nBuild complete!" -ForegroundColor Green
Write-Host "Package file: $OutputName" -ForegroundColor Cyan
Write-Host "`nTo install on Synology:" -ForegroundColor Yellow
Write-Host "1. Copy $OutputName to your Synology NAS" -ForegroundColor White
Write-Host "2. Open Package Center" -ForegroundColor White
Write-Host "3. Click Manual Install" -ForegroundColor White
Write-Host "4. Select the $OutputName file" -ForegroundColor White

