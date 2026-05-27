# LLMR2_ONE_ROW_FAST_PATH_DRY_RUN_PERF_0006_v1

## 0. Purpose And Boundary
This is a dry-run only scaffold for a bounded one-row LLM-R2 fast path on `PERF_0006`. No LLM-R2 execution, no OpenAI/API call, no Java rule applier run, no DB access, no checker, and no speedup occurred.

## 1. Prior Failure
The previous bounded `PERF_0006` smoke reached upstream preprocessing but did not reach the first prompt/API dispatch. The runtime failure audit concluded that the adapter one-row query CSV was used, but `LLM_R2.py` still loaded full positive/negative pools and ran heavy `queryCL` preprocessing first. This dry-run addresses that contract gap by staging a bounded runtime root with exact upstream-like one-row and tiny-pool paths.

## 2. Runtime Staging
Runtime root:
- `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/`

Staged upstream-like paths:
- one-row query CSV: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/queries/queries_rewritebench_perf_0006_test.csv`
- schema JSON: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.json`
- tiny positive pool: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/pos_pool_rewritebench_perf_0006_updated.csv`
- tiny negative pool: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/neg_pool_rewritebench_perf_0006_updated.csv`

Staging result:
- runtime root created: yes
- query CSV contains exactly one `PERF_0006` row: yes
- positive pool reduced to at most one demo row: yes
- negative pool reduced to at most one demo row: yes
- schema stub staged: yes
- staged names match upstream naming conventions: yes

## 3. Fast-path Contract
The bounded fast path avoids full-pool preprocessing by staging dataset-specific tiny pool files under the exact `data/data_llmr2/pools/*rewritebench_perf_0006_updated.csv` names that the future bounded execution path is expected to consume.

Future command:
```bash
cd /tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/src
PYTHONPATH=. OPENAI_API_KEY=${OPENAI_API_KEY} python3 LLM_R2.py
```

NOT RUN.

Future artifact paths:
- result CSV: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv`
- generated SQL: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_v1.sql`
- activated rules: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/activated_rules_v1.json`
- prompt trace: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/prompt_trace_v1.md`
- demo trace: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/demo_trace_v1.json`
- token/cost log: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/token_cost_log_v1.json`
- stdout: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stdout_v1.log`
- stderr: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stderr_v1.log`
- checker candidate SQL: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_candidate_sql_v1.sql`

Prompt/API requirement:
- `OPENAI_API_KEY` visibility confirmed: yes

Java rule applier requirement:
- `src/rewriter_java.jar` visibility confirmed: yes

## 4. Dry-run Result
- `can_execute_fast_path_next`: `true`
- blockers: none

Classification shift:
- from `adapter input used but upstream preprocessing unbounded`
- to `bounded_one_row_fast_path_dry_run_ready_not_executed`

## 5. Forbidden Claims
No LLM-R2 execution occurred. No generated SQL exists. No checker-backed result exists. No speedup result exists. This is not leaderboard evidence.

## 6. Recommended Next Step
- `execute bounded one-row LLM-R2 fast-path smoke`

## 7. Non-Modification Note
No execution, model/API call, Java rule applier run, DB access, checker, or speedup occurred. No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were changed. The taxonomy notes were untouched.
