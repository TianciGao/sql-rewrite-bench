# Expected Artifacts

## Package outputs

Human-run outputs should be written under:

- `reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_execution_canary_02/`

Core package-level artifacts:

- `run_results.json`
- `run_event_long.csv`

## Row-level outputs

For each row:

- `workspaces/<CASE>/<engine>/source.tsv`
- `workspaces/<CASE>/<engine>/generated.tsv`
- `workspaces/<CASE>/<engine>/result_check.json`
- `logs/<CASE>/<engine>/source.stdout.log`
- `logs/<CASE>/<engine>/source.stderr.log`
- `logs/<CASE>/<engine>/generated.stdout.log`
- `logs/<CASE>/<engine>/generated.stderr.log`
- `metadata/<CASE>/<engine>/row_metadata.json`

## Status fields

Each row should record:

- `execution_status`
  - `executed`
  - `source_execution_failed`
  - `generated_execution_failed`
  - `setup_failed`
  - `comparison_failed`
- `consistency_status`
  - `match_exact`
  - `mismatch`
  - `not_applicable`

## Package boundary

This package must not compute:

- timing
- speedup
- leaderboard artifacts

It is a bounded execution/validity canary only.
