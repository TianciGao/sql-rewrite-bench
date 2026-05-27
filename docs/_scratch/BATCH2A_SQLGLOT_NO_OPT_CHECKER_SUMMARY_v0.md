# Status

This is a Batch 2A formal execution plus report-local exact TSV checker summary for `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` on PostgreSQL. The route is evaluated as a separate baseline candidate and does not replace `SQLGLOT_OPT_SAME_DIALECT`.

# Why This Route Was Evaluated

Prior Batch 2A evidence showed:

- `SQLGLOT_OPT_SAME_DIALECT`: `4/19` PostgreSQL execution success, `15/19` failure
- Batch 2A no-opt fallback diagnostic on those 15 failed cases:
  - generation `15/15`
  - PostgreSQL execution `15/15`

That justified a separate formal check of the no-opt route across the full 19-case Batch 2A PERF slice.

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

# Comparison To SQLGLOT_OPT_SAME_DIALECT Failure Profile

- Existing optimize route:
  - PostgreSQL execution success: `4`
  - PostgreSQL execution failed: `15`
- No-opt route in this run:
  - generation success: `19`
  - candidate PostgreSQL execution success: `19`
  - checker consistent: `19`

Interpretation: the no-opt path is materially different from the optimize path and should be treated as a separate method route.

# No-Opt Generation / PG Execution Summary

- Generation success: `19/19`
- Generation failed: `0/19`
- Source execution success: `19/19`
- Candidate execution success: `19/19`
- Candidate execution failed: `0/19`

Canary:

- `PERF_0010`
  - generation: success
  - source PG execution: success
  - candidate PG execution: success
  - exact TSV checker: consistent

# Report-Local Checker Result

- Checker mode: `exact_tsv_report_local`
- Consistent: `19/19`
- Inconsistent: `0/19`
- Checker failed: `0/19`
- Result consistency rate: `1.0`
- Row-count match count: `19`
- Row-count mismatch count: `0`

# Failed / Inconsistent Cases

None in this run.

# Interpretation

- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is now supported by stronger evidence than the earlier fallback diagnostic because it completed source-vs-candidate exact TSV checking across the full Batch 2A slice.
- This is still a separate baseline candidate only.
- It does not justify silently replacing `SQLGLOT_OPT_SAME_DIALECT`.
- This is not speedup evidence.
- This is not leaderboard evidence.

# Recommended Next Action

Add `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` to the next Batch 2A scoring and speedup plan as a separately named baseline candidate, while keeping `SQLGLOT_OPT_SAME_DIALECT` tracked independently.

# Claim Boundaries

- not silent baseline replacement
- not speedup
- not leaderboard
- PostgreSQL only
- no PORT or CONS execution
- no registry or formal-review update

# Verification / Non-Modification Note

- only this scratch summary was created
- no reports were force-added
- no case-local artifacts were written
- no registry, `docs/EXECUTION_STATUS.md`, or formal review files were changed
