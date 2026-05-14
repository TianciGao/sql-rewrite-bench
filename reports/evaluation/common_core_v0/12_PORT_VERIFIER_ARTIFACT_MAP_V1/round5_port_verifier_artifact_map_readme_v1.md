# Round 5 PORT Verifier Artifact Map Readme v1

## Inputs inspected

- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/verifier_support_artifact_audit_v1.csv`
- `reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv`
- `reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_existing_values_patch_v1.csv`
- `reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv`
- `inventory/case_registry.csv`
- Prior round outputs under `08_SECTION8_EVIDENCE_FREEZE_V1`, `09_TAXONOMY_COVERAGE_V1`, `10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1`, `11_TIMING_OBSERVABILITY_V1`
- Current paper-facing index / claim / gap files in `00_PAPER_EVIDENCE_FREEZE_V1`

## Outputs created

- `port_bounded_route_closure_v1.csv`
- `port_bounded_route_closure_v1.md`
- `speedup_transfer_readiness_v1.csv`
- `speedup_transfer_readiness_v1.md`
- `verifier_support_pair_ledger_v1.csv`
- `verifier_support_pair_ledger_v1.md`
- `paper_artifact_index_v1.csv`
- `paper_artifact_index_v1.md`
- `round5_port_verifier_artifact_map_readme_v1.md`

## PORT closure aggregation rules

- Retained Table 8 synthesis is treated as canonical for bounded PORT closure.
- Because the retained evidence is summary-level, this packet emits bounded summary rows rather than inventing per-case/per-target-engine closure cells.
- Every PORT row keeps `denominator_scope=bounded_PORT6` and explicit boundaries against full PORT9 or full registry closure.

## SpeedupTransferRate readiness rules

- `paired_benefit_ready=yes` only if paired target-engine source/candidate timing evidence or equivalent repeated runtime summaries are retained.
- No such retained evidence exists in the bounded PORT packet, so all rows stay blocked by `missing_paired_target_engine_timing`.
- Same-engine timing slices are not reused as Track C transfer-speed evidence.

## Verifier support aggregation rules

- Verifier rows are support-layer rows only.
- SQLSolver remains a `support_pairs_4_smoke` summary row because no clean per-pair verdict split is retained in the freeze layer.
- VeriEQL remains a bounded `CONS_0035` canary summary row with explicit denominator scope and caveated interpretation.

## Artifact index rules

- The artifact index maps existing artifacts to paper locations and claim boundaries only.
- Status values are limited to `ready`, `ready_with_boundary`, `aggregation_ready`, `manual_review_needed`, `new_experiment_needed`, and `not_supported_write_NA`.
- The index does not create new metrics, new denominators, or new paper claims.

## Known limitations

- Bounded PORT closure is not full PORT9 closure.
- SpeedupTransferRate remains not computed.
- Verifier support remains bounded smoke/canary evidence rather than denominator-complete support packets.
- Appendix I reproducibility packaging still requires human review of packaging scope.

## Whether source-of-truth writeback is needed

- No. These are freeze-layer aggregation and packaging artifacts only.
