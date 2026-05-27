# LLMR2_10CASE_SMOKE_BATCH_C_v1

## 0. Purpose And Boundary
- bounded LLM-R2 10-case subset Batch C execution
- cases: PERF_0052 / PERF_0054 / PERF_0063
- not leaderboard
- not full prior-method coverage
- no speedup
- no registry writeback

## 1. Batch C Cases
- `PERF_0052`: selected from the 10-case expansion preflight as a ready-for-bounded-smoke case on the shared denominator, with source SQL, PostgreSQL schema, witness data, one-row staging, schema-native JSON, tiny pools, and checker handoff contract all available.
- `PERF_0054`: selected from the same ready-for-bounded-smoke pool with the same bounded one-row fast-path prerequisites already staged.
- `PERF_0063`: selected from the same ready-for-bounded-smoke pool with the same bounded one-row fast-path prerequisites already staged.

## 2. Per-case Result Table
| case_id | dry_run_passed | logical_plan_probe_status | candidate_generated | clean_candidate_recovered | extraction_version_used | candidate_executed | checker_status | consistency_status | candidate_type | failure_category | failure_summary | speedup_status | artifact_paths | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0052` | `true` | `passed` | `yes` | `yes` | `v2` | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `none` | `not_run` | `result_csv`, `clean_candidate_v2`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0052/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0054` | `true` | `passed` | `yes` | `yes` | `v1` | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `none` | `not_run` | `result_csv`, `clean_candidate_v1`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0054/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0063` | `true` | `failed` | `no` | `no` | `none` | `not_run` | `not_run` | `not_checked` | `none` | `logical_plan_probe_failed` | `java_extractor_output_malformed before LLM-R2 execution on both raw and comment-stripped probes` | `not_run` | `logical_plan_probe_json`, `probe_stdout`, `probe_stderr` under `/tmp/rewritebench_llmr2_fast_path/PERF_0063/` | `bounded_1_case_LLMR2_smoke_attempt_not_speedup_not_leaderboard` |

## 3. Batch C Metrics
- denominator = `3`
- candidate_generation_count = `2`
- candidate_generation_rate@3 = `2/3`
- clean_candidate_recovered_count = `2`
- candidate_execution_count = `2`
- executable_rate@3 = `2/3`
- checker_consistent_count = `2`
- result_consistency_rate@3 = `2/3`
- checker_failed_count = `0`
- generation_or_method_failure_count = `1`
- output_extraction_failure_count = `0`
- logical_plan_failure_count = `1`
- speedup_status = `not_run`

## 4. Failure / Behavior Analysis
- `PERF_0052` and `PERF_0054` cleared dry-run, logical-plan probe, CPU-only bounded smoke, output extraction cleanup, and PostgreSQL checker handoff.
- `PERF_0052` needed the safer nested-query extraction path. The raw output SQL contained a truncated prefix plus inline source-comment contamination, so earliest balanced structural `SELECT/WITH` recovery was used and recorded as `v2`.
- `PERF_0054` did not need the nested-query fallback. The bounded cleanup path recovered a valid outermost `SELECT` and checker handoff succeeded.
- `PERF_0063` did not reach LLM-R2 execution. The logical-plan probe failed on both the raw-query path and the comment-stripped path, with malformed Java extractor output before any prompt/API phase.
- Batch C therefore introduces one genuine upstream blocker at the logical-plan stage while still adding two more checker-consistent bounded cases.

## 5. Contribution To LLM-R2 @10
- Batch C completes the planned denominator coverage attempt across:
  - `PERF_0006` anchor
  - Batch A: `PERF_0008`, `PERF_0013`, `PERF_0017`
  - Batch B: `PERF_0019`, `PERF_0024`, `PERF_0033`
  - Batch C: `PERF_0052`, `PERF_0054`, `PERF_0063`
- The full LLM-R2 `@10` rollup can now be computed from:
  - checker-backed successes on `PERF_0006`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0033`, `PERF_0052`, `PERF_0054`
  - one logical-plan-stage failure on `PERF_0063`

## 6. Recommended Next Step
- create full LLM-R2 @10 rollup

Justification:
- Batch C completed the planned bounded denominator attempt.
- The remaining work is now aggregation, not more discovery within this denominator.
- The correct next step is to roll up the full 10-case LLM-R2 bounded smoke evidence, with explicit accounting for the `PERF_0063` logical-plan blocker and without introducing any speedup claims.

## 7. Non-Modification Note
- only `PERF_0052`, `PERF_0054`, and `PERF_0063` were targeted
- no speedup was run
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made
- no case files were modified
- no MySQL, Spark, or standalone SQLGlot routes were used
- the three long-standing taxonomy notes were untouched
