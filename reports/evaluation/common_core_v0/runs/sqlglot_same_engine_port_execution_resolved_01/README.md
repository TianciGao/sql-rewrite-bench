This package is the resolved PORT-only SQLGlot same-engine execution materialization for Common-core v0.

It covers all `54` planned PORT rows across the `9` Common-core portability cases, `pg/mysql/spark`, and the two same-engine SQLGlot routes.

It is execution-only method evidence:
- no result validation claim
- no timing
- no speedup
- no final leaderboard

The two original PostgreSQL optimize failures for `PORT_0003` and `PORT_0005` were package witness gaps, not SQLGlot method failures. They were resolved by backfilling `pg_witness_data.sql` and using the narrow retry package.
