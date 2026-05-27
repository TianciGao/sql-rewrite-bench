# LLMR2_OUTPUT_SQL_EXTRACTION_AUDIT_PERF_0006_v1

## 0. Purpose And Boundary
State output extraction audit only, not execution/checker.

## 1. Input Artifacts
Report:
- result CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv` and exists: `yes`
- raw generated SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_schema_native_v1.sql` and exists: `yes`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stdout_schema_native_v1.log`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/method_stderr_schema_native_v1.log`
- token/cost path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/token_cost_log_schema_native_v1.json`
- activated rules path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/activated_rules_schema_native_v1.json`

## 2. Result CSV Inspection
Report:
- columns: `db_id`, `original_sql`, `rewritten_sql_gpt`, `activated_rules_gpt`, `prompt_sql_similar`, `prompt_rules_similar`
- row count: `1`
- candidate SQL column: `rewritten_sql_gpt`
- raw cell excerpt:
```text
l_returnflag, l_linestatus, sum(l_quantity) as sum_qty, ... order by l_returnflag, l_linestatus SELECT l_returnflag, l_linestatus, SUM(l_quantity) ...
```

## 3. Generated SQL Artifact Inspection
Report:
- current `generated_sql_schema_native_v1.sql` status: exists
- it appears concatenated: `yes`
- this is likely extraction artifact vs method output: `extraction artifact`

Reason:
- the CSV cell contains a leading fragment followed by a second full `SELECT ...` statement
- the clean statement boundary is recoverable deterministically from the last full `SELECT`

## 4. Clean Candidate Extraction
Recovered:
- clean candidate path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_schema_native_clean_v1.sql`
- checker handoff path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_candidate_sql_schema_native_clean_v1.sql`
- extraction rule used: keep the last full `SELECT`/`WITH` statement in `rewritten_sql_gpt`, normalize whitespace, append a trailing semicolon

Excerpt:
```sql
SELECT l_returnflag, l_linestatus, SUM(l_quantity) AS sum_qty, SUM(l_extendedprice) AS sum_base_price, SUM(l_extendedprice * (1 - l_discount)) AS sum_disc_price, SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge, AVG(l_quantity) AS avg_qty, AVG(l_extendedprice) AS avg_price, AVG(l_discount) AS avg_disc, COUNT(*) AS count_order FROM lineitem WHERE l_shipdate <= DATE '1998-08-27' GROUP BY l_returnflag, l_linestatus ORDER BY l_returnflag, l_linestatus;
```

Checks:
- begins with `SELECT`: `yes`
- exactly one candidate statement: `yes`
- checker handoff allowed after cleanup: `yes`

## 5. Classification
- `extraction_bug_clean_candidate_recovered`

## 6. Recommended Next Step
- `run PG checker handoff on clean candidate`

## 7. Non-Modification Note
Confirm no LLM-R2 rerun, no model/API, no Java, no DB, no checker, no speedup, no registry/case changes.
