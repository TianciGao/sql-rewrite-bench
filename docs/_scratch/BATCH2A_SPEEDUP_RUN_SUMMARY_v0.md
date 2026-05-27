# Status

This is a bounded Batch 2A PostgreSQL speedup run for:

- `HUMAN_REFERENCE_POSITIVE`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

Scope is the 19 PERF Batch 2A cases only.

# Case List

- `PERF_0007`
- `PERF_0009`
- `PERF_0010`
- `PERF_0011`
- `PERF_0012`
- `PERF_0014`
- `PERF_0015`
- `PERF_0016`
- `PERF_0018`
- `PERF_0019`
- `PERF_0020`
- `PERF_0021`
- `PERF_0022`
- `PERF_0023`
- `PERF_0025`
- `PERF_0026`
- `PERF_0034`
- `PERF_0035`
- `PERF_0036`

# Route List

- `HUMAN_REFERENCE_POSITIVE`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

# Frozen Policy

- `repeat_count=5`
- `warmup_count=1`
- `statement_timeout_ms=30000`
- primary statistic: `median`
- tie threshold: `0.05`
- regression threshold: `1.2`

# Canary Result

Canary case: `PERF_0007`

- routes executed: `2/2`
- success: `2/2`
- `HUMAN_REFERENCE_POSITIVE`
  - source median: `0.164 ms`
  - candidate median: `0.156 ms`
  - speedup ratio: `1.0513`
  - status: `win`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - source median: `0.188 ms`
  - candidate median: `0.188 ms`
  - speedup ratio: `1.0000`
  - status: `tie`

# Full Run Result

- cases: `19`
- routes: `2`
- total records: `38`
- executed: `38`
- success: `38`
- failed: `0`
- row-count match count: `38`

# GM_Speedup By Route

- `HUMAN_REFERENCE_POSITIVE`: `0.9733`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: `1.0119`

# Win/Tie/Loss By Route

- `HUMAN_REFERENCE_POSITIVE`: `4 / 9 / 6`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: `4 / 13 / 2`

# RegressionRate@20% By Route

- `HUMAN_REFERENCE_POSITIVE`: `3/19`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: `0/19`

# Per-Case Compact Table

| case_id | human ratio | human W/T/L | human reg20 | no-opt ratio | no-opt W/T/L | no-opt reg20 |
|---|---:|---|---|---:|---|---|
| `PERF_0007` | `1.1111` | `win` | `false` | `0.9880` | `tie` | `false` |
| `PERF_0009` | `1.0358` | `tie` | `false` | `1.0717` | `win` | `false` |
| `PERF_0010` | `0.9774` | `tie` | `false` | `1.0264` | `tie` | `false` |
| `PERF_0011` | `0.9643` | `tie` | `false` | `0.9588` | `tie` | `false` |
| `PERF_0012` | `0.8170` | `loss` | `true` | `1.0248` | `tie` | `false` |
| `PERF_0014` | `0.9546` | `tie` | `false` | `1.0018` | `tie` | `false` |
| `PERF_0015` | `0.9547` | `tie` | `false` | `0.9416` | `loss` | `false` |
| `PERF_0016` | `1.0030` | `tie` | `false` | `1.0269` | `tie` | `false` |
| `PERF_0018` | `0.9243` | `loss` | `false` | `1.0464` | `tie` | `false` |
| `PERF_0019` | `0.9565` | `tie` | `false` | `1.0251` | `tie` | `false` |
| `PERF_0020` | `0.8477` | `loss` | `false` | `1.0029` | `tie` | `false` |
| `PERF_0021` | `0.8092` | `loss` | `true` | `1.0443` | `tie` | `false` |
| `PERF_0022` | `1.0692` | `win` | `false` | `0.9291` | `loss` | `false` |
| `PERF_0023` | `0.9848` | `tie` | `false` | `1.0693` | `win` | `false` |
| `PERF_0025` | `1.0277` | `tie` | `false` | `0.9985` | `tie` | `false` |
| `PERF_0026` | `0.7093` | `loss` | `true` | `0.9577` | `tie` | `false` |
| `PERF_0034` | `1.4394` | `win` | `false` | `1.0612` | `win` | `false` |
| `PERF_0035` | `0.8880` | `loss` | `false` | `1.0563` | `win` | `false` |
| `PERF_0036` | `1.2406` | `win` | `false` | `1.0107` | `tie` | `false` |

# Failed Cases / Failure Categories

- none

# Interpretation

- `HUMAN_REFERENCE_POSITIVE` remained fully executable and row-count aligned, but the route-level GM speedup is below `1.0` and it shows `3/19` regressions at the `20%` threshold.
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` remained fully executable and row-count aligned, with route-level GM speedup above `1.0` and `0/19` regressions at the `20%` threshold.
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` remains a separate baseline candidate. It does not replace `SQLGLOT_OPT_SAME_DIALECT`.

# Recommended Next Action

- run Batch 2A checker/scoring preflight for successful routes, carrying `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` as a separately named baseline candidate

# Boundaries

- Batch 2A PERF-only
- PostgreSQL only
- not full benchmark leaderboard
- not correctness scoring
- no LLM / PORT / CONS / MySQL / Spark work
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is a separate baseline candidate, not a replacement for the optimize route

# Verification / Non-Modification Note

- only this summary note was created
- no registry or `docs/EXECUTION_STATUS.md` changes were made
- no formal review files were changed
- no case-local artifacts were written
- taxonomy calibration notes were untouched
