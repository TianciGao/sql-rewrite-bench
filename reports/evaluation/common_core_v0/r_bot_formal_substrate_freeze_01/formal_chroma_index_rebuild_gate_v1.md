# Formal Chroma Index Rebuild Gate v1

## Direct Answer

- formal Chroma index identifier exists: `no`
- current visible `/tmp` index acceptable: `no`
- formal `R-Bot @120` generation may start: `no`

## Gate Rule

The Chroma index blocker is closed only when a retained formal index metadata
record exists with:

- `index_id`
- `build_timestamp`
- `corpus_artifact_uri`
- `corpus_sha256`
- `extraction_contract_version`
- `embedding_model`
- `embedding_provider_base_url_family`
- `rule_vector_width`
- `total_dimension`
- `chroma_collection_name`
- `index_file_hashes` if retained
- `build_script_command`

## Current Classification

Current state:

- `blocked_missing_formal_index_identifier`

Why:

1. no retained `index_id` exists
2. no retained build metadata package exists
3. the only visible index is `/tmp` scratch lineage

## Remaining Non-Index Blockers

1. runtime/dependency lock
2. retained run-path artifact-contract validation

## Bottom Line

The index gate remains blocked.
Formal `R-Bot @120` generation may not start.
