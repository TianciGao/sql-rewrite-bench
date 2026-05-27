# CALCITE_HEP_MISSING_SPEEDUP_AFTER_READINESS_FIX_v1

## 0. Purpose And Boundary
This is a PG-only Calcite HEP speedup run for five newly checker-consistent missing cases only. It does not rerun generation, does not include PERF_0063, does not run MySQL or Spark, does not compute cross-engine transfer, and is not a final baseline.

## 1. Eligibility Source
- checker rerun after readiness fix produced five newly checker-consistent cases
- `PERF_0063` remains excluded due function-signature generation failure

## 2. Runtime Policy
- engine: `postgresql`
- repeats: `5`
- warmup policy: `1` optional warmup per query, not included in metrics
- timeout policy: `60s` wall timeout via PostgreSQL statement timeout `60000ms`
- isolation/cleanup policy: `SET search_path` to validation schema and `public`, with rollback after each execution
- speedup formula: `source_median_ms / candidate_median_ms`
- win/tie/loss thresholds: `win >= 1.05`, `loss <= 0.95`, else `tie`
- regression@20 definition: `candidate_median_ms >= 1.20 * source_median_ms`

## 3. Per-case Result Table
| case_id | source_median_ms | candidate_median_ms | speedup | win_tie_loss | regression_at_20 | source_execution_status | candidate_execution_status | failure_category | artifact_paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0013 | 0.627483 | 0.644344 | 0.9738323007586009 | tie | False | success | success | none | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0013.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0013.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0013.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0013.tsv"} |
| PERF_0017 | 0.393879 | 0.386998 | 1.017780453645755 | tie | False | success | success | none | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0017.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0017.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0017.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0017.tsv"} |
| PERF_0019 | 0.301961 | 0.297356 | 1.01548648757718 | tie | False | success | success | none | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0019.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0019.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0019.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0019.tsv"} |
| PERF_0024 | 0.341967 | 0.342732 | 0.9977679352963833 | tie | False | success | success | none | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0024.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0024.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0024.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0024.tsv"} |
| PERF_0052 | 0.338447 | 0.41939 | 0.8069982593767138 | loss | True | success | success | none | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0052.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0052.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0052.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_missing_rerun_after_fix_v1.json", "generation_report_path": "reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0052.tsv"} |

## 4. Batch Metrics
- `denominator` = `5`
- `valid_measured_count` = `5`
- `gm_speedup` = `0.9588328711588356`
- `win_count` = `0`
- `tie_count` = `4`
- `loss_count` = `1`
- `regression_count@20` = `1`
- `measurement_failure_count` = `0`
- `timeout_count` = `0`
- `speedup_status` = `measured`

## 5. Updated Calcite HEP Coverage
- `existing_4case_speedup_subset` = `4`
- `new_speedup_measured_count` = `5`
- `total_measured_calcite_hep_speedup_count` = `9`
- `remaining_unmeasured_blocker` = `PERF_0063:generation_failed_function_signature_mismatch`

## 6. Interpretation
This is bounded PG-only Calcite HEP speedup evidence. It is not a final @10 baseline because PERF_0063 remains blocked, it is not cross-engine transfer, and witness-scale caveats still apply if runtimes are sub-ms or near-sub-ms.

## 7. Recommended Next Step
- `run Calcite HEP speedup sanity audit`

## 8. Non-Modification Note
No generation rerun, no PERF_0063 targeting, no MySQL/Spark, no model/API, and no registry/review/rules/EXECUTION_STATUS/case changes occurred. Taxonomy notes remained untouched.
