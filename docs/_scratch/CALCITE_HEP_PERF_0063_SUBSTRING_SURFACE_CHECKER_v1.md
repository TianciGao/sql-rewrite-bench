# CALCITE_HEP_PERF_0063_SUBSTRING_SURFACE_CHECKER_v1

## 0. Purpose And Boundary
This note records PERF_0063-only Calcite HEP substring-surface normalization plus generation/checker. It does not run speedup, does not rerun the existing 9 cases, does not edit case files, and is the final narrow attempt before retaining the 9/10 boundary if it fails.

## 1. Failed CAST Attempt Recap
- previous attempt normalized `substr(ca_zip, 1, 5)` to `substr(ca_zip, CAST(1 AS INTEGER), CAST(5 AS INTEGER))`
- the normalization was applied and reached parse-only emitted SQL
- Calcite still reported `substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)`
- classification: `calcite_cast_still_typed_numeric`

## 2. Normalization Applied
- original expression: `substr(ca_zip, 1, 5)`
- normalized expression: `substring(ca_zip FROM 1 FOR 5)`
- normalization scope: case-specific adapter-local normalization for `PERF_0063` only
- normalized input artifact path: `/tmp/calcite-hep-wrapper/real-route/perf_0063_substring_surface_input.sql`
- original case source file was not modified; normalization was applied only to the Calcite input artifact

## 3. Generation Result
- `validation_succeeded` = `True`
- `sql_to_rel_succeeded` = `True`
- `hep_planner_succeeded` = `True`
- `output_sql_extracted` = `True`
- `candidate_sql_path` = `/tmp/calcite-hep-wrapper/real-route/perf_0063.sql`
- `generation_status` = `generated`

## 4. PostgreSQL Checker Result
- `source_execution_status` = `success`
- `candidate_execution_status` = `success`
- `checker_status` = `consistent`
- `consistency_status` = `consistent`
- `failure_category` = `none`
- `failure_summary` = ``
- `artifact_paths` = `{"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0063.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0063.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0063.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_perf_0063_substring_surface_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_perf_0063_substring_surface_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0063.tsv"}`

## 5. Updated Calcite HEP @10 Checker Coverage
- `previous_checker_consistent` = `9`
- `perf_0063_checker_result` = `consistent`
- `total_10case_checker_consistent_count` = `10`
- `remaining_checker_blockers` = `[]`

## 6. Recommended Next Step
- `run Calcite HEP speedup for PERF_0063`

## 7. Non-Modification Note
Only `PERF_0063` was targeted. No speedup ran, no existing 9-case rerun occurred, no MySQL/Spark/model/API path was used, and no case/registry/review/rules/EXECUTION_STATUS changes were made. Taxonomy notes remained untouched.
