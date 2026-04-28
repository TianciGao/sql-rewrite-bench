# Witness Design Notes

This draft package does not include loaded or executed witness data yet.

## Tables

- `patient`

## Minimal Draft Witness

- 4 to 5 patient rows should be enough.
- Include mixed `sex`, mixed `diagnosis`, and birth years around 1980 and 1981.

## Boundary Goal

- The source and positive rewrites should agree on the female-percentage calculation for the `RA` subset born in 1980.
- The hard negative should fail when the year-filter boundary changes.
