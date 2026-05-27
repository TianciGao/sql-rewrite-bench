# FORMAL_COMMON_CORE_SQLGLOT_SCORING_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of formal common-core SQLGlot same-dialect scoring state.

## 2. Inputs / Report References

Command:

- `python -m scripts.cli formal-common-core-sqlglot-scoring`

Reports:

- `reports/formal_common_core/sqlglot_opt_same_dialect_execution_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_scoring_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_scoring_execute_refused_v0.json`

## 3. SQLGlot Route Summary

- `parse_success_rate=1.0`
- `generation_success_rate=1.0`
- `executable_rate=1.0`
- row-count match: `9 / 9`
- `result_consistency_rate_status=not_computed_checker_required`
- `formal_correctness_scoring_complete=false`
- `speedup_scoring_complete=false`

## 4. Per-Case Compact Observations

| case_id | parse_status | generation_status | execution_status | native_row_count | sqlglot_row_count | row_count_match |
|---|---|---|---|---:|---:|---|
| `PERF_0006` | `success` | `success` | `success` | `2` | `2` | `true` |
| `PERF_0008` | `success` | `success` | `success` | `1` | `1` | `true` |
| `PERF_0013` | `success` | `success` | `success` | `1` | `1` | `true` |
| `PERF_0017` | `success` | `success` | `success` | `1` | `1` | `true` |
| `PERF_0024` | `success` | `success` | `success` | `1` | `1` | `true` |
| `PERF_0033` | `success` | `success` | `success` | `1` | `1` | `true` |
| `PERF_0054` | `success` | `success` | `success` | `1` | `1` | `true` |
| `CONS_0007` | `success` | `success` | `success` | `2` | `2` | `true` |
| `CONS_0012` | `success` | `success` | `success` | `2` | `2` | `true` |

## 5. Interpretation

- SQLGlot same-dialect formal execution is complete
- SQLGlot row-count observation is complete
- checker-backed consistency is not complete
- speedup scoring is not complete

## 6. Boundary

- row-count match is not semantic equivalence
- this is not SQLGlot correctness=`1.0`
- this is not final leaderboard data
- this is not speedup scoring

## 7. Recommended Next Action

- begin Direct LLM rewrite formal execution/scoring

## 8. Verification / Non-Modification Note

- only this note was created
- no database workloads were run
- no SQL was executed
- no SQLGlot was run
- no checker was run
- no LLM calls were made
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
