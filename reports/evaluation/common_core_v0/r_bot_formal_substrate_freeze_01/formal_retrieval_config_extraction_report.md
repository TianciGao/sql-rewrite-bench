# Formal Retrieval Config Extraction Report

## Status

- top_k: `blocked_not_visible_in_config_text`
- reranking_mode: `blocked_not_visible_in_config_text`
- similarity_threshold: `blocked_not_visible_in_config_text`
- embedding_model_identity: `extracted`
- index_identifier: `scratch_only_visible_not_formal_evidence`
- rule_vector_width: `taken_from_formal_dimension_contract`
- total_dimension: `taken_from_formal_dimension_contract`

## Visible Sources

- config_file: visible at /tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/config.py
- prompt_file_rag: visible at /tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/prompts.py
- prompt_file_rewriter: visible at /tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/prompts.py

## Gate Impact

- formal gate open: `no`
- formal `R-Bot @120` generation may start: `no`
