# R-Bot PG15 Timing Expansion Triage

## Scope

This is a read-only triage of the retained R-Bot PG15 timing expansion run.

Boundary: this is PG15 timing evidence only. It is not:

- full PG40 timing evidence
- full `common_core_v0_40_same_engine_120` timing evidence
- tri-engine timing evidence
- leaderboard evidence

The `25` failed PG generation rows remain explicit outside this timing subset.

## Summary

- Planned timing rows: `15`
- `timing_success` rows: `15`
- `timing_failed` rows: `0`
- Rows with timing payloads: `15`
- Speedup summary can be materialized for this PG15 subset: `yes`

## Per-Row Timing

- `PERF_0006:pg`: `median_source_ms = 376.400599`, `median_generated_ms = 379.397234`, `speedup_ratio = 0.992102`
- `PERF_0007:pg`: `median_source_ms = 495.742877`, `median_generated_ms = 616.102595`, `speedup_ratio = 0.804643`
- `PERF_0008:pg`: `median_source_ms = 477.554582`, `median_generated_ms = 486.271162`, `speedup_ratio = 0.982075`
- `PERF_0013:pg`: `median_source_ms = 432.855090`, `median_generated_ms = 491.480802`, `speedup_ratio = 0.880716`
- `PERF_0017:pg`: `median_source_ms = 372.227991`, `median_generated_ms = 372.839029`, `speedup_ratio = 0.998361`
- `PERF_0024:pg`: `median_source_ms = 373.895693`, `median_generated_ms = 373.891135`, `speedup_ratio = 1.000012`
- `PERF_0052:pg`: `median_source_ms = 376.302581`, `median_generated_ms = 486.804782`, `speedup_ratio = 0.773005`
- `PERF_0054:pg`: `median_source_ms = 371.125917`, `median_generated_ms = 394.171610`, `speedup_ratio = 0.941534`
- `PERF_0062:pg`: `median_source_ms = 379.004350`, `median_generated_ms = 482.704658`, `speedup_ratio = 0.785168`
- `CONS_0005:pg`: `median_source_ms = 441.811145`, `median_generated_ms = 476.473903`, `speedup_ratio = 0.927252`
- `CONS_0007:pg`: `median_source_ms = 372.782463`, `median_generated_ms = 592.324415`, `speedup_ratio = 0.629355`
- `CONS_0009:pg`: `median_source_ms = 480.721847`, `median_generated_ms = 371.037618`, `speedup_ratio = 1.295615`
- `CONS_0010:pg`: `median_source_ms = 471.371609`, `median_generated_ms = 477.044668`, `speedup_ratio = 0.988108`
- `CONS_0012:pg`: `median_source_ms = 366.623089`, `median_generated_ms = 369.505673`, `speedup_ratio = 0.992199`
- `CONS_0036:pg`: `median_source_ms = 369.243766`, `median_generated_ms = 365.572512`, `speedup_ratio = 1.010042`

## PG15-Only Aggregate

- `min_speedup_ratio = 0.629355`
- `median_speedup_ratio = 0.982075`
- `max_speedup_ratio = 1.295615`
- Preliminary `GM_Speedup` over PG15 only: `0.921825`
- Preliminary `RegressionRate@20%` over PG15 only: `3 / 15 = 0.200000`

Interpretation:

- the PG15-local geometric mean remains below `1.0`, so this retained PG15 subset is net regressive on timing
- following the observed package convention for this triage, `RegressionRate@20%` is counted with the material-regression cutoff `speedup_ratio < 0.8`

## Material Regression Rows

Rows with `speedup_ratio < 0.8`:

- `PERF_0052:pg` with `speedup_ratio = 0.773005`
- `PERF_0062:pg` with `speedup_ratio = 0.785168`
- `CONS_0007:pg` with `speedup_ratio = 0.629355`

## High-Variance Or Suspicious Rows

- `PERF_0006:pg`: near-parity median, but generated repeats contain a clear slow outlier (`686.091608 ms`)
- `PERF_0007:pg`: mild regression on median, with wide generated spread (`376.086108 ms` to `629.521631 ms`)
- `PERF_0013:pg`: both source and generated repeats show large spread, so the sub-`1.0` median should be read cautiously
- `PERF_0017:pg`: near parity on medians, but one generated repeat is substantially slower (`879.801269 ms`)
- `PERF_0024:pg`: median is effectively parity, but source repeats include one elevated run (`573.965830 ms`)
- `PERF_0062:pg`: regressive median, with one elevated source repeat and lower generated median stability than the parity rows
- `CONS_0005:pg`: modest regression with generated-repeat spread (`370.087466 ms` to `594.326830 ms`)
- `CONS_0007:pg`: strongest material regression and persistently slow generated repeats on two of three timed runs
- `CONS_0012:pg`: near parity median, but source repeats include one elevated run (`593.874405 ms`)

`CONS_0009:pg` is the strongest apparent speedup row in this subset with
`speedup_ratio = 1.295615`, but this remains subset-scoped evidence only.

## Artifact Presence

- Timing JSON files exist for all 15 rows: `yes`
- Stdout logs exist for all 15 rows: `yes`
- Stderr logs exist for all 15 rows: `yes`

## Comparison Against Prior PG7 Timing Evidence

Relative to the retained PG7 timing package:

- prior PG7 timing denominator: `generated_pg7_match_exact_only`
- prior PG7 timing rows: `7`
- prior PG7-only `GM_Speedup`: `0.947444`
- current PG15 timing denominator:
  `generated_pg15_from_pg40_expansion_match_exact_only`
- current PG15 timing rows: `15`
- current PG15-only `GM_Speedup`: `0.921825`

This comparison is useful only as subset-to-subset same-method context. It is
not a like-for-like leaderboard comparison because the timing denominators are
different:

- PG7 timing is based on the earlier retained PG7 subset
- PG15 timing is based on the expanded PG40 generation plus PG15 execution
  subset

## Boundary

This triage supports PG15-only timing follow-on reporting for the fifteen
retained `match_exact` PostgreSQL rows in the expansion path.

It does not establish:

- timing evidence for all PG40 rows
- timing evidence for the full formal `120`-row same-engine denominator
- any final same-engine leaderboard artifact
- any method-comparison summary update
