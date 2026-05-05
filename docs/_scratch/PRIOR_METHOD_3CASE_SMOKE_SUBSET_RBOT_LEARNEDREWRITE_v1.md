# PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1

## 0. Purpose And Boundary
This note records a bounded 3-case prior-method smoke subset for `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite` on `PERF_0006`, `PERF_0008`, and `PERF_0033`. It is not leaderboard evidence, not full prior-method coverage, not speedup evaluation, and not registry writeback.

## 1. Cases And Methods
Methods:
- `R-Bot / LLM4Rewrite`
- `LearnedRewrite / embedded LLM4Rewrite`

Cases:
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`

## 2. Per-case Result Table
| method | case_id | candidate_generated | candidate_executed | checker_status | consistency_status | candidate_type | failure_category | failure_summary | speedup_status | artifact_paths | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | `PERF_0006` | yes | yes | inconsistent | inconsistent | nontrivial_rewrite_candidate | result_mismatch_numeric_avg_precision | generated SQL changed `avg_disc` semantics (`0.075...` vs `0.08`) | not_run | `docs/_scratch/RBOT_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v3.md`; `docs/_scratch/RBOT_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md` | `checker_smoke_failed_not_speedup` |
| `R-Bot / LLM4Rewrite` | `PERF_0008` | yes | yes | consistent | consistent | nontrivial_rewrite_candidate | none | none | not_run | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0008/smoke_result_v3.json`; `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0008/checker_result_v1.json` | `bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard` |
| `R-Bot / LLM4Rewrite` | `PERF_0033` | no | no | not_run | not_checked | not_applicable | subprocess_nonzero_exit | upstream `gen_sql_templates.py` failed with `AttributeError` after retrieval/model activity | not_run | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0033/smoke_result_v3.json` | `bounded_1_case_RBot_LLM4Rewrite_smoke_attempt_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0006` | yes | yes | consistent | consistent | source_echo_or_noop_candidate | none | none | not_run | `docs/_scratch/LEARNEDREWRITE_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v1.md`; `docs/_scratch/LEARNEDREWRITE_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md` | `checker_smoke_source_like_noop_not_speedup` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0008` | yes | yes | consistent | consistent | source_echo_or_noop_candidate | none | none | not_run | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0008/smoke_result_v1.json`; `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0008/checker_result_v1.json` | `checker_smoke_source_like_noop_not_speedup` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0033` | yes | yes | consistent | consistent | nontrivial_rewrite_candidate | none | none | not_run | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0033/smoke_result_v1.json`; `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0033/checker_result_v1.json` | `bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard` |

## 3. Method-level Bounded Metrics
| method | denominator | candidate_generation_count | candidate_generation_rate@3 | candidate_execution_count | executable_rate@3 | checker_consistent_count | result_consistency_rate@3 | checker_failed_count | source_like_or_noop_count | speedup_status | speedup_comparable_count | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | 3 | 2 | 2/3 | 2 | 2/3 | 1 | 1/3 | 1 | 0 | not_run | 1 | `bounded_3case_prior_method_smoke_subset_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | 3 | 3 | 3/3 | 3 | 3/3 | 3 | 3/3 | 0 | 2 | not_run | 1 | `bounded_3case_prior_method_smoke_subset_not_leaderboard` |

## 4. Correctness-gated Interpretation
`R-Bot / LLM4Rewrite` is speedup-comparable only on checker-consistent candidates. Within this bounded denominator, that condition is met only on `PERF_0008`.

`LearnedRewrite / embedded LLM4Rewrite` is checker-consistent on all three cases, but two of the three checker-consistent candidates are source-like / no-op outputs. Those two cases should not be treated as evidence of useful rewrite improvement. Only `PERF_0033` is a checker-consistent non-no-op candidate in this bounded subset.

This remains smoke-subset evidence rather than final prior-method ranking or leaderboard evidence.

## 5. Failure / Behavior Analysis
`R-Bot / LLM4Rewrite` shows three distinct behaviors across the shared denominator:
- `PERF_0006`: candidate generated and executed, but checker failed due to numeric average / decimal semantic drift.
- `PERF_0008`: nontrivial candidate generated, executed, and passed the PostgreSQL checker.
- `PERF_0033`: retrieval/model path was reached, but candidate generation failed before `output_sql` capture due to an upstream template-generation exception.

`LearnedRewrite / embedded LLM4Rewrite` shows two behavior modes:
- `PERF_0006` and `PERF_0008`: checker-consistent source-like / no-op outputs with empty `used_rules` and `output_cost = -1`.
- `PERF_0033`: checker-consistent nontrivial rewrite with non-empty `used_rules` and changed cost output.

These outcomes separate three different failure/behavior patterns that RewriteBench keeps distinct:
- nontrivial but checker-inconsistent generation
- source-like / no-op but checker-consistent generation
- generation-path failure before `output_sql`

## 6. Paper-facing Wording
“This bounded 3-case smoke subset is not a leaderboard. It shows whether external prior-method substrates can generate candidate SQL, execute, and pass RewriteBench’s checker on a small shared denominator. R-Bot and LearnedRewrite are compared under correctness gating; speedup is not computed.”

“Within this subset, R-Bot produced one checker-consistent nontrivial candidate, one checker-inconsistent candidate, and one generation-path failure. LearnedRewrite produced three checker-consistent candidates, but two were source-like / no-op outputs rather than useful rewrite improvements.”

## 7. Recommended Next Step
Expand to additional cases only after reviewing the 3-case results.

## 8. Non-Modification Note
Only `PERF_0006`, `PERF_0008`, and `PERF_0033` were targeted. No speedup was run. No registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made. No case files were modified. No MySQL, Spark, or standalone SQLGlot routes were run. The long-standing taxonomy notes were untouched.
