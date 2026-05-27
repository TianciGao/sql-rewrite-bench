# Status

This is a Batch 2A formal results closeout packet for the expanded PERF denominator.

# Executive Summary

- Batch 2A extends beyond the earlier seed packet with `19` additional PERF cases.
- Control routes are healthy across the full Batch 2A slice.
- `SQLGLOT_OPT_SAME_DIALECT` exposes a major capability boundary on the expanded denominator.
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` recovers all prior optimize-route failures and is checker-consistent on the full 19-case slice.
- Speedup outcomes are modest and mostly tie-like rather than strong systematic wins.
- This packet does not claim full common-core closure, full leaderboard status, or admission.

# Batch 2A Denominator

Scope:

- pool: `PERF` only
- engine: PostgreSQL only
- no LLM
- no PORT
- no CONS
- no MySQL
- no Spark

Cases:

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

# Table A: Execution Expansion

| route | success | failed | interpretation |
| --- | ---: | ---: | --- |
| `NATIVE_IDENTITY` | `19` | `0` | Native source execution is stable across the full Batch 2A PERF slice. |
| `HUMAN_REFERENCE_POSITIVE` | `19` | `0` | Human positive controls remain fully executable across the expanded denominator. |
| `HARD_NEGATIVE_GUARD` | `19` | `0` | Negative guard route also remains operational, which supports package/validation health. |
| `SQLGLOT_OPT_SAME_DIALECT` | `4` | `15` | Failures are route-specific rather than package-wide because all control routes pass. |

Batch total:

- total records: `76`
- success: `61`
- failed: `15`

# Table B: SQLGlot Optimize Failure Profile

| cluster | count | cases / status | interpretation |
| --- | ---: | --- | --- |
| `OptimizeError` | `13` | optimizer-stage unresolved-column failures on `PERF_0010`, `PERF_0011`, `PERF_0012`, `PERF_0014`, `PERF_0015`, `PERF_0016`, `PERF_0018`, `PERF_0019`, `PERF_0020`, `PERF_0021`, `PERF_0022`, `PERF_0023`, `PERF_0025` | The dominant failure mode is an optimizer capability boundary under the current same-dialect optimize route. |
| `UndefinedColumn` | `2` | execution-stage generated-SQL bad column references on `PERF_0009`, `PERF_0026` | These are distinct generated-SQL alias/column resolution failures, not package health failures. |
| `Success cases` | `4` | `PERF_0007`, `PERF_0034`, `PERF_0035`, `PERF_0036` | The optimize route is selective rather than universally broken, but its success region is narrow on the expanded denominator. |

# Table C: SQLGlot No-Opt Fallback / Checker

| evidence slice | result | interpretation |
| --- | --- | --- |
| Prior optimize-failed cases only | generation `15/15`, PG execution `15/15` | The no-opt same-dialect transpile path recovers all cases that previously failed under the optimize route. |
| Recovery split | `13/13` OptimizeError recovered, `2/2` UndefinedColumn recovered | The earlier optimize-route failure cluster is strongly optimizer-specific under current settings. |
| Full 19-case formal no-opt checker | generation `19/19`, PG execution `19/19`, exact TSV consistent `19/19`, `ResultConsistencyRate=1.0` | `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is supported as a separate baseline candidate. |

Boundary:

- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is a separate baseline candidate
- it is not a silent replacement for `SQLGLOT_OPT_SAME_DIALECT`

# Table D: Batch 2A Speedup

| route | GM_Speedup | W/T/L | RegressionRate@20% | claim boundary |
| --- | ---: | --- | --- | --- |
| `HUMAN_REFERENCE_POSITIVE` | `0.9733` | `4 / 9 / 6` | `3/19` | PostgreSQL-only Batch 2A PERF runtime evidence; not leaderboard or correctness closure. |
| `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` | `1.0119` | `4 / 13 / 2` | `0/19` | PostgreSQL-only Batch 2A PERF runtime evidence for a separate baseline candidate; not replacement for optimize route. |

Shared speedup run facts:

- cases: `19`
- records: `38`
- success: `38/38`
- row-count matches: `38/38`

# Interpretation

The earlier seed packet was optimistic for `SQLGLOT_OPT_SAME_DIALECT`. The expanded Batch 2A denominator makes the optimizer boundary visible: control routes are fully healthy, while the optimize route fails on most of the expanded TPC-H / TPC-DS PERF slice. The no-opt SQLGlot route has much broader coverage and closes exact TSV consistency on all 19 cases, but its speedup behavior is modest and mostly tie-like. Human positive rewrites also do not guarantee speedup: they remain fully executable and logically valid in this slice, yet the route-level GM speedup is below `1.0` with `3/19` regressions at the 20% threshold. The combined result supports the benchmark requirement to gate routes on execution, correctness/consistency, and runtime behavior rather than relying on any single dimension.

# Claim Boundaries

- not a full benchmark leaderboard
- PERF-only
- PostgreSQL-only
- no LLM in Batch 2A
- no PORT
- no CONS
- no MySQL
- no Spark
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is a separate baseline candidate
- no registry writeback
- no formal review update

# Recommended Next Action

- run Batch 2B CONS minor-backfill preflight for `CONS_0024`, `CONS_0031`, and `CONS_0034`

# Verification / Non-Modification Note

- only this closeout doc was created
- no SQL/database/model/SQLGlot/checker/speedup execution was performed in this step
- no reports were force-added
- no registry, `docs/EXECUTION_STATUS.md`, or formal review files were changed
- taxonomy calibration notes were untouched
