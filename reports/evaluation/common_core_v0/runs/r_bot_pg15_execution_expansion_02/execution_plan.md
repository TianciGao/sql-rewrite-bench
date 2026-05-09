# R-Bot PG15 Execution Expansion Plan

## Scope

- `run_id = r_bot_pg15_execution_expansion_02`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- source generation run:
  - `r_bot_pg40_generation_expansion_02`
- source generation denominator:
  - `common_core_v0_40_pg40`
- execution denominator:
  - `generated_pg15_from_pg40_expansion_only`
- planned execution rows: `15`
- engine: `pg`

## Purpose

This package prepares a human-run PostgreSQL execution and validity check for
the `15` generated PostgreSQL rows retained by the PG40 expansion generation
run.

It does not:

- call any LLM or API
- run R-Bot generation
- modify generated SQL outputs
- modify case files
- modify registry files
- compute timing
- compute speedup
- create a leaderboard
- update method comparison or the retained R-Bot result card

## Generated Rows In Scope

- `PERF_0006:pg`
- `PERF_0007:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`
- `PERF_0062:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `CONS_0009:pg`
- `CONS_0010:pg`
- `CONS_0012:pg`
- `CONS_0036:pg`

## Evidence Boundary

- `current_benchmark_metric_evidence = false`
- claim boundary:
  - `formal_generated_pg15_from_pg40_expansion_execution_validity_only_not_timing_speedup_or_leaderboard_evidence`
- this package produces execution/validity evidence only for the `15`
  generated PostgreSQL rows from the PG40 expansion run
- it does not imply that R-Bot has full PG40 validity evidence yet
- it does not imply any timing or speedup evidence
- the `25` failed generation rows remain explicit generation outcomes in the
  PG40 generation denominator and are not silently dropped
- existing PG7 retained evidence remains separate and untouched

## Inputs

- generation expansion run summary:
  - [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg40_generation_expansion_02/run_results.json)
- generation expansion row table:
  - [run_event_long.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg40_generation_expansion_02/run_event_long.csv)
- generation expansion triage:
  - [generation_expansion_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg40_generation_expansion_02/generation_expansion_triage.md)
  - [generation_expansion_triage.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg40_generation_expansion_02/generation_expansion_triage.csv)
- protocol reference:
  - [COMMON_CORE_V0_EVALUATION_PROTOCOL.md](/home/tianci_gao/code/sql-rewrite-bench/benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md)

## Execution Semantics

For each of the `15` planned rows, the human-run script should:

1. run from repo root
2. source `scripts/env_postgres.sh`
3. run PostgreSQL preflight
4. create an isolated schema for the row
5. load `ddl_pg.sql`
6. load `pg_witness_data.sql`
7. execute the frozen source SQL and export `source.tsv`
8. execute the retained generated R-Bot SQL and export `generated.tsv`
9. compare the TSV outputs by exact text equality only
10. write `result_check.json`
11. write package-level `run_results.json`
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

- if PostgreSQL preflight fails, keep all `15` rows explicit as
  `not_executed_preflight_failed`
- if the generated SQL execution fails, keep that row explicit as
  `execution_failed`
- if source and generated TSV outputs differ, keep that row explicit as
  `mismatch`
- continue after row failures
- do not silently suppress any failure

## Boundary To Generation Denominator

This package executes only the `15` generated PostgreSQL rows from
`r_bot_pg40_generation_expansion_02`.

It must preserve in `run_results.json`:

- the reference to the source generation run
- the source generation denominator ID `common_core_v0_40_pg40`
- the narrower execution denominator ID
  `generated_pg15_from_pg40_expansion_only`

This package is not allowed to reinterpret the `25` failed PG generation rows
as execution omissions. They remain explicit generation outcomes outside this
execution subset.
