# Formal `stackoverflow-rewrite-embed.zip` Retention Decision

## Decision Summary

Current decision:

- treat `stackoverflow-rewrite-embed.zip` as a checksum-identified external retrieval artifact and deterministic rebuild input
- do not treat the outer ZIP container itself as a text corpus file
- do not treat the archive as “binary-only non-text corpus”
- keep the formal gate closed until retained provenance and checker-consumable text extraction are both closed

## Basis

Known facts:

1. the exact archive bytes are visible by path and SHA-256
2. the archive contains `4` text-readable JSONL members
3. those members contain contamination-relevant SQL and rule text
4. the archive remains `/tmp`-only
5. retained external provenance handle is still missing
6. the current formal checkers do not yet consume ZIP-member text under a frozen extraction contract

## Classification Decision

### External retained artifact with checksum

Decision: `yes_in_principle_but_not_yet_closed`

Required closure:

- retain an external provenance handle or equivalent retained artifact reference for the exact SHA-256

### Deterministic rebuild input

Decision: `yes`

Reason:

- the artifact is part of the benchmark-common retrieval corpus family
- the exact bytes are identified
- a deterministic member-level text extraction recipe can be specified

### Binary-only non-text corpus

Decision: `no`

Reason:

- the outer container is binary
- the non-metadata contents are text-readable JSONL members

### Blocker that keeps the formal gate closed

Decision: `yes`

Remaining blocking reasons:

1. external retained provenance is still missing
2. checker-consumable deterministic text extraction is not yet frozen and rerun
3. the archive is still `/tmp`-only rather than retained in a formal package

## Operational Consequence

The blocker should be reinterpreted from:

- `binary_or_unavailable_text_corpus`

to a more precise next-step blocker such as:

- `text_present_inside_tmp_only_archive_but_retention_and_checker_extraction_not_closed`

That is a classification refinement only.
It does not open the gate.

## Next Package

The next small package should:

1. freeze the ZIP-member text extraction contract
2. assign or record retained external provenance for the exact archive checksum
3. create checker-consumable manifest rows for the extracted text fields
4. rerun the near-duplicate and generated-output exclusion checks against that extracted text view

## Bottom Line

Formal `R-Bot @120` generation still may not start.

The ZIP is no longer best described as wholly non-text, but retention and checker-consumable extraction are still unresolved and remain gate blockers.
