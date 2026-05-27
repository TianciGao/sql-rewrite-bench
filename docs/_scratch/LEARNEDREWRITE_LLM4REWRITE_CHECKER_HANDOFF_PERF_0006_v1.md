# LEARNEDREWRITE_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1

## 0. Purpose And Boundary
This is a PostgreSQL checker handoff only.

- candidate came from LearnedRewrite / LLM4Rewrite embedded path
- `PERF_0006` only
- not speedup
- not leaderboard
- not registry writeback

## 1. Inputs
- source SQL path:
  `/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/source.sql`
- candidate SQL path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v1.sql`
- DDL path:
  `/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/schema/ddl_pg.sql`
- witness data path:
  `/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/validation/pg_witness_data.sql`
- candidate exists: yes
- candidate non-empty: yes
- candidate_type: `source_echo_or_noop_candidate`

## 2. Execution Result
- source_execution_status: `success`
- candidate_execution_status: `success`
- source_row_count: `2`
- candidate_row_count: `2`
- source_output_path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/checker_source_v1.tsv`
- candidate_output_path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/checker_candidate_v1.tsv`

## 3. Checker Result
- checker_status: `consistent`
- consistency_status: `consistent`
- normalization_policy:
  `sort_rows=true,trim_whitespace=true,normalize_numeric_format=true,normalize_null=true`
- failure_category: none
- failure_summary: none

## 4. Candidate Interpretation
- candidate appears source-like / no-op
- `used_rules` was empty in the smoke artifact
- `output_cost` was `-1`
- checker pass here is correctness evidence for a source-like output, not evidence of useful rewrite improvement

## 5. Speedup
- speedup_status: `not_run`

## 6. Claim Boundary
`bounded_1_case_LearnedRewrite_checker_smoke_not_speedup_not_leaderboard`

## 7. Next Step
Update the `PERF_0006` baseline comparison with LearnedRewrite as source-like/no-op and checker-consistent, but still not speedup-evaluated unless explicitly approved later.

## 8. Non-Modification Note
- only `PERF_0006` targeted
- no LearnedRewrite rerun
- no R-Bot
- no model/API
- no speedup
- no MySQL/Spark/SQLGlot routes
- no registry/review/rules/EXECUTION_STATUS changes
- no case files modified
- taxonomy notes untouched
