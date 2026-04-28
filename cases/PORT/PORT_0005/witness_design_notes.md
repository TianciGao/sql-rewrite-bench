# Witness Design Notes

This draft package does not include loaded or executed witness data yet.

## Tables

- `drivers`

## Minimal Draft Witness

- 4 rows are likely enough.
- Include one `NULL` `dob` plus three non-null `dob` values in different years.

## Boundary Goal

- The source and positive rewrites should agree on the earliest non-null `dob`.
- The hard negative should fail by selecting the wrong non-null row when ordering direction changes.
