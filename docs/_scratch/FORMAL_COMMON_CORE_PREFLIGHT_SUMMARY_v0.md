# FORMAL_COMMON_CORE_PREFLIGHT_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the artifact-only formal common-core preflight.

It records the result of:

- `python -m scripts.cli formal-common-core-preflight`

It summarizes artifact-only readiness for the proposed first formal common-core run.

## 2. Denominator

Formal common-core denominator checked by the preflight:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

## 3. Preflight Result

Recorded result from `reports/formal_common_core/common_core_preflight_v0.json`:

- `ok=true`
- `formal_run_ready=true`
- `case_count=9`
- `ready_case_count=9`
- `partial_case_count=0`
- `blocked_case_count=0`

## 4. Artifact Presence Summary

Artifact presence counts:

- `source_sql_present_count=9`
- `manifest_present_count=9`
- `positive_rewrite_present_count=9`
- `negative_rewrite_present_count=9`
- `checker_or_result_artifact_present_count=9`
- `plan_source_present_count=9`
- `plan_positive_present_count=9`
- `plan_negative_present_count=9`
- `plan_check_present_count=9`
- `smoke_evidence_present_count=9`

## 5. Route Readiness Summary

Formal-route readiness counts:

- `NATIVE_IDENTITY`: `{"ready_if_core_inputs_present": 9}`
- `HUMAN_REFERENCE_POSITIVE`: `{"ready_if_positive_present": 9}`
- `HARD_NEGATIVE_GUARD`: `{"ready_if_negative_present": 9}`
- `SQLGLOT_OPT_SAME_DIALECT`: `{"ready_for_generation_preflight": 9}`
- `LLM_DIRECT_REWRITE_STRONG`: `{"ready_for_prompt_or_call_preflight": 9}`

## 6. Interpretation

The current 9-case denominator is artifact-ready for the first formal common-core run.

This result is stronger than the original planning assumption in the formal run plan. The preflight found the full denominator already has:

- core case-package inputs
- positive and negative rewrites
- checker or result-check artifacts
- source and candidate plan artifacts
- matching baseline smoke evidence

This does not mean formal scoring has started.

It means only that the repository artifact layer is ready enough to begin the formal common-core control routes without first backfilling missing denominator files.

## 7. Claim Boundaries

- no correctness result
- no speedup result
- no leaderboard result
- no admission
- no registry writeback
- no formal review update

Important boundary:

- `formal_run_ready=true` means artifact-only preflight readiness only
- it is not correctness scoring
- it is not speedup scoring
- it is not leaderboard readiness
- it is not common-core admission

## 8. Recommended Next Action

- Begin the formal common-core control routes:
  - `NATIVE_IDENTITY`
  - `HUMAN_REFERENCE_POSITIVE`
  - `HARD_NEGATIVE_GUARD`

## 9. Verification / Non-Modification Note

- only this summary note was created
- no database workloads were run
- no SQL was executed
- no LLM calls were made
- no SQLGlot generation was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
