# Board References

Use these profiles only after identifying the exact board, revision, module
suffix, Arduino core/framework, and toolchain version. Values marked as a gap
are intentionally not guessed. Board-family facts do not prove that a clone,
carrier, or populated module exposes the same pins.

`index.json` is the compact AI retrieval surface. It contains aliases, MCU and
architecture identity, logic level, capability/risk tags, an identity contract,
toolchain families, and evidence status for fast routing. The Markdown profile
linked by `path` is still required for detailed pin, bus, memory, current, boot,
and source claims. Use `scripts/resolve_board_profile.py` for exact lookups;
do not replace an `identity_contract` boundary with fuzzy matching.
Use [the board-support skill](../../skills/board-support/SKILL.md) for named
board lookup and [the AI reference schema](ai-reference-schema.md) when adding
or reviewing an index record. Use [board-selection](../../skills/board-selection/SKILL.md)
when the user is choosing or replacing a board from requirements.

The machine-readable inventory is [index.json](index.json). It is the
discovery surface used by the board-reference validator; the Markdown profiles
remain the human-readable source of the fact-to-source maps.

| Target | Reference |
|---|---|
| Arduino Uno R3 | [arduino-uno-r3.md](arduino-uno-r3.md) |
| Arduino Uno R4 Minima and WiFi | [arduino-uno-r4.md](arduino-uno-r4.md) |
| Arduino Mega 2560 Rev3 | [arduino-mega-2560.md](arduino-mega-2560.md) |
| Arduino Nano Every | [arduino-nano-every.md](arduino-nano-every.md) |
| Arduino Nano ESP32 | [arduino-nano-esp32.md](arduino-nano-esp32.md) |
| Classic ESP32 DevKit / WROOM | [esp32-devkit.md](esp32-devkit.md) |
| ESP32-C3-DevKitC-02 | [esp32-c3-devkitc-02.md](esp32-c3-devkitc-02.md) |
| ESP32-S3 DevKit | [esp32-s3-devkit.md](esp32-s3-devkit.md) |
| Raspberry Pi Pico and Pico W | [pico-pico-w.md](pico-pico-w.md) |

The source and accessibility ledger is [source-ledger.md](source-ledger.md).
It records the check date, immutable commit pins where a repository is used,
document identifiers where a datasheet exposes one, and any fetch or
verification gap.

## AI lookup boundary

Resolve `id`, `name`, or `aliases` to exactly one profile. Zero matches are
unsupported by this indexed set; multiple matches are ambiguous. A single
profile match with `profile_type: bounded-variant-family` is still incomplete
for variant-sensitive advice until its required identity fields are confirmed.
Do not use a capability tag as proof that every pin is available. Load the
detailed profile and selected framework variant before assigning pins or giving
electrical, current, boot, upload, or recovery advice. `physical_status:
unverified` remains true until a user supplies board-specific evidence.

## Source policy

Prefer the board product page and MCU/module datasheet, then the selected
Arduino core's variant source for default bus maps. Record the source revision
when a pin assignment or electrical limit matters. Do not treat `PWM`, `ADC`,
or `touch` labels as available pins until conflicts with boot, flash, PSRAM,
USB, debug, radio, and other buses are checked.

The five baseline profiles were checked on 2026-08-10 and the four added
profiles on 2026-08-11. A product page without a public revision is identified
as date-checked rather than falsely treated as a pinned snapshot. A fact that
cannot be confirmed from an accessible primary source is listed as a gap in
the profile and ledger.

## Shared safety rules

- 5 V logic is not automatically safe for a 3.3 V MCU.
- A per-pin maximum is not a safe total-board load budget.
- ADC resolution is not ADC accuracy or a guaranteed input range.
- PWM is not a DAC voltage.
- A successful compile or upload is not hardware or system proof.
