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
| `PERF_0019` | `true` | `passed` | `yes` | `yes`, via `v2` extraction | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `original v1 checker attempt failed from extraction artifact; v2 checker passed` | `not_run` | `result_csv`, `clean_candidate_v2`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0019/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0024` | `true` | `passed` | `yes` | `yes`, via `v2` extraction | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `original v1 checker attempt failed from extraction artifact; v2 checker passed` | `not_run` | `result_csv`, `clean_candidate_v2`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0024/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0033` | `true` | `passed` | `yes` | `yes` | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `none` | `not_run` | `result_csv`, `clean_candidate`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0033/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |

## 3. Batch B Metrics
- denominator = `3`
- candidate_generation_count = `3`
- candidate_generation_rate@3 = `3/3`
- clean_candidate_recovered_count = `3`
- candidate_execution_count = `3`
- executable_rate@3 = `3/3`
- checker_consistent_count = `3`
- result_consistency_rate@3 = `3/3`
- checker_failed_count = `0`
- generation_or_method_failure_count = `0`
- output_extraction_failure_count = `0`
- logical_plan_failure_count = `0`
- speedup_status = `not_run`

## 4. Failure / Behavior Analysis
- No Batch B case stopped at dry-run or logical-plan extraction. The schema-native contract and bounded one-row runtime staging were sufficient for `PERF_0019`, `PERF_0024`, and `PERF_0033`.
- All three cases completed CPU-only schema-native LLM-R2 generation and produced output SQL in the result CSV.
- All three cases required deterministic cleanup of `rewritten_sql_gpt` before checker handoff.
- The original `v1` cleanup rule used a “last `SELECT` wins” heuristic. That was unsafe for nested queries and caused `PERF_0019` and `PERF_0024` to be truncated into inner-subquery fragments during the original checker attempt.
- A `v2` extraction cleanup using earliest balanced `SELECT/WITH` recovery fixed both nested-query cases without rerunning LLM-R2.
- `PERF_0019`, `PERF_0024`, and `PERF_0033` therefore all end Batch B with checker-consistent clean extracted candidates.
- Batch B now matches Batch A at the final checker-backed outcome layer, while also exposing an important adapter lesson: output extraction can be a first-class failure mode separate from candidate generation and semantic checking.

## 5. Contribution To LLM-R2 @10
- Batch B adds three more bounded smoke results on top of the existing `PERF_0006` anchor and Batch A.
- The current bounded evidence now spans:
  - `PERF_0006` anchor
  - Batch A: `PERF_0008`, `PERF_0013`, `PERF_0017`
  - Batch B: `PERF_0019`, `PERF_0024`, `PERF_0033`
- This note does not compute the final LLM-R2 `@10` rollup yet because Batch C is still pending and the combined `@10` aggregation should be done once the full denominator is closed.

## 6. Recommended Next Step
- execute LLM-R2 Batch C

Justification:
- The Batch B checker failures were resolved as extraction artifact rather than method-generation failure.
- Batch B now reflects the same bounded end state as Batch A: generated candidates, clean recovery, successful PostgreSQL execution, and checker consistency on all three cases.
- The highest-value next step is to continue the bounded rollout on `PERF_0052`, `PERF_0054`, and `PERF_0063`.

## 7. Non-Modification Note
- only `PERF_0019`, `PERF_0024`, and `PERF_0033` were targeted
- no speedup was run
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made
- no case files were modified
- no MySQL, Spark, or standalone SQLGlot routes were used
- the three long-standing taxonomy notes were untouched
