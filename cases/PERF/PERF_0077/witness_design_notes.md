# PERF_0077 Witness Design Notes

## Case identity

- case_id: `PERF_0077`
- draft_origin: `JOB_DRAFT_0003`

## Intended equality behavior

- `source.sql` and `rewrite_pos_01.sql` are intended to remain equal because the positive rewrite only normalizes the old-style comma join into explicit inner joins.
- Equality should be assessed over the same `movie_id` bridge paths used by the source query.

## Intended negative divergence

- `rewrite_neg_01.sql` narrows `%sequel%` to `sequel%`.
- The witness therefore preserves three keyword behaviors:
  - source-only match: `presequelpost`
  - shared match: `sequel-start`
  - non-match: `standalone`

## Minimal witness strategy

- At least one valid movie path must satisfy the source and positive rewrite.
- At least one additional valid movie path must survive both source and negative so the divergence is not demonstrated by a single surviving row.
- At least one non-matching path should remain present to guard against accidental over-permissive behavior.

## Human review caveats

- `MIN(title)` is sensitive to the surviving witness rows, so later validation should confirm that the divergence is not an artifact of over-minimal data.
- Text `LIKE` semantics should be reviewed across PostgreSQL, MySQL, and Spark before any reporting claim is made.
- No witness script or engine execution was run in this construction task.
