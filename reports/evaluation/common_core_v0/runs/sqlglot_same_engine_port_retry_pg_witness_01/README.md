This package is for human-run retry only.

Codex must not execute the retry script.

Scope is limited to the two PostgreSQL optimizer rows that previously failed before generated SQL execution because the case packages were missing `pg_witness_data.sql`:

- `PORT_0003 / pg / sqlglot_optimize_same_dialect`
- `PORT_0005 / pg / sqlglot_optimize_same_dialect`

The backfilled witness files were derived conservatively from existing case-local artifacts:

- `data/witness_rows.yaml`
- existing `load_witness_pg.sql`, `load_witness_mysql.sql`, and `load_witness_spark.sql`

This is not a full rerun of the PORT package and does not compute timing, speedup, or leaderboard metrics.
