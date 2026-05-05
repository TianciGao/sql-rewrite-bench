# LLMR2_SINGLE_CASE_SMOKE_RUN_PERF_0006_v1

## 0. Purpose And Boundary
This was the first bounded LLM-R2 smoke attempt on `PERF_0006`.

Boundary:
- `PERF_0006` only
- OpenAI/API approved
- Java rule applier approved
- not leaderboard
- not full prior-method coverage
- not registry writeback
- checker not run
- speedup not run

## 1. Preconditions
- dry-run status: passed
- adapter bundle path: `/tmp/rewritebench_llmr2_adapter_preflight/PERF_0006`
- LLM-R2 repo path: `/tmp/rewritebench_llmr2_audit/LLM-R2`
- query CSV path: `/tmp/rewritebench_llmr2_adapter_preflight/PERF_0006/perf_0006_queries.csv`
- schema stub path: `/tmp/rewritebench_llmr2_adapter_preflight/PERF_0006/perf_0006_schema_stub.json`
- OpenAI/API visible: yes, env visibility only
- Java rule applier path: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/rewriter_java.jar`
- no DB, checker, or speedup was intended

## 2. Execution Summary
- method command:
  `python -m scripts.cli formal-llmr2-single-case-run --case PERF_0006`
- method_executed: yes
- openai_api_used: no observed prompt/API marker
- java_rule_applier_used: yes
- generation_status: `method_execution_failed`
- output_sql_extracted: no
- generated_sql_path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/generated_sql_v1.sql`
- checker_candidate_sql_path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/checker_candidate_sql_v1.sql`
- result_csv_path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv`
- activated_rules_path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/activated_rules_v1.json`
- prompt_trace_path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/prompt_trace_v1.md`
- demo_trace_path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/demo_trace_v1.json`
- token_cost_log_path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/token_cost_log_v1.json`
- stdout path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/method_stdout_v1.log`
- stderr path: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/method_stderr_v1.log`
- failure category: `runtime_timeout_before_prompt_api_phase`
- failure summary:
  in-sandbox run failed during Hugging Face model resolution; the external rerun loaded sentence-transformer weights and touched the Java rewriter import path, but did not reach a prompt/API marker or emit a result CSV within the bounded smoke window

## 3. Candidate SQL
No generated SQL was captured in this smoke attempt.

Observed stdout only showed the upstream `rewriter.py` import-time example SQL emission, not a bounded `PERF_0006` candidate artifact.

## 4. Checker / Consistency
- checker_status: `not_run`
- consistency_status: `not_checked`
- checker was intentionally not run in this step

## 5. Speedup
- speedup_status: `not_run`

## 6. Claim Boundary
`bounded_1_case_LLMR2_smoke_attempt_not_leaderboard`

## 7. Remaining Blockers / Next Step
- next step should be diagnose exact failure
- likely immediate blocker is upstream runtime initialization / preprocessing cost before prompt/API dispatch on the bounded one-case wrapper path

## 8. Non-Modification Note
Confirmed:
- only `PERF_0006` targeted
- no DB
- no checker
- no speedup
- no R-Bot
- no LearnedRewrite
- no MySQL, Spark, or standalone SQLGlot route
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes
- no case files changed
- taxonomy notes untouched
