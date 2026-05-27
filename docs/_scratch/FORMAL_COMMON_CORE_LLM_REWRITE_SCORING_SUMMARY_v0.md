# FORMAL_COMMON_CORE_LLM_REWRITE_SCORING_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the current formal common-core Direct LLM rewrite execution/scoring state.

## 2. Inputs / Report References

Command:

- `python -m scripts.cli formal-common-core-llm-rewrite-scoring`

Reports:

- `reports/formal_common_core/llm_direct_rewrite_execution_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_scoring_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_scoring_execute_refused_v0.json`

## 3. Execution Formalization Result

Existing formal execution-layer report shows:

- `call_success_count=9`
- `extracted_sql_count=9`
- `pg_execution_success_count=9`
- `executable_rate=1.0`

This route state comes entirely from existing smoke artifacts. No new model call or PostgreSQL execution was performed by the scoring command.

## 4. Scoring Summary

Current formal LLM rewrite scoring summary:

- `call_success_rate=1.0`
- `extraction_success_rate=1.0`
- `pg_execution_success_rate=1.0`
- `executable_rate=1.0`
- `row_count_match_count=9`
- `row_count_mismatch_count=0`
- `row_count_unknown_count=0`
- `result_consistency_rate_status=not_computed_checker_required`
- `result_consistency_rate_observed_existing_artifacts=null`
- `formal_correctness_scoring_complete=false`
- `speedup_scoring_complete=false`

## 5. Token Summary

- `total_token_usage=5089`
- `token_per_executable_rewrite=565.4444444444445`

Current route metadata remains artifact-derived from the earlier smoke pass. Pricing remains outside formal scoring freeze.

## 6. Row-Count Observations

Row-count observations versus `NATIVE_IDENTITY`:

- `PERF_0006`: native `2`, llm `2`, match `true`
- `PERF_0008`: native `1`, llm `1`, match `true`
- `PERF_0013`: native `1`, llm `1`, match `true`
- `PERF_0017`: native `1`, llm `1`, match `true`
- `PERF_0024`: native `1`, llm `1`, match `true`
- `PERF_0033`: native `1`, llm `1`, match `true`
- `PERF_0054`: native `1`, llm `1`, match `true`
- `CONS_0007`: native `2`, llm `2`, match `true`
- `CONS_0012`: native `2`, llm `2`, match `true`

## 7. Checker-Backed Consistency Status

Checker-backed LLM result consistency was not computed.

Current status:

- `result_consistency_rate_status=not_computed_checker_required`
- route-level checker-backed correctness remains incomplete

Reason:

- existing route artifacts do not safely expose an explicit LLM-vs-native consistency field that can be consumed without rerunning checker logic

## 8. Boundary

- no new model call
- no new SQL execution
- no speedup scoring
- no leaderboard claim
- row-count match is not semantic equivalence
- this is a read-existing-reports-only LLM route scoring summary

## 9. Recommended Next Action

- create / update current formal common-core results snapshot

## 10. Verification / Non-Modification Note

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
