# Status

This is a bounded Batch 2A SQLGlot fallback diagnostic over the 15 cases that failed under the `SQLGLOT_OPT_SAME_DIALECT` route. It evaluates a same-dialect PostgreSQL no-opt / transpile variant as a separate diagnostic route, not as a baseline replacement.

# Why This Diagnostic Was Needed

The Batch 2A execution expansion showed:

- `NATIVE_IDENTITY`: `19/19` success
- `HUMAN_REFERENCE_POSITIVE`: `19/19` success
- `HARD_NEGATIVE_GUARD`: `19/19` success
- `SQLGLOT_OPT_SAME_DIALECT`: `4/19` success, `15/19` failed

The control-route health suggested the case packages and PostgreSQL environment were sound. The open question was whether the SQLGlot failures were optimizer-specific, or whether same-dialect SQLGlot without the optimizer would also fail.

# Input Failure Clusters

- OptimizeError cluster: `13`
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
- UndefinedColumn cluster: `2`
  - `PERF_0009`
  - `PERF_0026`

# Diagnostic Variant Definitions

- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - reads `source.sql`
  - uses SQLGlot PostgreSQL-to-PostgreSQL transpile / emit without the optimizer
  - executes the emitted SQL in PostgreSQL only when `--execute` is provided

No separate `SQLGLOT_PARSE_ROUNDTRIP_NO_OPT` variant was added. In the current CLI path that would duplicate the same no-opt parse / emit behavior without adding useful contrast.

# Generation Result

- Case count: `15`
- Variant count: `1`
- Generation success:
  - `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: `15/15`

Interpretation: every Batch 2A optimize-failed case still parses and emits SQL cleanly when the optimizer is removed from the same-dialect path.

# PostgreSQL Execution Result

- Canary `PERF_0010`:
  - original optimize failure: `OptimizeError`
  - fallback result: PG success, `row_count=2`
- Canary `PERF_0009`:
  - original optimize/execution failure: `UndefinedColumn`
  - fallback result: PG success, `row_count=1`
- Full 15-case fallback diagnostic:
  - PG success: `15/15`
  - PG failed: `0/15`

Representative row counts from the full diagnostic:

- `PERF_0010`: `2`
- `PERF_0011`: `1`
- `PERF_0012`: `1`
- `PERF_0014`: `2`
- `PERF_0015`: `1`
- `PERF_0016`: `1`
- `PERF_0018`: `2`
- `PERF_0019`: `2`
- `PERF_0020`: `2`
- `PERF_0021`: `1`
- `PERF_0022`: `1`
- `PERF_0023`: `1`
- `PERF_0025`: `1`
- `PERF_0009`: `1`
- `PERF_0026`: `1`

# Recovery Analysis

- Original SQLGlot optimize-failed cases: `15`
- Recovered by no-opt / transpile fallback: `15`
- Still failed under no-opt / transpile fallback: `0`

Split by original failure cluster:

- OptimizeError recoveries: `13/13`
- UndefinedColumn recoveries: `2/2`

# Interpretation

- The OptimizeError cluster now looks strongly optimizer-specific rather than a broader SQLGlot PostgreSQL generation failure.
- The previous UndefinedColumn execution failures also disappeared under no-opt transpile, which suggests those two failures were produced by the optimize same-dialect route rather than by PostgreSQL incompatibility in the source query itself.
- This is strong evidence that the current `SQLGLOT_OPT_SAME_DIALECT` baseline and a possible `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` baseline should be treated as separate method variants.
- This is not evidence that the fallback route is correct, only that it executes successfully on PostgreSQL for this bounded Batch 2A slice.

# Recommended Next Action

Keep the optimize same-dialect baseline separate, and add the SQLGlot no-opt / transpile route only as a separately named diagnostic or baseline candidate if a later checker-backed comparison confirms it is worth formalizing.

# Claim Boundaries

- not correctness scoring
- not speedup
- not leaderboard
- not silent baseline replacement
- PostgreSQL only
- no PORT or CONS coverage
- no checker-backed equivalence claim yet
