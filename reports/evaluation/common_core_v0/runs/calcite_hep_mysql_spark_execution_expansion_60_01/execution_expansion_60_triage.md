# Calcite HEP MySQL/Spark Execution Expansion 60 Triage

## Summary

- `planned_rows = 60`
- `executed = 59`
- `setup_failed = 1`
- `match_exact = 49`
- `mismatch = 10`
- `not_applicable = 1`
- execution coverage = `59/60`
- exact-match on executed denominator = `49/59`
- exact-match on planned denominator = `49/60`

This is bounded MySQL/Spark execution-validity evidence for Calcite HEP. It is
not timing evidence, not speedup evidence, not leaderboard evidence, and not
full `120`-row comparable evidence.

## By Engine

### MySQL

- planned = `28`
- executed = `28`
- match_exact = `23`
- mismatch = `5`
- setup_failed = `0`

### Spark

- planned = `32`
- executed = `31`
- match_exact = `26`
- mismatch = `5`
- setup_failed = `1`

## Match-Exact Rows

`PERF_0007:mysql`, `PERF_0007:spark`, `PERF_0008:spark`, `PERF_0013:spark`,
`PERF_0017:spark`, `PERF_0019:spark`, `PERF_0024:mysql`, `PERF_0024:spark`,
`PERF_0033:mysql`, `PERF_0033:spark`, `PERF_0034:mysql`, `PERF_0034:spark`,
`PERF_0052:mysql`, `PERF_0052:spark`, `PERF_0054:mysql`, `PERF_0054:spark`,
`PERF_0056:mysql`, `PERF_0056:spark`, `PERF_0077:mysql`, `PERF_0082:mysql`,
`PERF_0082:spark`, `CONS_0005:mysql`, `CONS_0005:spark`, `CONS_0007:mysql`,
`CONS_0007:spark`, `CONS_0009:mysql`, `CONS_0009:spark`, `CONS_0010:mysql`,
`CONS_0010:spark`, `CONS_0011:mysql`, `CONS_0011:spark`, `CONS_0012:mysql`,
`CONS_0012:spark`, `CONS_0024:mysql`, `CONS_0024:spark`, `CONS_0036:mysql`,
`CONS_0036:spark`, `CONS_0037:mysql`, `CONS_0037:spark`, `PORT_0024:mysql`,
`PORT_0024:spark`, `LONGTAIL_0011:mysql`, `LONGTAIL_0011:spark`,
`LONGTAIL_0022:mysql`, `LONGTAIL_0022:spark`, `LONGTAIL_0023:mysql`,
`LONGTAIL_0023:spark`, `LONGTAIL_0024:mysql`, `LONGTAIL_0024:spark`

All match-exact rows retain `source.tsv`, `generated.tsv`, and
`result_check.json`.

## Mismatch Rows

`PERF_0006:mysql`, `PERF_0006:spark`, `PERF_0035:mysql`, `PERF_0035:spark`,
`PERF_0062:mysql`, `PERF_0062:spark`, `LONGTAIL_0012:mysql`,
`LONGTAIL_0012:spark`, `LONGTAIL_0013:mysql`, `LONGTAIL_0013:spark`

### Mismatch Classification

- `PERF_0006:mysql`
  - category: `aggregate_rewrite_precision_decimal_scale_loss`
  - evidence: source has `15.000000`, `150.000000`, `0.075000`; generated has
    `15`, `150`, `0`
  - note: `0.075000` vs `0` is a semantic mismatch, not merely formatting

- `PERF_0006:spark`
  - category: `aggregate_rewrite_precision_decimal_scale_loss`
  - evidence: source has `15.000000`, `150.000000`, `0.075000`; generated has
    `15`, `150`, `0`
  - note: `0.075000` vs `0` is a semantic mismatch, not merely formatting

- `PERF_0035:mysql`
  - category: `rewrite_output_shape_changed_extra_column_and_scale_loss`
  - evidence: generated output adds an extra trailing column
    (`-50.00`, `50.00`) and also changes `150.000000` to `150`
  - note: this is not an ordering or formatting-only difference

- `PERF_0035:spark`
  - category: `rewrite_output_shape_changed_extra_column_and_scale_loss`
  - evidence: generated output adds an extra trailing column
    (`-50.00`, `50.00`) and also changes `150.000000` to `150`
  - note: this is not an ordering or formatting-only difference

- `PERF_0062:mysql`
  - category: `numeric_format_scale_loss`
  - evidence: source `4.0000`, `120.000000`, `80.000000`; generated `4`,
    `120`, `80`
  - note: retained evidence shows exact TSV mismatch; semantic equivalence is
    not claimed

- `PERF_0062:spark`
  - category: `numeric_format_scale_loss`
  - evidence: source `4.0`, `120.000000`, `80.000000`; generated `4`, `120`,
    `80`
  - note: retained evidence shows exact TSV mismatch; semantic equivalence is
    not claimed

- `LONGTAIL_0012:mysql`
  - category: `numeric_format_scale_loss`
  - evidence: source contains `0.0000`, `1.0000`, `2.0000`; generated has `0`,
    `1`, `2`
  - note: retained evidence shows exact TSV mismatch; semantic equivalence is
    not claimed

- `LONGTAIL_0012:spark`
  - category: `numeric_format_scale_loss`
  - evidence: source contains `0.0`, `1.0`, `2.0`; generated has `0`, `1`, `2`
  - note: retained evidence shows exact TSV mismatch; semantic equivalence is
    not claimed

- `LONGTAIL_0013:mysql`
  - category: `numeric_format_scale_loss`
  - evidence: source `5.0000`, `4.0000`; generated `5`, `4`
  - note: retained evidence shows exact TSV mismatch; semantic equivalence is
    not claimed

- `LONGTAIL_0013:spark`
  - category: `numeric_format_scale_loss`
  - evidence: source `5.0`, `4.0`; generated `5`, `4`
  - note: retained evidence shows exact TSV mismatch; semantic equivalence is
    not claimed

Generated SQL was executable on all mismatch rows. The mismatch finding is about
strict output equality, not executability.

## Setup-Failed Rows

`PERF_0077:spark`

### PERF_0077:spark Classification

- category: `schema_setup_artifact_comment_only_ddl_fragment`
- evidence:
  - `cases/PERF/PERF_0077/schema/ddl_spark.sql` begins with comment lines
  - the retained Spark setup log shows a `ParseException` at the comment-only
    fragment before the first `CREATE TABLE`
- conclusion:
  - this is a schema/setup artifact issue in the retained DDL parsing path, not
    a generated-SQL execution failure
  - this triage does not modify the case or runner

## Artifact Coverage

For executed rows, retained artifacts are present:

- `source.tsv`
- `generated.tsv`
- `result_check.json`

The single setup-failed row retains row metadata and setup logs with
`consistency_status = not_applicable`.

## Conclusion

This run supports:

- `59/60` execution coverage
- `49/59` exact-match on the executed denominator
- `49/60` exact-match on the planned denominator

It is bounded MySQL/Spark execution-validity evidence for Calcite HEP on the
non-PG expansion subset.

It is not timing, speedup, leaderboard, or full `120`-row comparable evidence.

Timing, if pursued, should only use the explicit `49` `match_exact` rows.

`method_comparison_summary_v2` should remain unchanged.
