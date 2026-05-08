# Formal Gate Status v5

## Scope

This document updates the formal gate status after the similarity-threshold
audit and retrieval-config v4 update.

It incorporates:

- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)
- [r_bot_paper_parameter_extraction_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_paper_parameter_extraction_v1.md)
- [formal_retrieval_config_extracted_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_extracted_v1.json)
- [formal_retrieval_config_v3.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v3.json)
- [formal_retrieval_config_v4.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v4.json)
- [formal_similarity_threshold_audit.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_similarity_threshold_audit.md)
- [formal_similarity_threshold_audit.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_similarity_threshold_audit.json)
- [formal_gate_status_v4.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v4.md)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- similarity-threshold gate: `closed_as_explicit_none_observed`
- updated retrieval config status: `similarity_threshold_closed_other_retrieval_and_artifact_gates_still_blocked`
- formal `R-Bot @120` generation may start: `no`
- `current_benchmark_gate_ready`: `false`

## What Closed In v5

Closed by this package:

1. the remaining retrieval-config ambiguity around similarity threshold is now resolved
2. the visible retrieval implementation supports:
   - `top_k = 10`
   - reranking mode `rrf`
   - `rrf_k = 60`
   - no active retrieval-time similarity threshold filter observed
3. the benchmark-common retrieval statement may now freeze:
   - `similarity_threshold.value = null`
   - `similarity_threshold.status = explicit_none_observed`

## Evidence Basis

Visible retrieval code shows:

- `similarity_top_k` is passed into retrievers:
  - [`rag_retrieve.py:66`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:66>)
  - [`rag_retrieve.py:68`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:68>)
  - [`rag_retrieve.py:89`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:89>)
  - [`rag_retrieve.py:119`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:119>)
- reciprocal-rank fusion is the active reranking mode:
  - [`rag_retrieve.py:68`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:68>)
  - [`my_query_fusion_retriver.py:29`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:29>)
- reciprocal-rank `k=60` is visible:
  - [`my_query_fusion_retriver.py:136`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:136>)
  - [`my_query_fusion_retriver.py:144`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:144>)
- the active retrieval path returns reranked results sliced to top-k, with no
  visible threshold filter:
  - [`my_query_fusion_retriver.py:329`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:329>)
  - [`my_query_fusion_retriver.py:363`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:363>)

## What Did Not Count As Retrieval Threshold Evidence

Not counted as retrieval-threshold evidence:

1. score normalization in non-default fusion modes
2. statistical comparison threshold in `my_rewriter/db_utils.py`
3. benchmark speedup/tie/regression thresholds in `scripts/cli.py`

These are real thresholds in other contexts, but not a retrieval-time
similarity cutoff for `R-Bot`.

## What Remains Open

The similarity-threshold gate is now closed, but the overall formal gate is not.

Still open:

1. exact retained rebuild-time embedding provider/base_url identity
2. formal rebuilt `chroma_db` index package and retained formal index identifier
3. contamination and corpus-retention gates
4. retained runtime package snapshot and environment metadata path
5. dependency lock finalization
6. retained artifact-contract closure

## Gate Outcome

This package closes only the threshold-or-none ambiguity.

It does not close:

- contamination
- corpus provenance
- rebuilt formal index
- retained runtime/dependency closure
- retained artifact contract

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

The visible evidence is sufficient to freeze the similarity-threshold question
as:

- `explicit_none_observed`

The overall formal gate remains closed for other retained-evidence reasons.
