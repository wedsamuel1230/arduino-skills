# Recovery And Rollback Planning

Use this reference before recommending OTA for a device whose physical access is
limited.

## Pre-Deployment Questions

- Is there still a practical USB or serial recovery path?
- Can the device be power-cycled safely if the update fails?
- Is the rollout changing networking, boot flow, or storage layout?
- Is there a known-good version to return to?

## Recovery Principles

- do not spend the only recovery path in the same rollout that changes network
  behavior
- prefer one variable at a time for remote updates
- capture exact board core, library, and tooling versions when the old build is
  known good

## Rollback Checklist

- keep a known-good binary or sketch revision available
- preserve enough logging to distinguish boot failure from discovery failure
- avoid making the first remote rollout also the largest architectural change

## Uno R4 WiFi Note

Uno R4 WiFi has additional connectivity-side complexity. Before treating it
like a generic OTA board, review the shared board-family reference at
`../../docs/board-support/uno-r4-family.md`.
