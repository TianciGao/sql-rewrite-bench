# Formal Corpus Text Manifest Summary

## Status

- manifest id: `formal_corpus_text_manifest_v1`
- corpus candidate rows: `34`
- path status `tmp_only`: `34`
- path status `repo_retained`: `0`
- path status `external_retained`: `0`
- path status `missing`: `0`

## Text Availability

- text-readable rows: `31`
- non-text rows: `3`
- included for formal retrieval: `32`
- included for contamination check: `32`
- text-readable rows included for contamination check: `31`
- non-text rows included for contamination check: `1`

## Candidate Breakdown

- structural directory anchors:
  - `2`
  - `llm4rewrite_clone_root`
  - `knowledge_base_root`
- text-readable retrieval corpus rows:
  - `31`
  - `rule_cluster_summaries_structured.jsonl`
  - `30` `rule_cluster_funcs/*.py` files
- binary retrieval archive rows:
  - `1`
  - `stackoverflow-rewrite-embed.zip`

## Gate Interpretation

Current corpus text availability status: `partial`

What improved relative to the old blocker:

- visible text-readable retrieval corpus items are now explicitly enumerated
- the blanket `manifest_text_unavailable` interpretation is no longer necessary for the visible knowledge-base text files
- the single remaining text-availability blocker inside the retrieval corpus line is now precise:
  - `stackoverflow-rewrite-embed.zip` is binary-only in this package

What remains blocked:

- the formal retrieval corpus line still includes the binary-only archive
- all visible corpus items are still `/tmp`-only rather than formally retained
- retained external provenance for the ZIP archive is still missing

## Sufficiency

### Near-duplicate checker

- meaningful rerun against visible text corpus subset: `yes`
- full formal closure after this package alone: `no`

Reason:

- `31` text-readable included corpus rows now exist
- `1` included retrieval item remains binary-only and therefore not text-checkable

### Generated-output exclusion checker

- meaningful rerun against visible text corpus subset: `yes`
- full formal closure after this package alone: `no`

Reason:

- the same binary-only retrieval archive remains unresolved
- the separate Calcite source-path issue is not a corpus-text issue and must be handled independently

## Bottom Line

This package closes the broad ambiguity around visible corpus text.

It does **not** close the formal contamination gate, because `stackoverflow-rewrite-embed.zip` remains included, binary-only, and not yet retained through an external provenance handle or equivalent deterministic text-readable expansion.
