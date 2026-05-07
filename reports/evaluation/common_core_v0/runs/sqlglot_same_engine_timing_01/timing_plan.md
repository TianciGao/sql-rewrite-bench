**Timing Plan**
This package prepares the full human-run SQLGlot same-engine timing pass for `common_core_v0_40`. It is scoped to the `137` rows already marked `timing_eligible=yes` in the timing preflight, with `warmup_count=1` and `repeat_count=3`.

The execution matrix in [timing_command_matrix.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/sqlglot_same_engine_timing_01/timing_command_matrix.csv) includes only runnable timing rows. Non-timing-eligible rows from the full `240` planned same-engine rows are preserved later during materialization, not in the execution script.

Coverage:
- cases: all `common_core_v0_40` cases that already have SQLGlot execution success and were marked timing-eligible in preflight
- engines: `pg`, `mysql`, `spark`
- routes: `sqlglot_optimize_same_dialect`, `sqlglot_transpile_same_dialect_noop`

Matrix counts:
- total execution rows: `137`
- by engine: `pg=49`, `mysql=50`, `spark=38`
- by route: `optimize=65`, `transpile_noop=72`
- by pool: `performance=56`, `consistency=36`, `longtail=36`, `portability=9`

Execution rules:
- run from repo root only
- source `scripts/env_postgres.sh`, `scripts/env_mysql.sh`, and `scripts/env_spark.sh`
- no `tmp_repo`
- capture `stdout` and `stderr` per row
- keep going after failures
- write one timing JSON per executed row plus a consolidated `run_results.json`
- do not compute `GM_Speedup`
- do not compute `RegressionRate@20%`
- do not create `same_engine_leaderboard.csv`

Planned outputs under this run directory:
- `logs/`
- `workspaces/`
- `timings/<CASE>/<engine>/<route>.json`
- `records.tmp.jsonl`
- `run_results.json`

Next step after human execution:
- materialize denominator-aware timing evidence into `run_event_long.csv` and `method_case_summary.csv`
- preserve non-timing-eligible rows explicitly during materialization
- defer leaderboard construction until timing evidence is validated and policy-ready
