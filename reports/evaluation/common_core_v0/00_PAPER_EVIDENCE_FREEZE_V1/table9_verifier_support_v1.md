# Table 9. Verifier Support Table v1

This is paper-facing synthesis from retained artifacts.

This does not create a final ranked leaderboard.

Support-layer metrics are not rewrite method ranking metrics.

Verifier support tools evaluate SQL pairs or support evidence. They are not rewrite generators and must not be interpreted as speed baselines.

| tool | pair_denominator | positive_pairs | negative_pairs | prove | refute | unknown | timeout | support_rate | paper_table_placement | claim_boundary | source_artifacts | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SQLSolver | support_pairs_4 | NA_not_found | NA_not_found | NA_not_found | NA_not_found | NA_not_found | NA_not_found | bounded_3_over_4_support_smoke | support_table_bounded_smoke | verifier_support_only_not_rewrite_generator | docs/_scratch/BASELINE_EVIDENCE_MATRIX_CURRENT_v1.md;reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json;docs/_scratch/SQLSOLVER_EXTERNAL_SUBSTRATE_ACQUISITION_AUDIT_v1.md | smoke_only | 4-pair bounded smoke only and no retained clean verdict split for prove refute unknown timeout |
| VeriEQL | cons_0035_pairs_2 | 1 | 1 | 0 | 2 | 0 | 0 | bounded_1.0_on_2_pairs_caveated | support_table_bounded_canary | verifier_support_only_not_rewrite_generator | docs/_scratch/VERIEQL_SUPPORT_CANARY_v0.md;docs/_scratch/BASELINE_EVIDENCE_MATRIX_CURRENT_v1.md | canary_only | One-case canary only and the positive outcome is constraint-sensitive so it should not be generalized to CONS9 |

## Interpretation notes

- Table 9 is a support-track table rather than a rewrite leaderboard table.
- SQLSolver currently has only a bounded smoke packet in retained evidence.
- VeriEQL currently has only a bounded `CONS_0035` canary packet and its positive outcome remains caveated.

