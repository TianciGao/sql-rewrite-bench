# Recovery PERF_0035 Canary Plan

## Purpose

Test the only remaining retained family that appears recoverable under the
unchanged route by bounded implementation-level repair after the ledger reached
`90/120`.

## Row Scope

- `PERF_0035:pg`
- `PERF_0035:mysql`
- `PERF_0035:spark`

## Retained Mismatch Pattern

For all three rows, the retained generated query:

- preserves the first seven logical source output columns
- adds one trailing helper projection for `sum_sales - avg_monthly_sales`
- loses the source textual scale of `avg_monthly_sales`

## Planned Repair

For each row:

1. reuse the retained generated SQL
2. alias the retained trailing helper expression as an internal helper column
3. wrap the retained generated SQL in a final projection that:
   - removes the helper column from the exposed output
   - preserves engine-specific `avg_monthly_sales` textual scale
4. execute source and repaired generated SQL under the unchanged checker

## Engine-Specific Scale Targets

- `PERF_0035:pg`
  - `avg_monthly_sales` scale `16`
- `PERF_0035:mysql`
  - `avg_monthly_sales` scale `6`
- `PERF_0035:spark`
  - `avg_monthly_sales` scale `6`

## Ledger Policy

- denominator_id remains `common_core_v0_40_same_engine_120`
- previous_fail_closed_exact_ledger = `90/120`
- maximum_possible_ledger_after_this_canary = `93/120`
- success counts only as `executed + match_exact + recovered_exact=true`
