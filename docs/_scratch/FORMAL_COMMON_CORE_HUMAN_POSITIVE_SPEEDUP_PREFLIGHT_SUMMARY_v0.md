# FORMAL_COMMON_CORE_HUMAN_POSITIVE_SPEEDUP_PREFLIGHT_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the `HUMAN_REFERENCE_POSITIVE` PERF-only formal speedup preflight state.

This is a preflight only.

## 2. Policy Basis

Policy basis:

- `docs/_scratch/FORMAL_COMMON_CORE_SPEEDUP_POLICY_DECISION_PACKET_v0.md`

Frozen policy fields applied by this preflight:

- `repeat_count=5`
- `warmup_count=1`
- `statement_timeout_ms=30000`
- `primary_runtime_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

## 3. PERF-Only Denominator

The first formal speedup rerun scope is PERF-only:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

## 4. Readiness Result

- `ready_case_count=7`
- `blocked_case_count=0`
- `formal_speedup_rerun_ready=true`
- `formal_speedup_scoring_complete=false`

## 5. Required Artifacts And Gates

All required gates clear across the 7-case PERF denominator:

- `source_sql_present_count=7`
- `positive_sql_present_count=7`
- `native_execution_success_count=7`
- `human_positive_execution_success_count=7`
- `consistency_gate_pass_count=7`
- `runtime_observation_available_count=7`
- `plan_pair_ready_count=7`

Per current preflight interpretation:

- source SQL exists for all 7 PERF cases
- positive rewrite SQL exists for all 7 PERF cases
- native execution success exists for all 7 PERF cases
- human positive execution success exists for all 7 PERF cases
- checker-backed human-positive consistency gate passed for all 7 PERF cases
- source-positive plan pair readiness exists for all 7 PERF cases

## 6. Route Eligibility

- route: `HUMAN_REFERENCE_POSITIVE`
- baseline id: `HUMAN_REFERENCE_POSITIVE`
- denominator scope: `PERF_only`
- current route status: ready for the next formal speedup rerun step

## 7. Claim Boundaries

- no runtime repeats have run
- no speedup has been computed
- no `GM_Speedup` has been computed
- no leaderboard result exists
- this preflight only authorizes the next rerun step

## 8. Recommended Next Action

- run `HUMAN_REFERENCE_POSITIVE` PERF-only formal speedup rerun under the frozen policy
