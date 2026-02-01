# Arduino CLI Workflow Script (Windows PowerShell)

# This script demonstrates a complete workflow: detect board, compile, and upload
# Requires arduino-cli installed and a connected Arduino board

param(
    [string]$SketchPath = "C:\path\to\sketch",  # Update this path
    [string]$BoardFQBN = "arduino:avr:uno"      # Update for your board
)

Write-Host "Arduino CLI Workflow Script (Windows)" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Step 1: Detect COM ports
Write-Host "`n1. Detecting serial ports..." -ForegroundColor Yellow
$ports = Get-PnpDevice -Class Ports | Where-Object { $_.FriendlyName -match 'COM' }
if ($ports) {
    Write-Host "Found ports:" -ForegroundColor Green
    $ports | ForEach-Object { Write-Host "  $($_.Name) - $($_.FriendlyName)" }
    $port = $ports[0].Name  # Use first detected port
    Write-Host "Using port: $port" -ForegroundColor Cyan
} else {
    Write-Host "No COM ports detected. Please connect your Arduino board." -ForegroundColor Red
    exit 1
}

# Step 2: Compile sketch
Write-Host "`n2. Compiling sketch..." -ForegroundColor Yellow
& arduino-cli compile --fqbn $BoardFQBN $SketchPath
if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed." -ForegroundColor Red
    exit 1
}
Write-Host "Compilation successful." -ForegroundColor Green

# Step 3: Upload to board
Write-Host "`n3. Uploading to board..." -ForegroundColor Yellow
& arduino-cli upload -p $port --fqbn $BoardFQBN $SketchPath
if ($LASTEXITCODE -ne 0) {
    Write-Host "Upload failed." -ForegroundColor Red
    exit 1
}
Write-Host "Upload successful!" -ForegroundColor Green

Write-Host "`nWorkflow complete. Your sketch should now be running on the board." -ForegroundColor Green