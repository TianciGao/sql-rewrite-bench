# Status

This is a bounded Batch 3A PostgreSQL speedup run for:

- `HUMAN_REFERENCE_POSITIVE`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

Scope is the 11 PERF Batch 3A cases only.

# Batch 3A Cases

- `PERF_0043`
- `PERF_0044`
- `PERF_0047`
- `PERF_0050`
- `PERF_0052`
- `PERF_0053`
- `PERF_0056`
- `PERF_0062`
- `PERF_0063`
- `PERF_0065`
- `PERF_0066`

# Route List

- `HUMAN_REFERENCE_POSITIVE`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

# Runtime Policy

- `warmup_count=1`
- `repeat_count=5`
- `statement_timeout_ms=30000`
- primary runtime statistic: `median`
- tie threshold: `0.05`
- regression threshold: `1.2`

# Canary Result

Canary case: `PERF_0043`

- routes executed: `2/2`
- success: `2/2`
- `HUMAN_REFERENCE_POSITIVE`
  - source median: `0.688 ms`
  - candidate median: `0.702 ms`
  - speedup ratio: `0.9801`
  - status: `tie`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - source median: `0.718 ms`
  - candidate median: `0.698 ms`
  - speedup ratio: `1.0287`
  - status: `tie`

# Full Run Summary

- cases: `11`
- routes: `2`
- total records: `22`
- executed: `22`
- success: `22`
- failed: `0`
- row-count match count: `22`
- row-count mismatch count: `0`

# Route-Level GM_Speedup / W/T/L / RegressionRate@20%

- `HUMAN_REFERENCE_POSITIVE`
  - `GM_Speedup=0.9984`
  - `W/T/L=0/10/1`
  - `RegressionRate@20%=0/11`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - `GM_Speedup=1.0023`
  - `W/T/L=2/7/2`
  - `RegressionRate@20%=0/11`

# Failed Cases

- none

# Interpretation

- both routes remained fully executable on the full Batch 3A PERF slice
- both routes remained row-count aligned with source on all 11 cases
- `HUMAN_REFERENCE_POSITIVE` is effectively tie-heavy at the route level and remains slightly below `1.0` GM speedup
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is also mostly tie-heavy, but lands slightly above `1.0` GM speedup with zero `20%` regressions
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` remains a separate SQLGlot route and does not replace `SQLGLOT_OPT_SAME_DIALECT`

# Boundary

- PERF-only
- PostgreSQL-only
- not final leaderboard
- no LLM
- no MySQL
- no Spark
- no PORT
- no CONS
- no registry update
- no formal review update
- no SQLGlot optimize route

# Recommended Next Action

- update expanded common-core rollup with Batch 3A speedup and decide whether to freeze expanded paper v1 evidence or continue to Batch 3B

# Verification / Non-Modification Note

- only this summary note was created
- no case-local artifacts were written
- no registry or `docs/EXECUTION_STATUS.md` changes were made
- no formal review files were changed
- taxonomy calibration notes were untouched
