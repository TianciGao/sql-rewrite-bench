# Formal Corpus Retention Plan

## Scope

This package classifies the visible `R-Bot` retrieval substrate for formal contamination and generated-output exclusion governance.

It is a retention and text-availability package only.
It does not run databases, execute SQL, call any API, run `R-Bot`, or open the formal gate.

Sources read for this package:

- [formal_gate_status_v6.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v6.md)
- [formal_gate_status_v6.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v6.json)
- [formal_near_duplicate_check_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_summary.md)
- [formal_generated_output_exclusion_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_summary.md)
- [formal_corpus_manifest_draft.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_manifest_draft.csv)
- [formal_corpus_index_audit.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_index_audit.csv)
- [r_bot_substrate_inventory.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_substrate_inventory.md)
- [r_bot_substrate_inventory.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_substrate_inventory.csv)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)
- [COMMON_CORE_V0_EVALUATION_PROTOCOL.md](/home/tianci_gao/code/sql-rewrite-bench/benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md)

## Direct Outcome

Current corpus text availability status: `partial`

What is now visible and classifiable:

- text-readable retrieval corpus items under `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
- a binary retrieval archive at `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- text-readable prompt/config source files under `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- tmp-only binary Chroma index artifacts
- the actual Calcite generated-output tree under `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generated`

What remains unresolved:

- the retrieval archive is still binary-only to this package
- the retrieval corpus line is still `/tmp`-only rather than formally retained
- retained external provenance for `stackoverflow-rewrite-embed.zip` is still missing

Therefore corpus text is **not yet sufficient** for full formal near-duplicate and generated-output exclusion closure.

## Visible Corpus Candidates

### Text-readable retrieval corpus candidates

These are visible and text-readable now:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_summaries_structured.jsonl`
- `30` Python files under `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_funcs/`

Observed properties:

- all are `/tmp`-only
- the summary file has a retained SHA-256 anchor
- each visible rule-function file is text-readable and hashable
- none of these text corpus files are yet repo-retained or externally retained

### Binary or non-text retrieval corpus candidates

These are visible but not text-readable corpus bytes for this package:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- Chroma anchor files such as `chroma.sqlite3`, `index_metadata.pickle`, and `header.bin`

Observed properties:

- the ZIP archive has a retained SHA-256 anchor
- the Chroma artifacts have anchor hashes but are index outputs, not readable corpus text
- none of these binary items can be honestly treated as text-readable contamination-check input

### Structural or policy-side candidates

These are visible but are not retrieval corpus text items:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/prompts.py`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/prompts.py`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/config.py`

Interpretation:

- the clone root and knowledge-base root are structural anchors
- the prompt/config files are text-readable policy sources
- they are useful for runtime reproducibility and audit
- they are not the retrieval corpus bytes whose contents must be contamination-checked

## Tmp-Only Status

The following visible substrate remains `/tmp`-only:

- upstream `LLM4Rewrite` clone root
- knowledge-base root
- rule summary file
- all `30` rule-function files
- retrieval archive ZIP
- prompt/config source files
- Chroma index build output

No visible retrieval corpus item in this package is currently `repo_retained` or `external_retained`.

## SHA-256 And Anchor Availability

Known hashes or anchors already visible:

- `rule_cluster_summaries_structured.jsonl`
  - `039823a6b5e87476dfc7a7be1cc9ac1bbeed31ec8972ceaa72364c1a56a03b5d`
- `stackoverflow-rewrite-embed.zip`
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- `rag/prompts.py`
  - `5d512e0ce872f9818731ef36afa997f50d762af2b40cf54e3f2897f0ee83a8fd`
- `my_rewriter/prompts.py`
  - `8343c81948836589d4b21c76e82bdc7d2e448afb57ca416805a87b054a0e3999`
- `my_rewriter/config.py`
  - `0440f9dfe5b7ee00f276f9edb3b8b776da5ada21829db2eafc5b7d1aa0bf98d8`
- the visible `30` rule-function files
  - individually hashable and enumerated in the new text manifest
- Chroma anchor files
  - visible but binary/index-only

## Retention Decision By Candidate Type

### Must be retained as text-readable corpus line

- `rule_cluster_summaries_structured.jsonl`
- all `30` `rule_cluster_funcs/*.py` files

Required action:

- retain them through a formal corpus text manifest and future retained artifact line

### Must be retained as external artifact or replaced by deterministic unpacked text line

- `stackoverflow-rewrite-embed.zip`

Required action:

- either assign retained external provenance to the exact ZIP bytes
- or materialize a deterministic unpacked text-readable manifest line derived from the same retained bytes

Important:

- until one of those happens this archive remains a formal contamination blocker

### Must be deterministically rebuilt rather than treated as retained corpus text

- the `LLM4Rewrite` clone root
- the knowledge-base root as a directory root
- the Chroma index outputs

Required action:

- keep remote, commit, dimensions, and anchor hashes
- rebuild from pinned inputs rather than copying the temporary binary index into the repo

## Sufficiency For Contamination Checks

### Near-duplicate checking

Current answer: `not yet sufficient for full formal closure`

Why:

- meaningful text input now exists for the rule summary plus `30` rule-function files
- but the formally included retrieval substrate still contains the binary-only `stackoverflow-rewrite-embed.zip`
- that archive remains text-unavailable to this package

Interpretation:

- a rerun can now be meaningful against the visible text corpus subset
- a rerun still cannot honestly produce full formal `pass` status for all contamination rows

### Generated-output exclusion checking

Current answer: `not yet sufficient for full formal closure`

Why:

- the same binary-only retrieval archive still blocks complete text-side exclusion attestation
- the old single Calcite blocker is separately a path-template issue, not a corpus-text issue

Interpretation:

- a rerun can now distinguish text-readable corpus rows from the archive blocker
- the formal gate must still remain closed

## Recommended Next Step

The next package should do two things, in this order:

1. use [formal_corpus_text_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_text_manifest_v1.csv) as the include-side text manifest for the human-run contamination and generated-output exclusion checkers
2. close the retained provenance or deterministic text expansion story for `stackoverflow-rewrite-embed.zip`

Until then:

- formal contamination rows should remain blocked
- formal `R-Bot @120` generation must not start
