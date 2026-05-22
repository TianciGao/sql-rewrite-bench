# Formal Chroma Index Rebuild Plan v2

## Scope

This package updates the formal `R-Bot` Chroma index blocker after ZIP
provenance closure.

It does not execute a rebuild.
It does not authorize benchmark execution.

## Current Answer

- formal Chroma index blocker closed: `no`
- current visible `/tmp` index acceptable as formal evidence: `no`
- formal `R-Bot @120` generation may start: `no`

## Frozen Inputs

### Formal Corpus Input

- corpus artifact URI:
  - `https://doi.org/10.5281/zenodo.20087267`
- expected ZIP filename:
  - `stackoverflow-rewrite-embed.zip`
- expected outer ZIP SHA-256:
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- extraction contract:
  - [formal_zip_text_extraction_contract.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_extraction_contract.md)

### Retrieval / Vector Settings

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

## Required Formal Index Identifier Fields

The future retained index identifier must record all of the following:

1. `index_id`
2. `build_timestamp`
3. `corpus_artifact_uri`
4. `corpus_sha256`
5. `extraction_contract_version`
6. `embedding_model`
7. `embedding_provider_base_url_family`
8. `rule_vector_width`
9. `total_dimension`
10. `chroma_collection_name`
11. `index_file_hashes`
12. `build_script_command`

Minimum interpretation of these fields:

- `corpus_artifact_uri`
  - `https://doi.org/10.5281/zenodo.20087267`
- `corpus_sha256`
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- `extraction_contract_version`
  - reference to the frozen ZIP extraction contract
- `embedding_provider_base_url_family`
  - provider/base URL family only, without secrets

## Why The Current `/tmp` Index Cannot Be Accepted

Current visible index:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`

It cannot be accepted as formal evidence because:

1. it is scratch-only `/tmp` lineage
2. no retained formal `index_id` exists
3. no retained formal build timestamp exists
4. no retained formal build command identity exists
5. no retained formal collection name and file-hash package exists
6. it predates the now-closed DOI-backed corpus provenance package and the now-frozen retrieval settings package

So the expected answer remains:

- current visible `/tmp` index acceptable: `no`

## Conditions That Close The Index Blocker

The formal Chroma index blocker becomes closed only when all of the following
are retained:

1. a real `index_id`
2. retained build metadata with timestamp
3. corpus URI and corpus SHA-256
4. extraction contract reference
5. embedding model identity
6. provider/base URL family without secrets
7. rule-vector width `100`
8. total dimension `3172`
9. collection name
10. retained index file hashes if the rebuilt index files are retained
11. exact build script/command identity

## Required Failure Rule

The rebuild must remain blocked if any of the following are missing:

- `index_id`
- build timestamp
- corpus URI
- corpus SHA-256
- extraction contract reference
- embedding model
- provider/base URL family
- rule-vector width
- total dimension
- collection name
- build command identity

## Remaining Blockers Carried Forward

1. runtime/dependency lock
2. retained run-path artifact-contract validation

These are separate from the index-identifier blocker and remain open even after
this planning package.

## Bottom Line

The Chroma index blocker is not closed by this package.

This package converts the blocker into an explicit retained-metadata contract
and confirms that the visible `/tmp` index is not formal evidence.
