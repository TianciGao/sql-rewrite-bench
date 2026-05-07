# Controls v0 Fresh Source Positive 01

This run executes the first fresh Controls @40 pass for `native_source` and `human_positive` only.

## Scope

- `denominator_id = common_core_v0_40`
- `method_id = controls`
- `method_role = controls`
- `artifact_mode = fresh_execution_partial_controls`
- `route_scope = native_source_and_human_positive_only`

## Execution Isolation

Fresh commands were executed only inside copied case trees under `tmp_repo/` so the original `cases/...` packages were not modified.

## Route Handling

- `native_source` and `human_positive` rows are included for all 40 cases across `pg`, `mysql`, and `spark`.
- `hard_negative` was intentionally excluded from this run because the requested scope is source+positive only and the validator does not require variant-complete visibility for this partial controls pass.
- `PORT_0003`, `PORT_0004`, and `PORT_0005` preserve the missing dedicated human-positive command caveat and are represented as non-executed rows rather than using invented commands.

## Accounting

- executed rows: `223`
- non-executed rows: `17`
- distinct cases represented: `40`
- executed row status outcome in this pass: `223 failed`, `0 success`

No failed, skipped, or manual-review rows were dropped from denominator-aware reporting.

## Validation

See `validation_report.json` for validator output.
