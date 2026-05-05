# RBOT_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1

## 0. Purpose And Boundary
This was a PostgreSQL checker handoff only for an R-Bot / LLM4Rewrite candidate on `PERF_0006`. It is not speedup evaluation, not leaderboard evidence, and not registry writeback.

## 1. Inputs
- source SQL path: `cases/PERF/PERF_0006/source.sql`
- candidate SQL path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v3.sql`
- DDL path: `cases/PERF/PERF_0006/schema/ddl_pg.sql`
- witness data path: `cases/PERF/PERF_0006/validation/pg_witness_data.sql`
- candidate exists: yes
- candidate non-empty: yes

## 2. Execution Result
- source_execution_status: `success`
- candidate_execution_status: `success`
- source_row_count: `2`
- candidate_row_count: `2`
- source_output_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/checker_source_v1.tsv`
- candidate_output_path: `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/checker_candidate_v1.tsv`

Observed row-level mismatch:

```text
source:    A F ... avg_qty=15.0000000000000000 avg_price=150.0000000000000000 avg_disc=0.07500000000000000000
candidate: A F ... avg_qty=15.00               avg_price=150.00               avg_disc=0.08

source:    N O ... avg_qty=15.0000000000000000 avg_price=150.0000000000000000 avg_disc=0E-20
candidate: N O ... avg_qty=15.00               avg_price=150.00               avg_disc=0.00
```

The decisive semantic mismatch is `avg_disc`: `0.075...` in source vs `0.08` in candidate.

## 3. Checker Result
- checker_status: `inconsistent`
- consistency_status: `inconsistent`
- normalization_policy: `sort_rows=true,trim_whitespace=true,normalize_numeric_format=true,normalize_null=true`
- failure_category: `result_mismatch`
- failure_summary: `normalized TSV outputs differed`

## 4. Speedup
- speedup_status: `not_run`

## 5. Claim Boundary
`bounded_1_case_RBot_LLM4Rewrite_checker_smoke_not_speedup_not_leaderboard`

## 6. Next Step
The next step is failure analysis, not speedup. The candidate appears to have rewritten `AVG(...)` via rounded decimal division, which changes result semantics for `avg_disc`.

## 7. Non-Modification Note
- only `PERF_0006` was targeted
- no model call occurred
- no R-Bot rerun occurred
- no speedup was run
- no MySQL, Spark, or standalone SQLGlot route was run
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes occurred
- no case files were modified
- taxonomy notes were untouched
