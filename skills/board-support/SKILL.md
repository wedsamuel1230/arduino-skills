---
name: board-support
description: Resolve a named Arduino, ESP32, RP2040, or other embedded board to a source-backed exact profile, including pin/peripheral capability, voltage/current, buses, framework/core/toolchain, and variant or revision risks. Use this whenever a user asks for a board reference, pinout, GPIO restrictions, board capability, board profile, or safe handoff before pin assignment. Do not use it to choose a board from requirements; use board-selection for that decision.
metadata: {triggers: "board reference, board capabilities, supported board, exact board, board pinout, GPIO restrictions, board profile, pin capability lookup, board variant, board revision"}
---

# Board Support

This is the authoritative AI-facing exact-board reference and lookup entry point
for the repository's source-backed board inventory. It resolves a named target to one exact profile,
extracts capabilities and risks, and hands the result to downstream skills. It
does not replace `board-selection`, which owns choosing or replacing a board
from project requirements.

## Read First

1. Read the [shared Arduino skill contract](../../docs/arduino-skill-contract.md).
2. Read the [board inventory](../../references/boards/index.json) and the
   [AI reference schema](../../references/boards/ai-reference-schema.md).
3. Read the matched Markdown profile and its fact-to-source map from
   `../../references/boards/`.
4. Load `../pin-assignment/SKILL.md` only when the user also asks for a GPIO
   allocation or declarations.
5. Load `../embedded-project-loop/SKILL.md` first when the request includes
   wiring, flashing, powering, measurement, recovery, or multi-session work.

For a repository checkout, use the deterministic resolver before interpreting
the profile:

```bash
python3 ../../scripts/resolve_board_profile.py \
  --query "<board name>" --purpose lookup
```

Use `--purpose pin` or `--purpose electrical` for those advice paths and pass
confirmed values with repeated `--identity FIELD=VALUE` options. A non-zero
resolver status is a stop condition, not permission to guess.

The index is a compact retrieval surface. The Markdown profile is the detailed
source-of-truth for facts, caveats, and gaps. Do not invent fields that are not
in the profile or its cited primary sources.

## Ownership And Routing

- Named-board lookup, capability questions, profile retrieval, exact pin-risk
  checks, source-confidence questions, and framework compatibility checks start
  here.
- Board choice, replacement, trade-off comparison, and lifecycle selection from
  requirements start at `board-selection`; it may call this skill for facts.
- Combined firmware/electronics/power/networking/deployment work starts at
  `arduino-workflow-router`; the router loads this skill when a named board must
  be resolved.
- Pin allocation and raw declaration formatting belong to `pin-assignment`.

## Resolution Procedure

1. Capture the board name, exact revision, module suffix, MCU, framework/core,
   toolchain, host, and requested proof stage. Mark missing values as unknown.
2. Normalize the user's board name against `id`, `name`, and `aliases` in the
   index. Require exactly one match. A marketing family, clone, carrier, or
   module with a different suffix is not an exact match.
3. Read the matched `identity_contract`. If its `profile_type` is
   `bounded-variant-family`, confirm the requested `variant` and every field in
   `required_for_pin_advice` or `required_for_electrical_advice` before giving
   advice that depends on that boundary. Common facts may be reported only when
   the profile marks them as shared; never silently choose a variant.
4. If identity is sufficient, read its Markdown profile and return the compact
   identity, logic level, memory, buses, ADC/PWM/timer capabilities, reserved
   or risky pins, framework/toolchain boundary, source confidence, and open gaps.
5. Keep MCU electrical limits separate from board regulator, connector, total
   GPIO, radio peak, or external-load limits. Preserve `unknown`, `gap`, and
   `verify` statements instead of filling them with family assumptions.
6. For a framework request, record the exact board package/core, version or
   commit, FQBN/PlatformIO environment, library versions, and upload tool. A
   profile's framework list is compatibility scope, not proof that a build ran.
7. For a pin request, pass this handoff to `pin-assignment`:

   ```text
   board_id: <index id>
   profile: <references/boards/*.md>
   resolution_status: <resolved | needs-disambiguation | unsupported | profile-gap>
   exact_identity: <board revision and module, or unknown>
   identity_contract: <profile_type, variant, and required fields>
   framework_core: <framework/core/version or unknown>
   logic_level: <value and source status>
   reserved_or_risky_pins: <input-only, strapping, flash/PSRAM, USB, debug, bus, LED>
   usable_capabilities: <ADC/PWM/UART/I2C/SPI/touch/PIO/etc.>
   unresolved: <gaps that block a safe assignment>
   ```

   `pin-assignment` must re-check the exact physical pins before emitting any
   declaration. Keep logical IDs separate from physical GPIO numbers and
   preserve the raw ordered `constexpr int` convention.

## Resolution Envelope

Start the response with this compact record so another skill can consume the
lookup without parsing prose. Use `needs-disambiguation` when a bounded family
is matched but a required variant, revision, module, or framework field is
missing. Use `profile-gap` when the identity is sufficient but the requested
fact is not source-backed in the profile.

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

## Ambiguous And Unsupported Targets

- If multiple profiles match, stop and ask for the revision, module suffix,
  board photo, product identifier, or framework target needed to disambiguate.
- If no profile matches, say `unsupported by the indexed board set`, provide the
  minimum primary sources needed for a new profile, and do not map pins from a
  similar board. `board-selection` may compare it only after its identity and
  sources are established.
- For clones and carriers, identify the reference profile as a comparison only
  and label every unverified board-level assumption.

## Output Contract

Return these sections, even for a short lookup:

1. **Assumptions**: exact identity, unknowns, and clone/revision boundary.
2. **Required tools and versions**: framework/core, board package, toolchain,
   host, and library versions needed for the requested path.
3. **Implementation steps**: ordered lookup, profile, and downstream handoff.
4. **Tests and evidence**: source/profile checks and proof stage; mark physical,
   build, upload, system, and deployment stages separately.
5. **Known limitations**: unsupported fields, source gaps, and revision scope.
6. **Recovery and security notes**: boot/USB/debug risks, rollback path, and
   secret-handling requirements when the target is connected.

## Anti-Rationalization

| Shortcut | Required response |
|---|---|
| "It is an ESP32, so the pins are known." | Resolve exact family, module, DevKit revision, and framework variant. |
| "The index says source-backed, so every value is verified." | Read the profile's fact-to-source map and preserve explicit gaps. |
| "A similar board has the same header." | Stop at the identity boundary; request a primary board source. |
| "The core supports the board, so it compiled." | Report compatibility scope only; require fresh build evidence. |
| "The pin list looks safe." | Re-check boot, flash/PSRAM, USB, bus, voltage, pull, and current constraints. |
| "The family profile matched, so I can choose its variant." | Return `needs-disambiguation` and ask for the required variant or revision. |
| "The resolution envelope says resolved, so hardware is proven." | Keep `physical_status: unverified` until the user supplies board-specific evidence. |

## Verification Boundary

Source lookup and schema validation are documentation evidence. They do not
prove wiring, power, flashing, runtime behavior, system behavior, or field
deployment. If the next step requires a physical action, use the shared
physical-world gate and ask one concrete user question before continuing.

Use the [shared Arduino skill contract](../../docs/arduino-skill-contract.md)
for assumptions, tools, implementation steps, evidence, limitations, and
recovery/security notes.
