# Witness Design Notes

This draft package does not include loaded or executed witness data yet.

## Tables

- `schools`

## Minimal Draft Witness

- 4 rows are likely enough.
- Include one positive longitude, one negative longitude, one smaller absolute value, and one `NULL` longitude.

## Boundary Goal

- The source and positive rewrites should agree on the highest absolute longitude after explicit null handling.
- The hard negative should fail by choosing the wrong row when sort direction or null ordering is mishandled.
