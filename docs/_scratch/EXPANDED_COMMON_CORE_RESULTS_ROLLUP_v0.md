# Status

This is expanded common-core results rollup v0.

It consolidates the current expanded common-core evidence only.

It is not a registry writeback.

It is not a common-core admission decision.

It is not a formal review update.

It is not a final leaderboard.

It is not a protocol freeze.

# Executive Summary

Expanded common-core evidence has moved from the original `9`-case seed packet to a `31`-case evidence packet:

- seed common-core: `9` cases
- Batch 2A PERF expansion: `19` additional PERF cases
- Batch 2B CONS expansion: `3` additional CONS cases

The expanded packet shows three things clearly:

- the seed packet validated the end-to-end formal pipeline on a compact mixed PERF/CONS slice
- Batch 2A exposes a major capability boundary for `SQLGLOT_OPT_SAME_DIALECT`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` closes Batch 2A consistency and executes cleanly, but it should be treated as a separate baseline candidate rather than a silent replacement

Batch 2B adds three checker-backed CONS cases to the expanded common-core consistency line and closes that narrow expansion cleanly.

# Denominator / Scope Table

| packet | scope | case count | notes |
| --- | --- | ---: | --- |
| seed common-core | mixed `PERF` + `CONS`, PostgreSQL formal packet | `9` | full seed pipeline already closed |
| Batch 2A | `PERF` only, PostgreSQL | `19` | execution expansion, SQLGlot optimize boundary, no-opt candidate, speedup |
| Batch 2B | `CONS` only, PostgreSQL | `3` | control execution + checker-backed consistency expansion |
| total current expanded evidence | mixed across the three packets | `31` | route coverage differs by batch and must not be collapsed into one uniform leaderboard denominator |

Current 31-case evidence composition:

- seed:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0013`
  - `PERF_0017`
  - `PERF_0024`
  - `PERF_0033`
  - `PERF_0054`
  - `CONS_0007`
  - `CONS_0012`
- Batch 2A:
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
- Batch 2B:
  - `CONS_0024`
  - `CONS_0031`
  - `CONS_0034`

# Correctness / Consistency Summary

Seed common-core:

- control correctness and guard behavior are complete on `9` cases
- `SQLGLOT_OPT_SAME_DIALECT` seed generated-method consistency: `9 / 9`
- `LLM_DIRECT_REWRITE_STRONG` seed generated-method consistency: `9 / 9`

Batch 2A PERF:

- control execution:
  - `NATIVE_IDENTITY 19 / 19`
  - `HUMAN_REFERENCE_POSITIVE 19 / 19`
  - `HARD_NEGATIVE_GUARD 19 / 19`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - generation `19 / 19`
  - PostgreSQL execution `19 / 19`
  - exact TSV checker consistency `19 / 19`
  - `ResultConsistencyRate = 1.0`

Batch 2B CONS:

- native executable: `3 / 3`
- human positive executable: `3 / 3`
- hard negative executable: `3 / 3`
- `ResultConsistencyRate = 1.0`
- `NegativeRejectionRate = 1.0`
- `FalseAcceptRate = 0.0`
- checker mode:
  - `value_normalized_in_memory_from_checker_yaml`

Important route distinction:

- `SQLGLOT_OPT_SAME_DIALECT` seed route remained fully consistent on the original `9` cases
- Batch 2A shows that this does not generalize across the expanded PERF slice
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is the route that closes Batch 2A consistency on the expanded slice

# Execution / Capability Boundary Summary

Batch 2A control routes are healthy:

- `NATIVE_IDENTITY 19 / 19`
- `HUMAN_REFERENCE_POSITIVE 19 / 19`
- `HARD_NEGATIVE_GUARD 19 / 19`

`SQLGLOT_OPT_SAME_DIALECT` on Batch 2A:

- success: `4 / 19`
- failed: `15 / 19`

Failure clusters:

- `OptimizeError = 13`
- `UndefinedColumn = 2`

Interpretation:

- the dominant problem is optimizer-stage unresolved-column failure
- the smaller second cluster is execution-stage generated SQL bad-column reference failure
- because all three control routes stay healthy, the observed failures are method-route capability failures rather than package-health failures

# Speedup Summary

| route | denominator | GM_Speedup | W / T / L | RegressionRate@20% | note |
| --- | --- | ---: | --- | --- | --- |
| `HUMAN_REFERENCE_POSITIVE` | seed PERF-only `7` | `0.96159127168004` | `1 / 2 / 4` | `0 / 7` | positive-control speedup only |
| `SQLGLOT_OPT_SAME_DIALECT` | seed PERF-only `7` | `0.9709643241218479` | `1 / 2 / 4` | `0 / 7` | seed only; expanded PERF capability later proved narrow |
| `LLM_DIRECT_REWRITE_STRONG` | seed PERF-only `7` | `1.0023345046000625` | `1 / 5 / 1` | `0 / 7` | seed only; PERF-only runtime packet |
| `HUMAN_REFERENCE_POSITIVE` | Batch 2A PERF `19` | `0.9733` | `4 / 9 / 6` | `3 / 19` | expanded PERF positive-control runtime |
| `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` | Batch 2A PERF `19` | `1.0119` | `4 / 13 / 2` | `0 / 19` | separate baseline candidate, not replacement for optimize route |

Speedup interpretation:

- performance trends remain modest and mostly tie-like
- positive-control rewrites do not guarantee speedup
- the no-opt SQLGlot route has broader execution/correctness coverage than optimize on Batch 2A, but runtime gains are limited

# What This Means For Paper

The seed packet validated the end-to-end formal pipeline on a compact mixed common-core slice. Batch 2A then showed that the seed packet was optimistic for `SQLGLOT_OPT_SAME_DIALECT`: the expanded PERF denominator exposes a strong optimizer capability boundary that was not visible in the smaller seed. The no-opt SQLGlot route provides materially broader coverage and closes exact TSV consistency across Batch 2A, which strengthens the method capability-boundary story, but it should be reported as a separately named baseline candidate. Batch 2B adds three clean CONS cases and strengthens the expanded consistency line. Across the runtime packets, speedup results are modest and mostly tie-like, which supports the need to gate benchmark interpretation on execution, correctness/consistency, and runtime together rather than on speedup alone.

# Boundaries / Non-Claims

- not a final leaderboard
- not admission
- not registry writeback
- route denominators differ and should not be collapsed into a single uniform table
- PORT remains separate from this rollup
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is not a silent replacement for `SQLGLOT_OPT_SAME_DIALECT`
- no expanded MySQL / Spark matrix yet
- no formal review update

# Remaining Work

- Batch 2C PORT expansion
- larger common-core scorer consolidation if needed
- method-specific LLM expansion if API budget allows
- final denominator freeze / protocol review
- later registry, formal review, and admission work

# Recommended Next Action

- run Batch 2C PORT candidate preflight / execution expansion, because common-core has now been expanded while PORT remains narrow

# Verification / Non-Modification Note

- only this rollup doc was created
- no SQL execution was performed
- no database workload was run
- no model / LLM call was made
- no SQLGlot execution was run
- no checker execution was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
