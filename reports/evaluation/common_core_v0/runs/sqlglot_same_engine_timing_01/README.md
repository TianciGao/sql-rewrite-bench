**SQLGlot Same-Engine Timing**
This is a human-run package for the full SQLGlot same-engine timing pass on `common_core_v0_40`. Codex must not execute [run_manual_sqlglot_timing.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/sqlglot_same_engine_timing_01/run_manual_sqlglot_timing.sh).

The scope is the `137` rows already marked `timing_eligible=yes` in the timing preflight. It uses the corrected runner logic proven by the timing canary and runs only from the real repo root with `pg`, `mysql`, and `spark` environment scripts sourced in the same shell.

This package is timing-bearing but still pre-leaderboard:
- it records repeated source/generated runtimes
- it writes per-row timing JSON and a consolidated `run_results.json`
- it does not compute final `GM_Speedup`
- it does not compute final `RegressionRate@20%`
- it does not create `same_engine_leaderboard.csv`

Non-timing-eligible rows from the full `240` planned SQLGlot same-engine rows are not executed here. They remain part of later denominator-aware materialization and must not be silently dropped from reporting.
