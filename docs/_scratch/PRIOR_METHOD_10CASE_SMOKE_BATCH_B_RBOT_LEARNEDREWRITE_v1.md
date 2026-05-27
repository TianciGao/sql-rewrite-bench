# PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1

## 0. Purpose And Boundary
This note records bounded 10-case subset Batch B execution for `PERF_0024`, `PERF_0052`, `PERF_0054`, and `PERF_0063` across `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite`. It is not leaderboard evidence, not full prior-method coverage, does not include speedup, and does not write back to any registry.

## 1. Batch B Cases
- `PERF_0024`: selected from the 10-case preflight as the correlated nested-subquery case with established PG/control evidence.
- `PERF_0052`: selected to add a compact TPC-DS decorrelation / correlated-aggregate pattern with clean PG evidence.
- `PERF_0054`: selected as a TPC-DS join/aggregate/order case already present in the proposed denominator and useful for comparing nontrivial outputs.
- `PERF_0063`: selected to add string-function and disjunctive-filter behavior absent from the earlier batches.

## 2. Per-case Result Table
| method | case_id | candidate_generated | candidate_executed | checker_status | consistency_status | candidate_type | failure_category | failure_summary | speedup_status | artifact_paths | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | `PERF_0024` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | none | not_run | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0024/` | `bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard` |
| `R-Bot / LLM4Rewrite` | `PERF_0052` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | none | not_run | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0052/` | `bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard` |
| `R-Bot / LLM4Rewrite` | `PERF_0054` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | none | not_run | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0054/` | `bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard` |
| `R-Bot / LLM4Rewrite` | `PERF_0063` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | none | not_run | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0063/` | `bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0024` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | none | not_run | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0024/` | `bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0052` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | none | not_run | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0052/` | `bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0054` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | none | not_run | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0054/` | `bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0063` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | none | not_run | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0063/` | `bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard` |

## 3. Batch B Method Metrics
| method | denominator | candidate_generation_count | candidate_generation_rate@4 | candidate_execution_count | executable_rate@4 | checker_consistent_count | result_consistency_rate@4 | checker_failed_count | source_like_or_noop_count | speedup_status | speedup_comparable_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | 4 | 4 | 4/4 | 4 | 4/4 | 4 | 4/4 | 0 | 0 | not_run | 4 |
| `LearnedRewrite / embedded LLM4Rewrite` | 4 | 4 | 4/4 | 4 | 4/4 | 4 | 4/4 | 0 | 3 | not_run | 1 |

## 4. Contribution To 10-case Subset
Batch B adds four completed case/method pairs on top of the already executed base:
- prior executed base: `PERF_0006`, `PERF_0008`, `PERF_0033`
- Batch A: `PERF_0013`, `PERF_0017`, `PERF_0019`
- Batch B: `PERF_0024`, `PERF_0052`, `PERF_0054`, `PERF_0063`

The next rollup can merge these artifacts directly into the bounded 10-case denominator without rerunning any earlier case.

## 5. Failure / Behavior Analysis
- `R-Bot / LLM4Rewrite` produced four nontrivial candidates and all four executed and passed the PostgreSQL checker.
- `LearnedRewrite / embedded LLM4Rewrite` also produced four executable, checker-consistent candidates, but three of them remained source-like / no-op outputs: `PERF_0024`, `PERF_0052`, and `PERF_0063`.
- `LearnedRewrite / embedded LLM4Rewrite` showed one checker-consistent nontrivial candidate in this batch: `PERF_0054`.
- No Batch B case hit `output_sql_missing`, execution failure, checker failure, or method exception after smoke launch.
- This batch therefore distinguishes useful correctness-backed generation behavior from checker-consistent but mostly source-like fallback behavior.

## 6. Recommended Next Step
`create full 10-case rollup`

Reason:
- Batch B completed cleanly for both methods.
- The bounded 10-case denominator now has execution evidence for all planned cases.
- A full rollup is the next bounded reporting step before any further expansion or any speedup discussion.

## 7. Non-Modification Note
- only `PERF_0024`, `PERF_0052`, `PERF_0054`, and `PERF_0063` were targeted in this batch
- no speedup was run
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` files were changed
- no case files were modified
- no MySQL, Spark, or standalone SQLGlot routes were run
- taxonomy notes were untouched
