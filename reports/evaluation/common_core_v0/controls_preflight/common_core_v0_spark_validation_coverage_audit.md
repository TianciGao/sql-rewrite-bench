# Common-core v0 Spark Validation Coverage Audit

This is a read-only coverage audit over the frozen Common-core v0 denominator. It checks whether each case currently has a Spark validation entrypoint and the expected Spark-side result artifacts in the repository layout.

## Summary

- total frozen denominator cases: `40`
- `ready_for_manual_spark_validation`: `36`
- `artifact_reuse_only`: `4`
- `missing_script_but_has_legacy_artifact`: `0`
- `missing_spark_evidence`: `0`

## Counts By Pool

| Pool | Total | ready_for_manual_spark_validation | artifact_reuse_only | missing_script_but_has_legacy_artifact | missing_spark_evidence |
|---|---:|---:|---:|---:|---:|
| performance | 16 | 12 | 4 | 0 | 0 |
| consistency | 9 | 9 | 0 | 0 | 0 |
| portability | 9 | 9 | 0 | 0 | 0 |
| longtail | 6 | 6 | 0 | 0 | 0 |

## Bucket Notes

- `artifact_reuse_only`
  - `PERF_0006`
  - `PERF_0007`
  - `PERF_0008`
  - `PERF_0013`
  - These four cases have legacy Spark artifacts under `runs/spark/` but no discoverable `validation/run_spark_validation.sh`.
  - `PERF_0006` is already confirmed by the Spark canary notes as a `missing_script` case that should stay explicit rather than being silently treated as fresh-run-capable.

- `ready_for_manual_spark_validation`
  - All `9` consistency cases, all `6` longtail cases, all `9` portability cases, and `12` of `16` performance cases have a discoverable Spark validation script.
  - Portability cases still carry a caveat: several use cross-dialect / reference-based Spark checker layouts rather than a straightforward Spark-local source baseline.

## Recommendation

Recommend `Spark subset fresh` first, not immediate `Spark @40 fresh`.

Reason:
- `36 / 40` cases are fresh-runnable from a script-coverage standpoint, which is strong enough for a broad fresh subset.
- The remaining `4` performance cases are not fresh-runnable today because they lack `run_spark_validation.sh`; they are better treated as `artifact_reuse_only` until script coverage is repaired.
- The portability line is script-covered, but its result semantics are more heterogeneous because several cases rely on cross-dialect reference checkers. A subset-first run keeps that risk bounded before scaling.

Practical next step:
- run a Spark fresh subset that includes representative performance, consistency, longtail, and portability cases with existing scripts
- keep `PERF_0006`, `PERF_0007`, `PERF_0008`, and `PERF_0013` out of that fresh subset unless Spark validation scripts are added
- use artifact-reuse only for those four legacy-script-gap cases if Spark-wide reporting is needed before script repair
