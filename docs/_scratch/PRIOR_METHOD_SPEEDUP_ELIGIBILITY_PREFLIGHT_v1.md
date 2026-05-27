# PRIOR_METHOD_SPEEDUP_ELIGIBILITY_PREFLIGHT_v1

## 0. Purpose And Boundary
State:
- speedup eligibility preflight only
- no speedup run
- no SQL execution
- no model/API
- PG-only future slice
- correctness-gated

## 1. Source Evidence
Source reports used:
- `R-Bot / LearnedRewrite @10` rollup: [docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md)
- cross-method evidence summary: [docs/_scratch/PRIOR_METHOD_EVIDENCE_SUMMARY_RBOT_LEARNEDREWRITE_LLMR2_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_EVIDENCE_SUMMARY_RBOT_LEARNEDREWRITE_LLMR2_v1.md)
- `LLM-R2 @10` rollup: [docs/_scratch/LLMR2_10CASE_SMOKE_ROLLUP_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_10CASE_SMOKE_ROLLUP_v1.md)
- case-level checker notes for anchor and batch interpretation where needed:
  - [docs/_scratch/RBOT_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/RBOT_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md)
  - [docs/_scratch/LEARNEDREWRITE_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LEARNEDREWRITE_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md)
  - [docs/_scratch/LLMR2_CHECKER_HANDOFF_PERF_0006_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_CHECKER_HANDOFF_PERF_0006_v1.md)
  - [docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_A_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_A_v1.md)
  - [docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_B_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_B_v1.md)
  - [docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_C_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_C_v1.md)

Static artifact inspection was also used for:
- `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/*`
- `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/*`
- `/tmp/rewritebench_llmr2_fast_path/*`

## 2. Eligibility Rules
A method-case candidate is eligible for future PG-only speedup only if:
1. `candidate_generated = yes`
2. `candidate_executed = yes`
3. `checker_status = consistent`
4. `consistency_status = consistent`
5. candidate SQL path exists and is non-empty
6. `candidate_type` is not `source_echo_or_noop_candidate`
7. candidate is not classified as source-like/no-op
8. no unresolved extraction artifact remains
9. source SQL path exists
10. future PG speedup command can be defined

## 3. Method-level Eligibility Summary
| method | denominator | checker_consistent_count | non_noop_checker_consistent_count | eligible_for_pg_speedup_count | excluded_count | main_exclusion_reasons | speedup_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | `10` | `7` | `7` | `7` | `3` | `checker_inconsistent_candidate`; `generation_or_path_failure` | `not_run` |
| `LearnedRewrite / embedded LLM4Rewrite` | `10` | `10` | `2` | `2` | `8` | `source_like_or_noop_candidate` | `not_run` |
| `LLM-R2` | `10` | `9` | `9` | `9` | `1` | `logical_plan_failure_before_generation` | `not_run` |

The expected high-level counts and the static artifact check agree:
- `R-Bot / LLM4Rewrite`: `7` eligible
- `LearnedRewrite / embedded LLM4Rewrite`: `2` eligible
- `LLM-R2`: `9` eligible
- missing artifact count among expected eligible candidates: `0`

## 4. Eligible Candidate Table
| method | case_id | candidate_sql_path | source_sql_path | checker_evidence_path | candidate_type | extraction_version | eligibility_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | `PERF_0008` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0008/generated_sql_v3.sql` | `cases/PERF/PERF_0008/source.sql` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0008/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `R-Bot / LLM4Rewrite` | `PERF_0013` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0013/generated_sql_v3.sql` | `cases/PERF/PERF_0013/source.sql` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0013/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `R-Bot / LLM4Rewrite` | `PERF_0017` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0017/generated_sql_v3.sql` | `cases/PERF/PERF_0017/source.sql` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0017/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `R-Bot / LLM4Rewrite` | `PERF_0024` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0024/generated_sql_v3.sql` | `cases/PERF/PERF_0024/source.sql` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0024/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `R-Bot / LLM4Rewrite` | `PERF_0052` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0052/generated_sql_v3.sql` | `cases/PERF/PERF_0052/source.sql` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0052/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `R-Bot / LLM4Rewrite` | `PERF_0054` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0054/generated_sql_v3.sql` | `cases/PERF/PERF_0054/source.sql` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0054/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `R-Bot / LLM4Rewrite` | `PERF_0063` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0063/generated_sql_v3.sql` | `cases/PERF/PERF_0063/source.sql` | `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0063/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0033` | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0033/generated_sql_v1.sql` | `cases/PERF/PERF_0033/source.sql` | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0033/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0054` | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0054/generated_sql_v1.sql` | `cases/PERF/PERF_0054/source.sql` | `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0054/checker_result_v1.json` | `nontrivial_rewrite_candidate` | `not_applicable` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LLM-R2` | `PERF_0006` | `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0006/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_result_v1.json` | `clean_extracted_candidate` | `v1` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LLM-R2` | `PERF_0008` | `/tmp/rewritebench_llmr2_fast_path/PERF_0008/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0008/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0008/checker_result_v1.json` | `clean_extracted_candidate` | `v1` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LLM-R2` | `PERF_0013` | `/tmp/rewritebench_llmr2_fast_path/PERF_0013/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0013/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0013/checker_result_v1.json` | `clean_extracted_candidate` | `v1` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LLM-R2` | `PERF_0017` | `/tmp/rewritebench_llmr2_fast_path/PERF_0017/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0017/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0017/checker_result_v1.json` | `clean_extracted_candidate` | `v1` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LLM-R2` | `PERF_0019` | `/tmp/rewritebench_llmr2_fast_path/PERF_0019/generated_sql_schema_native_clean_v2.sql` | `cases/PERF/PERF_0019/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0019/checker_result_v1.json` | `clean_extracted_candidate` | `v2` | `eligible_for_pg_speedup` | original extraction artifact resolved; use clean `v2` candidate |
| `LLM-R2` | `PERF_0024` | `/tmp/rewritebench_llmr2_fast_path/PERF_0024/generated_sql_schema_native_clean_v2.sql` | `cases/PERF/PERF_0024/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0024/checker_result_v1.json` | `clean_extracted_candidate` | `v2` | `eligible_for_pg_speedup` | original extraction artifact resolved; use clean `v2` candidate |
| `LLM-R2` | `PERF_0033` | `/tmp/rewritebench_llmr2_fast_path/PERF_0033/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0033/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0033/checker_result_v1.json` | `clean_extracted_candidate` | `v1` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |
| `LLM-R2` | `PERF_0052` | `/tmp/rewritebench_llmr2_fast_path/PERF_0052/generated_sql_schema_native_clean_v2.sql` | `cases/PERF/PERF_0052/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0052/checker_result_v1.json` | `clean_extracted_candidate` | `v2` | `eligible_for_pg_speedup` | nested-query extraction cleanup resolved; use clean `v2` candidate |
| `LLM-R2` | `PERF_0054` | `/tmp/rewritebench_llmr2_fast_path/PERF_0054/generated_sql_schema_native_clean_v1.sql` | `cases/PERF/PERF_0054/source.sql` | `/tmp/rewritebench_llmr2_fast_path/PERF_0054/checker_result_v1.json` | `clean_extracted_candidate` | `v1` | `eligible_for_pg_speedup` | static artifact checks passed; future PG speedup command shape exists |

## 5. Exclusion Table
| method | case_id | exclusion_reason | evidence_source | notes |
| --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | `PERF_0006` | `checker_inconsistent_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | semantic checker failure excludes future speedup |
| `R-Bot / LLM4Rewrite` | `PERF_0019` | `generation_or_path_failure` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | no candidate generation artifact |
| `R-Bot / LLM4Rewrite` | `PERF_0033` | `generation_or_path_failure` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | no candidate generation artifact |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0006` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0008` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0013` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0017` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0019` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0024` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0052` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0063` | `source_like_or_noop_candidate` | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1.md` | checker-consistent but excluded from primary speedup |
| `LLM-R2` | `PERF_0063` | `logical_plan_failure_before_generation` | `docs/_scratch/LLMR2_10CASE_SMOKE_ROLLUP_v1.md` | no candidate generation, no clean SQL artifact |

## 6. Future Speedup Slice Contract
Define:
- PG-only
- correctness-gated
- source runtime baseline required
- candidate runtime required
- repeated runs policy: propose `5` repeats unless existing project policy says otherwise
- timeout policy: use existing PG baseline timeout if defined; otherwise pin it before execution
- output metrics:
  - `gm_speedup`
  - `win/tie/loss`
  - `regression_rate@20`
  - per-method eligible denominator
- no cross-engine transfer in this step

SQLSolver / VeriEQL remain entirely out of scope for this slice.

## 7. Recommended Next Step
- `run PG-only speedup for eligible candidates`

Reason:
- the eligibility list is correctness-gated from existing checker-backed evidence
- all expected eligible candidates have non-empty clean SQL artifacts plus future command stubs
- no missing artifact blocker remains in this preflight

## 8. Non-Modification Note
Confirm:
- no baseline rerun
- no model/API
- no DB
- no checker
- no speedup
- no registry/review/rules/EXECUTION_STATUS/case changes
