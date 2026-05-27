# LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_CPU_PERF_0006_v1

## 0. Purpose And Boundary
This was a bounded one-row LLM-R2 fast-path CPU-only retry for `PERF_0006` only.

Boundary:
- OpenAI/API use was approved
- Java rule applier use was approved
- not leaderboard
- not full prior-method coverage
- not registry writeback
- DB not run
- checker not run
- speedup not run

## 1. Prior Failure
The prior bounded fast-path smoke proved that the staged one-row query and tiny demo pools were used, but it failed in `queryCL` pool embedding before prompt/API dispatch with a CPU/CUDA tensor device mismatch.

This CPU-only retry forced:
- `force_cpu = true`
- `CUDA_VISIBLE_DEVICES=""`

That removed the earlier mixed-device failure.

## 2. CPU-only Retry Configuration
- `force_cpu`: `true`
- `CUDA_VISIBLE_DEVICES`: `""`
- runtime root: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/`
- one-row query CSV: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/queries/queries_rewritebench_perf_0006_test.csv`
- tiny positive pool: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/pos_pool_rewritebench_perf_0006_updated.csv`
- tiny negative pool: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/neg_pool_rewritebench_perf_0006_updated.csv`
- OpenAI/API visible, no secret: yes
- Java rule applier path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/src/rewriter_java.jar`

## 3. Execution Summary
Method command:
```bash
python -m scripts.cli formal-llmr2-one-row-fast-path --case PERF_0006 --force-cpu
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
- generated SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_cpu_v1.sql`
- checker candidate SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_candidate_sql_cpu_v1.sql`
- result CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv`
- activated rules path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/activated_rules_cpu_v1.json`
- prompt trace path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/prompt_trace_cpu_v1.md`
- demo trace path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/demo_trace_cpu_v1.json`
- token/cost log path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/token_cost_log_cpu_v1.json`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stdout_cpu_v1.log`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stderr_cpu_v1.log`
- failure category: `subprocess_nonzero_exit`
- failure summary: `LLM-R2 subprocess exited with code 1`

Narrowed failure from stderr:
- CPU-only preprocessing succeeded far enough to print:
  - `preprocess time: ...`
  - `query pool embeddings collected`
- the next failure happened when upstream iterated the staged schema JSON:
  - `TypeError: string indices must be integers, not 'str'`
- failing line:
  - `if tab['table'] in q_names ...`

Interpretation:
- the CPU/CUDA device mismatch was resolved by the CPU-only retry
- the next blocker is a schema contract mismatch
- upstream expects the loaded schema file to be a list of table objects
- the current RewriteBench adapter stub is wrapped as an object with metadata fields, so iteration yields string keys instead of table dicts

## 4. Candidate SQL
No generated SQL was produced.

The stdout artifact still contains upstream `rewriter.py` import-time example SQL emission. That is not a `PERF_0006` candidate artifact and should not be treated as output SQL.

## 5. Checker / Consistency
- `checker_status`: `not_run`
- `consistency_status`: `not_checked`
- checker intentionally not run in this step

## 6. Speedup
- `speedup_status`: `not_run`

## 7. Claim Boundary
- `bounded_1_case_LLMR2_cpu_fast_path_smoke_attempt_not_leaderboard`

## 8. Remaining Blockers / Next Step
Next step:
- diagnose and patch the bounded schema staging contract for LLM-R2

More specifically:
- keep the bounded one-row query and tiny-pool fast path
- rewrite the staged schema JSON into the upstream list-of-table-dicts shape that `LLM_R2.py` expects
- retry only after that contract is corrected

## 9. Non-Modification Note
Only `PERF_0006` was targeted.

No DB, checker, or speedup ran. No R-Bot or LearnedRewrite ran. No MySQL, Spark, or standalone SQLGlot routes were run. No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were changed. The taxonomy notes were untouched.
