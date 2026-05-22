**SQLGlot Same-Engine Timing Canary Plan**

This package is a human-run timing canary for SQLGlot same-engine measurement on a small Common-core v0 slice before any broader timing run.

Scope:
- cases: `PERF_0006`, `CONS_0010`, `LONGTAIL_0011`
- engines: `pg`, `mysql`, `spark`
- routes:
  - `sqlglot_optimize_same_dialect`
  - `sqlglot_transpile_same_dialect_noop`

Timing policy:
- `warmup_count = 1`
- `repeat_count = 3`
- baseline and generated SQL are both measured per row
- rows remain explicit even when timing fails

Run model:
- run from real repo root
- source `scripts/env_postgres.sh`, `scripts/env_mysql.sh`, `scripts/env_spark.sh`
- no `tmp_repo`
- no plan collection
- no leaderboard computation
- no final `GM_Speedup`
- no final `RegressionRate@20%`

Expected timing denominator in this canary:
- planned scoped rows: `18`
- timing-eligible scoped rows: `18`
- speedup-eligible scoped rows: `18`

Output model:
- per-row timing JSON under `timings/<case_id>/<engine>/<route_id>.json`
- stdout/stderr logs under `logs/`
- aggregate `run_results.json`

Boundary:
- this canary records timing measurements only
- it does not materialize final performance claims
- it does not create `same_engine_leaderboard.csv`
