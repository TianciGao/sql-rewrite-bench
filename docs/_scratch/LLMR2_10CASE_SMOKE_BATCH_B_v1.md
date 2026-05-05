# LLMR2_10CASE_SMOKE_BATCH_B_v1

## 0. Purpose And Boundary
- bounded LLM-R2 10-case subset Batch B execution
- cases: PERF_0019 / PERF_0024 / PERF_0033
- not leaderboard
- not full prior-method coverage
- no speedup
- no registry writeback

## 1. Batch B Cases
- `PERF_0019`: selected from the 10-case expansion preflight as a ready-for-bounded-smoke case on the shared denominator, with source SQL, PostgreSQL schema, witness data, one-row staging, schema-native JSON, tiny pools, and checker handoff contract all available.
- `PERF_0024`: selected from the same ready-for-bounded-smoke pool with the same bounded one-row fast-path prerequisites already staged.
- `PERF_0033`: selected from the same ready-for-bounded-smoke pool with the same bounded one-row fast-path prerequisites already staged.

## 2. Per-case Result Table
| case_id | dry_run_passed | logical_plan_probe_status | candidate_generated | clean_candidate_recovered | candidate_executed | checker_status | consistency_status | candidate_type | failure_category | failure_summary | speedup_status | artifact_paths | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0019` | `true` | `passed` | `yes` | `yes` | `no` | `failed` | `not_checked` | `clean_extracted_candidate` | `SyntaxError` | `candidate failed PG execution near derived-table alias syntax` | `not_run` | `result_csv`, `clean_candidate`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0019/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0024` | `true` | `passed` | `yes` | `yes` | `no` | `failed` | `not_checked` | `clean_extracted_candidate` | `SyntaxError` | `candidate failed PG execution near derived-table join fragment` | `not_run` | `result_csv`, `clean_candidate`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0024/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0033` | `true` | `passed` | `yes` | `yes` | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `none` | `not_run` | `result_csv`, `clean_candidate`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0033/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |

## 3. Batch B Metrics
- denominator = `3`
- candidate_generation_count = `3`
- candidate_generation_rate@3 = `3/3`
- clean_candidate_recovered_count = `3`
- candidate_execution_count = `1`
- executable_rate@3 = `1/3`
- checker_consistent_count = `1`
- result_consistency_rate@3 = `1/3`
- checker_failed_count = `2`
- generation_or_method_failure_count = `0`
- output_extraction_failure_count = `0`
- logical_plan_failure_count = `0`
- speedup_status = `not_run`

## 4. Failure / Behavior Analysis
- No Batch B case stopped at dry-run or logical-plan extraction. The schema-native contract and bounded one-row runtime staging were sufficient for `PERF_0019`, `PERF_0024`, and `PERF_0033`.
- All three cases completed CPU-only schema-native LLM-R2 generation and produced output SQL in the result CSV.
- All three cases required the same deterministic cleanup pattern already used on `PERF_0006` and Batch A: a clean single-statement candidate had to be recovered from `rewritten_sql_gpt` before checker handoff.
- `PERF_0019` and `PERF_0024` then failed at PostgreSQL execution time. These are checker-stage execution failures on recovered candidates, not logical-plan failures, generation failures, or output-extraction failures.
- `PERF_0033` completed the full bounded path and produced a checker-consistent candidate.
- Batch B therefore shows a different behavior profile from Batch A: candidate generation remained stable, but checker-backed execution dropped because two recovered candidates were not valid PostgreSQL statements.

## 5. Contribution To LLM-R2 @10
- Batch B adds three more bounded smoke results on top of the existing `PERF_0006` anchor and Batch A.
- The current bounded evidence now spans:
  - `PERF_0006` anchor
  - Batch A: `PERF_0008`, `PERF_0013`, `PERF_0017`
  - Batch B: `PERF_0019`, `PERF_0024`, `PERF_0033`
- This note does not compute the final LLM-R2 `@10` rollup yet because Batch C is still pending and the combined `@10` aggregation should be done once the full denominator is closed.

## 6. Recommended Next Step
- pause and diagnose Batch B failures

Justification:
- Batch B surfaced a new bounded failure mode that did not appear in Batch A: checker-stage PostgreSQL syntax failure after otherwise successful candidate generation and cleanup.
- Advancing immediately to Batch C would risk conflating a repeatable extraction-or-normalization issue with true case-level method behavior.
- The highest-value next step is to inspect the recovered `PERF_0019` and `PERF_0024` candidates and determine whether the failure is:
  - residual extraction contamination,
  - dialect mismatch in the generated SQL, or
  - genuine method-level invalid SQL generation.

## 7. Non-Modification Note
- only `PERF_0019`, `PERF_0024`, and `PERF_0033` were targeted
- no speedup was run
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made
- no case files were modified
- no MySQL, Spark, or standalone SQLGlot routes were used
- the three long-standing taxonomy notes were untouched
