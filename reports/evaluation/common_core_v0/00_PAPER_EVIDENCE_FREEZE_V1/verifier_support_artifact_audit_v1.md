# Verifier Support Artifact Audit v1

This is paper-facing synthesis from retained artifacts.

This does not create a final ranked leaderboard.

Support-layer metrics are not rewrite method ranking metrics.

| tool | retained_denominator_id | retained_pair_count | positive_pairs_found | negative_pairs_found | prove_count_found | refute_count_found | unknown_count_found | timeout_count_found | retained_support_rate | source_artifacts | readiness_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SQLSolver | support_pairs_4 | 4 | NA_not_found | NA_not_found | NA_not_found | NA_not_found | NA_not_found | NA_not_found | bounded_3_over_4_support_smoke | docs/_scratch/BASELINE_EVIDENCE_MATRIX_CURRENT_v1.md;reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json;docs/_scratch/SQLSOLVER_EXTERNAL_SUBSTRATE_ACQUISITION_AUDIT_v1.md | smoke_only | Retained evidence confirms a 4-pair bounded smoke and 3 over 4 support rate but does not expose a clean per-verdict prove refute unknown timeout breakdown in the evaluation folder |
| VeriEQL | cons_0035_pairs_2 | 2 | 1 | 1 | 0 | 2 | 0 | 0 | bounded_1.0_on_2_pairs_caveated | docs/_scratch/VERIEQL_SUPPORT_CANARY_v0.md;docs/_scratch/BASELINE_EVIDENCE_MATRIX_CURRENT_v1.md | canary_only | Negative refutation is clean support evidence while the positive pair is constraint-sensitive and should remain caveated |

## Interpretation notes

- SQLSolver and VeriEQL are support/verifier tools, not rewrite generators.
- The retained artifacts are bounded smoke or canary packets rather than denominator-complete support tables.
- No row here should be read as CONS9-complete verifier support unless a dedicated retained packet later proves that scope.
