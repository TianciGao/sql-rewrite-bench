# PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1

## 0. Purpose And Boundary
This is a bounded 10-case subset Batch A execution note for `PERF_0013`, `PERF_0017`, and `PERF_0019`, covering `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite`. It is not leaderboard evidence, not full prior-method coverage, runs no speedup, and does not perform registry writeback.

## 1. Batch A Cases
- `PERF_0013`: selected from the 10-case preflight as a stable PG-backed TPC-H aggregate/join case with existing control evidence and a date-range filter.
- `PERF_0017`: selected as another stable TPC-H aggregate/join case with explicit date filtering and `LIMIT`, useful for contrasting nontrivial rewrite vs source-like behavior.
- `PERF_0019`: selected for behavior diversity because it uses a nested aggregate over a `LEFT OUTER JOIN` with a filtered join-side predicate, which is a meaningful stress point for both prior baselines.

## 2. Per-case Result Table
| method | case_id | candidate_generated | candidate_executed | checker_status | consistency_status | candidate_type | failure_category | failure_summary | speedup_status | artifact_paths | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-Bot / LLM4Rewrite | PERF_0013 | yes | yes | consistent | consistent | nontrivial_rewrite_candidate | none | none | not_run | smoke `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0013/smoke_result_v3.json`; checker `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0013/checker_result_v1.json` | bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard |
| LearnedRewrite / embedded LLM4Rewrite | PERF_0013 | yes | yes | consistent | consistent | source_echo_or_noop_candidate | none | none | not_run | smoke `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0013/smoke_result_v1.json`; checker `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0013/checker_result_v1.json` | bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard |
| R-Bot / LLM4Rewrite | PERF_0017 | yes | yes | consistent | consistent | nontrivial_rewrite_candidate | none | none | not_run | smoke `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0017/smoke_result_v3.json`; checker `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0017/checker_result_v1.json` | bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard |
| LearnedRewrite / embedded LLM4Rewrite | PERF_0017 | yes | yes | consistent | consistent | source_echo_or_noop_candidate | none | none | not_run | smoke `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0017/smoke_result_v1.json`; checker `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0017/checker_result_v1.json` | bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard |
| R-Bot / LLM4Rewrite | PERF_0019 | no | no | not_run | not_checked | not_available | sql_template_generation_attribute_error | `gen_sql_templates.py` hit `AttributeError: 'NoneType' object has no attribute 'find_all'` | not_run | smoke `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0019/smoke_result_v3.json` | bounded_1_case_RBot_LLM4Rewrite_smoke_attempt_not_leaderboard |
| LearnedRewrite / embedded LLM4Rewrite | PERF_0019 | yes | yes | consistent | consistent | source_echo_or_noop_candidate | none | none | not_run | smoke `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0019/smoke_result_v1.json`; checker `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0019/checker_result_v1.json` | bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard |

## 3. Batch A Method Metrics
| method | denominator | candidate_generation_count | candidate_generation_rate@3 | candidate_execution_count | executable_rate@3 | checker_consistent_count | result_consistency_rate@3 | checker_failed_count | source_like_or_noop_count | speedup_status | speedup_comparable_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-Bot / LLM4Rewrite | 3 | 2 | 2/3 | 2 | 2/3 | 2 | 2/3 | 0 | 0 | not_run | 2 |
| LearnedRewrite / embedded LLM4Rewrite | 3 | 3 | 3/3 | 3 | 3/3 | 3 | 3/3 | 0 | 3 | not_run | 0 |

## 4. Contribution To 10-case Subset
Batch A adds new evidence for three not-yet-run cases without recomputing the full bounded-10 denominator. Later rollup work can merge:
- existing executed subset: `PERF_0006`, `PERF_0008`, `PERF_0033`
- Batch A: `PERF_0013`, `PERF_0017`, `PERF_0019`
- future remaining proposed cases: `PERF_0024`, `PERF_0052`, `PERF_0054`, `PERF_0063`

## 5. Failure / Behavior Analysis
- `R-Bot / LLM4Rewrite` showed two nontrivial, checker-consistent candidate generations on `PERF_0013` and `PERF_0017`. The generated SQL was structurally rewritten rather than source-like.
- `R-Bot / LLM4Rewrite` failed on `PERF_0019` before output SQL capture. The method reached model-backed retrieval and rule matching, then died in SQL template generation with `AttributeError: 'NoneType' object has no attribute 'find_all'`.
- `LearnedRewrite / embedded LLM4Rewrite` generated executable, checker-consistent output on all three Batch A cases.
- The LearnedRewrite outputs remained source-like / no-op on all three Batch A cases. The emitted `res.jsonl` records had `used_rules: []` and `output_cost: -1`, so these are correctness-preserving smoke artifacts rather than evidence of useful rewrite improvement.

## 6. Recommended Next Step
execute Batch B

## 7. Non-Modification Note
Only `PERF_0013`, `PERF_0017`, and `PERF_0019` were targeted in this batch. No speedup was run. No registry, review, rules, case package, or `docs/EXECUTION_STATUS.md` changes were made. No MySQL, Spark, or standalone SQLGlot routes were used. The long-standing taxonomy notes were untouched.
