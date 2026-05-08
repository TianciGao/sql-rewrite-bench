# Formal Retrieval Config Extraction Plan

## Role

This plan defines the human-run-only retrieval-config extraction utility for formal `R-Bot` gate closure.

The extractor must:

- inspect visible `R-Bot` and `LLM4Rewrite` substrate files only
- not execute `R-Bot`
- not call any API
- not execute SQL

## Inputs

Primary visible inputs:

1. `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_substrate_inventory.csv`
2. `scripts/cli.py`
3. visible upstream config/prompt files if they exist at the inventory paths:
   - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/prompts.py`
   - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/prompts.py`
   - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/config.py`
4. visible index anchor paths if they exist:
   - `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`

## Extraction Targets

The extractor must extract or mark blocked:

1. `top_k`
2. reranking mode
3. similarity threshold or explicit none
4. embedding model identity
5. index identifier
6. rule-vector width
7. total dimension

## Extraction Rules

`top_k`:

- extract only if a direct assignment or unambiguous literal is visible
- otherwise mark `blocked_not_visible_in_config_text`

Reranking mode:

- extract only if a direct assignment or explicit disable flag is visible
- otherwise mark `blocked_not_visible_in_config_text`

Similarity threshold:

- extract literal threshold if visible
- else extract explicit `none` only if the text clearly disables thresholds
- otherwise mark blocked

Embedding model identity:

- extract exact model string if visible
- if only provider family is visible, keep exact identity blocked

Index identifier:

- prefer visible path plus visible anchor hashes
- mark as scratch-only if the only visible identifier is the `/tmp` index path

Rule-vector width and total dimension:

- extract from visible patch notes or CLI-visible align-dimension metadata if unambiguous
- preserve formal contract values `100` and `3172` where already frozen in repo-local policy artifacts

## Required Outputs

The extractor must write:

1. `formal_retrieval_config_extracted_v1.json`
2. `formal_retrieval_config_extraction_report.md`

## Gate Impact

The extractor does not open the gate by itself.
It only produces machine-readable evidence about which retrieval settings are visible and which remain blocked.

