# Witness Design Notes

The witness rows are intentionally small and remain draft-only.

`LA_A` is set to `fm_count=1` and `enrollment=300`, which yields `0.333333...` on the package's percentage scale (`fm_count * 100 / enrollment`).
That row is designed to:

- fail the source and positive threshold `< 0.18`
- pass the negative threshold `< 0.50`

`LA_B` remains above `0.50` as a guard row.

The Spark path is split onto `rewrite_pos_02_spark.sql` and `rewrite_neg_02_spark.sql` so Spark can use `CAST(... AS DOUBLE)` while PostgreSQL keeps `DOUBLE PRECISION`.
