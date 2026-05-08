# Formal Similarity Threshold Audit

## Scope

This audit resolves the remaining retrieval-config question around
`similarity_threshold` for formal `R-Bot @120`.

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
- [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py)
- visible files under `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`

## Direct Answer

The similarity-threshold gate is closed as:

- `similarity_threshold_policy = explicit_none_observed`

Meaning:

- no explicit retrieval-time similarity threshold was found in the visible
  `LLM4Rewrite` retrieval config/scripts
- visible retrieval behavior is top-k bounded and rerank-driven
- no score-cutoff filter was observed in the active retrieval path

This closes the threshold question specifically.
It does not open the overall formal gate.

## Distinguishing Threshold, Reranking, Top-K, And Filtering

### Top-k

Visible evidence:

- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test.py:15`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test.py:15>)
  defines `--topk` with default `10`
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test.py:25`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test.py:25>)
  binds `RETRIEVER_TOP_K = args.topk`
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:66`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:66>)
  calls `as_retriever(similarity_top_k=RETRIEVER_TOP_K)`
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:68`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:68>)
  passes `similarity_top_k=RETRIEVER_TOP_K` into `MyQueryFusionRetriever`
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:89`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:89>)
  uses `as_retriever(similarity_top_k=RETRIEVER_TOP_K)` in semantic retrieval
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:119`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:119>)
  uses `as_retriever(similarity_top_k=RETRIEVER_TOP_K)` in structure retrieval

Interpretation:

- top-k is explicit and visible
- retrieval breadth is bounded by count, not by score cutoff

### Reranking

Visible evidence:

- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:29`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:29>)
  defines reciprocal-rank fusion mode
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:68`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:68>)
  sets `mode=FUSION_MODES.RECIPROCAL_RANK`
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:121`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rag_retrieve.py:121>)
  sets `mode=FUSION_MODES.RECIPROCAL_RANK` for structure retrieval
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:136`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:136>)
  states the original paper uses `k=60`
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:144`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:144>)
  hardcodes `k = 60.0`

Interpretation:

- reranking is visible and explicit
- reranking parameter `k=60` is part of reciprocal-rank fusion, not a
  similarity score threshold

### Filtering

Visible evidence:

- the active retrieval path returns the reranked list sliced to top-k:
  - [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:329`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:329>)
  - [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:363`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:363>)
- no active retrieval branch compares node score against a user-visible minimum
  score or similarity cutoff

Interpretation:

- the observed filtering mechanism is rank truncation by `similarity_top_k`
- no additional retrieval-time score threshold was observed

### What Is Not A Retrieval Threshold

Not retrieval-threshold evidence:

- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:182`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:182>)
  to
  [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:220`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/my_query_fusion_retriver.py:220>)
  implements score normalization for non-default fusion modes
- [`/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/db_utils.py:26`](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/db_utils.py:26>)
  uses `threshold: float = 0.1` in statistical comparison logic, not retrieval
- `scripts/cli.py` contains benchmark/result thresholds such as
  `tie_threshold` and `regression_threshold`, but no `R-Bot` retrieval
  similarity threshold

## Negative Search Results

Targeted searches over visible `my_rewriter` and `rag` files found:

- explicit `similarity_top_k`
- explicit reciprocal rerank mode
- explicit `k = 60` for RRF

But did not find:

- `similarity_threshold`
- `score_threshold`
- `similarity_cutoff`
- `min_similarity`
- `min_score` used as active retrieval-time acceptance filter

## Paper And Formal-Freeze Interpretation

Paper/freeze layer still says:

- paper facts do not state a threshold
- prior formal freeze left threshold unresolved because no retained evidence had
  yet shown either a positive threshold or explicit none

Visible code audit now changes that interpretation:

- the paper still does not state a threshold
- the visible retrieval implementation shows top-k plus reranking
- no explicit threshold filter is observed

Therefore the correct formal statement is:

- `similarity_threshold.value = null`
- `similarity_threshold.status = explicit_none_observed`

## Gate Effect

This closes the similarity-threshold gate specifically.

It does **not** open formal `@120` generation.
Other blockers still remain, including:

1. retained rebuild-time embedding provider/base_url identity
2. formal rebuilt index identifier/package
3. contamination and corpus-retention gates
4. retained runtime/dependency/artifact-contract gates

## Bottom Line

The visible evidence is sufficient to close the similarity-threshold question
as:

- `explicit_none_observed`

The overall formal gate remains closed for reasons unrelated to threshold
ambiguity.
