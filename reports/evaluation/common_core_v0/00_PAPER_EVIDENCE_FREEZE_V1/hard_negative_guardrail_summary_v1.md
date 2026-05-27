# Hard Negative Guardrail Summary v1

This is paper-facing synthesis from retained artifacts.

- This does not create a final ranked leaderboard.
- All denominator and scope labels must be read before comparing rows.
- Correctness is denominator-aware and speedup must be gated by correctness.

| guardrail_scope | denominator_id | tested_negative_rows | correctly_rejected_rows | false_accept_rows | checker_failed_or_unknown_rows | negative_rejection_rate | false_accept_rate | source_artifacts | notes |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `controls_hard_negative_aggregate` | `common_core_v0_40_controls_hard_negative_120_planned` | 111 | 111 | 0 | 0 | 1.0000 | 0.0000 | `common_core_v0_controls_status_table_v2.csv` | Tested-denominator view; 9 planned rows were skipped_unsupported before testing. |
| `cons9_hard_negative_pairs` | `common_core_v0_40_controls_hard_negative_consistency_27` | 27 | 27 | 0 | 0 | 1.0000 | 0.0000 | `common_core_v0_controls_status_table_v2.csv` | Consistency-pool hard negatives are fully retained as successes. |
| `available_hard_negatives_all_pools` | `common_core_v0_40_controls_hard_negative_120_available` | 120 | 111 | 0 | 9 | 0.9250 | 0.0000 | `common_core_v0_controls_status_table_v2.csv`; `common_core_v0_controls_status_summary_v2.md` | Planned-denominator view that keeps skipped_unsupported route cells explicit. |

## Interpretation Notes

- The retained control table supports explicit hard-negative route counts.
- What it does **not** provide is a richer taxonomy of why an unsupported hard-negative row was skipped beyond the retained `skipped_unsupported` label.
- Negative rejection should therefore be reported with its denominator basis made explicit.
