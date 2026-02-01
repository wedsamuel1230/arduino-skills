#!/usr/bin/env bash
set -euo pipefail

FQBNS=(
  "arduino:avr:uno"
  "esp32:esp32:esp32"
  "rp2040:rp2040:rpipico"
)

if ! command -v arduino-cli >/dev/null 2>&1; then
  echo "arduino-cli not found in PATH. Install it before running this script." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="${SCRIPT_DIR}/../examples"

EXAMPLES=(
  "config-example.ino"
  "filtering-example.ino"
  "buttons-example.ino"
  "i2c-example.ino"
  "csv-example.ino"
  "scheduler-example.ino"
  "state-machine-example.ino"
  "hardware-detection-example.ino"
  "data-logging-example.ino"
)

FAILED=()

for fqbn in "${FQBNS[@]}"; do
  echo ""
  echo "=== Compiling examples for ${fqbn} ==="

  for example in "${EXAMPLES[@]}"; do
    echo "Compiling ${example}"
    if ! arduino-cli compile --fqbn "${fqbn}" "${EXAMPLES_DIR}/${example}"; then
      FAILED+=("${fqbn} :: ${example}")
    fi
  done
done

if [ "${#FAILED[@]}" -gt 0 ]; then
  echo ""
  echo "Compilation failures:"
  for item in "${FAILED[@]}"; do
    echo " - ${item}"
  done
  exit 1
fi

echo ""
echo "All examples compiled successfully."
