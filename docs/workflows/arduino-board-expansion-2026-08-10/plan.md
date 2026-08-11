# Board Expansion Loop Plan

## Define

Use the existing board-reference format and preserve all five current
profiles. The primary metric is the number of complete, source-backed profiles
that pass the new board-reference validator.

## Plan

1. Establish the five-profile baseline and preserve hashes.
2. Research the candidate pool from Arduino, Espressif, MCU datasheets, and
   pinned Arduino-core variant sources.
3. Keep only candidates that satisfy the source and field gates.
4. Add profiles, a machine-readable board index, source-ledger rows, and
   validator coverage in one cohesive patch.
5. Run targeted board checks, then the full plugin, contract, forward, syntax,
   link, and regression suite.
6. Obtain an independent read-only review and keep or revert the candidate.

## Stop and rollback

Stop if a candidate's board identity, pin map, or electrical limits cannot be
verified from primary sources. Roll back only the expansion patch if any
existing profile hash or validator gate regresses.
