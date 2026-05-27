# CALCITE_HEP_PERF0006_NUMERIC_MISMATCH_DIAGNOSTIC_v0

## Status

This note diagnoses the Calcite HEP `PERF_0006` numeric mismatch using existing source SQL, Calcite-generated SQL, materialized TSVs, and checker artifacts only.

Explicit boundary:

- diagnostic only
- no speedup
- no baseline claim
- not a claim that Calcite HEP is fully implemented

## Commands Run

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-calcite-hep-perf0006-numeric-mismatch-diagnostic`
- `python -m json.tool reports/formal_expansion/calcite_hep_perf0006_numeric_mismatch_diagnostic_v0.json >/dev/null`

## Exact Classification

Final mismatch classification:

- `numeric_scale_rounding_difference`

Why it is not `formatting_only`:

- Decimal-normalized comparison still finds one numerically different cell
- checker remains `inconsistent`
- `row_count_equal=true` but `byte_equal=false`

Why it is not just a generic `true_value_difference` bucket:

- the differing cell is in an `AVG(...)`-derived metric
- Calcite rewrote the aggregate using `SUM/COUNT` with `DECIMAL(15,2)` casts
- the mismatch shape is a scale / rounding loss introduced by the rewrite path

## Expression-Level Cause

Source expressions producing the affected output columns:

- `avg_qty`: `avg(l_quantity)`
- `avg_price`: `avg(l_extendedprice)`
- `avg_disc`: `avg(l_discount)`

Calcite emitted expressions for the same columns:

- `avg_qty`: `CAST(CAST(COALESCE(SUM("l_quantity"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2))`
- `avg_price`: `CAST(CAST(COALESCE(SUM("l_extendedprice"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2))`
- `avg_disc`: `CAST(CAST(COALESCE(SUM("l_discount"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2))`

Likely root cause:

- `AVG rewrite to SUM/COUNT`
- combined with `COALESCE(SUM(...), 0)` and `DECIMAL(15,2)` casts
- causing numeric scale / cast loss on `avg_disc`

Most likely failing subexpression:

- `avg(l_discount)` became a `SUM(l_discount) / COUNT(*)` path rounded to `DECIMAL(15,2)`

## Numeric-Normalized Result

Formatting-only differences that disappear under Decimal normalization:

- row 1 `avg_qty`: `15.0000000000000000` vs `15.00`
- row 1 `avg_price`: `150.0000000000000000` vs `150.00`
- row 2 `avg_qty`: `15.0000000000000000` vs `15.00`
- row 2 `avg_price`: `150.0000000000000000` vs `150.00`
- row 2 `avg_disc`: `0E-20` vs `0.00`

Cell(s) that still differ numerically after Decimal normalization:

- row 1 `avg_disc`:
  - source: `0.07500000000000000000`
  - Calcite: `0.08`
  - Decimal values: `0.075` vs `0.08`

Numeric-normalized summary:

- `numeric_normalized_equal=false`
- `numeric_difference_count=1`
- `formatting_only_difference_count=5`

Interpretation:

- most mismatches are rendering-only
- one `avg_disc` cell remains a true numeric mismatch
- `PERF_0006` must stay inconsistent for checker purposes

## Recovery Assessment

Can `PERF_0006` be recovered safely?

- yes, likely with a targeted wrapper fix

Why:

- the mismatch is narrow and localized
- PostgreSQL execution already succeeds
- only one numerically different cell remains
- the failure mode points to cast / scale handling in Calcite emission, not a broad relational error

Recommended next action:

- fix Calcite wrapper/type casts and rerun `PERF_0006` checker

This is preferable to:

- using a numeric-normalized checker now

because:

- a true numeric value difference still remains
- checker normalization must not mask a real numeric change

## Subset Decision

Can Calcite HEP proceed on a 3-case checker-clean subset?

- yes

Safe checker-clean subset:

- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Condition:

- keep `PERF_0006` out of the first checker-clean subset until the cast / scale issue is fixed and rerun

## Conclusion

`PERF_0006` is not blocked by execution. It is blocked by one real numeric mismatch in `avg_disc`, caused by the current Calcite `AVG -> SUM/COUNT` rewrite plus `DECIMAL(15,2)` casting. The correct next move is to fix the wrapper’s emitted type-cast behavior and rerun the `PERF_0006` checker, while allowing Calcite HEP to proceed on the 3-case checker-clean subset for bounded follow-on work.
