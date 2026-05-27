# Status

This note records the bounded Batch 3B PERF PostgreSQL speedup runtime/scoring pass for the four paper-draft execution candidates.

# Case List

- `PERF_0027`
- `PERF_0028`
- `PERF_0030`
- `PERF_0031`

# Override Basis

Execution used the paper-draft gate documented in `docs/_scratch/BATCH3B_PERF_REGISTRY_GATE_DECISION_v0.md`.

Registry staging remains unchanged.

# Runtime Policy

- `warmup_count=1`
- `repeat_count=5`
- `statement_timeout_ms=30000`
- `primary_runtime_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

# Canary Result

Canary case: `PERF_0027`

- `HUMAN_REFERENCE_POSITIVE`
  - source median: `0.730 ms`
  - candidate median: `0.674 ms`
  - speedup ratio: `1.0831`
  - outcome: `win`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - source median: `0.649 ms`
  - candidate median: `0.648 ms`
  - speedup ratio: `1.0015`
  - outcome: `tie`

Both routes completed successfully and both row-count checks matched source.

# Full Run Result

- cases: `4`
- routes: `2`
- total records: `8`
- executed: `8`
- success: `8`
- failed: `0`
- row-count match count: `8`
- row-count mismatch count: `0`

# Route-Level Summary

`HUMAN_REFERENCE_POSITIVE`

- `GM_Speedup=0.9853`
- `W/T/L=1/1/2`
- `RegressionRate@20%=0/4`

`SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

- `GM_Speedup=0.9841`
- `W/T/L=1/2/1`
- `RegressionRate@20%=0/4`

# Row-Count Match Summary

- `HUMAN_REFERENCE_POSITIVE`: `4/4`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: `4/4`
- overall: `8/8`

# Boundaries

- paper-draft evidence only
- registry unchanged
- not admission
- not final denominator
- not final leaderboard
- PostgreSQL only
- no SQLGlot optimize
- no LLM
- no MySQL
- no Spark
- no PORT
- no CONS

