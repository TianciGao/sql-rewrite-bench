# Formal Gate Status v5

## Scope

This document updates the formal gate status after the similarity-threshold audit package.

It incorporates:

- [formal_similarity_threshold_audit.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_similarity_threshold_audit.md)
- [formal_similarity_threshold_audit.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_similarity_threshold_audit.json)
- [formal_retrieval_config_v4.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v4.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- similarity threshold closed as explicit none or remains blocked: `closed as explicit_none_observed`
- updated retrieval config status: `similarity_threshold_closed_other_substrate_items_still_blocked`
- formal `R-Bot @120` generation may start: `no`
- `current_benchmark_gate_ready`: `false`

## What Closed In v5

Closed by the similarity-threshold audit:

1. the retrieval path now has an explicit formal interpretation for `similarity_threshold`
2. `similarity_threshold` is no longer treated as unresolved
3. the correct formal reading is:
   - `similarity_threshold.value = null`
   - `similarity_threshold.status = explicit_none_observed`

Why this closure is valid:

- visible retrieval code explicitly uses `similarity_top_k`
- visible retrieval code explicitly uses reciprocal-rank reranking
- visible retrieval code does not show a retrieval-time threshold parameter
- visible retrieval code does not show a score-cutoff filter
- the only visible `threshold` hit is in non-retrieval statistical comparison code

## Retrieval Status After v5

Resolved at the retrieval-config layer:

- `top_k = 10`
- `reranking_mode = rrf`
- `rrf_k = 60`
- `similarity_threshold = explicit_none_observed`
- embedding model candidate `= text-embedding-3-small`
- rule-vector width `= 100`
- total dimension `= 3172`

Still unresolved at the retrieval/substrate layer:

- retained rebuild-time embedding provider/base_url identity
- formal rebuilt index identifier
- corpus manifest completeness
- retained external archive provenance

## Remaining Blockers

1. exact retained rebuild-time embedding provider/base_url identity is still not fully attested
2. formal rebuilt `chroma_db` index package and retained formal index identifier do not yet exist
3. corpus manifest is still not complete enough for deterministic retained rebuild
4. retained external provenance handle for `stackoverflow-rewrite-embed.zip` is still missing
5. dependency lock is still candidate-only rather than a complete retained final lock
6. retained runtime package snapshot and environment metadata path do not yet exist
7. contamination attestation is still blocked because all `40` rows remain blocked
8. exact generated-output contamination hits remain present on `11` rows and must be resolved or formally excluded in the retained corpus/output line
9. manifest-side contamination coverage is incomplete because current included manifest entries are not all text-readable hashable items
10. generated-output contamination coverage is incomplete because the visible `calcite` generated family is missing
11. machine-readable near-duplicate exclusion checking is not implemented
12. the future retained run package has not yet been validated as satisfying the full artifact contract

## Gate Outcome

The similarity-threshold gate is now closed.

The overall formal gate remains closed.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

This package resolves the threshold ambiguity cleanly:

- `similarity_threshold_policy = explicit_none_observed`

That closes one retrieval-config blocker, but formal `@120` generation remains blocked by contamination, corpus, index, runtime, and artifact-contract gates.
