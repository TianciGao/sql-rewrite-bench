# Index Dry-Run Consistency Review

## Scope

This review checks the dry-run consistency of:

- [formal_chroma_index_build_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_build_report_v1.md)
- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)
- [formal_zip_text_manifest_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_summary.md)
- [formal_zip_text_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_v1.csv)
- [formal_zip_text_extraction_contract.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_extraction_contract.md)
- [run_manual_r_bot_formal_index_build.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/run_manual_r_bot_formal_index_build.py)

No databases were run. No SQL was executed. No API or build step was executed.

## Conclusion

- ZIP SHA-256 verification is internally consistent.
- The `18745` versus `18744` discrepancy is a counting-policy difference, not evidence of a true extraction-contract mismatch.
- The build helper should reuse `formal_zip_text_manifest_v1.csv` or its retained row counts instead of independently recounting directly from the ZIP.
- `embedding_provider_base_url_family` should be explicit in retained metadata for any execute-build run.
- A rerun with `--provider-family api.gptsapi.net` is sufficient to populate that metadata field, but it is not sufficient to make the build formally ready.
- The current `--execute-build` path does not populate embeddings or build a full retrieval index; it only creates a Chroma shell and then fails closed.
- Execute-build is not the safe next formal step yet.
- Formal `@120` generation may not start.

## Row Count Discrepancy

The dry-run build report records `18745` extracted rows [formal_chroma_index_build_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_build_report_v1.md:5), while the frozen substrate summary records `18744` [formal_zip_text_manifest_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_summary.md:5).

The per-entry delta is also isolated to the rules member:

- dry-run identifier: `stackoverflow-rewrite-rules-query-optimization.jsonl = 6585`
- frozen manifest summary: `stackoverflow-rewrite-rules-query-optimization.jsonl = 6584`

Cause:

- The frozen manifest generator normalizes text and drops rows whose normalized text is empty. That behavior is explicit in `normalize_text()` and `maybe_add_row()` [run_manual_r_bot_formal_zip_text_manifest.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_zip_text_manifest.py:64) [run_manual_r_bot_formal_zip_text_manifest.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_zip_text_manifest.py:78).
- The build helper recounts rows directly from the ZIP and accepts any field whose raw string is non-empty after `strip()`, without applying the same normalization gate [run_manual_r_bot_formal_index_build.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/run_manual_r_bot_formal_index_build.py:77).

Read-only inspection of the ZIP identified one extra counted item in `stackoverflow-rewrite-rules-query-optimization.jsonl`: record `385`, field `schema`, whose value is only a SQL line comment:

`-- No CREATE TABLE statements are needed as the query generates data on-the-fly using SELECT statements from UNIONs.`

Under the freeze contract normalization, that text collapses to empty and is therefore excluded from `formal_zip_text_manifest_v1.csv`. Under the dry-run build helper, it is still counted because the raw string is non-empty before normalization.

Assessment:

- This is not a substantive extraction mismatch.
- This is a reporting/counting mismatch between:
  - contract-compliant normalized manifest counting
  - non-normalized recounting in the index dry-run helper

## Reuse Of Frozen Manifest

The rebuild recipe says the formal rebuild must use the frozen corpus manifest only [formal_chroma_index_rebuild_recipe.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_chroma_index_rebuild_recipe.md:63).

Current helper behavior does not do that. It independently streams the ZIP and derives `extracted_text_row_count` again [run_manual_r_bot_formal_index_build.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/run_manual_r_bot_formal_index_build.py:134).

Review answer:

- Should `run_manual_r_bot_formal_index_build.py` reuse `formal_zip_text_manifest_v1.csv` instead of independently streaming the ZIP? `yes`

Reason:

- the frozen manifest is the retained contract artifact
- it already encodes the normalization policy
- it avoids future drift in row counts and per-entry counts
- it keeps the index metadata aligned with the substrate-freeze evidence package

If direct ZIP validation is still desired, it should be limited to:

- ZIP filename check
- ZIP SHA-256 check
- member SHA-256 check

The reported extracted row counts should come from the frozen manifest or from `formal_zip_text_hashes_v1.json`, not from an independent recount path.

## Provider Family Metadata

The gate requires retained metadata to include `embedding_provider_base_url_family` [formal_chroma_index_rebuild_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_chroma_index_rebuild_gate_v1.md:11). The current dry-run identifier records this field as `null` [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json:1).

Review answers:

- must `embedding_provider_base_url_family` be passed explicitly? `yes`, for any retained execute-build metadata record
- is a rerun with `--provider-family api.gptsapi.net` sufficient for metadata? `yes`, for this field only, assuming that is the actual intended provider/base URL family

But that rerun is not sufficient for overall formal readiness because other blockers remain:

- no actual built index hashes are retained
- the helper does not populate embeddings
- the external archive provenance / retention blocker remains open
- the formal gate still says generation may not start [formal_chroma_index_rebuild_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_chroma_index_rebuild_gate_v1.md:3)

## What Execute-Build Would Do

Current helper behavior for `--execute-build`:

1. import `chromadb`
2. create the target directory
3. create or open the named Chroma collection
4. require `--provider-family`
5. raise a runtime error stating that actual embedding population is intentionally not automated [run_manual_r_bot_formal_index_build.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/run_manual_r_bot_formal_index_build.py:192)

Review answer:

- would execute-build call an embedding API or only build from existing vectors? `neither, in the current implementation`

It does not consume existing retained vectors, and it does not implement embedding population. It only creates a Chroma shell and then stops with an explicit failure message. The message also makes clear that any real embedding population would require explicit human wiring for embedding/API execution.

## Safe Next Step

Review answers:

- is execute-build safe to run next? `no`
- may formal `@120` generation start? `no`

Reason:

- the dry-run metadata is internally inconsistent on extracted row count
- the helper is not yet aligned to the frozen manifest contract
- `embedding_provider_base_url_family` is still null
- execute-build does not actually produce a populated formal index
- formal gate status remains blocked [formal_chroma_index_rebuild_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_chroma_index_rebuild_gate_v1.md:29)

## Recommended Pre-Build Corrections

Before any formal execute-build step, the helper should be corrected so that:

1. extracted row counts are sourced from `formal_zip_text_manifest_v1.csv` or `formal_zip_text_hashes_v1.json`
2. dry-run and substrate-freeze counts cannot diverge on normalization policy
3. `embedding_provider_base_url_family` is passed explicitly into retained metadata
4. the execute-build contract is clarified as either:
   - metadata-only shell creation, not a build, or
   - a real embedding/index build path with explicit external API semantics and retained output hashes

Until those conditions are closed, the dry-run should be treated as informative but not execute-ready.
