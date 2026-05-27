This package is a human-run timing canary for SQLGlot same-engine measurement on a small Common-core v0 slice.

Codex must not execute this script.

Scope:
- cases:
  - `PERF_0006`
  - `CONS_0010`
  - `LONGTAIL_0011`
- engines:
  - `pg`
  - `mysql`
  - `spark`
- routes:
  - `sqlglot_optimize_same_dialect`
  - `sqlglot_transpile_same_dialect_noop`

This is not full `@40` timing.

Success here means:
- the corrected SQLGlot execution harness can be reused for timing
- repeated baseline and generated measurements can be captured from the real repo root
- timing JSON can be produced per row without introducing denominator dropouts

This canary does not:
- compute final `GM_Speedup`
- compute final `RegressionRate@20%`
- create `same_engine_leaderboard.csv`

Rows outside timing eligibility would remain explicit if present in this scope. In the current chosen canary slice, all `18` scoped rows are timing-eligible according to the timing preflight matrix.
