# Controls @40 Fresh Source+Positive Failure Triage

## Executive Summary

This run is schema-valid and denominator-complete, but execution-unsuccessful.

- validator: `ok=true`
- validator issue count: `0`
- validator success here means the run package satisfies schema and denominator-accounting rules; it does **not** mean the fresh executions succeeded.

## Status Counts

- `failed`: `223`
- `manual_review_required`: `8`
- `skipped`: `9`

## Failure Bucket Counts

- `execution_error`: `223`
- `unsupported`: `17`

## route_id x engine x failure_bucket

- `human_positive / mysql / execution_error`: `37`
- `human_positive / mysql / unsupported`: `3`
- `human_positive / pg / execution_error`: `37`
- `human_positive / pg / unsupported`: `3`
- `human_positive / spark / execution_error`: `33`
- `human_positive / spark / unsupported`: `7`
- `native_source / mysql / execution_error`: `40`
- `native_source / pg / execution_error`: `40`
- `native_source / spark / execution_error`: `36`
- `native_source / spark / unsupported`: `4`

## Diagnosis

### 1. Uniform executed-row failure pattern

- All `223` executed rows landed in `status=failed` and `failure_bucket=execution_error`.
- The pattern spans performance, consistency, portability, and longtail, which argues against a narrow case-level SQL defect.
- No file inside `tmp_repo/` has a modification time newer than the run itself, which strongly suggests the copied preexisting artifacts were not actually refreshed during this pass.

Inference: the dominant failure mode looks orchestration/environmental rather than case-specific SQL breakage.

### 2. DB/runtime bootstrap risk is more likely than case-level SQL failure

- PostgreSQL, MySQL, and Spark executed rows all failed in bulk.
- This cross-engine uniformity is not consistent with one or two bad case packages.
- The run did not persist stdout/stderr logs, so the exact low-level error text is unavailable in this run artifact.

Inference: likely classes are DB connectivity/auth/bootstrap problems or shell/runtime environment problems, not a denominator-wide SQL semantics collapse.

### 3. tmp_repo isolation likely introduced path/cwd risk for portability scripts

- Several copied PORT validation scripts in `tmp_repo/` still reference `REPO_ROOT/.venv/bin/python` or repo-root-relative helpers.
- In the copied tree, `REPO_ROOT` resolves to the isolated `tmp_repo/`, which does not contain the original repo `.venv`.
- That makes portability MySQL/Spark checker stages especially vulnerable to path failures even before SQL semantics are evaluated.

Inference: `tmp_repo` isolation is a credible root cause for at least part of the portability failure surface.

### 4. Missing-command rows behaved as expected and are not hidden

- `8` rows are `manual_review_required` from preflight command gaps.
- `9` rows are `skipped` for the preserved `PORT_0003/0004/0005` human-positive command caveat.
- These rows are denominator-visible and not execution failures in the same sense as the `223` executed rows.

## Top Recurring Observable Messages

- `command_failed`: `223`
- `fresh_execution`: `223`
- `stderr_present`: `160`
- `common_core_v0_candidate retained in review packet`: `78`
- `keep as tri-engine template-backed PERF candidate`: `78`
- `common_core_v0 consistency candidate`: `48`
- `human review required before freeze`: `48`
- `human approved for review slate only`: `36`
- `common_core_v0 portability stress candidate`: `24`
- `final reporting must separate execution and consistency policy`: `24`
- `portability stress candidate`: `24`
- `normalization caveat`: `24`

Note: no per-row stderr text was persisted, so the run only exposes note-level recurrence, not exact shell/database error strings.

## Sample Rows By Failure Type

### uniform_execution_error_executed_rows

- case: `PERF_0006`
- route: `native_source`
- engine: `pg`
- status: `failed`
- failure_bucket: `execution_error`
- notes: `command_failed; stderr_present; fresh_execution; common_core_v0_candidate retained in review packet; keep as tri-engine template-backed PERF candidate`

### manual_command_review_rows

- case: `PERF_0006`
- route: `native_source`
- engine: `spark`
- status: `manual_review_required`
- failure_bucket: `unsupported`
- notes: `not_executed; manual_command_review_required; common_core_v0_candidate retained in review packet; keep as tri-engine template-backed PERF candidate; no discoverable native/source command for engine`

### missing_port_human_positive_rows

- case: `PORT_0003`
- route: `human_positive`
- engine: `pg`
- status: `skipped`
- failure_bucket: `unsupported`
- notes: `not_executed; preflight_skip; missing_dedicated_human_positive_command_caveat_preserved; common_core_v0 portability stress candidate; final reporting must separate execution and consistency policy; no dedicated plan-collection command discovered; missing dedicated human-positive command in preflight`

## Recommended Next Execution Strategy

Recommended choices: `A + C + D + E`.

- `A. execute from real repo root rather than tmp_repo`: **yes**. This reduces repo-root-relative path breakage, especially for portability scripts referencing `.venv` or repo-root helpers.
- `B. use case-local scripts in place`: **not by default**. Those scripts write into `cases/.../runs/`, so using them in place would mutate benchmark case directories unless explicitly approved.
- `C. source env scripts once in the root shell`: **yes**. This is the cleanest way to stabilize shared PG/MySQL/Spark environment state before launching any batch commands.
- `D. avoid copying case trees`: **yes**. The copied-tree isolation likely contributed path/cwd problems and did not deliver the intended clean execution isolation.
- `E. run a 2-case canary before 40-case execution`: **yes**. Use one representative PERF/CONS case and one representative PORT case to capture stdout/stderr and confirm environment readiness before scaling back to 40 cases.

Suggested canary shape:

- one tri-engine template-backed case such as `PERF_0006` or `CONS_0005`
- one portability case such as `PORT_0012` or `PORT_0022`

## Bottom Line

The run is governance-valid but execution-invalid. The strongest current explanation is a combination of environment/bootstrap failure plus `tmp_repo` path risk, not a 40-case SQL-quality collapse.
