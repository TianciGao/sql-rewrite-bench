# R-Bot PG Expansion Result Card v2

## Identity

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `engine_scope = pg_only`
- `leaderboard_comparable = no`

## Concise Summary

In the PostgreSQL-only expansion path, R-Bot improved retained PG generation
coverage from `7 / 40` to `15 / 40` rows. All `15 / 15` generated PG rows then
passed exact-match execution, and timing evidence exists for that
`generated_pg15_from_pg40_expansion_match_exact_only` subset with
`GM_Speedup = 0.921825` and `RegressionRate@20% = 20.00% (3/15)`.

## Denominator Table

| Layer | Denominator ID | Planned Rows | Outcome |
|---|---|---:|---|
| Generation | `common_core_v0_40_pg40` | 40 | `generated=15`, `failed=25`, `blocked=0`, `unsupported=0` |
| Execution | `generated_pg15_from_pg40_expansion_only` | 15 | `executed=15`, `match_exact=15`, `mismatch=0`, `execution_failed=0` |
| Timing | `generated_pg15_from_pg40_expansion_match_exact_only` | 15 | `timing_success=15`, `timing_failed=0` |

## Metric Table

| Metric | Value |
|---|---:|
| PG generation success rate over PG40 | `15 / 40 = 37.50%` |
| Exact-match validity over generated PG15 | `15 / 15 = 100.00%` |
| Exact-match validity over PG40 | `15 / 40 = 37.50%` |
| `GM_Speedup` over PG15 only | `0.921825` |
| `RegressionRate@20%` over PG15 only | `3 / 15 = 20.00%` |

## Material Regression Rows

- `CONS_0007`
- `PERF_0052`
- `PERF_0062`

## Caveats

- This card does not overwrite [r_bot_formal_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.md).
- This is not full PG40 timing.
- This is not full `120`-row timing.
- This is not tri-engine evidence.
- This is not leaderboard evidence.
- The `25` failed generation rows remain explicit denominator rows and were not
  silently dropped.
- Timing is only for the `15` generated-and-`match_exact` rows.

## Relation To Prior PG7 Evidence

Compared with the earlier PG7 retained path:

- prior PG generation coverage: `7 / 40`
- PG expansion generation coverage: `15 / 40`
- prior PG7-only `GM_Speedup`: `0.947444`
- current PG15-only `GM_Speedup`: `0.921825`

This comparison is same-method historical context only and should not be read
as a leaderboard progression claim.
