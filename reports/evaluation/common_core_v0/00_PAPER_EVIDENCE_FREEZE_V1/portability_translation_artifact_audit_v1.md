# Portability Translation Artifact Audit v1

This is paper-facing synthesis from retained artifacts.

This does not create a final ranked leaderboard.

Track C portability is separate from Track A same-engine rewrite.

Parser or translation success is not enough; target execution and consistency are separate.

| evidence_scope | method_id | route_id | retained_denominator_id | planned_translation_rows | generated_translation_rows | target_execution_success_rows | cross_engine_exact_rows | speedup_transfer_rows | speedup_transfer_rate | source_artifacts | readiness_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall_track_c_portability | track_c_portability | NA_not_applicable | port9_or_explicitly_frozen_selected_port_subset | NA_not_found | NA_not_found | 6 | 6 | 0 | NA_not_computed | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_table_contract_v1.csv;reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv;docs/_scratch/PORT_CROSS_ENGINE_CLOSURE_PREFLIGHT_v1.md | selected_port_subset_retained | Track C contract expects PORT9 or an explicitly frozen selected subset; retained evidence currently supports a bounded 6-case closure packet rather than full PORT9 |
| sqlglot_cross_dialect_transpile | sqlglot_cross_dialect_transpile | UNKNOWN_NOT_RECOVERED | port_bounded_6 | 6 | NA_not_found | 1 | 1 | 0 | NA_not_computed | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv;docs/_scratch/PORT_CROSS_ENGINE_CLOSURE_PREFLIGHT_v1.md;reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv | bounded_port6_only | Retained notes support bounded PG-side route evidence on 6 cases with only one clearly closed both-engine case in the earlier closure preflight and no retained transfer-speed metric |
| llm_translate | llm_translate | UNKNOWN_NOT_RECOVERED | port_bounded_6 | 6 | 6 | 6 | 6 | 0 | NA_not_computed | reports/evaluation/common_core_v0/direct_llm_llm_translate_120_readiness_audit_v1.csv;reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv;reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv | bounded_port6_only | Retained governance treats LLM Translate as Track C portability evidence on the bounded 6-case packet rather than a same-engine route and no transfer-speed metric is retained |
| port_bounded_6_packet | bounded_cross_engine_closure_packet | bounded_port_route_packet | port_bounded_6 | 6 | 6 | 6 | 6 | 0 | NA_not_computed | docs/_scratch/PORT_CROSS_ENGINE_CLOSURE_SNAPSHOT_6OF6_v1.md;reports/evaluation/common_core_v0/EXPERIMENT_RESULTS_LEDGER_CURRENT_v1.csv | bounded_port6_only | Bounded 6-case cross-engine closure packet is retained and paper-safe but remains portability-only and explicitly not a SpeedupTransferRate packet |

## Interpretation notes

- Full PORT9 closure is not retained here.
- The retained portability line is a bounded `port_bounded_6` packet.
- `SpeedupTransferRate` remains uncomputed and must stay separate from mere route closure or target-engine execution.
