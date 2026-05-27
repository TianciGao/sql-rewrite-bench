# CALCITE_HEP_MISSING_CHECKER_RERUN_AFTER_READINESS_FIX_v1

## 0. Purpose And Boundary
This note records a Calcite HEP checker rerun after readiness/report-path fix for five generated missing cases only. It does not rerun generation, does not include PERF_0063, runs PostgreSQL checker only, and does not run speedup.

## 1. Prior Diagnostic Recap
- five cases were classified as `wrapper_readiness_gate_too_strict`
- candidate SQL was present and SQL-like
- checker had been reading the wrong generation report path
- `PERF_0063` remains a separate function-signature blocker and is not part of this rerun

## 2. Fix Applied
- `scripts/cli.py` updated `formal-calcite-hep-pg-checker-run` to accept `--generation-report`
- the rerun points checker at `reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json`
- this is a wrapper contract fix only; no Calcite generation rerun was performed

## 3. Per-case Checker Rerun Result
| case_id | readiness_record_found | candidate_sql_path | source_execution_status | candidate_execution_status | checker_status | consistency_status | failure_category | failure_summary | artifact_paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0013 | True | /tmp/calcite-hep-wrapper/real-route/perf_0013.sql | success | success | consistent | consistent | none |  | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0013.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0013.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0013.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0013.tsv"} |
| PERF_0017 | True | /tmp/calcite-hep-wrapper/real-route/perf_0017.sql | success | success | consistent | consistent | none |  | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0017.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0017.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0017.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0017.tsv"} |
| PERF_0019 | True | /tmp/calcite-hep-wrapper/real-route/perf_0019.sql | success | success | consistent | consistent | none |  | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0019.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0019.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0019.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0019.tsv"} |
| PERF_0024 | True | /tmp/calcite-hep-wrapper/real-route/perf_0024.sql | success | success | consistent | consistent | none |  | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0024.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0024.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0024.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0024.tsv"} |
| PERF_0052 | True | /tmp/calcite-hep-wrapper/real-route/perf_0052.sql | success | success | consistent | consistent | none |  | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0052.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0052.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0052.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0052.tsv"} |

## 4. Updated @10 Checker Coverage
- `existing_consistent_subset` = `4`
- `fixed_rerun_target_cases` = `5`
- `fixed_rerun_consistent_count` = `5`
- `fixed_rerun_checker_failures` = `0`
- `perf_0063_generation_failure_remains` = `True`
- `total_10case_checker_consistent_count` = `9`
- `total_10case_remaining_blockers` = `['PERF_0063:generation_failed_function_signature_mismatch']`

## 5. Interpretation
This rerun tests the shared checker readiness/report-path issue only. It does not resolve `PERF_0063`, remains checker expansion evidence only, and keeps speedup as not run for the newly checked cases.

## 6. Recommended Next Step
- `run Calcite HEP speedup for newly checker-consistent cases`

## 7. Non-Modification Note
No generation rerun, no speedup, no MySQL/Spark, no model/API, and no registry/review/rules/EXECUTION_STATUS/case changes occurred. Taxonomy note files remained untouched.
