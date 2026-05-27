# Controls Route Split v1

This is paper-facing synthesis from retained artifacts.

- This does not create a final ranked leaderboard.
- All denominator and scope labels must be read before comparing rows.
- Correctness is denominator-aware and speedup must be gated by correctness.

| route_id | route_role | denominator_id | planned_rows | applicable_rows | success_rows | skipped_unsupported_rows | failed_rows | exact_or_expected_outcome | source_artifacts | notes |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `controls_aggregate` | `controls_aggregate` | `common_core_v0_40_controls_360` | 360 | 324 | 324 | 36 | 0 | `aggregate_expected_control_outcome_success` | `common_core_v0_controls_status_summary_v2.md`; `common_core_v0_controls_status_table_v2.csv`; `EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv` | Denominator-complete aggregate controls coverage. |
| `native_source` | `control_route` | `common_core_v0_40_controls_native_source_120` | 120 | 102 | 102 | 18 | 0 | `native_source_expected_outcome_success` | `common_core_v0_controls_status_table_v2.csv` | Route-level split is explicitly recoverable. |
| `human_positive` | `control_route` | `common_core_v0_40_controls_human_positive_120` | 120 | 111 | 111 | 9 | 0 | `human_positive_expected_outcome_success` | `common_core_v0_controls_status_table_v2.csv` | Route-level split is explicitly recoverable. |
| `hard_negative` | `control_route` | `common_core_v0_40_controls_hard_negative_120` | 120 | 111 | 111 | 9 | 0 | `hard_negative_expected_outcome_success` | `common_core_v0_controls_status_table_v2.csv` | Retained control table exposes success/skipped/failed directly for hard-negative rows. |

## Interpretation Notes

- The controls packet supports a clean `native_source / human_positive / hard_negative` route split.
- `skipped_unsupported` rows are retained denominator rows and should remain visible rather than being silently dropped.
