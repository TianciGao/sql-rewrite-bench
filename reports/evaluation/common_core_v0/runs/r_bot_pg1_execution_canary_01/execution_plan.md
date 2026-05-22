# R-Bot PG1 Execution Canary 01 Plan

## Scope

- `run_id = r_bot_pg1_execution_canary_01`
- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- `engine = pg`
- planned rows: `1`
- generated SQL:
  - [r_bot_pg_rewrite.sql](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql)

## Purpose

This package prepares a human-run PostgreSQL execution and validity check for the existing R-Bot PG1 exploratory generation result on `PERF_0006`.

This package does not:

- call any LLM or API
- modify generated SQL outputs
- modify case files
- modify registry files
- compute timing
- compute speedup
- create a leaderboard

## Evidence Boundary

- `current_benchmark_metric_evidence = false`
- claim boundary:
  - `exploratory_smoke_only_not_current_common_core_metric_evidence`
- this package is exploratory PG1 recovery evidence only
- successful execution does not upgrade the row into current benchmark metric evidence

## Inputs

- recovery run summary:
  - [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json)
- retained generated SQL:
  - [r_bot_pg_rewrite.sql](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql)
- recovery triage:
  - [recovery_generation_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/recovery_generation_triage.md)
  - [recovery_generation_triage.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/recovery_generation_triage.csv)
- case source SQL:
  - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/source.sql)
- PostgreSQL schema:
  - [ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/schema/ddl_pg.sql)
- PostgreSQL witness data:
  - [pg_witness_data.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/validation/pg_witness_data.sql)
- protocol reference:
  - [COMMON_CORE_V0_EVALUATION_PROTOCOL.md](/home/tianci_gao/code/sql-rewrite-bench/benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md)

## Execution Semantics

For the single planned row, the human-run script should:

1. run from repo root
2. source `scripts/env_postgres.sh`
3. run PostgreSQL preflight
4. create an isolated schema
5. load `ddl_pg.sql`
6. load `pg_witness_data.sql`
7. execute the frozen source SQL and export `source.tsv`
8. execute the retained generated R-Bot SQL and export `generated.tsv`
9. compare the TSV outputs by exact text equality only
10. write `result_check.json`
11. write `run_results.json`
12. drop the isolated schema in cleanup

## Status Contract

Pre-execution row status:

- `ready_to_execute`

Execution-time observed statuses:

- `executed`
- `execution_failed`
- `not_executed_preflight_failed`

Consistency statuses:

- `match_exact`
- `mismatch`
- `not_checked_execution_failed`
- `not_checked_preflight_failed`

## Failure Handling

- if PostgreSQL preflight fails, keep the row explicit as `not_executed_preflight_failed`
- if the generated SQL execution fails, keep the row explicit as `execution_failed`
- if source and generated TSV outputs differ, keep the row explicit as `mismatch`
- do not silently suppress any failure

## Boundaries

- human-run only
- PostgreSQL only
- no timing
- no speedup
- no leaderboard
