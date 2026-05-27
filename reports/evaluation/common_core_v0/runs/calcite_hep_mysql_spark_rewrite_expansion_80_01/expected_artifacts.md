# Expected Artifacts

## Package Outputs

Human-run outputs should be written under:

- `reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_rewrite_expansion_80_01/`

Core package-level artifacts:

- `run_results.json`
- `run_event_long.csv`

## Row-Level Outputs

For each row:

- generated SQL for successful rows:
  - `generated/<CASE>/<engine>/calcite_hep_rewrite.sql`
- stdout log:
  - `logs/<CASE>/<engine>/rewrite.stdout.log`
- stderr log:
  - `logs/<CASE>/<engine>/rewrite.stderr.log`
- row metadata:
  - `metadata/<CASE>/<engine>/row_metadata.json`

## Status Contract

`row_status` must be one of:

- `rewrite_success`
- `parser_failed`
- `hep_rewrite_failed`
- `target_dialect_unavailable`
- `rel_to_sql_failed`
- `generated_sql_missing`
- `setup_failed`

Each row should also record:

- `dialect_class_used`
- `rewrite_changed`
- `failure_category`
- `blocker_reason`
- `witness_missing_for_later_execution`

Setup failure categories should distinguish:

- `missing_source_sql`
- `missing_schema_sql`
- `wrapper_compile_failed`

## Boundary

This package must not compute:

- execution validity
- timing
- speedup
- leaderboard artifacts
