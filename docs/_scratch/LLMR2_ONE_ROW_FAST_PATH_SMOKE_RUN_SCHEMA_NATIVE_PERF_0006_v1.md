# LLMR2_ONE_ROW_FAST_PATH_SMOKE_RUN_SCHEMA_NATIVE_PERF_0006_v1

## 0. Purpose And Boundary
State:
- bounded one-row LLM-R2 fast-path schema-native retry
- PERF_0006 only
- CPU-only
- OpenAI/API approved
- Java rule applier approved
- not leaderboard
- not full prior-method coverage
- not registry writeback
- DB not run
- checker not run
- speedup not run

## 1. Prior Readiness
Summarize:
- CPU/CUDA mismatch fixed
- schema object/list mismatch fixed
- logical-plan probe now succeeds with schema-native contract

## 2. Execution Configuration
Report:
- force_cpu: `true`
- schema_native_contract: `true`
- runtime root: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/`
- one-row query path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/queries/queries_rewritebench_perf_0006_test.csv`
- tiny positive pool path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/pos_pool_rewritebench_perf_0006_updated.csv`
- tiny negative pool path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/pools/neg_pool_rewritebench_perf_0006_updated.csv`
- OpenAI/API visible: `yes`
- Java rule applier path: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/rewriter_java.jar`

## 3. Execution Summary
Report:
- method command: `python -m scripts.cli formal-llmr2-one-row-fast-path --case PERF_0006 --force-cpu --schema-native-contract`
- method_executed: `true`
- fast_path_runtime_used: `true`
- one_row_query_used: `true`
- tiny_demo_pools_used: `true`
- openai_api_used: `true`
- java_rule_applier_used: `true`
- generation_status: `generation_success_with_output_sql`
- output_sql_extracted: `true`
- generated_sql_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_schema_native_v1.sql`
- checker_candidate_sql_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_candidate_sql_schema_native_v1.sql`
- result_csv_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv`
- activated_rules_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/activated_rules_schema_native_v1.json`
- prompt_trace_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/prompt_trace_schema_native_v1.md`
- demo_trace_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/demo_trace_schema_native_v1.json`
- token_cost_log_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/token_cost_log_schema_native_v1.json`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stdout_schema_native_v1.log`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stderr_schema_native_v1.log`
- failure category: none
- failure summary: none

## 4. Candidate SQL
Path:
- `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_schema_native_v1.sql`

Excerpt:
```sql
l_returnflag, 	l_linestatus, 	sum(l_quantity) as sum_qty, 	sum(l_extendedprice) as sum_base_price, 	sum(l_extendedprice * (1 - l_discount)) as sum_disc_price, 	sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge, 	avg(l_quantity) as avg_qty, 	avg(l_extendedprice) as avg_price, 	avg(l_discount) as avg_disc, 	count(*) as count_order from 	lineitem where 	l_shipdate <= date '1998-08-27' group by 	l_returnflag, 	l_linestatus order by 	l_returnflag, 	l_linestatus SELECT l_returnflag, l_linestatus, SUM(l_quantity) AS sum_qty, SUM(l_extendedprice) AS sum_base_price, SUM(l_extendedprice * (1 - l_discount)) AS sum_disc_price, SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge, AVG(l_quantity) AS avg_qty, AVG(l_extendedprice) AS avg_price, AVG(l_discount) AS avg_disc, COUNT(*) AS count_order FROM lineitem WHERE l_shipdate <= DATE '1998-08-27' GROUP BY l_returnflag, l_linestatus ORDER BY l_returnflag, l_linestatus
```

Note:
- output SQL was captured, but the artifact appears concatenated rather than cleanly normalized

## 5. Checker / Consistency
Report:
- checker_status: `not_run`
- consistency_status: `not_checked`
- checker intentionally not run in this step

## 6. Speedup
State:
- speedup_status: `not_run`

## 7. Claim Boundary
- `bounded_1_case_LLMR2_candidate_generation_smoke_not_leaderboard`

## 8. Remaining Blockers / Next Step
- next step should be PG checker handoff for generated SQL
- because the extracted SQL shape looks concatenated, validate the candidate artifact carefully before any checker claim

## 9. Non-Modification Note
Confirm:
- only PERF_0006 targeted
- no DB
- no checker
- no speedup
- no R-Bot
- no LearnedRewrite
- no MySQL/Spark/SQLGlot routes
- no registry/review/rules/EXECUTION_STATUS changes
- no case files changed
- taxonomy notes untouched
