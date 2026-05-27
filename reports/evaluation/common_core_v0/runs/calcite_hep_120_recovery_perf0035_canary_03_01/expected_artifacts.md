# Expected Artifacts

When the human operator runs this bounded canary, it should retain:

- `run_results.json`
- `run_event_long.csv`
- repaired generated SQL under `generated/<CASE>/<engine>/`
- workspaces with:
  - `source.sql`
  - `generated.sql`
  - `source.tsv`
  - `generated.tsv`
  - `result_check.json`
- per-row logs
- per-row metadata

Package-level expected fields:

- `previous_fail_closed_exact_ledger = 90/120`
- `planned_rows = 3`
- `maximum_possible_ledger_after_this_canary = 93/120`
- `timing_denominator_id = NA_not_computed`
- `leaderboard_comparable = no`
- `claim_boundary = calcite_hep_120_recovery_perf0035_canary_only_not_timing_speedup_or_leaderboard_evidence`
