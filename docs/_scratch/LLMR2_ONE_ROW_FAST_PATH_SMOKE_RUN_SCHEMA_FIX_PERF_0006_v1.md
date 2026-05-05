# LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_SCHEMA_FIX_PERF_0006_v1

## 0. Purpose And Boundary
This was a bounded one-row LLM-R2 fast-path schema-contract retry for `PERF_0006` only.

Boundary:
- CPU-only
- OpenAI/API approved
- Java rule applier approved
- not leaderboard
- not full prior-method coverage
- not registry writeback
- DB not run
- checker not run
- speedup not run

## 1. Prior Failure
The earlier CPU-only fast-path retry fixed the mixed CPU/CUDA tensor failure, then failed because upstream expected the schema JSON to be a list of table dicts while the staged RewriteBench schema was wrapped as an object with metadata fields.

## 2. Schema-contract Patch
- staged schema path:
  `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.json`
- backup path:
  `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.schema_stub_before_schema_list_contract.json`
- converted schema shape:
  JSON list of table dicts
- table count: `1`
- column count: `7`
- `schema_list_contract`: `true`
- only temp runtime root modified: yes

The staged schema is now a bare list like:
```json
[
  {
    "table": "lineitem",
    "rows": "unknown",
    "columns": [...]
  }
]
```

## 3. Execution Summary
Method command:
```bash
python -m scripts.cli formal-llmr2-one-row-fast-path --case PERF_0006 --force-cpu --schema-list-contract
```

Result:
- `method_executed`: `true`
- `fast_path_runtime_used`: `true`
- `one_row_query_used`: `true`
- `tiny_demo_pools_used`: `true`
- `force_cpu`: `true`
- `openai_api_used`: `false`
- `java_rule_applier_used`: `true`
- `generation_status`: `method_execution_failed`
- `output_sql_extracted`: `false`
- generated SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_schema_fix_v1.sql`
- checker candidate SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_candidate_sql_schema_fix_v1.sql`
- result CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv`
- activated rules path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/activated_rules_schema_fix_v1.json`
- prompt trace path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/prompt_trace_schema_fix_v1.md`
- demo trace path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/demo_trace_schema_fix_v1.json`
- token/cost log path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/token_cost_log_schema_fix_v1.json`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stdout_schema_fix_v1.log`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stderr_schema_fix_v1.log`
- failure category: `subprocess_nonzero_exit`
- failure summary: `LLM-R2 subprocess exited with code 1`

Narrowed failure from stderr:
- schema iteration now succeeded
- CPU-only preprocessing again succeeded far enough to print:
  - `preprocess time: ...`
  - `query pool embeddings collected`
- the next failure happened during target-query logical-plan extraction:
  - `IndexError: list index out of range`
- failing stack:
  - `logical_plan = get_logical_plan(db_id, edit_queries(query))`
  - `create_nested_tree(...)`

Interpretation:
- the schema contract mismatch was resolved
- the next blocker is upstream logical-plan extraction on the bounded `PERF_0006` target query
- prompt/API dispatch still was not reached

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
- `bounded_1_case_LLMR2_schema_fix_fast_path_smoke_attempt_not_leaderboard`

## 8. Remaining Blockers / Next Step
Next step:
- diagnose exact logical-plan extraction failure for `PERF_0006`

More specifically:
- bounded one-row query staging works
- tiny pool staging works
- CPU-only execution works past the prior device mismatch
- schema list contract works
- remaining blocker is upstream `get_logical_plan` / `create_nested_tree` handling for the target query before any prompt/API call

## 9. Non-Modification Note
Only `PERF_0006` was targeted.

No DB, checker, or speedup ran. No R-Bot or LearnedRewrite ran. No MySQL, Spark, or standalone SQLGlot routes were run. No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were changed. The taxonomy notes were untouched.
