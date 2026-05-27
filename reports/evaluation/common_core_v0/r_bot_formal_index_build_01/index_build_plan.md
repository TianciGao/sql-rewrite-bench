# R-Bot Formal Chroma Index Build Plan

## Scope

This package defines the human-run build and inspection workflow for the formal
`R-Bot` Chroma index.

It does not execute the build in this package creation step.
It does not authorize benchmark execution.

## Frozen Inputs

- corpus artifact URI:
  - `https://doi.org/10.5281/zenodo.20087267`
- expected ZIP filename:
  - `stackoverflow-rewrite-embed.zip`
- expected outer ZIP SHA-256:
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- extraction contract:
  - `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_extraction_contract.md`
- field mapping:
  - `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_field_mapping.csv`
- embedding model:
  - `text-embedding-3-small`
- rule-vector width:
  - `100`
- total dimension:
  - `3172`
- retrieval `top_k`:
  - `10`
- reranking mode:
  - `rrf`
- `rrf_k`:
  - `60`
- similarity threshold:
  - `explicit none`

## Human-Run Flow

1. Run `run_manual_r_bot_formal_index_build.py` in `--dry-run` mode first.
2. Review the generated build report and identifier preview.
3. Confirm the helper is reading the frozen `formal_zip_text_manifest_v1.csv` and `formal_zip_text_hashes_v1.json` package rather than defining an independent row count.
4. Confirm ZIP provenance closure is read from `formal_stackoverflow_zip_retention_manifest_v2.json` rather than from the stale blocker fields inside the older text-manifest package.
5. If dry-run metadata is intended to preview a formal run path, pass `--provider-family` explicitly.
6. `--execute-build` now targets a real provider-free corpus build that reuses retained ZIP embeddings and computes the `100`-dimensional rule vector locally.
7. If a stored semantic component is malformed or a non-empty template lacks its retained embedding, the build must fail closed with a precise status.
8. The inspect helper should be used after build to verify the resulting collection count and stored embedding dimension.

## Output Root

Default formal index output directory:

- `/tmp/rewritebench_rbot_formal_chroma_index_01`

The build scripts do not copy index files into the repo.

## Required Identifier Fields

The final retained identifier must include:

- `index_id`
- `build_timestamp`
- `corpus_artifact_uri`
- `corpus_sha256`
- `expected_zip_filename`
- `extraction_contract_version`
- `embedding_model`
- `embedding_provider_base_url_family`
- `rule_vector_width`
- `total_dimension`
- `retrieval_top_k`
- `reranking_mode`
- `rrf_k`
- `similarity_threshold`
- `similarity_threshold_policy`
- `chroma_collection_name`
- `index_file_hashes`
- `build_script_command`
- `index_directory`

Dry-run preview behavior:

- if `--provider-family` is absent, provider status must be `missing_provider_family`
- if `--provider-family` is supplied, provider status must be `provider_family_recorded`
- dry-run row counts must come from the frozen manifest package, not a fresh ZIP recount
- ZIP provenance closure must come from the retained v2 ZIP retention manifest, not the stale `formal_retention_blocker` field embedded in the older text-manifest package
- execute-build must not call an embedding provider when retained ZIP vectors are present
- execute-build may use explicit upstream-compatible zero-filled fallback vectors only for the known upstream empty-sql or empty-template cases, and those counts must be retained in metadata

## Current Gate Meaning

Expected answer remains:

- formal Chroma index blocker closed: `no`
- formal `R-Bot @120` generation may start: `no`

This package provides the build tooling only.
It does not close the formal Chroma index blocker.
