# FORMAL_COMMON_CORE_RUNTIME_SPEEDUP_POLICY_FREEZE_PLAN_v0

## 1. Status

This is a tracked scratch runtime / speedup policy-freeze plan.

It is not a speedup result.

It is not GM_Speedup output.

## 2. Current Runtime Observation State

Current formal common-core runtime observations are available for:

- `NATIVE_IDENTITY`
- `HUMAN_REFERENCE_POSITIVE`
- `HARD_NEGATIVE_GUARD`
- `SQLGLOT_OPT_SAME_DIALECT`
- `LLM_DIRECT_REWRITE_STRONG`

Current state from the runtime observation snapshot:

- runtime observations exist across the formal 9-case denominator
- current route-relative ratios are single-run observations only
- `formal_speedup_scoring_complete=false`
- `repeat_count_policy=not_frozen`
- `warmup_policy=not_frozen`
- `runtime_measurement_policy=not_frozen`

These current ratios must not be reported as formal `GM_Speedup`.

## 3. Proposed Runtime Measurement Policy

Proposed discussion-default policy for the first formal common-core speedup pass:

- `repeat_count=5`
- `warmup_count=1`
- `statement_timeout_ms=30000`, unless a stronger existing project default is already frozen elsewhere
- primary measurement statistic: median runtime across measured repeats
- auxiliary statistics: min and mean runtime recorded for context only
- failed executions and timeouts are excluded from the speedup numerator
- failed executions and timeouts are still counted in failure / timeout tracking fields
- only result-consistent method rewrites enter formal speedup scoring
- hard negatives do not enter the speedup leaderboard

## 4. Proposed Speedup Metrics

Proposed metric definitions for discussion:

- `speedup_ratio = source_median_runtime_ms / candidate_median_runtime_ms`
- `GM_Speedup` computed over valid rewrites only
- `Win / Tie / Loss` computed over valid rewrites only
- tie threshold: within `±5%`, unless a different project-default threshold is already frozen in project docs
- `RegressionRate@20%`: candidate runtime `>= 1.2 * source runtime`
- `SpeedupTransferRate`: defer to the PORT phase, not the common-core first pass

## 5. Eligible Routes For First Speedup Pass

Include:

- `NATIVE_IDENTITY` as the source/control baseline only
- `HUMAN_REFERENCE_POSITIVE` as the positive control / reference rewrite
- `SQLGLOT_OPT_SAME_DIALECT`
- `LLM_DIRECT_REWRITE_STRONG`

Exclude:

- `HARD_NEGATIVE_GUARD` from the speedup leaderboard
- SQLGlot transpile and Direct LLM translate PORT routes
- readiness-only or deferred routes
- `SQLSolver` / `VeriEQL` support for this first pass

## 6. Required Artifacts Before Formal Speedup Run

Required artifacts and policy fields:

- execution success report
- result consistency status
- source runtime repeats
- candidate runtime repeats
- timeout policy
- warmup policy
- plan pair availability, if plan-observable speedup is reported alongside runtime
- method route ID
- candidate SQL source reference

## 7. Interaction With Plan Observability

- speedup should be reported separately from plan attribution
- operator delta can be used as observation only
- attribution requires additional policy and a separate command path
- plan pair readiness exists already
- attribution is not computed yet

## 8. Open Decisions

- final `repeat_count`
- final `warmup_count`
- final tie-threshold value
- final timeout-policy value
- whether to use median only or median plus min/mean in the formal packet
- whether LLM token cost should be reported beside speedup, but not folded into runtime
- whether `CONS` cases should participate in `GM_Speedup`, or remain in correctness / semantic analysis only

## 9. Recommended Next Action

- implement a no-execution formal speedup-run preflight that checks repeat/warmup/timeout policy fields and route eligibility before any runtime reruns

## 10. Claim Boundaries

- no speedup scoring yet
- no `GM_Speedup` yet
- no `RegressionRate` yet
- no leaderboard claim
- no registry writeback
- no formal review update

## 11. Verification / Non-Modification Note

- only this plan was created
- no database workloads were run
- no SQL was executed
- no LLM calls were made
- no SQLGlot generation was run
- no checker was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
