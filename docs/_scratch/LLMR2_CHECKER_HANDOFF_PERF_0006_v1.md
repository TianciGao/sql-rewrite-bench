# LLMR2_CHECKER_HANDOFF_PERF_0006_v1

## 0. Purpose And Boundary
State:
- PG checker handoff only
- candidate came from LLM-R2 clean extracted candidate
- PERF_0006 only
- not speedup
- not leaderboard
- not registry writeback

## 1. Inputs
Report:
- source SQL path: `cases/PERF/PERF_0006/source.sql`
- candidate SQL path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/generated_sql_schema_native_clean_v1.sql`
- DDL path: `cases/PERF/PERF_0006/schema/ddl_pg.sql`
- witness data path: `cases/PERF/PERF_0006/validation/pg_witness_data.sql`
- candidate exists: `yes`
- candidate non-empty: `yes`
- candidate_type: `clean_extracted_candidate`

## 2. Execution Result
Report:
- source_execution_status: `success`
- candidate_execution_status: `success`
- source_row_count: `2`
- candidate_row_count: `2`
- source_output_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_source_v1.tsv`
- candidate_output_path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/checker_candidate_v1.tsv`

## 3. Checker Result
Report:
- checker_status: `consistent`
- consistency_status: `consistent`
- normalization_policy: `sort_rows=true,trim_whitespace=true,normalize_numeric_format=true,normalize_null=true`
- failure category: none
- failure summary: none

## 4. Candidate Interpretation
State:
- candidate was recovered from LLM-R2 `rewritten_sql_gpt` extraction audit
- raw artifact had extraction contamination
- clean candidate was used for checker

## 5. Speedup
State:
- speedup_status: `not_run`

## 6. Claim Boundary
- `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard`

## 7. Next Step
- record LLM-R2 as bounded 1-case checker-backed smoke evidence
- do not run speedup unless explicitly approved later

## 8. Non-Modification Note
Confirm:
- only PERF_0006 targeted
- no LLM-R2 rerun
- no model/API
- no Java rule applier
- no speedup
- no MySQL/Spark/SQLGlot routes
- no registry/review/rules/EXECUTION_STATUS changes
- no case files modified
- taxonomy notes untouched
