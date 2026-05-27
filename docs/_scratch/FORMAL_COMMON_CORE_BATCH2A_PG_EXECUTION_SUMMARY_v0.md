# Status

This note records the bounded Batch 2A PostgreSQL execution expansion for the first ready PERF wave. This is execution-layer evidence only.

# Batch 2A Case List

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

- `NATIVE_IDENTITY`
- `HUMAN_REFERENCE_POSITIVE`
- `HARD_NEGATIVE_GUARD`
- `SQLGLOT_OPT_SAME_DIALECT`

# Canary Result

One-case canary:

- case: `PERF_0007`
- routes executed: `4/4`
- success: `4/4`
- row counts:
  - native: `1`
  - human positive: `1`
  - hard negative: `1`
  - SQLGlot same-dialect: `1`

The canary was clean enough to run the full Batch 2A set.

# Full Execution Result

Batch size:

- cases: `19`
- routes: `4`
- total records: `76`

Execution result:

- executed: `76`
- success: `61`
- failed: `15`
- skipped: `0`

# Per-Route Success / Failure Summary

- `NATIVE_IDENTITY`
  - success: `19`
  - failed: `0`
- `HUMAN_REFERENCE_POSITIVE`
  - success: `19`
  - failed: `0`
- `HARD_NEGATIVE_GUARD`
  - success: `19`
  - failed: `0`
- `SQLGLOT_OPT_SAME_DIALECT`
  - success: `4`
  - failed: `15`

SQLGlot same-dialect succeeded for:

- `PERF_0007`
- `PERF_0034`
- `PERF_0035`
- `PERF_0036`

# Failed Cases / Failure Categories

All observed failures were on `SQLGLOT_OPT_SAME_DIALECT`.

`UndefinedColumn`:

- `PERF_0009`
- `PERF_0026`

`OptimizeError`:

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

Interpretation:

- the three control-like PostgreSQL execution routes scaled cleanly across the full Batch 2A set
- the SQLGlot same-dialect route remains selective, with most failures caused during schema-free optimizer qualification rather than by PostgreSQL execution of already-generated SQL

# Boundary

- execution-layer only
- not correctness scoring
- not speedup
- not leaderboard evidence
- no registry updates
- no formal review updates

# Recommended Next Action

- run Batch 2A checker/scoring preflight for the successful routes

