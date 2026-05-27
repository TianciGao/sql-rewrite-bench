# Formal Gate Status v3

## Scope

This document materializes the current formal gate state after:

- the human-run contamination hash check
- the retrieval config extraction

for:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

It is a gate-status document only.
It does not authorize generation.

## Direct Answers

- all 40 contamination rows pass: `no`
- why rows are still blocked: every row remains blocked because the checked artifact still has manifest text coverage gaps, generated-output coverage gaps, and no near-duplicate check implementation; 11 rows also have exact normalized hash matches in visible generated outputs
- near-duplicate checking implemented: `no`
- retrieval config fully frozen: `no`
- current_benchmark_gate_ready: `false`
- formal `R-Bot @120` generation may start: `no`

## Contamination Status

Sources:

- [formal_contamination_attestation_checked_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_attestation_checked_v1.csv)
- [formal_contamination_attestation_checked_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_attestation_checked_summary.md)
- [formal_contamination_hashes_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_hashes_v1.json)

Current result:

- rows covered: `40`
- rows passed: `0`
- rows blocked: `40`
- exact manifest matches found: `0`
- rows with exact generated-output matches: `11`
- row-level status: `blocked_partial_check_only`

Rows with exact normalized hash found in visible generated outputs:

- `PERF_0006`
- `CONS_0009`
- `CONS_0010`
- `CONS_0011`
- `CONS_0036`
- `CONS_0037`
- `PORT_0005`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`
- `LONGTAIL_0022`

Why all rows remain blocked even when no exact manifest match was found:

- the manifest-side check is incomplete, so the absence of a visible exact match is not sufficient evidence
- the generated-output-side check is incomplete, so the absence of a visible exact match is not sufficient evidence
- near-duplicate exclusion is required by policy and is not implemented by the checker

## Manifest And Generated-Output Blockers

Exact manifest blockers from the checked hash artifact:

- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_funcs`
- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`

Exact generated-output blockers from the checked hash artifact:

- `generated_source_missing:calcite:/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_same_engine_generation_01/generated`

Operational interpretation:

- manifest blockers are corpus-manifest visibility blockers, not pass results
- generated-output blockers are visible generated-family coverage blockers, not pass results
- because those blockers are global to the checked artifact, all 40 denominator rows remain blocked

## Retrieval Status

Sources:

- [formal_retrieval_config_extracted_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_extracted_v1.json)
- [formal_retrieval_config_extraction_report.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_extraction_report.md)
- [formal_gate_closure_checklist_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_closure_checklist_v1.md)

Retrieval config freeze status:

- `top_k`: `unresolved`
- reranking mode: `unresolved`
- threshold or explicit none: `unresolved`
- embedding model identity: `partially extracted but not formally closed`
- rule-vector width: `resolved`
- total dimension: `resolved`
- index identifier: `unresolved`

Exact extraction state:

- `top_k = null`, status `blocked_not_visible_in_config_text`
- `reranking_mode = null`, status `blocked_not_visible_in_config_text`
- `similarity_threshold = null`, status `blocked_not_visible_in_config_text`
- embedding model extraction recovered `provider_family = openai_compatible` and `value = text-embedding-3-small`, but the formal gate still lacks a fully retained exact rebuild-time provider/model/base_url identity attestation
- `rule_vector_width = 100`, status `taken_from_formal_dimension_contract`
- `total_dimension = 3172`, status `taken_from_formal_dimension_contract`
- index identifier is only visible as `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`, status `scratch_only_visible_not_formal_evidence`

Therefore:

- retrieval config fully frozen: `no`
- retrieval substrate formally resolved: `no`

## Gate Outcome

The formal gate remains closed.

`current_benchmark_gate_ready = false`

Formal `R-Bot @120` generation may not start.

## Exact Remaining Blockers

1. dependency lock is still candidate-only rather than a complete retained final lock
2. retained runtime package snapshot and environment metadata path do not yet exist
3. corpus manifest is still not complete enough for deterministic retained rebuild
4. retained external provenance handle for `stackoverflow-rewrite-embed.zip` is still missing
5. formal rebuilt `chroma_db` index package and retained formal index identifier do not yet exist
6. exact retrieval `top_k` is still not frozen
7. exact reranking mode is still not frozen
8. exact similarity threshold or explicit none is still not frozen
9. exact rebuild-time embedding provider/model/base_url identity is not yet fully retained as formal evidence
10. contamination attestation is still blocked because all 40 rows remain blocked
11. exact generated-output contamination hits remain present on 11 rows and must be resolved or formally excluded in the retained corpus/output line
12. manifest-side contamination coverage is incomplete because the current included manifest entries are not all text-readable hashable items
13. generated-output contamination coverage is incomplete because the visible `calcite` generated family is missing
14. machine-readable near-duplicate exclusion checking is not implemented
15. the future retained run package has not yet been validated as satisfying the full artifact contract

## Recommended Next Package

Recommended next package:

`formal_retrieval_and_contamination_closure_01`

Recommended contents:

1. replace non-text manifest include rows with a manifest-complete retained inventory that distinguishes text-hashable items from binary/container identities
2. assign retained provenance for `stackoverflow-rewrite-embed.zip`
3. freeze and retain exact `top_k`, reranking mode, threshold-or-none, and exact embedding provider/model/base_url identity
4. rebuild and retain the formal `chroma_db` index under the frozen `3172` contract and record the formal index identifier
5. close generated-output family coverage, including the current missing `calcite` generated root
6. implement and retain machine-readable near-duplicate checking
7. rerun the human contamination attestation so that all 40 rows can be evaluated on complete coverage rather than partial coverage

## Bottom Line

The human-run contamination hash check and retrieval config extraction materially improve observability, but they do not open the formal gate.

Current correct state remains:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`
