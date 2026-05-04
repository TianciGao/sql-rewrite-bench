# Status

This is the Batch 3A formal PostgreSQL execution summary for the bounded PERF expansion slice.

# Batch 3A Case List

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

- `NATIVE_IDENTITY`
- `HUMAN_REFERENCE_POSITIVE`
- `HARD_NEGATIVE_GUARD`
- `SQLGLOT_OPT_SAME_DIALECT`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

# Canary Result

Canary case:

- `PERF_0043`

Observed result:

- `NATIVE_IDENTITY`: success, `row_count=1`
- `HUMAN_REFERENCE_POSITIVE`: success, `row_count=1`
- `HARD_NEGATIVE_GUARD`: success, `row_count=0`
- `SQLGLOT_OPT_SAME_DIALECT`: failed, `OptimizeError`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: success, `row_count=1`

Interpretation:

- the canary confirmed the same structural pattern seen in Batch 2A
- control routes and the no-opt SQLGlot route were safe to execute
- the optimize route failed at SQLGlot generation rather than at PostgreSQL environment setup

# Full Execution Result

Full Batch 3A result:

- cases: `11`
- routes: `5`
- total records: `55`
- executed: `55`
- success: `46`
- failed: `9`
- skipped: `0`

# Per-Route Success / Failure Summary

- `NATIVE_IDENTITY`
  - success: `11`
  - failed: `0`
- `HUMAN_REFERENCE_POSITIVE`
  - success: `11`
  - failed: `0`
- `HARD_NEGATIVE_GUARD`
  - success: `11`
  - failed: `0`
- `SQLGLOT_OPT_SAME_DIALECT`
  - success: `2`
  - failed: `9`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - success: `11`
  - failed: `0`

# Failed Cases / Failure Categories

All observed failures were on `SQLGLOT_OPT_SAME_DIALECT`.

Failure category summary:

- `OptimizeError`: `9`

Failed cases:

- `PERF_0043`
- `PERF_0044`
- `PERF_0047`
- `PERF_0050`
- `PERF_0052`
- `PERF_0062`
- `PERF_0063`
- `PERF_0065`
- `PERF_0066`

Observed optimize-route success cases:

- `PERF_0053`
- `PERF_0056`

# Comparison Note With Batch 2A

Batch 3A preserves the same qualitative route boundary already exposed in Batch 2A:

- `SQLGLOT_OPT_SAME_DIALECT` remains selective and unstable on expanded PERF slices
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` remains broadly executable as a separate route

Comparison summary:

- Batch 2A optimize route: `4 / 19` success
- Batch 3A optimize route: `2 / 11` success
- Batch 2A no-opt route: `19 / 19` execution success
- Batch 3A no-opt route: `11 / 11` execution success

Interpretation:

- the optimize-route capability boundary persists beyond the earlier Batch 2A slice
- the no-opt route continues to look like the broader executable SQLGlot baseline candidate
- this note remains execution-layer evidence only and does not replace checker-backed scoring

# Boundary

- execution-layer only
- not correctness scoring
- not speedup
- not leaderboard
- no registry writeback
- no formal review update

# Recommended Next Action

- run Batch 3A SQLGlot no-opt checker / scoring if execution succeeds
