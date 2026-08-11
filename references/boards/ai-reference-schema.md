# AI Board Reference Schema

This schema defines the compact discovery record in `index.json` (schema
version 3). It is an
index for retrieval and routing, not a replacement for the Markdown profile.
Detailed values, caveats, source URLs, and fact-to-source mappings remain in
the linked profile. Unknown or board-specific values must stay explicit.

## Required Record Fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable lowercase profile identifier. |
| `name` | string | Exact board or explicitly bounded board family name. |
| `path` | string | One Markdown profile under `references/boards/`. |
| `aliases` | list of strings | Names an agent may normalize to this profile. Do not include broad family names that would hide ambiguity. |
| `mcu` | string | MCU/module identity used by the profile; include a split connectivity MCU when it changes the contract. |
| `architecture` | string | CPU/architecture summary relevant to code and library compatibility. |
| `logic_level` | string | Board GPIO logic class; never infer tolerance of a peripheral from this label. |
| `capability_tags` | list of strings | Query terms such as `adc`, `pwm`, `i2c`, `spi`, `uart`, `usb`, `pio`, `wifi`, or `5v-logic`. |
| `risk_tags` | list of strings | Queryable hazards such as `strapping-pins`, `flash-psram-pins`, `usb-pins`, or `clone-variance`. |
| `identity_scope` | string | What the profile covers and what requires a separate revision/module check. |
| `identity_contract` | object | Machine-readable exact-board or bounded-variant-family boundary used before pin or electrical advice. |
| `toolchains` | list of strings | Toolchain families that the profile discusses; versions remain a required intake field. |
| `evidence` | object | `source_confidence`, `checked`, and `physical_status`. |

## Evidence Values

- `source_confidence` describes documentation provenance, not runtime success.
  Use `primary-source-backed-with-explicit-gaps` when primary sources exist but
  board revision, aggregate current, calibration, or clone behavior remains
  unresolved.
- `checked` is the date of the profile source review. A mutable product page is
  date-checked, not immutable.
- `physical_status` is `unverified` until the user provides a board-specific
  measurement, log, or photo. A passing validator never changes this field.

### Identity contract

Every record has an `identity_contract` object:

| Field | Type | Meaning |
|---|---|---|
| `profile_type` | string | `exact-board` or `bounded-variant-family`. |
| `variants` | list of strings | Explicit variants covered by a shared profile; empty for an exact-board profile. |
| `required_for_pin_advice` | list of strings | Identity fields that must be confirmed before variant-sensitive pin advice. |
| `required_for_electrical_advice` | list of strings | Identity fields that must be confirmed before variant-sensitive voltage, current, or power advice. |

When `profile_type` is `bounded-variant-family`, the agent may use shared facts
only when the requested fact is explicitly common to the profile. It must return
`needs-disambiguation` for a variant-sensitive request until all applicable
required fields are known. This prevents a generic `Pico`, `Uno R4`, or `ESP32
DevKit` label from becoming an unsafe variant assumption.

## Retrieval Algorithm

1. Normalize a user name to lowercase words and compare it with `id`, `name`,
   and `aliases`.
2. Accept one exact match only. Zero matches are unsupported; multiple matches
   are ambiguous and require more identity data.
3. Apply `identity_contract` before routing variant-sensitive advice. A single
   profile match is not sufficient when a bounded family still needs a variant,
   module suffix, revision, flash/PSRAM population, USB mode, or similar field.
4. Use the compact fields to route and filter. Load the Markdown profile for
   any fact that affects pins, voltage, current, memory, buses, boot, USB,
   flash/PSRAM, library compatibility, or recovery.
5. Treat `capability_tags` as a search hint, not a promise of available pins.
   The profile and exact framework variant decide the physical assignment.
6. Pass the profile path, exact identity, framework/core, reserved pins, and
   unresolved gaps to `pin-assignment`, `wiring-safety-check`, or
   `board-selection` as appropriate.

## Resolution envelope

`board-support` returns a stable handoff before the shared prose sections:

```yaml
resolution_status: resolved | needs-disambiguation | unsupported | profile-gap
board_id: <index id or null>
profile: <references/boards/*.md or null>
matched_alias: <normalized user term or null>
identity:
  profile_type: <exact-board | bounded-variant-family | null>
  variant: <confirmed value or unknown>
  revision: <confirmed value or unknown>
  module_suffix: <confirmed value or unknown>
required_disambiguators: []
framework_core: <name/version or unknown>
evidence:
  source_confidence: <index value or unknown>
  checked: <YYYY-MM-DD or unknown>
  physical_status: unverified
```

The envelope is a routing record, not a build, upload, hardware, system, or
deployment claim. `unsupported` means no indexed profile matched; `profile-gap`
means the profile matched but the requested fact is not source-backed.

## Example Record

```json
{
  "id": "esp32-c3-devkitc-02",
  "name": "ESP32-C3-DevKitC-02",
  "aliases": ["ESP32-C3 DevKitC-02", "ESP32-C3-WROOM-02 DevKit"],
  "mcu": "ESP32-C3",
  "architecture": "single-core RISC-V",
  "logic_level": "3.3 V",
  "capability_tags": ["adc", "i2c", "pwm", "spi", "uart", "usb", "wifi", "ble"],
  "risk_tags": ["strapping-pins", "usb-jtag-pins", "adc2-wifi", "rgb-led-pin", "module-variance"],
  "identity_scope": "Official DevKitC-02 with WROOM-02/02U; clone and revision differences require verification.",
  "identity_contract": {
    "profile_type": "bounded-variant-family",
    "variants": ["WROOM-02", "WROOM-02U"],
    "required_for_pin_advice": ["module_suffix", "devkit_revision"],
    "required_for_electrical_advice": ["module_suffix", "devkit_revision"]
  },
  "toolchains": ["Arduino IDE", "Arduino CLI", "PlatformIO", "ESP-IDF"],
  "evidence": {
    "source_confidence": "primary-source-backed-with-explicit-gaps",
    "checked": "2026-08-11",
    "physical_status": "unverified"
  }
}
```

## Sources And Maintenance

- [Agent Skills specification](https://agentskills.io/specification)
- [Arduino board documentation](https://docs.arduino.cc/hardware/)
- [Espressif GPIO documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html)
- [Raspberry Pi Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)

When a profile changes, update its index summary, identity contract, Markdown fact-to-source map,
source ledger, and checked date together. Run
`python3 scripts/validate_board_references.py` before treating the record as
discoverable.
