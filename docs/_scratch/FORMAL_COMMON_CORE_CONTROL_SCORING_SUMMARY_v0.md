# FORMAL_COMMON_CORE_CONTROL_SCORING_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the current formal common-core control scoring state.

This note is derived from:

- `reports/formal_common_core/control_scoring_v0.json`

This is control-route scoring only.

## 2. Control Scoring Status

- `ok=true`
- control scoring was computed from existing execution reports and existing checker/result artifacts
- `claim_boundary=formal_control_scoring_from_existing_reports_only_not_full_correctness_or_speedup`

## 3. Execution Rates

- `native_executable_rate=1.0`
- `human_positive_executable_rate=1.0`
- `hard_negative_executable_rate=1.0`

## 4. Result Consistency

- `result_consistency_rate_observed_existing_artifacts=1.0`
- `result_consistency_rate_status=computed_from_existing_checker_artifacts`

Current interpretation:

- the existing checker/result artifacts support a fully observed control-route consistency summary for the current denominator
- this remains a control-route scoring summary, not a broader benchmark claim

## 5. Negative Guard

- `negative_rejection_rate_observed_existing_artifacts=1.0`
- `false_accept_rate_observed_existing_artifacts=0.0`
- `negative_rejection_rate_status=computed_from_existing_checker_artifacts`
- `false_accept_rate_status=computed_from_existing_checker_artifacts`

Current interpretation:

- the existing checker/result artifacts support a fully observed hard-negative control summary for the current denominator
- this is still limited to the current formal control-route slice

## 6. Row-Count Observations

- human positive row-count match: `9 / 9`
- hard negative row-count differs: `4 / 9`
- hard negative row-count same: `5 / 9`

Important boundary:

- row-count observations are not semantic correctness by themselves
- row-count difference is only an observation
- row-count equality is not semantic equivalence by itself

## 7. Boundary

- this is control-route scoring only
- SQLGlot scoring is not yet complete
- LLM scoring is not yet complete
- `speedup_scoring_complete=false`
- no leaderboard claim

## 8. Next Action

- begin SQLGlot same-dialect formal execution/scoring

## 9. Verification / Non-Modification Note

- only this note was created
- no database workloads were run
- no SQL was executed
- no LLM calls were made
- no SQLGlot generation was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
