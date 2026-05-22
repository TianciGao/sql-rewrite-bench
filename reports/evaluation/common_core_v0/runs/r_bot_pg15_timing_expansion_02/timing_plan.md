# R-Bot PG15 Timing Expansion Plan

This package prepares the human-run PostgreSQL timing pass for the fifteen
R-Bot rows that already passed execution/validity with `match_exact` in
`r_bot_pg15_execution_expansion_02`.

It does not execute timing by itself and does not create any leaderboard
artifact.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `source_generation_run_id = r_bot_pg40_generation_expansion_02`
- `source_execution_run_id = r_bot_pg15_execution_expansion_02`
- `generation_denominator_id = common_core_v0_40_pg40`
- `execution_denominator_id = generated_pg15_from_pg40_expansion_only`
- `timing_denominator_id = generated_pg15_from_pg40_expansion_match_exact_only`
- engine: `pg`
- planned timing rows: exactly `15`

The fifteen timing rows are:

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

## Timing Run Settings

- `warmup_count = 1`
- `repeat_count = 3`

Per row, the human-run timing script should:

- source PostgreSQL environment from `scripts/env_postgres.sh`
- materialize an isolated schema
- load `ddl_pg.sql`
- load `pg_witness_data.sql`
- time the source SQL
- time the generated R-Bot SQL
- record per-repeat source and generated runtimes
- compute `median_source_ms`, `median_generated_ms`, and `speedup_ratio`
- continue after row failures

## Output Boundary

The human-run script is expected to write:

- `logs/*.stdout.log`
- `logs/*.stderr.log`
- `timings/<case_id>/pg/r_bot_same_engine_rewrite.json`
- `workspaces/<case_id>/pg/r_bot_same_engine_rewrite/`
- `run_results.json`

This package is timing-only for the fifteen `match_exact` PG rows. It does not
imply timing evidence for all PG40 rows, for the full
`common_core_v0_40_same_engine_120` denominator, or for any tri-engine
comparison. The `25` failed PG generation rows remain explicit in the PG40
generation denominator outside this timing subset. Existing PG7 timing evidence
also remains retained and unchanged.
