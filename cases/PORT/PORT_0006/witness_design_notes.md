# Witness Design Notes

This draft package does not include loaded or executed witness data yet.

## Tables

- `loan`

## Minimal Draft Witness

- 4 rows should be enough.
- Include one `status = 'C'`, one non-`C`, one `NULL` status if possible, and one `amount = 100000` boundary row.
- Use at least one row below the threshold and one row exactly on the threshold so `<` and `<=` diverge.

## Boundary Goal

- The source and positive rewrites should agree on boolean-coercion count semantics below the threshold.
- The hard negative should fail by incorrectly including the `amount = 100000` boundary row.

## Intended Witness Exposure

- The witness should show that the MySQL boolean-sum source and the CASE-count positive rewrite preserve the same numerator.
- The threshold-boundary row should make the negative produce a different percentage.
