# Wayfinder Map: Authoritative Board-Support Agent Skill

## Destination

Define and, if justified by the research, implement one authoritative board-support
Agent Skill and reference contract that lets an AI identify an exact Arduino or
embedded board, retrieve source-backed capabilities safely, compare compatible
frameworks/toolchains, hand off valid pins to downstream skills, and expose
unknowns without guessing.

## Notes

- Local-markdown Wayfinder tracker: this repository has no configured issue tracker.
- Consult `loop-engine`, `wayfinder`, and the repository `AGENTS.md` before edits.
- `skills/` remains the sole skill-content source of truth.
- Preserve raw ordered `constexpr int` declarations and C/C++ embedded-first guidance.
- Keep build, upload, hardware, system, and deployment evidence separate.
- No physical board, compile, upload, power, or measurement proof is in scope.
- This map carries one bounded research decision; implementation follows only after
  the decision is recorded and its acceptance gates are testable.

## Decisions so far

- [Choose the authoritative board-support Agent Skill contract](tickets/authoritative-board-support-contract.md) — `board-support` owns exact named-board lookup; `board-selection` owns choosing or replacing a board; the index now exposes a compact AI retrieval contract.
- [Make Board Resolution Variant-Safe For AI Consumers](tickets/ai-resolution-and-trigger-contract.md) — schema v3 adds advice-specific identity contracts, a stable resolution envelope, a deterministic resolver, and a held-out trigger corpus.

## Not yet specified

- Whether to add GIGA R1 WiFi or ESP32-C6 profiles in a separate source/core
  variant review.
- How to run the held-out trigger corpus through a host agent and record activation rates.

## Out of scope

- Physical validation, flashing, wiring, power measurements, system tests, and
  deployment claims.
- Duplicating skill bodies into provider manifests.
- Adding a board profile without two authoritative sources and explicit gaps.
- Broad redesign of unrelated Arduino specialist skills.

## Frontier

No open ticket remains in this bounded map. The implementation handoff is ready;
host-level activation and physical evidence remain outside this local decision.
