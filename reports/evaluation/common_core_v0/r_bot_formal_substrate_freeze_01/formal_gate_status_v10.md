# Formal Gate Status v10

## Scope

This document updates the formal gate status after the DOI-backed StackOverflow
ZIP retention manifest update.

It incorporates:

- [formal_stackoverflow_zip_retention_manifest_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_zip_retention_manifest_v2.json)
- [formal_stackoverflow_zip_retention_manifest_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_zip_retention_manifest_v2.csv)
- [formal_gate_status_v9.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v9.md)
- [formal_gate_status_v9.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v9.json)
- [formal_gate_status_v8.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v8.md)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- ZIP external provenance blocker closed: `yes`
- DOI recorded:
  - `https://doi.org/10.5281/zenodo.20087267`
- expected filename preserved:
  - `stackoverflow-rewrite-embed.zip`
- expected outer SHA-256 preserved:
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- `current_benchmark_gate_ready`: `false`
- formal `R-Bot @120` generation may start: `no`

## What Closed In v10

Closed by this package:

1. the ZIP external retained URI/provenance blocker is now closed at the manifest layer
2. the DOI landing page is recorded as:
   - `https://doi.org/10.5281/zenodo.20087267`
3. the expected filename remains frozen as:
   - `stackoverflow-rewrite-embed.zip`
4. the expected outer ZIP SHA-256 remains frozen as:
   - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
5. the per-entry hashes remain preserved from the existing ZIP manifest

Closure basis used here:

- DOI present
- expected filename present
- expected outer SHA-256 present and unchanged

## What Did Not Close

The full formal gate does not open in v10.

Remaining blockers carried forward:

1. formal Chroma index identifier / rebuild
2. runtime/dependency lock
3. retained run-path artifact-contract validation

These remain sufficient to keep:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Gate Outcome

The ZIP provenance blocker is closed.

The overall formal gate remains closed.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

v10 closes the StackOverflow ZIP external provenance blocker using the Zenodo
DOI-backed retention manifests.

Formal `R-Bot @120` generation still may not start because the formal Chroma
index identifier/rebuild, runtime/dependency lock, and retained run-path
artifact-contract validation blockers remain open.
