# Calcite HEP PG40 Timing Triage

This is a read-only timing triage for the Calcite HEP PostgreSQL timing run on `common_core_v0_40_pg40`.

It is timing evidence only. It is not a final `GM_Speedup` summary, not a final `RegressionRate@20%` summary, and not a leaderboard artifact.

## Headline

- total timing rows: `21`
- timing_success rows: `21`
- timing_failed rows: `0`
- rows_with_timing: `21`
- engine: `pg`
- `method_id = calcite_hep`
- `denominator_id = common_core_v0_40_pg40`
- confirmed `warmup_count = 1`
- confirmed `repeat_count = 3`

## Counts By Pool

- `performance`: `14`
- `consistency`: `7`

## Distribution Summary

`median_source_ms`:

- min: `362.57`
- p25: `380.95`
- median: `472.27`
- p75: `479.46`
- max: `593.87`
- mean: `448.90`

`median_generated_ms`:

- min: `366.61`
- p25: `371.19`
- median: `471.91`
- p75: `479.25`
- max: `586.58`
- mean: `437.72`

`speedup_ratio`:

- min: `0.7669`
- p25: `0.8139`
- median: `1.0002`
- p75: `1.2765`
- max: `1.5999`
- mean: `1.0547`

Interpretation at triage level:

- the row-level timing set is complete and clean
- the center of the distribution is close to parity
- there are both meaningful wins and meaningful slowdowns, which is expected for a small PG-only timing slice

## Fastest Rows

Top `5` by `speedup_ratio`:

- `PERF_0054`: `1.5999`
- `PERF_0013`: `1.5672`
- `CONS_0009`: `1.3046`
- `PERF_0024`: `1.2840`
- `PERF_0006`: `1.2774`

## Slowest Rows

Top `5` slowest by `speedup_ratio`:

- `PERF_0008`: `0.7669`
- `CONS_0007`: `0.7683`
- `PERF_0056`: `0.7810`
- `PERF_0052`: `0.7937`
- `PERF_0034`: `0.7984`

## Extreme Or Suspicious Timing Values

No row failed timing, and every eligible row produced a timing JSON artifact.

Rows worth keeping on a watchlist during later speedup materialization:

- `PERF_0054` and `PERF_0013` have the highest observed speedups, both above `1.5`
- `PERF_0008` and `CONS_0007` are the slowest rows, both below `0.77`
- several rows show wide repeat-to-repeat spread in either source or generated runtimes, including `PERF_0017`, `PERF_0019`, `PERF_0033`, `PERF_0056`, `PERF_0082`, and `CONS_0009`

Current interpretation:

- these look like timing-variance watch items, not missing-artifact or runner-failure evidence
- the run is still complete enough to materialize a Calcite HEP speedup summary next

## Recommendation

Proceed to materialize the Calcite HEP PG40 speedup summary next.

That next step should:

- use these `21` timing-success rows only
- compute aggregate speedup metrics there, not here
- preserve the boundary that this Calcite package is PG-only and not a tri-engine method summary
