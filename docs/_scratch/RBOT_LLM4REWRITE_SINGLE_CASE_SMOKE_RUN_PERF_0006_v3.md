# RBOT_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v3

## 0. Purpose And Boundary
This was a bounded R-Bot / LLM4Rewrite smoke rerun with a temp retrieval-vector compatibility patch for `PERF_0006` only. It is not leaderboard evidence, not full prior-method coverage, not registry writeback, checker was not run, and speedup was not run.

## 1. Patch Applied
- copied runtime tree path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_patch_v3`
- files patched in temp runtime:
  - `rag/my_query_fusion_retriver.py`
  - `knowledge-base/rule_cluster_funcs/24.py`
  - `rag/gen_sql_templates.py`
- rule vector expected dimension: `100`
- alignment method: after constructing the live `rules_one_hot` vector from matched NL and Calcite-normal rules, the temp patch pads with trailing zeroes up to width `100` before concatenation with the two `1536`-dim embedding segments
- fresh run name: `rbot_perf_0006_1777983772588`
- upstream log path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/rbot_perf_0006_1777983772588.log`
- upstream clone changed: no
- project case files changed: no

## 2. Preconditions
- dry-run status: passed
- RAG index path: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- Chroma collection dimension if checked: `3172`
- smoke venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python`
- OpenAI/API visible: yes
- PG env visible: yes

## 3. Execution Summary
- method command:
  - `python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006 --fresh-run-name --align-rule-vector-dim 100`
- generation status: `generation_success_with_output_sql`
- output SQL extracted: yes
- generated SQL path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v3.sql`
- checker candidate SQL path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/checker_candidate_sql_v3.sql`
- selected rules path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/selected_rules_v3.json`
- retrieval trace path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/retrieval_trace_v3.json`
- token/cost log path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/token_cost_log_v3.json`
- stdout path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stdout_v3.log`
- stderr path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stderr_v3.log`
- failure category: none
- failure summary: none
- retrieval vector patch applied: yes
- retrieval vector expected dimension: `100`
- retrieval vector actual dimension if observed: not surfaced as an error after patch

## 4. Candidate SQL
Path:
- `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v3.sql`

Excerpt:

```sql
SELECT "l_returnflag", "l_linestatus", COALESCE(SUM("l_quantity"), 0) AS "sum_qty", COALESCE(SUM("l_extendedprice"), 0) AS "sum_base_price", COALESCE(SUM("l_extendedprice" * (1 - "l_discount")), 0) AS "sum_disc_price", COALESCE(SUM("l_extendedprice" * (1 - "l_discount") * (1 + "l_tax")), 0) AS "sum_charge", CAST(CAST(COALESCE(SUM("l_quantity"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2)) AS "avg_qty", CAST(CAST(COALESCE(SUM("l_extendedprice"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2)) AS "avg_price", CAST(CAST(COALESCE(SUM("l_discount"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2)) AS "avg_disc", COUNT(*) AS "count_order"
FROM "lineitem"
WHERE "l_shipdate" <= DATE '1998-08-27'
GROUP BY "l_returnflag", "l_linestatus"
ORDER BY "l_returnflag", "l_linestatus";
```

## 5. Checker / Consistency
- checker_status: `not_run`
- consistency_status: `not_checked`
- checker was intentionally not run in this step because this was bounded candidate-generation smoke only, not checker validation

## 6. Speedup
- speedup_status: `not_run`

## 7. Claim Boundary
`bounded_1_case_RBot_LLM4Rewrite_candidate_generation_smoke_not_leaderboard`

## 8. Remaining Blockers / Next Step
Generated SQL was captured successfully. The next step should be PG checker handoff for the generated SQL.

## 9. Non-Modification Note
- only `PERF_0006` was targeted
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made
- no checker was run
- no speedup was run
- no MySQL, Spark, or standalone SQLGlot route was run
- taxonomy notes were untouched
