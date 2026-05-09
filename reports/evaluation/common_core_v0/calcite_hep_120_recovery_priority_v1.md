# Calcite HEP 120 Recovery Priority v1

Current fail-closed exact ledger: `70/120`.

This audit classifies every retained non-exact or non-executed Calcite HEP row in the `120`-row fail-closed ledger and prioritizes only low-risk recovery work for the next bounded canary. It stays fail-closed, preserves strict exact-match semantics, and does not relax source, dialect, or semantic boundaries.

## Bucket Summary

- `likely_harness_or_packaging_recoverable`: `8`
- `likely_wrapper_dialect_recoverable`: `5`
- `likely_checker_or_representation_recoverable`: `7`
- `likely_method_semantic_failure`: `7`
- `source_or_case_dialect_boundary`: `23`

## Current 120-Row Gap Interpretation

- The PG route still has recoverable-seeming wrapper and DDL-parser issues, but also has semantic mismatches and clear source/dialect boundary rows.
- The non-PG route has three qualitatively different gap classes: low-risk harness/package rows, strict exact-match representation gaps, and clear semantic failures.
- PORT-family gaps remain the highest methodology risk and are excluded from the next canary.

## Proposed Next Canary

At most `8` rows, restricted to `likely_harness_or_packaging_recoverable` rows only:

- `LONGTAIL_0022:pg`: ddl_parser_unsupported_timestamp_type_pg
- `LONGTAIL_0023:pg`: ddl_parser_unsupported_timestamp_type_pg
- `LONGTAIL_0024:pg`: ddl_parser_unsupported_timestamp_type_pg
- `PERF_0008:mysql`: ddl_table_name_ingestion_brittle_mysql
- `PERF_0013:mysql`: ddl_table_name_ingestion_brittle_mysql
- `PERF_0017:mysql`: ddl_table_name_ingestion_brittle_mysql
- `PERF_0019:mysql`: ddl_table_name_ingestion_brittle_mysql
- `PERF_0077:spark`: schema_setup_artifact_comment_only_ddl_fragment

Maximum safe near-term upside: `+8` exact rows if every selected row recovers fully through exact-match validity, lifting the fail-closed ledger from `70/120` to at most `78/120`. Realized gain may be lower if any recovered row later mismatches.

## Rows Excluded From Recovery And Why

- `likely_method_semantic_failure` rows are excluded because the retained evidence already shows value change, output-shape change, or unsupported boolean-aggregation semantics.
- `likely_checker_or_representation_recoverable` rows are excluded because strict exact-match semantics must not be relaxed silently.
- `source_or_case_dialect_boundary` rows are excluded because they need methodology review before any same-engine recovery attempt.
- `likely_wrapper_dialect_recoverable` rows are deferred, not denied; the next canary prioritizes lower-risk harness/package fixes first.

## Paper-Safe Wording If The Canary Later Succeeds

`After a bounded recovery canary targeting low-risk Calcite HEP harness and wrapper defects, the fail-closed exact-match ledger improved from 70/120 to X/120. The recovered rows reflect implementation-level route repair rather than any relaxation of exact-match semantics or denominator scope.`

## Paper-Safe Wording If The Canary Later Fails

`The bounded recovery canary did not convert the targeted rows into additional exact-match evidence. This strengthens the conclusion that the remaining Calcite HEP 120-row gaps are not merely low-risk packaging defects and should remain explicit non-exact denominator rows rather than being silently normalized away.`
