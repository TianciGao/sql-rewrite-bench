# Formal Gate Status v11

## Scope

This document updates the formal gate status after the successful human-run
formal Chroma index build and inspect for R-Bot.

It incorporates:

- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)
- [formal_chroma_index_build_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_build_report_v1.md)
- [formal_chroma_index_inspect_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_inspect_report_v1.md)
- [formal_rule_vector_catalog_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_rule_vector_catalog_v1.json)
- [formal_gate_status_v10.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v10.md)
- [formal_chroma_index_rebuild_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_chroma_index_rebuild_gate_v1.md)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- formal Chroma index built: `yes`
- formal Chroma index inspected successfully: `yes`
- corpus artifact URI recorded: `yes`
- corpus SHA-256 recorded: `yes`
- extraction contract version recorded: `yes`
- embedding model recorded: `yes`
- embedding provider/base_url family recorded: `yes`
- `rule_vector_width = 100` recorded: `yes`
- `total_dimension = 3172` recorded: `yes`
- frozen `30 + 70` rule-vector catalog retained: `yes`
- index file hashes retained: `yes`
- formal Chroma index blocker closed: `yes`
- `current_benchmark_gate_ready`: `false`
- formal `R-Bot @120` generation may start: `no`

## Evidence Summary

### Build

The retained formal build report records:

- build executed: `yes`
- ZIP SHA-256 verified: `yes`
- extracted text row count: `18744`
- embedding model: `text-embedding-3-small`
- provider/base_url family: `api.gptsapi.net`
- rule-vector width: `100`
- total dimension: `3172`
- collection document count: `5507`
- verified embedding dimension: `3172`
- build status: `built_real_index_gate_still_closed`

### Inspect

The retained formal inspect artifacts record:

- `index_id = r_bot_formal_chroma_index_01`
- collection name: `r_bot_formal_stackoverflow`
- collection document count: `5507`
- verified embedding dimension: `3172`
- index file count: `6`
- inspect status: `inspected_existing_index_gate_still_closed`

### Identifier Metadata

The retained formal identifier records:

- `corpus_artifact_uri = https://doi.org/10.5281/zenodo.20087267`
- `corpus_sha256 = e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- `expected_zip_filename = stackoverflow-rewrite-embed.zip`
- `extraction_contract_version = reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_extraction_contract.md`
- `embedding_model = text-embedding-3-small`
- `embedding_provider_base_url_family = api.gptsapi.net`
- `rule_vector_width = 100`
- `total_dimension = 3172`
- `index_file_hashes` for all retained index files under `/tmp/rewritebench_rbot_formal_chroma_index_01`

### Rule Catalog

The retained frozen rule-vector catalog records:

- `catalog_fully_frozen = true`
- `nl_rule_count = 30`
- `calcite_rule_count = 70`
- `unresolved_slot_count = 0`
- canonical slot partition:
  - NL vector slots `0-29`
  - Calcite vector slots `30-99`

## What Closed In v11

Closed by this package:

1. the formal Chroma index rebuild blocker is now closed
2. a retained formal index identifier now exists
3. the retained identifier records corpus URI, SHA-256, extraction contract, embedding model, provider family, rule-vector width, total dimension, collection name, file hashes, and build command
4. the retained formal inspect confirms the stored collection dimension is `3172`
5. the frozen `30 + 70` rule-vector catalog is now retained alongside the built index package
6. the prior rule-vector alignment blocker is now satisfied at the formal index materialization layer

## What Remains Blocked

The overall formal gate does not open in v11.

Remaining blockers:

1. runtime/dependency lock remains open
2. retained run-path artifact-contract validation remains open
3. denominator-aware formal run evidence has not yet been retained
4. the unresolved similarity-threshold/runtime attestation layer remains outside the newly closed index blocker

These remain sufficient to keep:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Gate Outcome

The formal Chroma index blocker is closed.

The overall formal generation gate remains closed.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

v11 closes the formal Chroma index blocker because a formal retained index was
built, inspected successfully, and recorded with the required metadata,
dimension, and file hashes, alongside the frozen `30 + 70` rule-vector
catalog.

Formal `R-Bot @120` generation still may not start because runtime/dependency
lock and retained run-path artifact-contract validation blockers remain open.
