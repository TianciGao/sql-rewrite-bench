# Calcite HEP PG40 Timing Plan

This package prepares the timing-bearing PostgreSQL run for Calcite HEP on the frozen `common_core_v0_40_pg40` denominator.

It does not execute timing by itself and does not compute final `GM_Speedup`, final `RegressionRate@20%`, or any leaderboard artifact.

## Scope

- `denominator_id = common_core_v0_40_pg40`
- `method_id = calcite_hep`
- `route_id = calcite_hep_pg_rewrite`
- engine: `pg`
- timing rows: exactly the `21` `match_exact` rows from the PG40 validity phase
- excluded rows are preserved in preflight/materialization, not in this execution matrix

## Timing Run Settings

- `warmup_count = 1`
- `repeat_count = 3`
- per row:
  - load PostgreSQL schema and witness data into an isolated schema
  - time the source query
  - time the Calcite-generated query
  - record per-repeat runtimes
  - compute row-local medians and `speedup_ratio`

## Expected Eligible Rows

- `performance`: `14`
- `consistency`: `7`
- total: `21`

## Output Boundary

The human-run script is expected to write:

- `logs/*.stdout.log`
- `logs/*.stderr.log`
- `timings/<case_id>/pg/calcite_hep_pg_rewrite.json`
- `run_results.json`

This package is timing-only. It does not materialize final aggregated speedup metrics.
