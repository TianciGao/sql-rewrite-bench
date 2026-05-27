# Expected Artifacts

## Required Package Files

- `execution_plan.md`
- `execution_command_matrix.csv`
- `run_manual_r_bot_pg1_execution_canary.sh`
- `README.md`
- `expected_artifacts.md`

## Logs After Human Execution

- `logs/pg_check.stdout.log`
- `logs/pg_check.stderr.log`
- `logs/perf_0006__pg__r_bot_pg_rewrite.stdout.log`
- `logs/perf_0006__pg__r_bot_pg_rewrite.stderr.log`

## Per-row Outputs

Under `workspaces/PERF_0006/pg/r_bot_pg_rewrite/`:

- `source.sql`
- `generated.sql`
- `ddl_pg.sql`
- `pg_witness_data.sql`
- `source.tsv`
- `generated.tsv`
- `result_check.json`

## Run-level Outputs

- `records.tmp.jsonl`
- `run_results.json`

`run_results.json` should preserve:

- planned rows: `1`
- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- `engine = pg`
- claim boundary:
  - `exploratory_smoke_only_not_current_common_core_metric_evidence`
- `current_benchmark_metric_evidence = false`
- explicit execution outcome
- explicit consistency outcome
- full record payload

## Expected Result Check Semantics

`result_check.json` should preserve one of:

- `execution_status_observed = executed` with `consistency_check_status = match_exact`
- `execution_status_observed = executed` with `consistency_check_status = mismatch`
- `execution_status_observed = execution_failed` with `consistency_check_status = not_checked_execution_failed`
- `execution_status_observed = not_executed_preflight_failed` with `consistency_check_status = not_checked_preflight_failed`

## Not Produced By This Package

- no timing outputs
- no speedup outputs
- no leaderboard outputs
- no benchmark-metric-evidence upgrade
