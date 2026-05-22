# Table 8. PORT Cross-engine Translation v1

This is paper-facing synthesis from retained artifacts.

This does not create a final ranked leaderboard.

Track C portability is separate from Track A same-engine rewrite.

Parser or translation success is not enough; target execution and consistency are separate.

Table 8 reports portability / translation evidence only. It must not be read as same-engine rewrite performance. SpeedupTransferRate is reported only if target-engine exact timing evidence is retained.

| method | route_id | attempted_port_cases | denominator_id | target_engines | translation_success | translation_success_numerator | translation_success_denominator | cross_engine_executable_rate | cross_engine_executable_numerator | cross_engine_executable_denominator | cross_engine_consistency_rate | cross_engine_consistency_numerator | cross_engine_consistency_denominator | speedup_transfer_rate | unsupported_or_failed_cases | paper_table_placement | claim_boundary | source_artifacts | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SQLGlot Transpile | UNKNOWN_NOT_RECOVERED | 6 | port_bounded_6 | mysql_and_spark_from_pg_side_packet | bounded_port6_route_only | NA_not_found | 6 | bounded_selected_subset_only | 1 | 6 | bounded_selected_subset_only | 1 | 6 | NA_not_computed | PORT_0012;PORT_0013;PORT_0004 witness-contract caveat; earlier bounded closure preflights kept PORT_0022 and PORT_0025 blocked before full closure | track_c_portability_table | portability_route_only_not_same_engine_rewrite_and_not_transfer_speed | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv;docs/_scratch/PORT_CROSS_ENGINE_CLOSURE_PREFLIGHT_v1.md;reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv | bounded_port6_only | SQLGlot Transpile retained evidence is bounded portability-route evidence only and should not be read as same-engine rewrite performance |
| LLM Translate | UNKNOWN_NOT_RECOVERED | 6 | port_bounded_6 | pg_mysql_spark_bounded_port_packet | bounded_port6_only | 6 | 6 | bounded_6_over_6 | 6 | 6 | bounded_6_over_6 | 6 | 6 | NA_not_computed | none_retained_in_bounded_port6_packet | track_c_portability_table | portability_translation_only_target_execution_and_consistency_retained_but_no_speedup_transfer_rate | reports/evaluation/common_core_v0/direct_llm_llm_translate_120_readiness_audit_v1.csv;reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv;reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv | bounded_port6_only | Retained evidence supports bounded 6-case portability closure but it is not same-engine rewrite evidence and not a transfer-speed claim |
| Bounded PORT closure packet | bounded_port_route_packet | 6 | port_bounded_6 | pg_mysql_spark | bounded_port6_only | 6 | 6 | bounded_6_over_6 | 6 | 6 | bounded_6_over_6 | 6 | 6 | NA_not_computed | none_retained_in_snapshot | track_c_portability_appendix_or_context | bounded_cross_engine_closure_snapshot_only_not_same_engine_not_transfer_speed | docs/_scratch/PORT_CROSS_ENGINE_CLOSURE_SNAPSHOT_6OF6_v1.md;reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv | bounded_port6_only | Context row for the retained bounded closure packet rather than a separate not same-engine method row |

## Interpretation notes

- Table 8 is a Track C table, not a same-engine table.
- `LLM Translate` currently has the strongest retained bounded closure line on the 6-case packet.
- `SQLGlot Transpile` remains bounded and partial on that same packet.
- No row here justifies a `SpeedupTransferRate` claim.
