# Expected Artifacts

## Package Outputs

Retained package-level outputs:

- `run_results.json`
- `run_event_long.csv`

## Row-Level Outputs

For each row:

- `workspaces/<CASE>/<engine>/source.sql`
- `workspaces/<CASE>/<engine>/generated.sql`
- `workspaces/<CASE>/<engine>/ddl_<engine>.sql`
- `workspaces/<CASE>/<engine>/<engine>_witness_data.sql`
- `workspaces/<CASE>/<engine>/source.tsv`
- `workspaces/<CASE>/<engine>/generated.tsv`
- `workspaces/<CASE>/<engine>/result_check.json`
- `logs/<CASE>/<engine>/source.stdout.log`
- `logs/<CASE>/<engine>/source.stderr.log`
- `logs/<CASE>/<engine>/generated.stdout.log`
- `logs/<CASE>/<engine>/generated.stderr.log`
- `metadata/<CASE>/<engine>/row_metadata.json`

## Aggregates

`run_results.json` must include:

- `planned_rows`
- `counts_by_engine`
- `counts_by_execution_status`
- `counts_by_consistency_status`
- `current_benchmark_metric_evidence = false`
- `claim_boundary = mysql_spark_execution_validity_expansion_60_only_not_timing_speedup_or_leaderboard_evidence`

## Boundary

This package must not compute:

- timing
- speedup
- leaderboard artifacts
