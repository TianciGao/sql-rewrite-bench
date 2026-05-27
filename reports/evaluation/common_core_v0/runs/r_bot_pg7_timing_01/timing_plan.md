# R-Bot PG7 Timing Plan

This package prepares the human-run PostgreSQL timing pass for the seven R-Bot rows that already passed execution/validity with `match_exact`.

It does not execute timing by itself and does not create any leaderboard artifact.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `generation_denominator_id = common_core_v0_40_same_engine_120`
- `timing_denominator_id = generated_pg7_match_exact_only`
- engine: `pg`
- planned timing rows: exactly `7`

The seven timing rows are:

- `PERF_0006:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`

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

This package is timing-only for the seven `match_exact` PG rows. It does not imply timing evidence for the full `120`-row generation denominator, and it does not create any leaderboard or method-comparison summary.
