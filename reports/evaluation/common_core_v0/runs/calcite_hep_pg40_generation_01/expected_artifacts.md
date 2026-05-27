# Expected Artifacts

## Required

- `generation_plan.md`
- `generation_command_matrix.csv`
- `run_manual_calcite_hep_pg40_generation.sh`
- `README.md`
- `run_results.json`

## Per-row Generated SQL

For rows that emit a candidate:

- `generated/<case_id>/pg/calcite_hep_pg_rewrite.sql`

## Per-row Logs

- `logs/<case_id>_pg.stdout.log`
- `logs/<case_id>_pg.stderr.log`

## Per-row Machine-readable Status

- `row_results/<case_id>/pg/result.json`

Each row result should record at least:

- `case_id`
- `pool`
- `engine`
- `route_id`
- `generation_status`
- `blocker_reason`
- `is_noop`
- `generated_sql_path`
- `stdout_log_path`
- `stderr_log_path`

## Run-level Summary

`run_results.json` should record:

- `denominator_id`
- `method_id`
- `route_id`
- `planned_rows`
- `engine`
- `wrapper_status`
- `wrapper_blocker`
- `row_count`
- `counts_by_generation_status`
- full per-row records

## Not Produced By This Package

- no execution outputs
- no checker outputs
- no timing outputs
- no speedup outputs
- no leaderboard outputs
