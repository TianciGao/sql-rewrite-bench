# R-Bot Validity Summary v1

## Scope

This summary materializes denominator-aware generation and execution validity evidence for:

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- generation denominator = `common_core_v0_40_same_engine_120`
- execution denominator = `generated_pg7_only`

This is **R-Bot generation/execution validity evidence only**. It is **not** timing evidence, not tri-engine evidence, and not a leaderboard artifact.

## Headline Counts

- planned generation rows: `120`
- generated rows: `7`
- failed rows: `2`
- blocked rows: `31`
- unsupported rows: `80`
- executed rows: `7`
- execution_failed rows: `0`
- match_exact rows: `7`
- mismatch rows: `0`

## Headline Rates

| metric | formula | value |
|---|---|---:|
| generation_success_rate over planned | `7 / 120` | `5.83%` |
| generation_failed_rate over planned | `2 / 120` | `1.67%` |
| blocked_rate over planned | `31 / 120` | `25.83%` |
| unsupported_rate over planned | `80 / 120` | `66.67%` |
| executable_rate over generated | `7 / 7` | `100.00%` |
| result_consistency_rate over generated | `7 / 7` | `100.00%` |
| result_consistency_rate over planned | `7 / 120` | `5.83%` |

## Outcome-Class Summary

| outcome_class | rows | rate over planned |
|---|---:|---:|
| `match_exact` | 7 | `5.83%` |
| `generation_failed` | 2 | `1.67%` |
| `blocked` | 31 | `25.83%` |
| `unsupported` | 80 | `66.67%` |

## Generated And Valid Rows

- `PERF_0006:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`

## Failed Rows

- `PERF_0019:pg`
- `PERF_0033:pg`

## Interpretation

- The retained formal generation denominator is fully visible at `120` rows.
- R-Bot generated only `7` PostgreSQL rows on that denominator, with `2` PostgreSQL generation failures, `31` PostgreSQL blocked rows, and `80` mysql/spark unsupported rows.
- All `7` generated PostgreSQL rows passed exact-match execution validity.
- The resulting validity rate is `100.00%` over the generated subset, but only `5.83%` over the original `120`-row generation denominator.

## Boundary

- This summary is denominator-aware and keeps failed, blocked, and unsupported rows visible.
- It does not imply full-denominator executability.
- It does not imply tri-engine validity coverage.
- It should not be normalized into a leaderboard claim without explicit denominator labels.
