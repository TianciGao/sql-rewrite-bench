# Calcite HEP PG40 Generation

This package prepares a human-run PostgreSQL generation rerun for Calcite HEP on the frozen `common_core_v0_40` case set.

## Scope

- `method_id = calcite_hep`
- `denominator_id = common_core_v0_40_pg40`
- `route_id = calcite_hep_pg_rewrite`
- planned rows: `40`
- engine: `pg`

## Important Policy

- PG9 overlap is historical recovery evidence only, not the final denominator for this packet.
- old `prior_method_pg10`, `seed9`, and other bounded numeric results are not reused as current metrics
- old Calcite wrapper/scaffold logic may be reused only as implementation templates

## Wrapper Basis

This package is based on repo-local scaffold evidence:

- [CalciteHepRewriteSmoke.java](/home/tianci_gao/code/sql-rewrite-bench/tools/calcite_hep/CalciteHepRewriteSmoke.java)
- [calcite_hep_wrapper_scaffold_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/calcite_hep_wrapper_scaffold_v0.json)
- [calcite_hep_real_route_canary_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/calcite_hep_real_route_canary_v0.json)

## How To Run

From repo root:

```bash
bash reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/run_manual_calcite_hep_pg40_generation.sh
```

The script is human-run only.
It does not execute SQL.

## Output Contract

The run should produce:

- `run_results.json`
- generated SQL under `generated/<case_id>/pg/`
- per-row logs under `logs/`
- per-row machine-readable row results under `row_results/<case_id>/pg/result.json`

## Status Semantics

- `generation_success`: generated SQL emitted and not source-equivalent after normalization
- `generation_success_noop`: generated SQL emitted but normalizes to the source SQL
- `generation_failed_parse`: Calcite parse failed
- `generation_failed_unsupported_sql`: parse may succeed but the route fails later on schema ingestion, validation, SQL-to-Rel, HEP, or Rel-to-SQL
- `generation_failed_no_output`: no emitted SQL artifact
- `generation_failed_command`: wrapper invocation failed
- `blocked_runner_missing`: wrapper or Calcite checkout was unavailable

## Denominator Discipline

All 40 PG rows remain explicit in the matrix.

That includes rows outside the historical Calcite HEP PERF slice:

- `CONS`
- `PORT`
- `LONGTAIL`

Those rows must be reported explicitly as success, noop, unsupported, or failure during the fresh rerun.
They must not be silently dropped.
