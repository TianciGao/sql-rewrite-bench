# SQLSOLVER_SUPPORT_SMOKE_CONS_0007_0035_v1

## 0. Purpose And Boundary
State:
- bounded SQLSolver support smoke
- support/verifier only
- `CONS_0007` / `CONS_0035` only
- not rewrite generation
- not speedup
- not leaderboard
- not registry writeback

## 1. Runtime Configuration
Report:
- jar path: `/tmp/rewritebench_sqlsolver_audit/candidate/build/libs/sqlsolver-v1.1.0.jar`
- Z3 artifacts path: `/tmp/rewritebench_sqlsolver_audit/candidate/lib`
- timeout policy:
  - wall timeout: `60s` per query pair
  - `sqlsolver.z3.timeout = 10000 ms`
- verdict mapping:
  - `EQ -> proved_equivalent`
  - `NEQ -> refuted_equivalence`
  - `TIMEOUT -> timeout`
  - `UNKNOWN -> unknown_or_unsupported`
- cases targeted: `CONS_0007`, `CONS_0035`

## 2. Per-pair Result Table
| case_id | pair_type | expected_support_intent | sqlsolver_raw_verdict | mapped_verdict | support_result | exit_code | timeout | failure_category | failure_summary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CONS_0007` | `positive` | `prove_equivalent` | `EQ` | `proved_equivalent` | `expected_supported` | `0` | `false` |  |  |
| `CONS_0007` | `negative` | `refute_equivalence` | `NEQ` | `refuted_equivalence` | `expected_supported` | `0` | `false` |  |  |
| `CONS_0035` | `positive` | `prove_equivalent` | `NEQ` | `refuted_equivalence` | `unexpected_verdict` | `0` | `false` |  |  |
| `CONS_0035` | `negative` | `refute_equivalence` | `NEQ` | `refuted_equivalence` | `expected_supported` | `0` | `false` |  |  |

## 3. Per-case Summary
For `CONS_0007`:
- positive pair result: `EQ -> proved_equivalent -> expected_supported`
- negative pair result: `NEQ -> refuted_equivalence -> expected_supported`
- support coverage interpretation: full support on both prepared pairs

For `CONS_0035`:
- positive pair result: `NEQ -> refuted_equivalence -> unexpected_verdict`
- negative pair result: `NEQ -> refuted_equivalence -> expected_supported`
- support coverage interpretation: SQLSolver supported the negative pair as expected, but did not support the prepared positive pair as equivalent

## 4. Aggregate Support Metrics
Report:
- denominator_pairs: `4`
- prove_count: `1`
- refute_count: `3`
- unknown_count: `0`
- timeout_count: `0`
- unsupported_count: `0`
- parser_or_translation_failure_count: `0`
- internal_error_count: `0`
- launch_failure_count: `0`
- expected_supported_count: `3`
- unexpected_verdict_count: `1`
- verifier_support_rate: `3/4`

## 5. Interpretation
State:
- SQLSolver is support/verifier-only.
- `EQ` / `NEQ` support is useful evidence.
- `UNKNOWN` / `TIMEOUT` / unsupported would be support gaps, not rewrite failures.
- No speedup, no leaderboard.
- In this bounded smoke, the only adverse outcome was an `unexpected_verdict` on the `CONS_0035` positive pair.

## 6. Recommended Next Step
Choose exactly one:
- `add SQLSolver support smoke rollup to prior-support evidence`

## 7. Non-Modification Note
Confirm:
- only `CONS_0007` / `CONS_0035` targeted
- no DB/checker/speedup
- no registry/review/rules/EXECUTION_STATUS changes
- no case files modified
- taxonomy notes untouched
