# LLMR2_BATCH_B_EXTRACTION_FIX_CHECKER_RERUN_v1

## 0. Purpose And Boundary
- extraction fix + checker rerun only
- `PERF_0019` / `PERF_0024` only
- no LLM-R2 rerun
- no model/API
- no Java
- no speedup
- no registry writeback

## 1. Prior Failure Recap
- the previous `v1` clean candidates were inner-subquery fragments
- the PostgreSQL `SyntaxError` came from extraction artifact, not from a fresh LLM-R2 run
- `PERF_0033` succeeded under the old extraction rule only because it had simpler top-level SQL without nested subquery ambiguity

## 2. Extraction Fix
### PERF_0019
- result CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0019/gpt_rewritebench_perf_0019_one_promo_queryCL_updated.csv`
- raw candidate source: `rewritten_sql_gpt`
- extraction rule used: `earliest_balanced_select_or_with`
- v2 clean candidate path: `/tmp/rewritebench_llmr2_fast_path/PERF_0019/generated_sql_schema_native_clean_v2.sql`
- starts with `SELECT`/`WITH`: yes
- statement count: `1`
- parentheses balance: `0`
- obvious syntax status: valid outermost query recovered; no dangling derived-table suffix remains

Recovered candidate:

```sql
select     c_count,     count(*) as custdist from     (         select             c_custkey,             count(o_orderkey)         from             customer left outer join orders on                 c_custkey = o_custkey                 and o_comment not like '%express%deposits%'         group by             c_custkey     ) as c_orders (c_custkey, c_count) group by     c_count order by     custdist desc,     c_count desc;
```

### PERF_0024
- result CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0024/gpt_rewritebench_perf_0024_one_promo_queryCL_updated.csv`
- raw candidate source: `rewritten_sql_gpt`
- extraction rule used: `earliest_balanced_select_or_with`
- v2 clean candidate path: `/tmp/rewritebench_llmr2_fast_path/PERF_0024/generated_sql_schema_native_clean_v2.sql`
- starts with `SELECT`/`WITH`: yes
- statement count: `1`
- parentheses balance: `0`
- obvious syntax status: valid outermost query recovered; no dangling join fragment remains

Recovered candidate:

```sql
SELECT supplier.s_name, supplier.s_address FROM supplier INNER JOIN (SELECT * FROM nation WHERE n_name = 'BRAZIL') AS t ON supplier.s_nationkey = t.n_nationkey INNER JOIN (SELECT partsupp.ps_suppkey FROM partsupp INNER JOIN (SELECT p_partkey FROM part WHERE p_name LIKE 'pale%') AS t1 ON partsupp.ps_partkey = t1.p_partkey INNER JOIN (SELECT l_partkey, l_suppkey, SUM(l_quantity) AS f2 FROM lineitem WHERE l_shipdate >= DATE '1997-01-01' AND l_shipdate < (DATE '1997-01-01' + INTERVAL '1' YEAR) GROUP BY l_partkey, l_suppkey) AS t4 ON partsupp.ps_partkey = t4.l_partkey AND partsupp.ps_suppkey = t4.l_suppkey AND partsupp.ps_availqty > 0.5 * t4.f2) AS t6 ON supplier.s_suppkey = t6.ps_suppkey ORDER BY supplier.s_name;
```

## 3. Checker Rerun Result
### PERF_0019
- source_execution_status: `success`
- candidate_execution_status: `success`
- source_row_count: `2`
- candidate_row_count: `2`
- checker_status: `consistent`
- consistency_status: `consistent`
- failure_category: `none`
- failure_summary: `none`
- output paths:
  - source: `/tmp/rewritebench_llmr2_fast_path/PERF_0019/checker_source_v1.tsv`
  - candidate: `/tmp/rewritebench_llmr2_fast_path/PERF_0019/checker_candidate_v1.tsv`

### PERF_0024
- source_execution_status: `success`
- candidate_execution_status: `success`
- source_row_count: `1`
- candidate_row_count: `1`
- checker_status: `consistent`
- consistency_status: `consistent`
- failure_category: `none`
- failure_summary: `none`
- output paths:
  - source: `/tmp/rewritebench_llmr2_fast_path/PERF_0024/checker_source_v1.tsv`
  - candidate: `/tmp/rewritebench_llmr2_fast_path/PERF_0024/checker_candidate_v1.tsv`

## 4. Batch B Status Update
- `PERF_0019`: previously failed because `v1` extraction started inside an inner subquery; after `v2` extraction, the candidate executed and passed checker handoff.
- `PERF_0024`: previously failed because `v1` extraction started inside an inner aggregation/join fragment; after `v2` extraction, the candidate executed and passed checker handoff.
- `PERF_0033`: unchanged; it remained checker consistent under the original extraction path.

## 5. Metrics Impact
- denominator = `3`
- candidate_generation_count = `3`
- clean_candidate_recovered_count = `3`
- candidate_execution_count = `3`
- executable_rate@3 = `3/3`
- checker_consistent_count = `3`
- result_consistency_rate@3 = `3/3`
- checker_failed_count = `0`
- output_extraction_failure_count = `0`
- speedup_status = `not_run`

## 6. Recommended Next Step
- update Batch B rollup with v2 extraction results

Justification:
- the failed cases were repaired without rerunning LLM-R2
- Batch B now reflects the same end state as Batch A: generated candidates, deterministic cleanup, successful PostgreSQL execution, and checker consistency
- the next bounded step should be to update the Batch B documentation before deciding whether to move to Batch C

## 7. Non-Modification Note
- no LLM-R2 rerun occurred
- no model/API call occurred
- no Java rule applier ran
- no speedup ran
- only PostgreSQL checker handoff on corrected candidates was executed
- no registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were changed
