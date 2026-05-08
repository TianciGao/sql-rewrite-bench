# Formal Gate Status v8

## Scope

This document updates the formal gate status after the human-run ZIP text
manifest, near-duplicate check, and generated-output exclusion check.

It incorporates:

- [formal_zip_text_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_v1.csv)
- [formal_zip_text_hashes_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_hashes_v1.json)
- [formal_zip_text_manifest_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_summary.md)
- [formal_near_duplicate_check_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_v1.csv)
- [formal_near_duplicate_check_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_summary.md)
- [formal_generated_output_exclusion_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_v1.csv)
- [formal_generated_output_exclusion_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_summary.md)
- [formal_generated_output_hashes_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_hashes_v1.json)
- [formal_gate_status_v7.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v7.md)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- ZIP text manifest extracted text rows: `18744`
- ZIP-derived text included in contamination checks: `yes`
- near-duplicate checking: `blocked_retention_provenance_missing`
- generated-output exclusion: `blocked_retention_provenance_missing`
- near-duplicate failures found: `0`
- generated-output matches found: `0`
- corpus_text_unavailable blockers: `0`
- generated-output family blockers: `0`
- `current_benchmark_gate_ready`: `false`
- formal `R-Bot @120` generation may start: `no`

## What Changed In v8

Closed relative to v7:

1. `stackoverflow-rewrite-embed.zip` is no longer treated as wholly unavailable text for checker consumption
2. the ZIP text manifest now contributes `18744` streamed text rows
3. ZIP-derived text is now included in both contamination checks
4. `corpus_text_unavailable` blockers are reduced to `0`
5. generated-output family blockers remain `0`

Not closed:

1. near-duplicate checking remains blocked by retention/provenance, not by text unavailability
2. generated-output exclusion remains blocked by retention/provenance, not by text unavailability
3. contamination attestation is still not formally complete because retained external provenance for the ZIP is still missing
4. the broader retained index/runtime/artifact-contract blockers carried in prior gate documents still remain open

## ZIP Text Manifest

- ZIP path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- ZIP SHA-256 verified:
  - `yes`
- extracted text rows:
  - `18744`
- streamed members:
  - `stackoverflow-rewrite-query-optimization.jsonl`: `2428`
  - `stackoverflow-rewrite-rules-query-optimization.jsonl`: `6584`
  - `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`: `5934`
  - `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`: `3798`
- ZIP-derived text included in contamination checks:
  - `yes`

## Checker Results After The Human-Run Rerun

### Near-Duplicate Check

- rows covered: `40`
- rows passed against visible text: `0`
- rows failed near-duplicate detection: `0`
- rows blocked by retention/provenance: `40`
- rows blocked by corpus text unavailability: `0`
- visible flat-file included manifest items: `31`
- ZIP-derived text rows available: `18744`
- corpus availability blockers: `0`
- gate interpretation: `blocked_retention_provenance_missing`

Interpretation:

- no near-duplicate failures were found against the visible flat-file plus ZIP-derived text view
- the checker did run against ZIP-derived text
- the outcome remains blocked because the ZIP still carries a formal retention blocker

### Generated-Output Exclusion

- rows covered: `357`
- rows passed against visible text: `0`
- rows failed generated-output exclusion: `0`
- rows blocked by retention/provenance: `357`
- rows blocked by corpus text unavailability: `0`
- visible flat-file included manifest items: `31`
- ZIP-derived text rows available: `18744`
- manifest blockers: `0`
- generated-output family blockers: `0`
- gate interpretation: `blocked_retention_provenance_missing`

Interpretation:

- no generated-output matches were found against the visible flat-file plus ZIP-derived text view
- the stale Calcite path blocker remains resolved
- the outcome remains blocked because the ZIP still carries a formal retention blocker

## Exact Remaining Blocker

The exact remaining primary blocker is now:

- retained external provenance / URI for `stackoverflow-rewrite-embed.zip`

Current blocker shape:

- ZIP text is visible and checker-consumable
- ZIP-derived text is included in contamination checks
- the archive remains `/tmp`-only
- retained external provenance / URI is still missing

Because of that:

- near-duplicate checking remains `formal_retention_blocked`
- generated-output exclusion remains `formal_retention_blocked`
- the formal gate remains closed

## Remaining Gate Blockers

1. retained external provenance / URI for `stackoverflow-rewrite-embed.zip` remains missing
2. exact retained rebuild-time embedding provider/model/base_url identity still requires final attestation
3. the formal rebuilt retained index identifier/package does not yet exist
4. dependency lock remains candidate-only rather than a retained final lock
5. retained runtime package snapshot and environment metadata path do not yet exist
6. the future retained run package has not yet been validated against the full artifact contract

## Gate Outcome

The overall formal gate remains closed.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

v8 closes the text-availability side of the last contamination blocker. The ZIP
now contributes `18744` streamed text rows, both contamination checkers include
that text, and neither checker found a substantive contamination failure.

However, the gate still does not open because retained external provenance / URI
for `stackoverflow-rewrite-embed.zip` is still missing, and the prior retained
index/runtime/artifact-contract blockers remain open.
