**Retry Scope**
- `PORT_0003 / pg / sqlglot_optimize_same_dialect`
- `PORT_0005 / pg / sqlglot_optimize_same_dialect`

**Why This Retry Exists**
- The earlier PORT SQLGlot same-engine execution triage identified package witness gaps, not SQLGlot method failures.
- Missing files:
  - `cases/PORT/PORT_0003/validation/pg_witness_data.sql`
  - `cases/PORT/PORT_0005/validation/pg_witness_data.sql`

**Backfill Basis**
- `PORT_0003`: rows copied from existing `data/witness_rows.yaml` and matched against `load_witness_pg.sql`, `load_witness_mysql.sql`, and `load_witness_spark.sql`.
- `PORT_0005`: rows copied from existing `data/witness_rows.yaml` and matched against `load_witness_pg.sql`, `load_witness_mysql.sql`, and `load_witness_spark.sql`.

**Execution Model**
- Run only the two PostgreSQL optimize rows from the real repo root.
- Reuse the corrected inline PostgreSQL runner pattern from the SQLGlot execution canary.
- Capture per-row stdout/stderr logs.
- Record exit codes into `run_results.json`.
- Do not execute any MySQL, Spark, transpile/no-op, or PORT-unsupported rows.
