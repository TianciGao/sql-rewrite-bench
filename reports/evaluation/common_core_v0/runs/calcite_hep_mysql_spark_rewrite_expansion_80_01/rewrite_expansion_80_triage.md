# Calcite HEP MySQL/Spark Rewrite Expansion 80 Triage

## Summary

- `run_id = calcite_hep_mysql_spark_rewrite_expansion_80_01`
- `planned_rows = 80`
- `rewrite_success = 60`
- `parser_failed = 14`
- `hep_rewrite_failed = 6`

This is rewrite-only evidence. It is not execution evidence, not correctness
evidence, not timing evidence, not speedup evidence, and not leaderboard
evidence.

## Counts By Engine

- MySQL: `rewrite_success = 28`, `parser_failed = 7`, `hep_rewrite_failed = 5`
- Spark: `rewrite_success = 32`, `parser_failed = 7`, `hep_rewrite_failed = 1`

## Counts By Pool

- `performance`: `rewrite_success = 28`, `hep_rewrite_failed = 4`
- `consistency`: `rewrite_success = 18`
- `portability`: `rewrite_success = 2`, `parser_failed = 14`, `hep_rewrite_failed = 2`
- `longtail`: `rewrite_success = 12`

## Rewrite Success Rows

`PERF_0006:mysql`, `PERF_0006:spark`, `PERF_0007:mysql`, `PERF_0007:spark`,
`PERF_0008:spark`, `PERF_0013:spark`, `PERF_0017:spark`, `PERF_0019:spark`,
`PERF_0024:mysql`, `PERF_0024:spark`, `PERF_0033:mysql`, `PERF_0033:spark`,
`PERF_0034:mysql`, `PERF_0034:spark`, `PERF_0035:mysql`, `PERF_0035:spark`,
`PERF_0052:mysql`, `PERF_0052:spark`, `PERF_0054:mysql`, `PERF_0054:spark`,
`PERF_0056:mysql`, `PERF_0056:spark`, `PERF_0062:mysql`, `PERF_0062:spark`,
`PERF_0077:mysql`, `PERF_0077:spark`, `PERF_0082:mysql`, `PERF_0082:spark`,
`CONS_0005:mysql`, `CONS_0005:spark`, `CONS_0007:mysql`, `CONS_0007:spark`,
`CONS_0009:mysql`, `CONS_0009:spark`, `CONS_0010:mysql`, `CONS_0010:spark`,
`CONS_0011:mysql`, `CONS_0011:spark`, `CONS_0012:mysql`, `CONS_0012:spark`,
`CONS_0024:mysql`, `CONS_0024:spark`, `CONS_0036:mysql`, `CONS_0036:spark`,
`CONS_0037:mysql`, `CONS_0037:spark`, `PORT_0024:mysql`, `PORT_0024:spark`,
`LONGTAIL_0011:mysql`, `LONGTAIL_0011:spark`, `LONGTAIL_0012:mysql`,
`LONGTAIL_0012:spark`, `LONGTAIL_0013:mysql`, `LONGTAIL_0013:spark`,
`LONGTAIL_0022:mysql`, `LONGTAIL_0022:spark`, `LONGTAIL_0023:mysql`,
`LONGTAIL_0023:spark`, `LONGTAIL_0024:mysql`, `LONGTAIL_0024:spark`

All `60` rewrite-success rows retain generated SQL, stdout log, stderr log, and
row metadata artifacts.

## Parser Failed Rows

`PORT_0003:mysql`, `PORT_0003:spark`, `PORT_0004:mysql`, `PORT_0004:spark`,
`PORT_0005:mysql`, `PORT_0005:spark`, `PORT_0008:mysql`, `PORT_0008:spark`,
`PORT_0012:mysql`, `PORT_0012:spark`, `PORT_0022:mysql`, `PORT_0022:spark`,
`PORT_0025:mysql`, `PORT_0025:spark`

Conservative classification: `parser_failed` indicates a Calcite parser or
dialect-acceptance boundary on the source SQL. It should not be called a
benchmark failure without later review.

## HEP Rewrite Failed Rows

`PERF_0008:mysql`, `PERF_0013:mysql`, `PERF_0017:mysql`, `PERF_0019:mysql`,
`PORT_0013:mysql`, `PORT_0013:spark`

Conservative classification: `hep_rewrite_failed` indicates a Calcite
SQL-to-rel, schema-ingestion, HEP validation, or rewrite boundary. It should
not be called a benchmark failure without later review.

## Witness Metadata

`witness_missing_for_later_execution` appears on `4` rows:

- `PORT_0003:mysql`
- `PORT_0003:spark`
- `PORT_0005:mysql`
- `PORT_0005:spark`

These rows were already `parser_failed`. Missing witness files were retained as
later execution metadata only and were not used as rewrite-time blockers.

## Conclusion

A bounded execution/validity package is justified next, but only for the `60`
`rewrite_success` rows.

Timing should not proceed until after execution and exact-match triage.

`method_comparison_summary_v2` should remain unchanged.

## Claim Boundary

This triage summarizes rewrite-generation outcomes only for:

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `expansion_denominator_id = calcite_hep_mysql_spark_common_core_v0_80`

It does not establish:

- execution closure
- correctness rates
- timing
- speedup
- leaderboard-comparable evidence
