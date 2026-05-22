# Formal Gate Status v8 Draft

## Scope

This is a draft gate-status update after the `stackoverflow-rewrite-embed.zip` retention and text-extraction audit package.

It incorporates:

- [formal_gate_status_v7.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v7.md)
- [formal_stackoverflow_embed_zip_audit.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_embed_zip_audit.md)
- [formal_stackoverflow_embed_zip_manifest.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_embed_zip_manifest.csv)
- [formal_stackoverflow_embed_zip_text_availability.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_embed_zip_text_availability.md)
- [formal_stackoverflow_embed_zip_retention_decision.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_embed_zip_retention_decision.md)
- [formal_corpus_text_manifest_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_text_manifest_v2.csv)

It remains a draft only.
It does not authorize generation.

## Draft Direct Answers

- ZIP path visible: `yes`
- ZIP SHA-256 visible: `yes`
- ZIP contains usable text corpus: `yes`
- deterministic text extraction recipe can be written: `yes`
- archive is best classified as binary-only non-text corpus: `no`
- contamination checkers can rerun as-is: `no`
- contamination checkers can rerun meaningfully after a small checker-side extraction support package: `yes`
- formal `R-Bot @120` generation may start: `no`

## What This Draft Changes

This package refines the final blocker classification.

The old v7 wording:

- `stackoverflow-rewrite-embed.zip / binary_or_unavailable_text_corpus`

is no longer the best technical description.

The more precise draft interpretation is:

- text is present inside the archive
- the archive is tmp-only
- retained external provenance is still missing
- checker-consumable deterministic member extraction is not yet frozen

## What Is Still Blocked

The formal gate remains closed because all of the following are still unresolved:

1. the exact archive still lacks a retained external provenance handle
2. the current checkers do not yet consume ZIP-member text under a frozen extraction contract
3. the archive remains `/tmp`-only
4. the broader retained runtime/index/artifact blockers from v7 are still open

## Recommended Next Package

The next small package should:

1. add deterministic ZIP-member streaming or temporary external extraction support to the contamination checkers
2. map the four text-bearing JSONL members into checker-consumable text rows
3. explicitly ignore `__MACOSX` metadata and embedding vectors as raw comparison text
4. assign or record retained external provenance for the exact archive checksum
5. rerun the near-duplicate and generated-output exclusion checks against the extracted text view

## Draft Gate Outcome

`current_benchmark_gate_ready` remains `false`.

Formal `R-Bot @120` generation may not start.

## Bottom Line

This package narrows the final blocker from “non-text archive” to “text-bearing archive with unresolved provenance and unresolved checker-consumable extraction.”

That is a real closure improvement, but not a gate-opening one.
