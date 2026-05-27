# R-Bot PG7 Timing Triage

## Scope

This is a read-only triage of the retained R-Bot PG7 timing run.

Boundary: this is PG7 timing evidence only. It is not full `120`-row timing evidence and it is not leaderboard evidence.

## Summary

- Planned timing rows: `7`
- `timing_success` rows: `7`
- `timing_failed` rows: `0`
- Rows with timing payloads: `7`
- Speedup summary can be materialized for this PG7 subset: `yes`

## Per-Row Timing

- `PERF_0006:pg`: `median_source_ms = 367.467208`, `median_generated_ms = 479.925861`, `speedup_ratio = 0.765675`
- `PERF_0008:pg`: `median_source_ms = 372.576692`, `median_generated_ms = 372.619104`, `speedup_ratio = 0.999886`
- `PERF_0013:pg`: `median_source_ms = 379.052893`, `median_generated_ms = 380.187911`, `speedup_ratio = 0.997015`
- `PERF_0017:pg`: `median_source_ms = 476.348873`, `median_generated_ms = 419.440504`, `speedup_ratio = 1.135677`
- `PERF_0024:pg`: `median_source_ms = 377.653649`, `median_generated_ms = 379.235020`, `speedup_ratio = 0.995830`
- `PERF_0052:pg`: `median_source_ms = 376.985535`, `median_generated_ms = 376.516769`, `speedup_ratio = 1.001245`
- `PERF_0054:pg`: `median_source_ms = 378.721539`, `median_generated_ms = 477.663194`, `speedup_ratio = 0.792863`

## PG7-Only Aggregate

- `min_speedup_ratio = 0.765675`
- `median_speedup_ratio = 0.997015`
- `max_speedup_ratio = 1.135677`
- Preliminary `GM_Speedup` over PG7 only: `0.947444`
- Preliminary `RegressionRate@20%` over PG7 only: `2 / 7 = 0.285714`

Interpretation:

- The PG7-local geometric mean is below `1.0`, so this seven-row subset is net regressive on timing.
- Two rows fall below the `1 / 1.2 = 0.833333` regression threshold used for `RegressionRate@20%`: `PERF_0006:pg` and `PERF_0054:pg`.

## High-Variance Or Suspicious Rows

- `PERF_0006:pg`: material regression. Generated runtimes are consistently higher than source runtimes, with one slower generated repeat (`569.452768 ms`).
- `PERF_0008:pg`: near parity, but source repeats include one elevated outlier (`588.009746 ms`) and generated repeats include one elevated repeat (`482.537973 ms`).
- `PERF_0013:pg`: near parity on medians, but source repeats include one elevated outlier (`733.303497 ms`) and generated repeats include one elevated repeat (`490.536148 ms`).
- `PERF_0024:pg`: near parity, with one elevated generated repeat (`479.690680 ms`).
- `PERF_0052:pg`: near parity, but both source and generated repeats include one elevated first repeat (`563.237958 ms` and `491.987153 ms`).
- `PERF_0054:pg`: material regression. Generated median is substantially slower than source median despite one faster generated repeat.

`PERF_0017:pg` is the only clear speedup row in this subset, with `speedup_ratio = 1.135677`, but it does not exceed a `20%` speedup threshold.

## Artifact Presence

- Timing JSON files exist for all 7 rows: `yes`
- Stdout logs exist for all 7 rows: `yes`
- Stderr logs exist for all 7 rows: `yes`

## Boundary

This triage supports PG7-only timing follow-on reporting for the seven retained `match_exact` PostgreSQL rows.

It does not establish:

- timing evidence for the full formal `120`-row denominator
- any final same-engine leaderboard artifact
- any method-comparison summary
