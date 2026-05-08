# Expected Artifacts

## Repo-Local Metadata Outputs

Human-run scripts in this package are expected to write:

- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)
- [formal_chroma_index_build_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_build_report_v1.md)
- [formal_chroma_index_inspect_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_inspect_report_v1.md)

The build helper must derive extracted row metadata from:

- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_v1.csv`
- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_hashes_v1.json`

The build helper must derive ZIP provenance closure metadata from:

- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_zip_retention_manifest_v2.json`
- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_zip_retention_manifest_v2.csv`

## External Index Output

Default external index output root:

- `/tmp/rewritebench_rbot_formal_chroma_index_01`

Expected retained output shape outside the repo:

- Chroma index directory
- retained file hashes for produced index files
- collection name recorded in the identifier JSON

Current execute-build safety behavior:

- `--execute-build` must build the external Chroma directory only from retained ZIP contents and local rule-vector construction
- `--execute-build` must not call an embedding provider for corpus-side vector materialization
- malformed stored semantic vectors or missing non-empty template embeddings must fail closed with a precise status
- no incomplete Chroma directory should remain under the final retained path after a failed build

## Required Frozen Metadata In Identifier

- corpus artifact URI `https://doi.org/10.5281/zenodo.20087267`
- expected ZIP filename `stackoverflow-rewrite-embed.zip`
- corpus SHA-256 `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- ZIP external artifact URI
- ZIP retention status
- ZIP provenance closed flag
- ZIP retention manifest path
- embedding model `text-embedding-3-small`
- rule-vector width `100`
- total dimension `3172`
- collection document count
- verified stored embedding dimension
- zero-fill rule-vector fallback count
- zero-fill template-embedding fallback count
- retrieval `top_k = 10`
- reranking `rrf`
- `rrf_k = 60`
- similarity threshold policy `explicit_none_observed`

## Gate Note

Producing these artifacts does not by itself open the formal gate.
The formal Chroma index blocker remains closed.
