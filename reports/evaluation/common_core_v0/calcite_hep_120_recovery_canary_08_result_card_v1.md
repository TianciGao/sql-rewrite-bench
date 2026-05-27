# Calcite HEP 120 Recovery Canary 08 Result Card v1

Calcite HEP recovery canary `08_01` targeted eight low-risk retained ledger-gap rows under the fixed `common_core_v0_40_same_engine_120` denominator. The fail-closed exact-match ledger improved from `70/120` to `75/120`, with `5/8` audited rows recovering retained `match_exact` validity evidence. The remaining three audited rows now reach target-dialect PostgreSQL SQL generation but fail during execution. This remains bounded execution-validity evidence, not timing, speedup, leaderboard, or full `120`-row comparable evidence.

## Denominator Summary

| field | value |
|---|---:|
| previous_fail_closed_exact_ledger | `70/120` |
| planned_rows | `8` |
| recovered_exact_count | `5` |
| new_fail_closed_exact_ledger | `75/120` |
| maximum_possible_ledger_after_this_canary | `78/120` |
| wrapper_compile_status | `ok` |
| leaderboard_comparable | `no` |
| timing_denominator_id | `NA_not_computed` |

## Recovered Exact Rows

- `PERF_0008:mysql`
- `PERF_0013:mysql`
- `PERF_0017:mysql`
- `PERF_0019:mysql`
- `PERF_0077:spark`

## Unrecovered Rows

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`

## Important Nuance

The three PostgreSQL `LONGTAIL` rows are no longer wrapper compile failures and are no longer generation failures. The package-local wrapper compiled, parsed source SQL, ingested the DDL, validated, converted to rel, ran HEP, and emitted target-dialect PostgreSQL SQL for all three rows. They remain unrecovered because execution failed under `psql`, so they should be classified as `generated_execution_failed` / `execution_failed`, not `generation_failed` and not `wrapper_compile_failed`.

## Paper-Safe Statement

`After a bounded recovery canary targeting low-risk Calcite HEP harness and wrapper defects, the fail-closed exact-match ledger improved from 70/120 to 75/120. Five rows recovered exact-match validity evidence. The recovered rows reflect implementation-level route repair rather than relaxation of exact-match semantics or denominator scope. The remaining three audited rows now reach target-dialect PostgreSQL SQL generation but fail during execution. This remains bounded execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`
