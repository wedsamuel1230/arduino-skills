# Plugin Distribution

`skills/` is the only skill-content source of truth. Provider manifests and
instruction files are thin adapters; they do not contain copies of `SKILL.md`.
For physical or multi-session requests, `skills/embedded-project-loop/` is the
recommended first skill; it owns durable state and user-provided evidence
while the router composes the remaining specialists.

## Install Commands

### Agent Skills CLI

Install the complete shared tree into the detected agent targets:

```bash
npx skills add wedsamuel1230/arduino-skills
```

To install one self-contained specialist from the repository, use the CLI's
per-skill path selection:

```bash
npx skills add wedsamuel1230/arduino-skills --skill pin-assignment
```

`board-support`, `board-selection`, `pin-assignment`, and the workflow router
are package-context skills: their contract, index, profiles, and neighboring
skills are intentionally shared resources. Install the complete repository or
host plugin for those entry points. A per-skill copy without
`references/boards/`, `docs/arduino-skill-contract.md`, and the resolver is not
a supported board-reference installation.

Use `-g -y` for a user-level install when the skill should be available across
projects, or `-a claude-code cursor` to target named Agent Skills hosts.

### Codex

From a checkout, the plugin manifest is `.codex-plugin/plugin.json` and the
repository marketplace entry is `.agents/plugins/marketplace.json`. Because
this is an explicit repository marketplace rather than Codex's default personal
marketplace, install it with:

```bash
codex plugin marketplace add /path/to/arduino-skills
codex plugin add arduino-skills@arduino-skills
```

The Codex marketplace entry uses the host schema's local source object:

```json
"source": {"source": "local", "path": "./"}
```

For a published repository, use the Codex plugin marketplace flow for the
repository URL, then install `arduino-skills` from the displayed marketplace:

```bash
codex plugin marketplace add https://github.com/wedsamuel1230/arduino-skills
codex plugin add arduino-skills@arduino-skills
```

The URL flow is the supported public-install path; use the local checkout form
above when validating unpublished changes.
Codex plugin behavior changes with releases; validate against the installed
Codex version before publishing a lock-step release.

### Claude Code

Test the local adapter:

```bash
claude --plugin-dir /path/to/arduino-skills
```

For distribution, add the repository's `.claude-plugin/marketplace.json` to the
Claude Code marketplace flow and install the `arduino-skills` plugin. Claude
loads the same `skills/` directories and namespaced skills.

### Cursor

Open or install the repository as a Cursor plugin using
`.cursor-plugin/marketplace.json`. The `.cursor/rules/arduino-skills.mdc` file
is only a thin routing rule; skill instructions remain under `skills/`.

### Repository wrappers

`AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are intentionally short conventions
for hosts that load those files automatically. They do not replace the plugin
or Agent Skills install path.

## Packaging checks

Run these before publishing:

```bash
python3 scripts/validate_agent_skills.py
python3 scripts/validate_arduino_plugin.py
python3 scripts/run_arduino_evals.py --output evals/eval-results.json
UV_CACHE_DIR=/private/tmp/arduino-skills-uv-cache uv run --no-project --with pyyaml \
  /Users/wed/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

The first validates each `SKILL.md`; the second checks links, manifests,
triggers, eval fixtures, board references, and preserved baseline inventory; the
third validates the Codex ingestion manifest.

## Source-of-truth rule

Do not copy skills into host-specific folders in this repository. A host may
cache or symlink the package during installation, but changes must be made in
`skills/` and then revalidated for every host adapter.
Per-skill provider marketplace files are intentionally absent; adding one would
create a second, stale discovery surface.

## Creator references

The authoring workflow follows the public Agent Skills creator guidance for
concise trigger descriptions, progressive disclosure, and fresh-context
forward testing. Plugin scaffolding and Codex manifest checks follow the
OpenAI `plugin-creator` guidance. The exact companion sources used during
development are pinned in `skills-lock.json`; they are optional tooling and
are not copied into this plugin's `skills/` payload.
