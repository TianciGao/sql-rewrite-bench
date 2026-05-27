# Calcite HEP Speedup Summary v1

This is a Calcite HEP PostgreSQL-only speedup summary for the frozen `common_core_v0_40_pg40` denominator.

It is not tri-engine evidence and it is not a final multi-method leaderboard. Any comparison to SQLGlot or Direct LLM belongs in a separate method-comparison summary.

## Scope

- `denominator_id = common_core_v0_40_pg40`
- `method_id = calcite_hep`
- `route_id = calcite_hep_pg_rewrite`
- engine: `pg`
- planned rows: `40`
- generation_success rows: `29`
- ready_to_execute rows: `29`
- executed rows: `23`
- match_exact rows: `21`
- timing_eligible rows: `21`
- timing_success rows: `21`
- timing_failed rows: `0`
- generation_failed rows: `11`
- execution_failed rows: `6`
- mismatch rows: `2`

## Coverage

- coverage over planned denominator: `52.50%` (`21 / 40`)
- coverage over timing_eligible denominator: `100.00%` (`21 / 21`)
- coverage over ready_to_execute denominator: `72.41%` (`21 / 29`)

## Overall Speedup

Using only the `21` `timing_success` rows:

- `GM_Speedup`: `1.0267`
- `RegressionRate@20%`: `23.81%` (`5 / 21`)
- median `speedup_ratio`: `1.0002`
- mean `speedup_ratio`: `1.0547`
- min / p25 / p75 / max `speedup_ratio`: `0.7669 / 0.8139 / 1.2765 / 1.5999`
- `count_speedup_gt_1`: `11`
- `count_speedup_lt_1`: `10`
- `count_regression_lt_0_8`: `5`

Interpretation:

- the PG40 timing slice is complete for all timing-eligible rows
- aggregate Calcite HEP speedup is slightly above parity on this PG-only denominator
- the win/loss split is close, and `5` rows fall below the `0.8` regression threshold

## By Pool

`performance`:

- timing_success rows: `14`
- `GM_Speedup`: `1.0365`
- `RegressionRate@20%`: `28.57%` (`4 / 14`)
- median `speedup_ratio`: `1.0006`
- mean `speedup_ratio`: `1.0699`
- min / p25 / p75 / max: `0.7669 / 0.8023 / 1.2772 / 1.5999`
- `count_speedup_gt_1`: `7`
- `count_speedup_lt_1`: `7`
- `count_regression_lt_0_8`: `4`
- coverage over planned denominator: `87.50%` (`14 / 16`)
- coverage over timing_eligible denominator: `100.00%` (`14 / 14`)
- coverage over ready_to_execute denominator: `87.50%` (`14 / 16`)

`consistency`:

- timing_success rows: `7`
- `GM_Speedup`: `1.0072`
- `RegressionRate@20%`: `14.29%` (`1 / 7`)
- median `speedup_ratio`: `1.0002`
- mean `speedup_ratio`: `1.0245`
- min / p25 / p75 / max: `0.7683 / 0.9056 / 1.1436 / 1.3046`
- `count_speedup_gt_1`: `4`
- `count_speedup_lt_1`: `3`
- `count_regression_lt_0_8`: `1`
- coverage over planned denominator: `77.78%` (`7 / 9`)
- coverage over timing_eligible denominator: `100.00%` (`7 / 7`)
- coverage over ready_to_execute denominator: `77.78%` (`7 / 9`)

## Boundary Notes

- only `timing_success` rows are used for `GM_Speedup` and `RegressionRate@20%`
- `generation_failed` rows remain visible denominator rows and are not silently dropped
- `execution_failed` rows and `mismatch` rows are excluded from speedup because they are not valid timing-eligible rewrites
- this summary should not be presented as a final leaderboard row across methods without a separate coverage-aware comparison layer
