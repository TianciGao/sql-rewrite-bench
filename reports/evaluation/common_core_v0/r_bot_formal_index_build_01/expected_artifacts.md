# Expected Artifacts

## Repo-Local Metadata Outputs

Human-run scripts in this package are expected to write:

- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)
- [formal_chroma_index_build_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_build_report_v1.md)
- [formal_chroma_index_inspect_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_inspect_report_v1.md)

## External Index Output

Default external index output root:

- `/tmp/rewritebench_rbot_formal_chroma_index_01`

Expected retained output shape outside the repo:

- Chroma index directory
- retained file hashes for produced index files
- collection name recorded in the identifier JSON

## Required Frozen Metadata In Identifier

- corpus artifact URI `https://doi.org/10.5281/zenodo.20087267`
- expected ZIP filename `stackoverflow-rewrite-embed.zip`
- corpus SHA-256 `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- embedding model `text-embedding-3-small`
- rule-vector width `100`
- total dimension `3172`
- retrieval `top_k = 10`
- reranking `rrf`
- `rrf_k = 60`
- similarity threshold policy `explicit_none_observed`

## Gate Note

Producing these artifacts does not by itself open the formal gate.
