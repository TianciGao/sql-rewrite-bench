# CALCITE_HEP_10CASE_MISSING_CHECKER_BATCH_v1

## 0. Purpose And Boundary
This note records a bounded Calcite HEP missing-case generation/checker batch for six target cases only. It uses PostgreSQL checker handoff only, does not run speedup, is not a final baseline, and does not write back to registries.

## 1. Existing Subset Recap
- existing 4 covered cases: `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054`
- checker result: `4/4` consistent
- speedup subset GM: `0.9588741913559858`
- claim boundary: bounded PG-only subset, not final baseline

## 2. Target Missing Cases
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0052`
- `PERF_0063`

## 3. Per-case Result Table
| case_id | generation_status | output_sql_extracted | candidate_sql_path | source_execution_status | candidate_execution_status | checker_status | consistency_status | failure_category | failure_summary | artifact_paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0013 | generated | True | /tmp/calcite-hep-wrapper/real-route/perf_0013.sql | not_attempted | not_attempted | candidate_execution_failed | not_consistent | candidate_sql_not_ready | Calcite candidate SQL was not ready for PostgreSQL execution | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0013.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0013.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0013.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_batch_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0013.tsv"} |
| PERF_0017 | generated | True | /tmp/calcite-hep-wrapper/real-route/perf_0017.sql | not_attempted | not_attempted | candidate_execution_failed | not_consistent | candidate_sql_not_ready | Calcite candidate SQL was not ready for PostgreSQL execution | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0017.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0017.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0017.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_batch_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0017.tsv"} |
| PERF_0019 | generated | True | /tmp/calcite-hep-wrapper/real-route/perf_0019.sql | not_attempted | not_attempted | candidate_execution_failed | not_consistent | candidate_sql_not_ready | Calcite candidate SQL was not ready for PostgreSQL execution | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0019.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0019.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0019.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_batch_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0019.tsv"} |
| PERF_0024 | generated | True | /tmp/calcite-hep-wrapper/real-route/perf_0024.sql | not_attempted | not_attempted | candidate_execution_failed | not_consistent | candidate_sql_not_ready | Calcite candidate SQL was not ready for PostgreSQL execution | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0024.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0024.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0024.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_batch_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0024.tsv"} |
| PERF_0052 | generated | True | /tmp/calcite-hep-wrapper/real-route/perf_0052.sql | not_attempted | not_attempted | candidate_execution_failed | not_consistent | candidate_sql_not_ready | Calcite candidate SQL was not ready for PostgreSQL execution | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0052.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0052.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0052.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_batch_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0052.tsv"} |
| PERF_0063 | generation_failed | True | /tmp/calcite-hep-wrapper/real-route/perf_0063.sql | not_run_generation_failed | not_run_generation_failed | not_run_generation_failed | not_run | real_route_partial_only | ValidationException: org.apache.calcite.runtime.CalciteContextException: From line 14, column 8 to line 14, column 27: No match found for function signature substr(<CHARACTER>, <NUMERIC>, <NUMERIC>) | {"candidate_result_path": "", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0063.sql", "checker_output_path": "", "checker_report_path": "", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": ""} |

## 4. Batch Metrics
- `target_denominator` = `6`
- `generation_success_count` = `5`
- `generation_failure_count` = `1`
- `checker_run_count` = `5`
- `checker_consistent_count` = `0`
- `checker_failed_count` = `5`
- `candidate_execution_failed_count` = `5`
- `speedup_status` = `not_run`

## 5. Updated @10 Checker Coverage
- `existing_consistent_count` = `4`
- `new_consistent_count` = `0`
- `total_10case_checker_consistent_count` = `4`
- `total_10case_generation_failures` = `1`
- `total_10case_checker_failures` = `5`
- `remaining_blockers` = `['PERF_0013:candidate_execution_failed', 'PERF_0017:candidate_execution_failed', 'PERF_0019:candidate_execution_failed', 'PERF_0024:candidate_execution_failed', 'PERF_0052:candidate_execution_failed', 'PERF_0063:real_route_partial_only']`

## 6. Interpretation
This is Calcite HEP checker expansion evidence only. It is not speedup, not a final baseline, and not cross-engine transfer evidence.

## 7. Recommended Next Step
- `diagnose Calcite HEP generation/checker failures`

## 8. Non-Modification Note
Only the six missing cases were targeted. No speedup, MySQL, Spark, model/API, registry, review, rules, EXECUTION_STATUS, or case-file changes were made. Taxonomy note files remained untouched.
