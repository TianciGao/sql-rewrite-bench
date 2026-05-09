# Calcite HEP 120 Recovery Round2 Canary 09 Result Card v1

Calcite HEP recovery round2 canary `09_01` targeted nine low-risk retained ledger-gap rows under the fixed `common_core_v0_40_same_engine_120` denominator. The fail-closed exact-match ledger improved from `75/120` to `80/120`, with `5/9` audited rows recovering retained `match_exact` validity evidence. The remaining four audited rows are still non-exact or non-recovered. This remains bounded execution-validity evidence, not timing, speedup, leaderboard, or full `120`-row comparable evidence.

## Denominator Summary

| field | value |
|---|---:|
| previous_fail_closed_exact_ledger | `75/120` |
| planned_rows | `9` |
| recovered_exact_count | `5` |
| new_fail_closed_exact_ledger | `80/120` |
| maximum_possible_ledger_after_this_canary | `84/120` |
| executed | `8` |
| generated_execution_failed | `1` |
| match_exact | `5` |
| mismatch | `3` |
| not_applicable | `1` |
| wrapper_compile_status | `ok` |
| leaderboard_comparable | `no` |
| timing_denominator_id | `NA_not_computed` |

## Recovered Exact Rows

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`
- `LONGTAIL_0012:mysql`
- `LONGTAIL_0012:spark`

## Non-Recovered Rows

- `PERF_0062:mysql` (`executed`, `mismatch`)
- `PERF_0062:spark` (`executed`, `mismatch`)
- `LONGTAIL_0013:mysql` (`generated_execution_failed`, `not_applicable`)
- `LONGTAIL_0013:spark` (`executed`, `mismatch`)

## Important Nuance

This canary did not change denominator scope, exact-match semantics, or checker policy. The three PostgreSQL `LONGTAIL` rows now recover exact-match validity evidence through implementation-level identifier-compatibility repair. The remaining four rows stay explicit non-exact denominator rows: two `PERF_0062` numeric mismatches, one `LONGTAIL_0013:spark` numeric mismatch, and one `LONGTAIL_0013:mysql` generated-execution failure during MySQL setup / DDL execution.

## Paper-Safe Statement

`After a bounded round-2 recovery canary targeting low-risk Calcite HEP identifier-compatibility and numeric-rendering defects, the fail-closed exact-match ledger improved from 75/120 to 80/120. Five additional rows recovered exact-match validity evidence. The recovered rows reflect implementation-level route repair under unchanged exact-match semantics and unchanged denominator scope. The remaining four audited rows are still non-exact or non-recovered. This remains bounded execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`
