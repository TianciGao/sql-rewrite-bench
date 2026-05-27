# CALCITE_HEP_PERF_0063_SPEEDUP_v1

## 0. Purpose And Boundary
This is a PG-only Calcite HEP speedup run for PERF_0063 only. It does not rerun generation, does not rerun the existing 9 cases, does not run MySQL or Spark, does not compute cross-engine transfer, and is not a final leaderboard.

## 1. Eligibility Source
- substring-surface normalization succeeded
- `PERF_0063` is checker consistent
- candidate SQL path: `/tmp/calcite-hep-wrapper/real-route/perf_0063.sql`
- speedup is now allowed because generation and PostgreSQL checker both succeeded for PERF_0063

## 2. Runtime Policy
- engine: `postgresql`
- repeats: `5`
- warmup policy: `1` optional warmup per query, not included in metrics
- timeout policy: `60s` wall timeout via PostgreSQL statement timeout `60000ms`
- isolation/cleanup policy: `SET search_path` to validation schema and `public`, with rollback after each execution
- speedup formula: `source_median_ms / candidate_median_ms`
- win/tie/loss thresholds: `win >= 1.05`, `loss <= 0.95`, else `tie`
- regression@20 definition: `candidate_median_ms >= 1.20 * source_median_ms`

## 3. PERF_0063 Speedup Result
| case_id | source_median_ms | candidate_median_ms | speedup | win_tie_loss | regression_at_20 | source_execution_status | candidate_execution_status | failure_category | artifact_paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0063 | 0.351643 | 0.427477 | 0.8226009820411391 | loss | True | success | success | none | {"candidate_result_path": "reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0063.tsv", "candidate_sql_path": "/tmp/calcite-hep-wrapper/real-route/perf_0063.sql", "checker_output_path": "reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0063.json", "checker_report_path": "reports/formal_expansion/calcite_hep_pg_checker_perf_0063_substring_surface_v1.json", "source_result_path": "reports/formal_expansion/result_materialization/calcite_hep/source/perf_0063.tsv"} |

## 4. Updated Calcite HEP Coverage
- `previous_measured_speedup_count` = `9`
- `perf_0063_measured_speedup_count` = `1`
- `total_measured_calcite_hep_speedup_count` = `10`
- `remaining_blockers` = `[]`
- `@10_checker+speedup_closed` = `True`

## 5. Interpretation
This is bounded PG-only Calcite HEP speedup evidence. It remains witness-scale if runtimes are sub-ms or near-sub-ms, is not cross-engine transfer, and is not a final leaderboard.

## 6. Recommended Next Step
- `run Calcite HEP PERF_0063 speedup sanity audit`

## 7. Non-Modification Note
No generation rerun, no existing 9-case rerun, no MySQL/Spark, no model/API, and no registry/review/rules/EXECUTION_STATUS/case changes occurred. Taxonomy notes remained untouched.
