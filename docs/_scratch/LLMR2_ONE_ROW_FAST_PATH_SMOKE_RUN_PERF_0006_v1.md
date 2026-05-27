# LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_PERF_0006_v1

## 0. Purpose And Boundary
This was the first bounded one-row LLM-R2 fast-path smoke for `PERF_0006` only.

Boundary:
- OpenAI/API use was approved
- Java rule applier use was approved
- not leaderboard evidence
- not full prior-method coverage
- not registry writeback
- DB not run
- checker not run
- speedup not run

## 1. Preconditions
- dry-run status: passed
- runtime root path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/`
- one-row query CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/queries/queries_rewritebench_perf_0006_test.csv`
- tiny positive pool path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/pos_pool_rewritebench_perf_0006_updated.csv`
- tiny negative pool path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/neg_pool_rewritebench_perf_0006_updated.csv`
- schema stub path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.json`
- OpenAI/API visible, no secret: yes
- Java rule applier path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/src/rewriter_java.jar`
- no DB/checker/speedup intended: yes

## 2. Execution Summary
Method command:
```bash
python -m scripts.cli formal-llmr2-one-row-fast-path --case PERF_0006
```

Result:
- `method_executed`: `true`
- `fast_path_runtime_used`: `true`
- `one_row_query_used`: `true`
- `tiny_demo_pools_used`: `true`
- `openai_api_used`: `false`
- `java_rule_applier_used`: `true`
- `generation_status`: `method_execution_failed`
- `output_sql_extracted`: `false`
- generated SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_v1.sql`
- checker candidate SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_candidate_sql_v1.sql`
- result CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv`
- activated rules path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/activated_rules_v1.json`
- prompt trace path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/prompt_trace_v1.md`
- demo trace path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/demo_trace_v1.json`
- token/cost log path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/token_cost_log_v1.json`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stdout_v1.log`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stderr_v1.log`
- failure category: `subprocess_nonzero_exit`
- failure summary: `LLM-R2 subprocess exited with code 1`

Observed root cause from stderr:
- the bounded fast path got past the earlier full-pool staging problem
- Hugging Face model weights loaded successfully on the external rerun
- the run then failed in `queryCL` pool embedding before prompt/API dispatch
- exact narrowed failure:
  `RuntimeError: Expected all tensors to be on the same device, but got mat2 is on cuda:0, different from other tensors on cpu`

## 3. Candidate SQL
No generated SQL was produced.

The stdout artifact still contains upstream `rewriter.py` import-time example SQL emission. That is not a `PERF_0006` candidate artifact and should not be treated as output SQL.

## 4. Checker / Consistency
- `checker_status`: `not_run`
- `consistency_status`: `not_checked`
- checker intentionally not run in this step

## 5. Speedup
- `speedup_status`: `not_run`

## 6. Claim Boundary
- `bounded_1_case_LLMR2_fast_path_smoke_attempt_not_leaderboard`

## 7. Remaining Blockers / Next Step
Next step:
- diagnose the exact `queryCL` device-placement failure before retrying execution

More concretely:
- the bounded one-row fast-path contract worked
- but upstream `SentenceTransformer` / `QueryformerForCL` preprocessing still fails before prompt/API dispatch because tensors land on mixed CPU / CUDA devices

## 8. Non-Modification Note
Only `PERF_0006` was targeted.

No DB, checker, or speedup ran. No R-Bot or LearnedRewrite ran. No MySQL, Spark, or standalone SQLGlot routes were run. No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were changed. The taxonomy notes were untouched.
