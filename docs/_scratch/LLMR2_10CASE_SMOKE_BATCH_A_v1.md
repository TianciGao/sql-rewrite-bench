# LLMR2_10CASE_SMOKE_BATCH_A_v1

## 0. Purpose And Boundary
- bounded LLM-R2 10-case subset Batch A execution
- cases: PERF_0008 / PERF_0013 / PERF_0017
- not leaderboard
- not full prior-method coverage
- no speedup
- no registry writeback

## 1. Batch A Cases
- `PERF_0008`: selected from the 10-case expansion preflight as a ready-for-bounded-smoke case on the shared denominator, with source SQL, PostgreSQL schema, witness data, one-row staging, schema-native JSON, tiny pools, and checker handoff contract all available.
- `PERF_0013`: selected from the same ready-for-bounded-smoke pool with the same bounded one-row fast-path prerequisites already staged.
- `PERF_0017`: selected from the same ready-for-bounded-smoke pool with the same bounded one-row fast-path prerequisites already staged.

## 2. Per-case Result Table
| case_id | dry_run_passed | logical_plan_probe_status | candidate_generated | clean_candidate_recovered | candidate_executed | checker_status | consistency_status | candidate_type | failure_category | failure_summary | speedup_status | artifact_paths | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0008` | `true` | `passed` | `yes` | `yes` | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `none` | `not_run` | `result_csv`, `clean_candidate`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0008/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0013` | `true` | `passed` | `yes` | `yes` | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `none` | `not_run` | `result_csv`, `clean_candidate`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0013/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |
| `PERF_0017` | `true` | `passed` | `yes` | `yes` | `yes` | `consistent` | `consistent` | `clean_extracted_candidate` | `none` | `none` | `not_run` | `result_csv`, `clean_candidate`, `checker_result`, `logs` under `/tmp/rewritebench_llmr2_fast_path/PERF_0017/` | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |

## 3. Batch A Metrics
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
- No Batch A case stopped at logical-plan extraction. The schema-native contract and bounded one-row runtime staging were sufficient for `PERF_0008`, `PERF_0013`, and `PERF_0017`.
- No Batch A case ended in method-generation failure after the approved external CPU-only runs. The only transient friction was wrapper/runtime setup noise before successful reruns, not a final case outcome.
- All three cases produced output SQL, but each required the same post-generation cleanup pattern already seen on `PERF_0006`: the raw extracted SQL artifact was not clean enough for direct checker handoff, and a deterministic clean single-statement candidate had to be recovered from `rewritten_sql_gpt`.
- After cleanup, all three clean candidates executed successfully under PostgreSQL checker handoff and matched the source outputs on witness data.
- Batch A therefore exposes an adapter/runtime pattern for LLM-R2 that is now repeatable on this bounded subset: one-row fast path, CPU-only execution, schema-native staging, output extraction cleanup, then checker handoff.

## 5. Contribution To LLM-R2 @10
- Batch A adds three new checker-backed bounded smoke results on top of the existing `PERF_0006` anchor.
- The current bounded evidence therefore covers `PERF_0006`, `PERF_0008`, `PERF_0013`, and `PERF_0017`, but this note does not compute the full LLM-R2 `@10` rollup yet because Batch B and Batch C are still pending.
- If later batches follow the same path, the final LLM-R2 `@10` report can merge:
  - `PERF_0006` anchor
  - Batch A: `PERF_0008`, `PERF_0013`, `PERF_0017`
  - future Batch B
  - future Batch C

## 6. Recommended Next Step
- execute LLM-R2 Batch B

Justification:
- Batch A did not reveal a new shared blocker that should stop expansion.
- The bounded runtime path now reproduced checker-consistent results on three additional cases beyond `PERF_0006`.
- The highest-value next step is to continue the same bounded execution path on `PERF_0019`, `PERF_0024`, and `PERF_0033` before attempting any broader aggregation.

## 7. Non-Modification Note
- only `PERF_0008`, `PERF_0013`, and `PERF_0017` were targeted
- no speedup was run
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made
- no case files were modified
- no MySQL, Spark, or standalone SQLGlot routes were used
- the three long-standing taxonomy notes were untouched
