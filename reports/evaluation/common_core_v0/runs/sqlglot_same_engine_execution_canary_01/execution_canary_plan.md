# SQLGlot Same-Engine Execution Canary Plan

This is a human-run execution canary plan for a narrow non-PORT SQLGlot same-engine slice.

## Scope

- cases:
  - `PERF_0006`
  - `CONS_0007`
  - `LONGTAIL_0011`
- engines:
  - `pg`
  - `mysql`
  - `spark`
- routes:
  - `sqlglot_optimize_same_dialect`
  - `sqlglot_transpile_same_dialect_noop`

This canary is execution-oriented, but it is still narrow:

- no `PORT`
- no timing
- no leaderboard metrics
- no plan collection
- no `tmp_repo`
- no case-file modification

## Input Basis

The execution candidate rows come from:

- [generation_event_long.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/sqlglot_same_engine_generation_01/generation_event_long.csv)
- [common_core_v0_controls_status_table_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv)

Execution policy for this canary:

- execute only rows with `generation_success`
- if any row were `generation_failed`, keep it explicit as `not_executed_generation_failed`
- if any row were `is_noop_output=yes`, keep it explicit as `noop_generated`

In the current chosen scope, all `18` rows are generation-success and none are currently no-op.

## Run-Local Discipline

The human-run script is designed to:

- run from repo root
- source `scripts/env_postgres.sh`
- source `scripts/env_mysql.sh`
- source `scripts/env_spark.sh`
- run `python -m scripts.cli env-check`
- execute generated SQL from the run-local `generated` artifacts
- write logs under this run directory
- write `records.tmp.jsonl`
- write `run_results.json`
- continue after failures

To avoid case-file mutation, execution is run against a run-local workspace under:

- `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_execution_canary_01/workspaces/`

The script stages:

- source SQL
- generated SQL
- schema DDL
- witness data

into a run-local workspace for each `case × engine × route`.

## Engine Execution Strategy

### PostgreSQL

- create a run-local temp schema name
- load staged `ddl_pg.sql`
- load staged `pg_witness_data.sql`
- execute staged `source.sql`
- execute staged generated SQL
- write stdout/stderr logs only

### MySQL

- create a run-local temp database name
- load staged `ddl_mysql.sql`
- load staged `mysql_witness_data.sql`
- execute staged `source.sql`
- execute staged generated SQL
- write stdout/stderr logs only

### Spark

- create a run-local temp warehouse directory under this run package
- load staged `ddl_spark.sql`
- load staged `spark_witness_data.sql`
- execute staged `source.sql`
- execute staged generated SQL through a small inline PySpark runner
- write stdout/stderr logs only

## Output Expectations

This canary is not yet a leaderboard package. It is a manual execution staging layer.

Primary outputs:

- `run_results.json`
- `records.tmp.jsonl`
- `logs/*.stdout.log`
- `logs/*.stderr.log`
- run-local staged workspaces under `workspaces/`

Not produced in this step:

- `run_event_long.csv`
- `method_case_summary.csv`
- `same_engine_leaderboard.csv`

## Explicit Row Handling

- `generation_success` rows: execute
- `generation_failed` rows: keep explicit as `not_executed_generation_failed`
- `is_noop_output=yes` rows: keep explicit as `noop_generated`

Even though the chosen three-case scope currently contains no failed-generation or no-op rows, the script still handles those states explicitly so the canary remains stable if the matrix is revised later.

## Why This Canary First

- all three cases have fresh controls evidence on `pg`, `mysql`, and `spark`
- all selected rows are non-PORT
- all selected rows already passed generation-only preflight
- this isolates SQLGlot execution behavior from explicit portability-policy caveats

## Boundary

This plan does not execute anything by itself.
It does not compute result-consistency metrics.
It does not compute speedup, regression, or leaderboard outputs.
