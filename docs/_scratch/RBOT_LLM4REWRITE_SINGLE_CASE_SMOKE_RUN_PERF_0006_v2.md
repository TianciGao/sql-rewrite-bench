# RBOT_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v2

## 0. Purpose And Boundary
This was a corrected bounded R-Bot / LLM4Rewrite smoke for `PERF_0006` only. A fresh run name was used to avoid the upstream log-exists short-circuit. It is not a leaderboard run, not full prior-method coverage, not registry writeback, and speedup was not run.

## 1. Fix Applied
- wrapper change: non-dry-run now uses a unique upstream run name instead of fixed `method_stdout`
- fresh run name: `rbot_perf_0006_1777982828529`
- upstream log path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/rbot_perf_0006_1777982828529.log`
- why this avoids the prior short-circuit:
  - upstream `test_utils.test()` returns immediately if `LOG_DIR/{name}.log` already exists
  - using a unique name ensures the upstream run does not no-op on a pre-existing fixed log file

## 2. Preconditions
- dry-run status: passed
- RAG index path: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- smoke venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- OpenAI/API visible: yes
- PG env visible: yes

## 3. Execution Summary
- method_command: `python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006 --fresh-run-name`
- generation_status: `method_execution_failed`
- output_sql_extracted: `false`
- generated_sql_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v2.sql`
- checker_candidate_sql_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/checker_candidate_sql_v2.sql`
- selected_rules_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/selected_rules_v2.json`
- retrieval_trace_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/retrieval_trace_v2.json`
- token_cost_log_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/token_cost_log_v2.json`
- stdout path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stdout_v2.log`
- stderr path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stderr_v2.log`
- failure_category: `subprocess_nonzero_exit`
- failure_summary: `smoke subprocess exited with code 1`

Observed execution evidence:
- upstream log shows a real chat-completion request
- upstream log shows real embedding requests
- early rewrite-stage logs include:
  - `Matched NL rewrite rules: [...]`
  - `Matched Calcite exploration rules: ['AGGREGATE_REDUCE_FUNCTIONS']`

Terminal failure in stderr:

```text
chromadb.errors.InvalidArgumentError: Collection expecting embedding with dimension of 3172, got 3139
```

## 4. Candidate SQL
No generated SQL file was captured in this rerun.

## 5. Checker / Consistency
- checker_status: `not_run`
- consistency_status: `not_checked`
- checker was not run because method execution failed before any candidate SQL was produced.

## 6. Speedup
- speedup_status: `not_run`

## 7. Claim Boundary
`bounded_1_case_RBot_LLM4Rewrite_generation_smoke_not_leaderboard`

This run is smoke evidence for corrected upstream invocation only. It is not checker-backed correctness evidence.

## 8. Remaining Blockers / Next Step
The fresh-name fix worked, but the new blocker is a retrieval/index runtime mismatch:
- existing Chroma collection expects embedding dimension `3172`
- live query embedding came back with dimension `3139`

Next step:
- diagnose and fix the exact Chroma/embedding dimension mismatch before another smoke attempt

## 9. Non-Modification Note
- only `PERF_0006` was targeted
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes occurred
- no speedup was run
- no MySQL, Spark, checker, or standalone SQLGlot routes were run
- taxonomy notes were untouched
