# Formal Gate Status v2

## Scope

This document summarizes the current gate state after the retrieval/demo/contamination closure package update for:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

## Retrieval Status

- retrieval config file: [formal_retrieval_config_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v2.json)
- status: `partially_frozen_still_blocked`

Frozen now:

- rule-vector width `100`
- total dimension `3172 = 1536 + 100 + 1536`
- current `/tmp` index cannot be retained as formal evidence
- formal path is deterministic rebuild
- StackOverflow-derived retrieval examples are allowed only from the frozen retained corpus line

Still blocked:

- exact `top_k`
- exact reranking mode
- exact similarity threshold or explicit none
- exact embedding model identity attestation
- formal rebuilt index identifier

## Demo Policy Status

- demo selection policy file:
  [formal_demo_selection_policy_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_demo_selection_policy_v2.md)
- status: `shape_frozen_but_settings_blocked`

Frozen now:

- exclusion of all `common_core_v0_40` source SQL
- exclusion of any generated SQL from SQLGlot, Direct LLM, Calcite, and `R-Bot` PG1 recovery
- prohibition on manual retrieved-example swapping or post-target tuning
- exclusion requirement for exact and near-duplicate normalized SQL

## Contamination Status

- contamination CSV:
  [formal_contamination_attestation_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_attestation_v1.csv)
- contamination summary:
  [formal_contamination_attestation_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_attestation_summary.md)

Current result:

- rows covered: `40`
- passed rows: `0`
- blocked rows: `40`
- row status used where checks are missing: `blocked_pending_hash_check`

## Artifact Contract Status

- validation plan:
  [formal_artifact_contract_validation_plan.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_artifact_contract_validation_plan.md)
- current status: `defined_but_not_satisfied`

## Gate Outcome

- formal gate open: `no`
- current benchmark-ready: `false`
- formal `R-Bot @120` generation may start: `no`

## Exact Remaining Blockers

1. freeze exact retrieval `top_k`
2. freeze exact reranking mode
3. freeze exact similarity threshold, or attest explicit none
4. attest exact embedding model identity for the formal rebuild line
5. complete corpus manifest and external retrieval archive provenance closure
6. rebuild and retain the formal `chroma_db` index
7. complete machine-readable normalized hash checks for all 40 denominator cases
8. complete machine-readable exact-match exclusion checks
9. complete machine-readable near-duplicate exclusion checks
10. complete machine-readable generated-output exclusion attestation
11. produce a retained formal run package that satisfies the full artifact contract

## Bottom Line

The retrieval/demo/contamination package is materially more explicit now, but it does not open the formal gate.

Formal `R-Bot @120` generation remains blocked.

