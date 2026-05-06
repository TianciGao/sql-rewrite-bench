# CALCITE_HEP_PERF_0063_SIGNATURE_FIX_CHECKER_v1

## 0. Purpose And Boundary
This note records PERF_0063-only Calcite HEP input normalization plus generation/checker. It does not run speedup, does not rerun the existing 9 cases, does not edit case files, and is not a final baseline until speedup is separately handled.

## 1. Preflight Recap
- previous blocker: `generation_failed_function_signature_mismatch`
- triggering expression: `substr(ca_zip, 1, 5)`
- approved patch plan: narrow integer-literal normalization before Calcite handoff
- narrow normalization was chosen because it preserves function surface and provenance while addressing the exact validator signature mismatch

## 2. Normalization Applied
- original expression: `substr(ca_zip, 1, 5)`
- normalized expression: `substr(ca_zip, CAST(1 AS INTEGER), CAST(5 AS INTEGER))`
- normalization scope: case-specific adapter-local normalization for `PERF_0063` only
- normalized input artifact path: `/tmp/calcite-hep-wrapper/real-route/perf_0063_normalized_input.sql`
- original case source file was not modified; normalization was applied only to the Calcite input artifact

## 3. Generation Result
- `validation_succeeded` = `False`
- `sql_to_rel_succeeded` = `False`
- `hep_planner_succeeded` = `False`
- `output_sql_extracted` = `True`
- `candidate_sql_path` = `/tmp/calcite-hep-wrapper/real-route/perf_0063.sql`
- `generation_status` = `generation_failed`
- generation failure: `real_route_partial_only` / `ValidationException: org.apache.calcite.runtime.CalciteContextException: From line 14, column 8 to line 14, column 61: No match found for function signature substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)`

## 4. PostgreSQL Checker Result
- `checker_status` = `not_run_generation_failed`

## 5. Updated Calcite HEP @10 Checker Coverage
- `previous_checker_consistent` = `9`
- `perf_0063_checker_result` = `not_run_generation_failed`
- `total_10case_checker_consistent_count` = `9`
- `remaining_checker_blockers` = `['PERF_0063:real_route_partial_only']`

## 6. Recommended Next Step
- `diagnose PERF_0063 checker/generation failure`

## 7. Non-Modification Note
Only `PERF_0063` was targeted. No speedup ran, no existing 9-case rerun occurred, no MySQL/Spark/model/API path was used, and no case/registry/review/rules/EXECUTION_STATUS changes were made. Taxonomy notes remained untouched.
