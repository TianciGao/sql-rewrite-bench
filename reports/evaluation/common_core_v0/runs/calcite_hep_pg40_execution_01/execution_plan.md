# Calcite HEP PG40 Execution Plan

## Scope

- `denominator_id = common_core_v0_40_pg40`
- `method_id = calcite_hep`
- `route_id = calcite_hep_pg_rewrite`
- engine: `pg`
- planned rows: `40`

This package prepares human-run PostgreSQL execution and validity evidence for Calcite HEP on the frozen Common-core v0 PG40 denominator.

## Row Policy

- execute only the `29` rows with `generation_status = generation_success`
- preserve the `11` generation-failed rows explicitly as `not_executed_generation_failed`
- do not silently drop any denominator row

## Inputs

- generation summary: [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/run_results.json)
- generation triage:
  - [generation_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generation_triage.md)
  - [generation_triage.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generation_triage.csv)
- controls status: [common_core_v0_controls_status_table_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv)
- frozen denominator: [common_core_v0_final_denominator.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.csv)

## Readiness Summary

- `29` rows are marked `ready_to_execute`
- `11` rows are preserved as `not_executed_generation_failed`
- one non-execution-target artifact gap remains visible:
  - `cases/PORT/PORT_0004/validation/pg_witness_data.sql`
- one execution-target row carries a control-source caveat:
  - `PORT_0024 / pg` has `control_native_source_status=skipped`

## Execution Semantics

For each executable row, the runner should:

1. create an isolated PostgreSQL schema for the row
2. load `ddl_pg.sql`
3. load `pg_witness_data.sql`
4. run the source SQL and export TSV
5. run the generated Calcite SQL and export TSV
6. compare TSV outputs
7. write `result_check.json`
8. drop the isolated schema

## Status Contract

Matrix-level pre-execution statuses:

- `ready_to_execute`
- `not_executed_generation_failed`

Execution-time observed statuses:

- `executed`
- `execution_failed`
- `not_executed_generation_failed`

Consistency statuses:

- `match_exact`
- `match_after_sort_normalization`
- `mismatch`
- `not_checked_execution_failed`
- `not_checked_generation_failed`

## Boundaries

- human-run only
- PostgreSQL only
- no timing
- no speedup
- no leaderboard
