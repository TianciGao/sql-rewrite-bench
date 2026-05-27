# RBOT_LLM4REWRITE_SINGLE_CASE_RUNNER_DRY_RUN_v1

## 0. Purpose And Boundary

This note records a dry-run scaffold only for the future `R-Bot` / `LLM4Rewrite` single-case smoke on `PERF_0006`. It is not method execution, not model execution, not DB execution, not checker execution, and not speedup evaluation.

## 1. Inputs Checked

- case: `PERF_0006`
- source SQL: found
- PG schema: found
- harness bundle: found at `/tmp/rewritebench_rbot_llm4rewrite_single_case_smoke/PERF_0006`
- RAG index: found at `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- smoke venv: found at `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- upstream clone: found at `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- env vars:
  - `OPENAI_API_KEY`: visible
  - `PGHOST`: visible
  - `PGPORT`: visible
  - `PGDATABASE`: visible
  - `PGUSER`: visible
  - `PGPASSWORD`: visible

## 2. Future Execution Artifact Plan

- `generated_sql_path`: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql.sql`
- `selected_rules_path`: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/selected_rules.json`
- `retrieval_trace_path`: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/retrieval_trace.json`
- `token_cost_log_path`: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/token_cost_log.json`
- `method_stdout_path`: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stdout.log`
- `method_stderr_path`: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stderr.log`
- `checker_candidate_sql_path`: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/checker_candidate_sql.sql`

## 3. Dry-run Result

- `can_execute_smoke_next`: `yes`
- blockers: none

The runner scaffold is now dry-run ready and not executed.

## 4. Future Execution Command

`NOT RUN`

```bash
python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run \
  --case PERF_0006
```

## 5. Forbidden Claims

- no R-Bot result
- no checker-backed result
- no speedup result
- no leaderboard evidence

## 6. Recommended Next Step

`execute_1-case_R-Bot_smoke`

## 7. Non-Modification Note

This step performed no R-Bot execution, no model call, no DB execution, no checker execution, no speedup evaluation, and no SQLGlot route execution. No case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md` were changed. The taxonomy notes were untouched.
