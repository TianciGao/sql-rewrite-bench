# Formal Gate Status v8

## Scope

This document updates the formal gate status after the ZIP-aware contamination
checks.

It incorporates:

- [formal_zip_text_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_v1.csv)
- [formal_zip_text_hashes_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_hashes_v1.json)
- [formal_zip_text_manifest_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_summary.md)
- [formal_near_duplicate_check_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_v1.csv)
- [formal_near_duplicate_check_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_summary.md)
- [formal_generated_output_exclusion_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_v1.csv)
- [formal_generated_output_exclusion_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_summary.md)
- [formal_generated_output_hashes_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_hashes_v1.json)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- ZIP text manifest extracted text rows: `18744`
- ZIP text was included in contamination checks: `yes`
- near-duplicate failures: `0`
- generated-output exact matches: `0`
- `corpus_text_unavailable` blockers: `0`
- generated-output family blockers: `0`
- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## ZIP-Aware Contamination State

### ZIP Text Manifest

- ZIP path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- ZIP SHA-256 verified:
  - `yes`
- extracted text rows:
  - `18744`
- ZIP text included in contamination checks:
  - `yes`

### Near-Duplicate Check

- rows covered: `40`
- near-duplicate failures: `0`
- rows blocked by retention/provenance: `40`
- rows blocked by corpus text unavailability: `0`
- visible flat-file included manifest items: `31`
- ZIP-derived text rows available: `18744`

Interpretation:

- no near-duplicate failures were found
- ZIP-derived text was included in the check
- the checker remains blocked only on retention/provenance

### Generated-Output Exclusion

- rows covered: `357`
- generated-output exact matches: `0`
- rows blocked by retention/provenance: `357`
- rows blocked by corpus text unavailability: `0`
- visible flat-file included manifest items: `31`
- ZIP-derived text rows available: `18744`
- generated-output family blockers: `0`

Interpretation:

- no generated-output exact matches were found
- ZIP-derived text was included in the check
- the checker remains blocked only on retention/provenance

## Remaining Blockers

1. ZIP external retained URI/provenance for `stackoverflow-rewrite-embed.zip`
2. formal index identifier/rebuild
3. runtime lock
4. artifact-contract validation

## Gate Outcome

The overall formal gate remains closed.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

The ZIP-aware contamination checks are now materially closed at the text and
comparison layer:

- `18744` ZIP text rows were extracted
- ZIP text was included in contamination checks
- near-duplicate failures remain `0`
- generated-output exact matches remain `0`
- `corpus_text_unavailable` blockers are `0`
- generated-output family blockers are `0`

The gate still does not open because retained ZIP provenance, formal index
rebuild/identifier, runtime lock, and artifact-contract validation remain open.
