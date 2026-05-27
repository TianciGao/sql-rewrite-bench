# Expected Artifacts

When a human runs this package successfully, it should retain:

- `run_results.json`
- `run_event_long.csv`
- `generated/<CASE>/mysql/calcite_hep_recovery_round3c_rewrite.sql`
- `logs/<CASE>/mysql/source.stdout.log`
- `logs/<CASE>/mysql/source.stderr.log`
- `logs/<CASE>/mysql/generated.stdout.log`
- `logs/<CASE>/mysql/generated.stderr.log`
- `workspaces/<CASE>/mysql/source.tsv`
- `workspaces/<CASE>/mysql/generated.tsv`
- `workspaces/<CASE>/mysql/result_check.json`
- `metadata/<CASE>/mysql/row_metadata.json`

Package-level `run_results.json` must retain:

- `previous_fail_closed_exact_ledger = 84/120`
- `planned_rows = 2`
- `recovered_exact_count`
- `new_fail_closed_exact_ledger = 84 + recovered_exact_count`
- `maximum_possible_ledger_after_this_canary = 86/120`
- `current_benchmark_metric_evidence = false`
- `timing_denominator_id = NA_not_computed`
- `leaderboard_comparable = no`
- `claim_boundary = calcite_hep_120_recovery_round3c_numeric_scale_canary_only_not_timing_speedup_or_leaderboard_evidence`
