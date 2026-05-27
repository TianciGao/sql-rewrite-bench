# SQLSOLVER_SUPPORT_SMOKE_ROLLUP_v1

## 0. Purpose And Boundary
State:
- SQLSolver support/verifier rollup only
- not rewrite generation
- not speedup
- not leaderboard
- no new experiment

## 1. Substrate And Build Status
Summarize:
- upstream repo acquired: `/tmp/rewritebench_sqlsolver_audit/candidate`
- Apache 2.0 license visible
- built jar path: `/tmp/rewritebench_sqlsolver_audit/candidate/build/libs/sqlsolver-v1.1.0.jar`
- entrypoint: `sqlsolver.api.Entry`
- verdict contract:
  - `EQ`
  - `NEQ`
  - `UNKNOWN`
  - `TIMEOUT`
- support-only role: SQLSolver is treated as verifier/support evidence only, not rewrite generation and not speedup

## 2. Adapter / Runner Status
Summarize:
- `CONS_0007` and `CONS_0035` adapter preflight complete
- runner dry-run with built jar complete
- support smoke executed on positive and negative pairs

## 3. Per-pair Result Table
| case_id | pair_type | expected_support_intent | raw_verdict | mapped_verdict | support_result | timeout | failure_category | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CONS_0007` | `positive` | `prove_equivalent` | `EQ` | `proved_equivalent` | `expected_supported` | `false` |  | `bounded_sqlsolver_support_smoke_not_rewrite_not_leaderboard` |
| `CONS_0007` | `negative` | `refute_equivalence` | `NEQ` | `refuted_equivalence` | `expected_supported` | `false` |  | `bounded_sqlsolver_support_smoke_not_rewrite_not_leaderboard` |
| `CONS_0035` | `positive` | `prove_equivalent` | `NEQ` | `refuted_equivalence` | `unexpected_verdict` | `false` |  | `bounded_sqlsolver_support_smoke_not_rewrite_not_leaderboard` |
| `CONS_0035` | `negative` | `refute_equivalence` | `NEQ` | `refuted_equivalence` | `expected_supported` | `false` |  | `bounded_sqlsolver_support_smoke_not_rewrite_not_leaderboard` |

## 4. Aggregate Support Metrics
Report:
- denominator_pairs = `4`
- prove_count = `1`
- refute_count = `3`
- unknown_count = `0`
- timeout_count = `0`
- unsupported_count = `0`
- parser_or_translation_failure_count = `0`
- internal_error_count = `0`
- launch_failure_count = `0`
- expected_supported_count = `3`
- unexpected_verdict_count = `1`
- verifier_support_rate = `3/4`

## 5. Interpretation
State:
- `CONS_0007` is fully supported on positive and negative pair.
- `CONS_0035` negative is supported as refuted equivalence.
- `CONS_0035` positive returned an unexpected `NEQ` verdict.
- This is support/verifier evidence only.
- `UNKNOWN` / `TIMEOUT` / unsupported would be support gaps.
- unexpected verdict is verifier behavior evidence, not rewrite speedup evidence.

## 6. Metric Use
Use:
- `verifier_support_rate`
- `prove_count`
- `refute_count`
- `unexpected_verdict_count`

Do not use:
- `gm_speedup`
- `regression_rate@20`
- `W/T/L`
- rewrite leaderboard ranking

## 7. Recommended Next Step
Choose exactly one:
- `add SQLSolver to prior-support evidence summary`

## 8. Non-Modification Note
Confirm no new execution, no DB/checker/speedup, no registry/review/rules/EXECUTION_STATUS/case changes.
