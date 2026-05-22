# Expected Artifacts

When a human runs this package successfully, it should retain:

- `run_results.json`
- `run_event_long.csv`
- `generated/<CASE>/<engine>/calcite_hep_recovery_round4_rewrite.sql`
- `logs/<CASE>/<engine>/source.stdout.log`
- `logs/<CASE>/<engine>/source.stderr.log`
- `logs/<CASE>/<engine>/generated.stdout.log`
- `logs/<CASE>/<engine>/generated.stderr.log`
- `workspaces/<CASE>/<engine>/source.tsv`
- `workspaces/<CASE>/<engine>/generated.tsv`
- `workspaces/<CASE>/<engine>/result_check.json`
- `metadata/<CASE>/<engine>/row_metadata.json`

Package-level `run_results.json` must retain:

- `previous_fail_closed_exact_ledger = 86/120`
- `planned_rows = 4`
- `recovered_exact_count`
- `new_fail_closed_exact_ledger = 86 + recovered_exact_count`
- `maximum_possible_ledger_after_this_canary = 90/120`
- `current_benchmark_metric_evidence = false`
- `timing_denominator_id = NA_not_computed`
- `leaderboard_comparable = no`
- `claim_boundary = calcite_hep_120_recovery_round4_numeric_scale_canary_only_not_timing_speedup_or_leaderboard_evidence`
