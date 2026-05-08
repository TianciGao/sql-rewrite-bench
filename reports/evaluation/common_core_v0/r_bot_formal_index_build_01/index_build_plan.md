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
3. If environment and dependencies are ready, rerun with `--execute-build`.
4. After build completion, run `run_manual_r_bot_formal_index_inspect.py`.
5. Review the retained identifier JSON and file-hash package.

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

## Current Gate Meaning

Expected answer remains:

- formal Chroma index blocker closed: `no`
- formal `R-Bot @120` generation may start: `no`

This package provides the build tooling only.
