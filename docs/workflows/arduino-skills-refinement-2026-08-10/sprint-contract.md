# Sprint Contract

```yaml
sprint_id: repair-and-independent-review
included_tasks:
  - "Remove the eager pyserial import so --help is usable without runtime dependencies."
  - "Create the required long-run harness recovery artifacts."
  - "Rerun the failed serial check and all applicable deterministic gates."
  - "Collect a fresh-context reviewer verdict."
excluded_tasks:
  - "Wiring, flashing, measuring, uploading, or deploying to physical boards."
  - "Global skill installation that overwrites the existing skill-creator."
  - "Publishing a release or changing the repository history."
done_criteria:
  - "The serial helper's --help path exits 0 under the host Python runtime."
  - "All structural, plugin, contract, forward-eval, syntax, and diff gates pass."
  - "The fresh reviewer artifact exists and its verdict is explicitly reported."
verification_criteria:
  - "Run only the failed serial check after the patch, then rerun the full suite."
  - "Inspect the final diff and check required artifact fields."
  - "Do not infer hardware or system success from any local result."
risks:
  - "The official Codex validator may require an unavailable PyYAML download."
  - "The reviewer may remain unavailable; this is a release blocker, not a passing verdict."
gate_expectations:
  functionality: ">=0.85"
  coverage: ">=0.85"
  regression: ">=0.85"
  evidence: ">=0.85"
```
