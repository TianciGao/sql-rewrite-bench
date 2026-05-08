# Formal Similarity Threshold Audit

## Scope

This audit resolves the remaining formal `R-Bot` retrieval-config question around `similarity_threshold` for:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

It is a read-only audit.
It does not run databases.
It does not execute SQL.
It does not call any LLM/API.
It does not authorize generation.

## Inputs Read

- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)
- [r_bot_paper_parameter_extraction_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_paper_parameter_extraction_v1.md)
- [formal_retrieval_config_v3.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v3.json)
- [formal_retrieval_config_extracted_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_extracted_v1.json)
- [formal_gate_status_v4.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v4.md)
- [cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py)
- visible `LLM4Rewrite` files under `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`

## Audit Question

Can the formal similarity-threshold gate be closed as:

- `explicit_none_observed`

or must it remain:

- `blocked`

## Evidence Search Summary

The visible retrieval path was searched for:

- `similarity_threshold`
- `threshold`
- `score_threshold`
- `similarity_cutoff`
- score-based filtering terms
- `top_k`
- reranking / fusion mode

### Retrieval path findings

Visible retrieval code shows:

- [rag_retrieve.py](/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py) uses `stackoverflow_index.as_retriever(similarity_top_k=RETRIEVER_TOP_K)`
- the same file instantiates `MyQueryFusionRetriever(... mode=FUSION_MODES.RECIPROCAL_RANK, similarity_top_k=RETRIEVER_TOP_K ...)`
- [my_query_fusion_retriver.py](/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py) defines fusion modes including `RECIPROCAL_RANK = "reciprocal_rerank"`
- the same file hard-codes reciprocal-rank fusion with `k = 60.0`
- the same file truncates retrieval results by slicing to `[: self.similarity_top_k]`

### Threshold findings

No explicit retrieval-time threshold was found in the visible `R-Bot` retrieval path.

Specifically:

- no `similarity_threshold` parameter was found in visible retrieval config/code
- no score-cutoff filter was found before or after retrieval result fusion
- no threshold comparison was found in `rag_retrieve.py`
- no threshold comparison was found in `my_query_fusion_retriver.py`
- no threshold-related formal R-Bot CLI flag or benchmark-side wrapper flag was found in [cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py)

### Non-retrieval threshold hit

One visible `threshold` hit exists in:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/db_utils.py`

That threshold is:

- `compare(... threshold: float = 0.1)`

This is a statistical significance helper for timing/comparison logic, not a retrieval similarity-threshold control.

Therefore it must not be interpreted as retrieval-threshold evidence.

## Distinguishing The Parameters

### `top_k`

Explicitly observed in visible retrieval code:

- `similarity_top_k`
- default task-level paper freeze already set this to `10`

Interpretation:

- this is rank truncation / result-count control
- this is not a similarity score threshold

### Reranking

Explicitly observed in visible retrieval code:

- reciprocal-rank fusion mode
- `RRF k = 60`

Interpretation:

- this is fusion / reranking behavior
- this is not a similarity threshold

### Filtering

Observed retrieval filtering behavior:

- result slicing to `[: self.similarity_top_k]`

Not observed:

- score cutoff
- minimum similarity threshold
- confidence threshold
- post-fusion threshold pruning

### Similarity threshold

Observed state:

- not present in visible retrieval config text
- not present in visible retrieval code path
- not present as a visible benchmark-side CLI control for formal R-Bot

## Audit Decision

`similarity_threshold_policy = explicit_none_observed`

Reason:

- the visible retrieval implementation shows explicit `top_k` and explicit reranking/fusion
- the visible retrieval implementation does not show any retrieval-time threshold parameter or score-cutoff filter
- the only visible `threshold` symbol belongs to non-retrieval statistical comparison logic

Accordingly, the formal retrieval freeze may treat:

- `similarity_threshold.value = null`
- `similarity_threshold.status = explicit_none_observed`

This closes the similarity-threshold gate specifically.

## What Remains Open

Closing the similarity-threshold gate does **not** open formal `@120` generation.

Still open:

- retained rebuild-time embedding provider/base_url identity
- formal rebuilt index identifier
- corpus manifest completeness
- retained external provenance for `stackoverflow-rewrite-embed.zip`
- contamination closure
- generated-output coverage closure
- near-duplicate checker closure
- retained artifact-contract closure
- runtime/dependency closure

## Gate Impact

- similarity-threshold gate: `closed_as_explicit_none_observed`
- retrieval config overall: `still_blocked_on_other_items`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

The visible evidence is sufficient to close the similarity-threshold question as:

- `explicit_none_observed`

The overall formal gate remains closed for reasons unrelated to threshold ambiguity.
