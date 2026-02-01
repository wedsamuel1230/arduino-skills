param(
    [string[]]$FqbnList = @(
        "arduino:avr:uno",
        "esp32:esp32:esp32",
        "rp2040:rp2040:rpipico"
    )
)

$cli = Get-Command arduino-cli -ErrorAction SilentlyContinue
if (-not $cli) {
    Write-Error "arduino-cli not found in PATH. Install it before running this script."
    exit 1
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$examplesDir = Resolve-Path (Join-Path $scriptRoot "..\examples")

$examples = @(
    "config-example.ino",
    "filtering-example.ino",
    "buttons-example.ino",
    "i2c-example.ino",
    "csv-example.ino",
    "scheduler-example.ino",
    "state-machine-example.ino",
    "hardware-detection-example.ino",
    "data-logging-example.ino"
)

$failed = @()

foreach ($fqbn in $FqbnList) {
    Write-Host "\n=== Compiling examples for $fqbn ===" -ForegroundColor Cyan

    foreach ($example in $examples) {
        $examplePath = Join-Path $examplesDir $example
        Write-Host "Compiling $example" -ForegroundColor Gray

        & arduino-cli compile --fqbn $fqbn $examplePath
        if ($LASTEXITCODE -ne 0) {
            $failed += "$fqbn :: $example"
        }
    }
}

if ($failed.Count -gt 0) {
    Write-Host "\nCompilation failures:" -ForegroundColor Red
    $failed | ForEach-Object { Write-Host " - $_" }
    exit 1
}

Write-Host "\nAll examples compiled successfully." -ForegroundColor Green
