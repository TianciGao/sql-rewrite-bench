# LLMR2_SINGLE_CASE_RUNNER_DRY_RUN_PERF_0006_v1

## 0. Purpose And Boundary
This is a dry-run scaffold only for a future one-case LLM-R2 smoke on `PERF_0006`.

No LLM-R2 execution occurred. No OpenAI/API call occurred. No Java rule applier ran. No database, checker, or speedup step ran.

## 1. Inputs Checked
- case: `PERF_0006`
- adapter bundle: `/tmp/rewritebench_llmr2_adapter_preflight/PERF_0006`
- query CSV: `/tmp/rewritebench_llmr2_adapter_preflight/PERF_0006/perf_0006_queries.csv`
- schema stub: `/tmp/rewritebench_llmr2_adapter_preflight/PERF_0006/perf_0006_schema_stub.json`
- LLM-R2 repo: `/tmp/rewritebench_llmr2_audit/LLM-R2`
- main script: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/LLM_R2.py`
- rewriter script: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/rewriter.py`
- Java rule applier: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/rewriter_java.jar`
- demo pool: `/tmp/rewritebench_llmr2_audit/LLM-R2/data/data_llmr2/pools`
- rule library: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/rules_for_selected`
- checkpoint: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/simcse_models/tpch/pytorch_model.bin`
- OpenAI env visibility: `yes` for `OPENAI_API_KEY` visibility only; value not printed

## 2. Future Execution Artifact Plan
- result CSV: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/gpt_rewritebench_perf_0006_one_promo_plan_updated.csv`
- generated SQL: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/generated_sql_v1.sql`
- activated rules: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/activated_rules_v1.json`
- prompt trace: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/prompt_trace_v1.md`
- demo trace: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/demo_trace_v1.json`
- stdout: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/method_stdout_v1.log`
- stderr: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/method_stderr_v1.log`
- checker handoff SQL: `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/checker_candidate_sql_v1.sql`

## 3. Future Execution Command
NOT RUN

```bash
cd /tmp/rewritebench_llmr2_audit/LLM-R2/src
PYTHONPATH=. OPENAI_API_KEY=${OPENAI_API_KEY} python3 LLM_R2.py
```

This future command shape would call OpenAI/API through `src/LLM_R2.py`.

This future command shape would also invoke the Java rule applier through `src/rewriter.py` and `src/rewriter_java.jar`.

## 4. Dry-run Result
- `can_execute_smoke_next`: `true`
- `blockers`: none

## 5. Forbidden Claims
- no LLM-R2 result
- no generated SQL
- no checker-backed result
- no speedup
- no leaderboard claim

## 6. Recommended Next Step
- `execute 1-case LLM-R2 smoke`

## 7. Non-Modification Note
No execution, model/API call, Java rule-applier run, DB access, checker, or speedup occurred.

No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were modified.
