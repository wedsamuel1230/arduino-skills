# Arduino skills source

The canonical skill content is under `skills/`. Select the smallest matching
`SKILL.md`, and load `references/` or `docs/` only when the skill points to it.

Preserve the raw ordered `constexpr int` pin-declaration convention and
C/C++ embedded-first guidance. Keep compile, upload, hardware, system, and
deployment evidence separate. Do not claim physical success without a user
provided measurement, log, or photo.

For physical or multi-session work, load `skills/embedded-project-loop/SKILL.md`
first, then use the workflow router for specialist routing.

Provider manifests in `.codex-plugin/`, `.claude-plugin/`, and
`.cursor-plugin/` are adapters only; do not duplicate skill instructions there.
