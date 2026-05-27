# RBOT_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v1

## 0. Purpose And Boundary
This was the first bounded R-Bot / LLM4Rewrite smoke for `PERF_0006` only. It is not a leaderboard run, not full prior-method coverage, not registry writeback, and speedup was not run.

## 1. Preconditions
- dry-run status: passed
- RAG index path: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- smoke venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- OpenAI/API visible: yes
- PG env visible: yes

## 2. Execution Summary
- method_command: `python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006`
- generation_status: `generation_success`
- output_sql_extracted: `false`
- generated_sql_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql.sql`
- selected_rules_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/selected_rules.json`
- retrieval_trace_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/retrieval_trace.json`
- token_cost_log_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/token_cost_log.json`
- stdout path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stdout.log`
- stderr path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stderr.log`
- failure_category: `output_sql_missing`
- failure_summary: `method finished without extractable output_sql`

## 3. Candidate SQL
No generated SQL file was captured. The method log only showed early-generation evidence:

```text
14:43:41,304 root INFO Input Cost: 36.37
14:43:41,551 root INFO Matched NL rewrite rules: ['can_be_optimized_by_function', 'can_be_optimized_by_constant_folding', 'can_be_optimized_by_out_of_range']
```

## 4. Checker / Consistency
- checker_status: `not_run`
- consistency_status: `not_checked`
- checker_result_path: none
- checker was not run because no candidate SQL was extracted for handoff.

## 5. Speedup
- speedup_status: `not_run`

## 6. Claim Boundary
`bounded_1_case_RBot_LLM4Rewrite_generation_smoke_not_leaderboard`

This is generation smoke evidence only, not correctness evidence.

## 7. Remaining Blockers / Next Step
The immediate blocker is `output_sql_missing`. The next step is to fix the exact upstream/output-capture failure category so the smoke can emit candidate SQL and then proceed to PG checker only after SQL capture succeeds.

## 8. Non-Modification Note
- only `PERF_0006` was targeted
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes occurred
- no speedup was run
- no MySQL, Spark, or standalone SQLGlot routes were run
- taxonomy notes were untouched
