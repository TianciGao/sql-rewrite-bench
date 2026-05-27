# FORMAL_COMMON_CORE_CONTROL_EXECUTION_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of formal common-core control execution-layer results.

This is a summary note only.

It is not correctness scoring.
It is not speedup scoring.
It is not a leaderboard result.
It is not registry writeback.
It is not a formal review update.

## 2. Inputs / Report References

The current summary is based on these existing formal control execution reports:

- `reports/formal_common_core/native_identity_execution_v0.json`
- `reports/formal_common_core/human_reference_positive_execution_v0.json`
- `reports/formal_common_core/hard_negative_guard_execution_v0.json`
- `reports/formal_common_core/control_execution_summary_v0.json`

## 3. Route-Level Execution Summary

| route | ok | case_count | success_count | failed_count | interpretation |
|---|---:|---:|---:|---:|---|
| `NATIVE_IDENTITY` | `true` | `9` | `9` | `0` | source SQL executed successfully across the 9-case denominator |
| `HUMAN_REFERENCE_POSITIVE` | `true` | `9` | `9` | `0` | positive reference SQL executed successfully across the 9-case denominator |
| `HARD_NEGATIVE_GUARD` | `true` | `9` | `9` | `0` | hard-negative SQL executed successfully across the 9-case denominator, but execution success is not rejection success |

## 4. Per-Case Compact Execution Observations

### 4.1 NATIVE_IDENTITY

| case_id | execution_status | row_count | runtime_ms | validation_schema |
|---|---|---:|---:|---|
| `PERF_0006` | `success` | `2` | `213` | `perf_0006_validation` |
| `PERF_0008` | `success` | `1` | `57` | `perf_0008_validation` |
| `PERF_0013` | `success` | `1` | `58` | `perf_0013_validation` |
| `PERF_0017` | `success` | `1` | `59` | `perf_0017_validation` |
| `PERF_0024` | `success` | `1` | `59` | `perf_0024_validation` |
| `PERF_0033` | `success` | `1` | `57` | `perf_0033_validation` |
| `PERF_0054` | `success` | `1` | `57` | `perf_0054_validation` |
| `CONS_0007` | `success` | `2` | `57` | `cons_0007_validation` |
| `CONS_0012` | `success` | `2` | `57` | `cons_0012_validation` |

### 4.2 HUMAN_REFERENCE_POSITIVE

| case_id | execution_status | row_count | runtime_ms | validation_schema |
|---|---|---:|---:|---|
| `PERF_0006` | `success` | `2` | `120` | `perf_0006_validation` |
| `PERF_0008` | `success` | `1` | `58` | `perf_0008_validation` |
| `PERF_0013` | `success` | `1` | `162` | `perf_0013_validation` |
| `PERF_0017` | `success` | `1` | `57` | `perf_0017_validation` |
| `PERF_0024` | `success` | `1` | `60` | `perf_0024_validation` |
| `PERF_0033` | `success` | `1` | `57` | `perf_0033_validation` |
| `PERF_0054` | `success` | `1` | `173` | `perf_0054_validation` |
| `CONS_0007` | `success` | `2` | `56` | `cons_0007_validation` |
| `CONS_0012` | `success` | `2` | `57` | `cons_0012_validation` |

### 4.3 HARD_NEGATIVE_GUARD

| case_id | execution_status | row_count | runtime_ms | validation_schema |
|---|---|---:|---:|---|
| `PERF_0006` | `success` | `2` | `109` | `perf_0006_validation` |
| `PERF_0008` | `success` | `1` | `59` | `perf_0008_validation` |
| `PERF_0013` | `success` | `1` | `58` | `perf_0013_validation` |
| `PERF_0017` | `success` | `1` | `58` | `perf_0017_validation` |
| `PERF_0024` | `success` | `0` | `59` | `perf_0024_validation` |
| `PERF_0033` | `success` | `1` | `162` | `perf_0033_validation` |
| `PERF_0054` | `success` | `0` | `59` | `perf_0054_validation` |
| `CONS_0007` | `success` | `4` | `58` | `cons_0007_validation` |
| `CONS_0012` | `success` | `3` | `59` | `cons_0012_validation` |

## 5. Hard-Negative Interpretation Warning

Hard-negative execution success is not negative rejection.

This route summary only shows that the hard-negative SQL executed successfully under the configured PostgreSQL validation schemas.

Important interpretation boundaries:

- hard-negative execution success is not `NegativeRejectionRate`
- hard-negative execution success is not `FalseAcceptRate`
- row-count difference is only an observation
- row-count equality is not semantic equivalence
- formal negative scoring is still required

## 6. Current Control-Route State

The current control-route state is:

- execution layer complete for three control routes
- result consistency scoring not yet complete
- negative rejection scoring not yet complete
- speedup scoring not yet complete
- leaderboard not yet produced

Aggregate execution summary from `reports/formal_common_core/control_execution_summary_v0.json`:

- `all_control_execution_succeeded=true`

## 7. Recommended Next Action

- implement `formal-common-core-control-scoring` to compute result consistency and hard-negative rejection / false-acceptance from existing execution reports and checker/result artifacts

## 8. Claim Boundaries

- no correctness scoring yet
- no speedup scoring yet
- no leaderboard result
- no registry writeback
- no formal review update

## 9. Verification / Non-Modification Note

- only this note was created
- no database workloads were run by this note creation
- no SQL was executed by this note creation
- no LLM calls were made
- no SQLGlot generation was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
